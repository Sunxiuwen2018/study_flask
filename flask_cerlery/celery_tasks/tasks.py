#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:SunXiuWen
# make_time:2019/1/10
from celery_tasks.my_celery import celery_app
import datetime


@celery_app.task
def hello():
    print("执行hello任务")
    return 'hello'


@celery_app.task
def go_on():
    print("xxxxx")
    return f"显示时间为:{datetime.datetime.now()}"


from celery.schedules import crontab  # 执行定时任务计划

# 定时任务
celery_app.conf.beat_schedule = {
    'add_every_10_seconds': {
        'task': 'celery_tasks.tasks.go_on',
        # 'schedule': 5.0
        'schedule': crontab(minute='*/1'),
        'args': ()
    }
}

if __name__ == '__main__':
    import os
    os.system('celery beat -A tasks -l info ')
