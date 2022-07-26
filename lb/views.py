from django.http import (
    HttpRequest,
    JsonResponse,
    HttpResponseNotAllowed,
)
from lb.models import Submission, User
import time
from django.forms.models import model_to_dict
from django.db.models import F
import json
from lb import utils
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.views.decorators.http import require_http_methods as method


def hello(req: HttpRequest):
    return JsonResponse({
        "code": 0,
        "msg": "hello"
    })


@method(["GET"])
def leaderboard(req: HttpRequest):
    return JsonResponse(
        utils.get_leaderboard(),
        safe=False,
    )


@method(["GET"])
def history(req: HttpRequest, username: str):
    # TODO: Complete `/history/<slug:username>` API
    his = Submission.objects.filter(user__username=username).order_by('time')
    if len(his) == 0:
        return JsonResponse({
            "code": -1
        })
    return JsonResponse({
        "code": 0,
        "data": [
            {
                "score": obj.score,
                "subs": [int(float(x)) for x in obj.subs[1:-1].split()],
                "time": obj.time
            }
            for obj in his
        ]})


@method(["POST"])
@csrf_exempt
def submit(req: HttpRequest):
    info = json.load(req.body)
    if not all(k in info.keys() for k in ("user", "avatar", "content")):
        return JsonResponse({
            "code": 1,
            "msg": "你是一个，一个一个一个不全的参数啊啊啊"
        })

    if len(info['user']) > 255:
        return JsonResponse({
            "code": -1,
            "msg": "你是一个，一个一个一个太长的用户啊啊啊"
        })

    if len(info['avatar']) > 100_000:
        return JsonResponse({
            "code": -2,
            "msg": "你是一个，一个一个一个太大的图像啊啊啊",
        })
    try:
        main_score, sub_score = utils.judge(info['content'])
    except Exception("114514"):
        return JsonResponse({
            "code": -3,
            "msg": "你是一个，一个一个一个非法的内容啊啊啊"
        })
    user = User.objects.filter(username=info['user']).first()
    if not user:
        user = User.objects.create(username=info['user'], votes=0)
    Submission.objects.create(user=user, avatar=info['avatar'], time=time.time(), score=main_score, subs=sub_score)
    return JsonResponse({
        "code": 0,
        "msg": "你是一个，一个一个一个成功的提交啊啊啊",
        "data": {
            "leaderboard": utils.get_leaderboard()
        }
    })


@method(["POST"])
@csrf_exempt
def vote(req: HttpRequest):
    if 'User-Agent' not in req.headers \
            or 'requests' in req.headers['User-Agent']:
        return JsonResponse({
            "code": -1,
            "msg": "压打莫压打，牡蛎莫牡蛎"
        })

    user = json.loads(req.body)['user']
    user = User.objects.filter(username=user).first()
    if not user:
        return JsonResponse({
            "code": -1,
            "msg": "该用户没有注册，已经等不及了，快端上来罢"
        })
    user.votes += 1
    user.save()
    return JsonResponse({
        "code": 0,
        "data": {
            "leaderboard": utils.get_leaderboard()
        }
    })

