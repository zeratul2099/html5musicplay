# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
import os, json
from django.conf import settings
from django.core.servers.basehttp import FileWrapper
import django.views.static
import subprocess
import mutagen


rootPath = settings.MUSIC_ROOT
cacheDir = "/tmp/html5playerCache/"
def home(request):

  return render_to_response("mainview.html",{});
  
def getFiles(request):
  
  try:
	if request.method == 'POST' and "path" in request.POST:
	  
	  path = request.POST["path"].lstrip("/")
	  if ".." in path:
		return HttpResponse("Forbidden", mimetype="text/plain", status=403)
	  files = sorted(map(lambda x: os.path.join(path,x), filter(lambda x: x.endswith(".ogg") or x.endswith(".mp3"),os.listdir(os.path.join(rootPath, path)))))
	  dirs = filter(lambda x: os.path.isdir(os.path.join(rootPath, path, x)),os.listdir(os.path.join(rootPath, path)))
	  files = map(_getOggedFilename, files)
	  print files
	else:
	  dirs = filter(lambda x: os.path.isdir(os.path.join(rootPath, x)),os.listdir(rootPath))
	  files = sorted(filter(lambda x: x.endswith(".ogg") or x.endswith(".mp3"),os.listdir("music")))

	fileData = {}
	for i, fileName in enumerate(files):
	  if not fileName.endswith(".mp3.ogg"):
		tags = dict(mutagen.File(os.path.join(rootPath, fileName), easy=True))
		fileData[i] = (fileName, tags)
	  else:
		tags = dict(mutagen.File(os.path.join(rootPath, fileName)[:-4], easy=True))
		fileData[i] = (fileName, tags)
	return HttpResponse(json.dumps([fileData,dirs]), mimetype="application/json")
  except Exception, e:
	print e

def _getOggedFilename(filename):
  if filename.endswith(".mp3"):
	return filename+".ogg"
  else:
	return filename

def fileConverter(request, filepath):
  if not filepath.endswith(".mp3.ogg"):
	return django.views.static.serve(request, filepath, document_root=rootPath)
  else:
	try:
	  if not os.path.exists(os.path.join(cacheDir,filepath)):
		dir = os.path.dirname(filepath)
		print dir
		if not os.path.exists(os.path.join(cacheDir,dir)):
		  print "creating "+cacheDir+dir
		  os.makedirs(os.path.join(cacheDir, dir))
		frommp3 = subprocess.Popen(['mpg123', '-w', '-', os.path.join(rootPath, filepath)[:-4]], stdout=subprocess.PIPE)
		toogg = subprocess.Popen(['oggenc', '-'], stdin=frommp3.stdout, stdout=subprocess.PIPE)
		with open(os.path.join(cacheDir,filepath), 'wb') as outfile:
		  while True:
			  data = toogg.stdout.read(1024 * 100)
			  if not data:
				  break
			  outfile.write(data)
	  wrapper = FileWrapper(file(os.path.join(cacheDir,filepath)))

	  response = HttpResponse(wrapper, mimetype='application/ogg')
	  response['Content-Length'] = os.path.getsize(os.path.join(cacheDir,filepath))

	  response['Content-Disposition'] = 'attachment; filename='+filepath.encode("utf8")
	  return response
	except Exception, e:
	  raise

# TODO:
# playlist
# stream file during conversion
# volume control
# style player
# seeking
# scrobble
# handle converting error