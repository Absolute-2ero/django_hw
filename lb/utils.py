from lb.models import Submission, User
from random import randint
import functools
import numpy as np

import math

def interpolate(x1, x2, y1, y2, x):
    if x < x1:
        return y1
    if x > x2:
        return y2
    return math.sqrt((x - x1) / (x2 - x1)) * (y2 - y1) + y1

def main_score(result: list):
    """
    :param result: catagory accuracy, element value in [0, 1]
    :return: main_score
    """
    mean_result = sum(result) / 3
    return round(
        55 * interpolate(.5, .8, 0, 1, mean_result) +
        15 * interpolate(.5, .7, 0, 1, result[0]) +
        15 * interpolate(.5, .9, 0, 1, result[1]) +
        15 * interpolate(.5, .75, 0, 1, result[2])
    )

def get_leaderboard():
    """
    Get the current leaderboard
    :return: list[dict]
    """

    # 坏了，我似乎已经忘了 ORM 中该怎么调 API 了
    # 在这里你可选择
    #    1. 看一眼数据表, 然后后裸写 SQL
    #    2. 把所有数据一股脑取回来然后手工选出每个用户的最后一次提交
    #    3. 学习 Django API 完成这个查询

    # 方案1: 直接裸写 SQL 摆烂，注意，由于数据库类型等因素，这个查询未必能正确执行，如果使用这种方法可能需要进行调整
    # subs = list(Submission.objects.raw(
    #         """
    #         SELECT
    #             `lb_submission`.`id`,
    #             `lb_submission`.`avatar`,
    #             `lb_submission`.`score`,
    #             `lb_submission`.`subs`,
    #             `lb_submission`.`time`
    #         FROM `lb_submission`, (
    #             SELECT `user_id`, MAX(`time`) AS mt FROM `lb_submission` GROUP BY `user_id`
    #         ) `sq`
    #         WHERE
    #             `lb_submission`.`user_id`=`sq`.`user_id` AND
    #             `time`=`sq`.`mt`;
    #         ORDER BY
    #             `lb_submission`.`subs` DESC,
    #             `lb_submission`.`time` ASC
    #         ;
    #         """
    # ))
    # return [
    #     {
    #         "user": obj.user.username,
    #         "score": obj.score,
    #         "subs": [int(x) for x in obj.subs.split()],
    #         "avatar": obj.avatar,
    #         "time": obj.time,
    #         "votes": obj.user.votes
    #     }
    #     for obj in subs
    # ]

    # 方案2：一股脑拿回本地计算
    all_submission = Submission.objects.all()
    subs = {}
    for s in all_submission:
        if s.user_id not in subs or (s.user_id in subs and s.time > subs[s.user_id].time):
            subs[s.user_id] = s

    subs = sorted(subs.values(), key=lambda x: (-x.score, x.time))
    return [
        {
            "user": obj.user.username,
            "score": obj.score,
            "subs": [int(x) for x in obj.subs.split()],
            "avatar": obj.avatar,
            "time": obj.time,
            "votes": obj.user.votes
        }
        for obj in subs
    ]

    # 方案3：调用 Django 的 API (俺不会了
    # ...


def judge(content: str):

    cont = []
    for line in content.split():
        temp = []
        for ele in line.strip().split(sep=','):
            temp.append(bool(int(ele)))
        cont.append(temp)

    ans = []
    with open("./lb/ground_truth.txt") as f:
        for line in f.readlines()[1:]:
            temp = []
            for ele in line.strip().split(sep=',')[1:]:
                temp.append(ele == 'True')
            ans.append(temp)

    if len(ans) != len(cont):
        raise Exception("114514")

    ans = np.array(ans)
    cont = np.array(cont)
    subs = (ans == cont).astype(np.int16).sum(axis=0) / 10

    return subs[0] * 11 + subs[1] * 45 + subs[2] * 14, subs

