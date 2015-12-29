from django.conf import settings
from django.contrib.auth.models import User

from django_common.helper import send_mail
from django_cron import CronJobBase, Schedule

from  feeds.models import RSS_url
from  feeds.models import Images 

from time import mktime
from datetime import datetime
import dateutil.parser

import os
import urllib
import PIL.ImageFile as ImageFile
import feedparser

import re

IMG_URL_REGEX = re.compile('https?://(?:[a-z0-9\-]+\.)+[a-z]{2,6}(?:/[^/#?]+)+\.(?:jpg|gif|png)')

class UpdateFeeds(CronJobBase):
    """
    Send an email with the user count.
    """
    RUN_EVERY_MINS = 1 

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'cron.UpdateFeeds'

    def do(self):
        print('start__parsing')
        for rss in RSS_url.objects.all():
            date_for_sync = self.get_date_to_sync(rss)
            for entrie in feedparser.parse(rss.url).entries:
                date_for_sync = date_for_sync.replace(tzinfo=None)
                date_time_publish = datetime.fromtimestamp(mktime(entrie.published_parsed))
#                print(dateutil.parser.parse(date_for_sync))
                if date_time_publish > date_for_sync:
                    #print(entrie.title)
                    try:
                        for img_url in IMG_URL_REGEX.findall(entrie.summary):
                            sizes = getsizes(img_url)
                            if sizes[1] is not None:
                                if (sizes[1][0] < 1024) and (sizes[1][1] < 1024):
                                    Images.objects.create(rss_url = rss, image_url = img_url)
                    except Exception:
                        pass
                    for enclosure in entrie.enclosures:
                        sizes = getsizes(enclosure.href)
                        if sizes[1] is not None:
                            if (sizes[1][0] < 1024) and (sizes[1][1] < 1024):
                                Images.objects.create(rss_url = rss, image_url = enclosure.href)
        print('end__parsing')


    def get_date_to_sync(self, rss_url_obj):
        create_date = rss_url_obj.date
        try:
            last_image_date = Images.objects.filter(url__exact = rss_url_obj.url).order_by('-date')[0].date
            if last_image_date > create_date:
                return last_image_date
            else:
                return create_date 
        except Exception:
            return create_date




def getsizes(uri):
    # get file size *and* image size (None if not known)
    file = urllib.urlopen(uri)
    size = file.headers.get("content-length")
    if size: size = int(size)
    p = ImageFile.Parser()
    while 1:
        data = file.read(1024)
        if not data:
            break
        p.feed(data)
        if p.image:
            return size, p.image.size
            break
    file.close()
    return size, None


