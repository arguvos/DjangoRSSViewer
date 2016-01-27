#!/bin/bash
FILE=/home/ubuntu/django_site/mysite/sync_parser
SYNC_NOW=sync_now
IN_SYNC=in_sync
if [ -f $FILE ];
then
	read line < $FILE
	if [ "$line" = "" ];
	then
		echo "$SYNC_NOW" 1>$FILE
	fi
else
	touch $FILE
	echo "$SYNC_NOW" 1>$FILE
fi
