from pygtrans import Translate
import numpy as np
import argparse


class Reviewer:
    def __init__(self, ss, lb, rb, r, t, num):
        self.client = Translate()
        self.file = open("./words/TPO_Reviewer.txt", "r", encoding='utf-8')
        self.word_list = []
        self.word_size = 0
        self.lower_bound = int(lb)
        self.upper_bound = int(rb)
        self.selected_words = []
        self.range = []
        self.size = int(ss)
        self.random = int(r)
        self.translate = int(t)
        self.num = int(num)

        for line in self.file:
            words = line.split(',')
            if len(words) == 1:
                words = [str(line)]
            for word in words:
                if word != '\n':
                    l = len(word)
                    if word[l - 1] == '\n' or word[l - 1] == ',':
                        word = word[0:l - 1]
                    if word[0] == ' ':
                        word = word[1:]
                    self.word_list.append(word)
        self.word_size = len(self.word_list)

    def select_words(self):
        if self.upper_bound > self.word_size:
            self.upper_bound = self.word_size
        self.selected_words = []
        self.range = []
        tmp = []
        for i in range(self.lower_bound, self.upper_bound):
            tmp.append(i)
        if self.random == 0:
            for i in range(self.lower_bound, min(self.lower_bound + self.size, self.upper_bound)):
                self.range.append(i)
        else:
            j = np.random.choice(tmp, size=self.size, replace=False)
            for i in range(0, self.size):
                self.range.append(j[i])

        print(self.range)

        for i in range(0, self.size):
            self.selected_words.append(self.word_list[self.range[i]])

    def generate(self):
        for i in range(1, self.num + 1):
            pair_list = []
            self.select_words()
            for word in self.selected_words:
                pair = []
                tr = self.client.translate(word, target="zh-CN")
                pair.append(word)
                pair.append(tr.translatedText)
                pair_list.append(pair)
            if self.translate == 1:
                filename = "./generated/translated_" + str(i) + ".txt"
                f = open(filename, "w", encoding='utf-8')
                i = 1
                for pair in pair_list:
                    f.write("第" + str(i) + "个单词：" + str(pair[0]) + ", " + str(pair[1]) + "\n")
                    i = i + 1
            else:
                filename = "./generated/untranslated_" + str(i) + ".txt"
                f = open(filename, "w", encoding='utf-8')
                i = 1
                for pair in pair_list:
                    f.write("第" + str(i) + "个单词：" + str(pair[0]) + "\n")
                    i = i + 1


ps = argparse.ArgumentParser(description="I i yo, Go i yo!")
ps.add_argument("-s", "--size", default=20)
ps.add_argument("-n", "--num", default=114)
ps.add_argument("-lb", "--lower_bound", default=0)
ps.add_argument("-rb", "--upper_bound", default=114514)
ps.add_argument("-r", "--rand", nargs='?', default=0)
ps.add_argument("-t", "--trans", nargs='?', default=0)

arg_list = ps.parse_args()
s, lb, rb, r, t, num = arg_list.size, arg_list.lower_bound, arg_list.upper_bound, arg_list.rand, arg_list.trans, arg_list.num
if r is None or r == [] or r != 0:
    r = 1
if t is None or t == [] or t != 0:
    t = 1
reviewer = Reviewer(s, lb, rb, r, t, num)
reviewer.generate()
