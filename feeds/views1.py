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
    url_q = 'www.def.ru'
    if (request.GET.get('url_text') and request.GET.get('add_btn')):
        url_q = request.GET['url_text']
        user_q = User.objects.get(username = request.user)
        rss = RSS_url.objects.filter(url=url_q)
        if len(rss) > 0: 
            subscr = Subscription.objects.filter(url = rss[0] , user = user_q)
            if len(subscr) <= 0:
            #    rss_url_q = RSS_url.objects.create(url = url_q)
                Subscription.objects.create(user = user_q, url = rss_url_q)
        else:
            rss_url_q = RSS_url.objects.create(url = url_q)
            Subscription.objects.create(user = user_q, url = rss_url_q)

    if (request.GET.get('clean_all')):
        clean_db()
    try:
        if (request.GET.get('remove_btn')):
            sub_id = request.GET.get('remove_btn')
        #try:
            Subscription.objects.get(id=sub_id).delete()
        #except Exeption:
    finally:
        feeds = Subscription.objects.all()[1:5]
        page_numb = 1;
        if (request.GET.get('page_numb')): 
            page_numb = request.GET.get['page_numb']
#        if len(feeds) > 5:
        return render_to_response(
            'settings.html',
    #       { 'user': request.user },
    { 'feeds': feeds, 'page_numb': page_numb, 'prev_page': prev_page, 'next_page': next_page }
        )
 
@login_required
def show_feeds(request):
    subscr = Subscription.objects.filter(user = request.user)
    images = None 
    for elem in subscr:
        if images is None:
            images = Images.objects.filter(rss_url = elem.url, date__gte = elem.date)
        else:
            images = images | Images.objects.filter(rss_url = elem.url, date__gte = elem.date)
    if iamges is not None:
        images.order_by("-date")

    return render_to_response(
        'feeds.html',
        { 'images': images }
    )
 
def clean_db():
    Subscription.objects.all().delete()
    RSS_url.objects.all().delete()
    Images.objects.all().delete()

