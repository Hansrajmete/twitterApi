from django.shortcuts import render
import twitter
import os,time
from project.twiit.models import Document
from project.twiit.forms import DocumentForm
from datetime import datetime
from email.utils import parsedate_tz, mktime_tz


# Create your views here.
def index(request):
    api = twitter.Api(consumer_key = '',
                      consumer_secret='',
                      access_token_key='',
                      access_token_secret='')
    form = DocumentForm()
    documents = Document.objects.all()
    is_file = request.FILES.get('docfile', False)
    if request.method == 'POST' and is_file and request.FILES['docfile'].name != '':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()
            api.PostMedia(request.POST['texttweet'], 'media\/'+ request.FILES['docfile'].name)
            os.remove('media\/'+ request.FILES['docfile'].name)
    elif request.method == 'POST':
        stat = request.POST['texttweet']
        x = api.PostUpdate(stat)

    statuses = api.GetHomeTimeline(count=70)
    for stats in statuses:
        stats.created_at=to_datetime(stats.created_at)
        #stats.created_at = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(stats.created_at,'%a %b %d %H:%M:%S +0000 %Y'))
    return render(
        request,
        'index.html' ,
        {'documents': documents, 'form': form,'statuses' : statuses}
    )

def to_datetime(datestring):
    timestamp = mktime_tz(parsedate_tz(datestring))
    s = str(datetime.fromtimestamp(timestamp))
    return s
