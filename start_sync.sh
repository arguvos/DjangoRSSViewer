#!/bin/bash
FILE=/home/ubuntu/django_site/mysite/sync_parser
SYNC_NOW=sync_now
IN_SYNC=in_sync
if [ -f $FILE ];
then
	read line < $FILE
	if [ "$line" = "$SYNC_NOW" ];
	then
		echo "$IN_SYNC" 1>$FILE
		date >> feedsync_log
		python /home/ubuntu/django_site/mysite/manage.py runcrons >> /home/ubuntu/feedsync_log
		echo "" 1>$FILE
	fi
else
	touch $FILE
fi
