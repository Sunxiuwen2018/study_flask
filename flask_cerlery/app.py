#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:SunXiuWen
# make_time:2019/1/10

from flask import Flask
from celery.result import AsyncResult  # 异步从backend中获取结果

from celery_tasks import tasks
from celery_tasks.my_celery import celery_app

app = Flask(__name__)

TASK_TD = None


@app.route('/')
def index():
    global TASK_TD
    res = tasks.hello.delay()
    # result_01 = tasks.task_01.apply_async(
    #     args=[1,3],
    #     eta=datetime.datetime(2019,1,11,23,59,59),
    # )
    TASK_TD = res.id
    return "任务已提交"


@app.route('/result')
def result():
    global TASK_TD
    res = AsyncResult(id=TASK_TD, app=celery_app)
    if res.ready():  # 没有结果未False，有结果为True
        return res.get()
    return '等待结果中'


if __name__ == '__main__':
    app.run()
