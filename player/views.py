# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
import os, json
from django.conf import settings
def home(request):

  return render_to_response("mainview.html",{});
  
def getFiles(request):
  rootPath = settings.MUSIC_ROOT
  try:
	if request.method == 'POST' and "path" in request.POST:
	  
	  path = request.POST["path"].lstrip("/");
	  print os.listdir(os.path.join(rootPath, path))
	  files = sorted(map(lambda x: os.path.join(path,x), filter(lambda x: x.endswith(".ogg"),os.listdir(os.path.join(rootPath, path)))));
	  dirs = filter(lambda x: os.path.isdir(os.path.join(rootPath, path, x)),os.listdir(os.path.join(rootPath, path)))
	else:
	  dirs = filter(lambda x: os.path.isdir(os.path.join(rootPath, x)),os.listdir(rootPath))
	  files = sorted(filter(lambda x: x.endswith(".ogg"),os.listdir("music")));
	return HttpResponse(json.dumps([files,dirs]), mimetype="application/json")
  except Exception, e:
	print e
	
	
# TODO:
# volume control
# shuffle, repeat
# style player
# seeking
# show id-tag information
# scrobble
# on-the-fly converting mp3 to ogg