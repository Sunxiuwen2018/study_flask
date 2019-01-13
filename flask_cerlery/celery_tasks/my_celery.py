#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:SunXiuWen
# make_time:2019/1/10
from celery import Celery

celery_app = Celery('task_name',
                    broker='redis://127.0.0.1:6379',
                    backend='redis://127.0.0.1:6379',
                    include=['celery_tasks.tasks']
                    )
celery_app.conf.timezone = 'Asia/Shanghai'
celery_app.conf.enable_utc = False

if __name__ == '__main__':
    import os
    os.system('celery worker -A my_celery -l info -P eventlet')
    # os.system('celery beat -A my_celery -l info ')   # 在这里执行无效果
