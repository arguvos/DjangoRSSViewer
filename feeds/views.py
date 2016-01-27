import math
from login.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template import RequestContext
from feeds.models import Subscription
from feeds.models import RSS_url
from feeds.models import Images
from django.contrib.auth.models import User

@login_required
def show_settings(request):
    url_q = ''
    numb_page = 0
    action = request.POST.get('action','')
    additional_info =  request.POST.get('additional_info','')
    force_update = 'false'

    if request.POST.get('url_text') and (action == 'add_feed'):
        url_q = request.POST['url_text']
        url_q = url_q.strip()
        if len(url_q) > 0:
            user_q = User.objects.get(username = request.user)
            rss = RSS_url.objects.filter(url=url_q)
            if len(rss) > 0: 
                subscr = Subscription.objects.filter(url = rss[0] , user = user_q)
                if len(subscr) <= 0:
                    Subscription.objects.create(user = user_q, url = rss[0])
            else:
                rss_url_q = RSS_url.objects.create(url = url_q)
                Subscription.objects.create(user = user_q, url = rss_url_q)
    elif action == 'update_parser':
        f = open('/home/ubuntu/django_site/mysite/sync_parser', 'w+')
        status_str = f.readline()[0:-1]
        if status_str is None or status_str == '':
            f.write('sync_now\n')
            force_update = 'sync_now'
        elif status_str == 'sync_now':
            force_updte = 'sync_now'
        elif status_str == 'in_sync':
            force_update = 'in_sync'
        f.close()
    elif action == 'clean_all':
        clean_db()
    elif action == 'remove':
        try:
            Subscription.objects.get(id=int(additional_info)).delete()
        except Exception:
            pass
    elif action == 'filter':
        all_list = additional_info.split(' ')
        checked_list = request.POST.getlist('show[]')
        for id_feed in all_list:
            try:
                subcription = Subscription.objects.get(id=int(id_feed))
                if id_feed in checked_list:
                    subcription.show = True
                else:
                    subcription.show = False
                subcription.save()
            except Exception:
               pass
    if action != 'update_parser':
        f = open('/home/ubuntu/django_site/mysite/sync_parser', 'r')
        force_update = f.readline()[0:-1]
        f.close()
    count_note_on_page = 5
    first_note = 0
    last_note = 5
    user_q = User.objects.get(username = request.user)
    feeds = Subscription.objects.filter(user = user_q)
    try:
        max_page = int(math.ceil(len(feeds) / count_note_on_page))
    except Exception:
        max_page = 0
    if request.POST.get('numb_page',''):
        try:
            numb_page = int(request.POST['numb_page'])
            if numb_page < 0:
                numb_page = 0
            if numb_page > max_page:
                numb_page = max_page
        except Exception:
            numb_page = 0
    if action == "prev_page": 
        if (numb_page > 0):
           numb_page = numb_page - 1
    elif action == "next_page":
        if (numb_page < max_page):
                numb_page = numb_page + 1
    first_note = numb_page * count_note_on_page
    last_note = first_note + count_note_on_page
    feeds = feeds[int(first_note) : int(last_note)]

    return render( request,
        'settings.html',
        { 'feeds': feeds, 'numb_page': numb_page, 'max_page': max_page, 'force_update': force_update }
        )
 
 
def clean_db():
    Subscription.objects.all().delete()
    RSS_url.objects.all().delete()
    Images.objects.all().delete()


@login_required
def show_feeds(request):
    subscr = Subscription.objects.filter(user = request.user, show = True)
    images = None
    for elem in subscr:
        if images is None:
            images = Images.objects.filter(rss_url = elem.url, date__gte = elem.date)
        else:
            images = images | Images.objects.filter(rss_url = elem.url, date__gte = elem.date)
    if images is not None:
        images.order_by("date")
        count_note_on_page = 5
        first_note = 0
        last_note = 5
        numb_page = 0
        try:
           max_page = int(math.ceil(len(images) / count_note_on_page))
        except Exception:
            max_page = 0
        if request.POST.get('numb_page', False):
            try:
                numb_page = int(request.POST.get('numb_page', "0"))
                if numb_page < 0:
                    numb_page = 0
                if numb_page > max_page:
                    numb_page = max_page
            except Exception:
                numb_page = 0
        if request.POST.get('action', "").lower() == "Prev Page".lower(): 
            if (numb_page > 0):
                numb_page = numb_page - 1
        if request.POST.get('action', "").lower() == "Next Page".lower():
            if (numb_page < max_page):
                numb_page = numb_page + 1
        first_note = numb_page * count_note_on_page
        last_note = first_note + count_note_on_page
        images = images[first_note : last_note]
#        return HttpResponseRedirect(redirect_to='/feeds/')
        return render( request,
            'feeds.html',
            { 'images': images, 'numb_page': numb_page, 'max_page': max_page }
            )
    else:
        return render_to_response(
            'feeds.html',
            { 'images': [], 'numb_page': 0, 'max_page': 0 }
        )

