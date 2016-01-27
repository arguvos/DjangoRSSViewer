#!/bin/bash
date >> feedsync_log
python /home/ubuntu/django_site/mysite/manage.py runcrons >> /home/ubuntu/feedsync_log
