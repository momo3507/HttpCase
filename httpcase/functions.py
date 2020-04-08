# coding: utf-8
"""
函数助手
"""
import random
import time


def __randInt(min,max):
    return str(random.randint(int(min),int(max)))

def __timeStamp():
    return str(int(time.time()*1000))


if __name__ == '__main__':
    print(__randInt(1,2))