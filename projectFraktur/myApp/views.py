from django.shortcuts import render, redirect
from PIL import Image as Im
import json
from pathlib import Path
import os

""" Read json files. """
base_dir = Path(__file__).resolve().parent.parent
def readDB(volume, session):
    filename = str(base_dir) + '/data/' + volume + '/' + session + '.json'
    with open(filename, mode="r", encoding='UTF-8') as jsonFile:
        data = json.load(jsonFile)
    return data

def readvolume():
    filename = str(base_dir) + '/data/volumes.json'
    with open(filename, mode="r", encoding='UTF-8') as jsonFile:
        data = json.load(jsonFile)
    return data

""" Function: Home page. """
def home(request):
    return render(request, 'myApp/home.html')

""" Function: transcription. """
def transcription(request):

    trans_data = 'nothing'
    if request.POST:

        """ Getting the image from input by user. """
        image = request.FILES['image']

        """ Transfer the image to text. """

    return render(request, 'myApp/transcription.html', {'trans_data' : trans_data})

"""Function: the exact content according to index. """
def data(request, volume, session):
    sessiondata = readDB(volume, session)
    return render(request, 'myApp/data.html', {'volume' : volume, 'sessiondata' : sessiondata})

""" Function: list the index. """
def volume(request):
    volumes = readvolume()["volumes"]
    return render(request, 'myApp/volume.html', {'volumes' : volumes})

""" Function: list the index. """
def index(request, volume):
    indexes = readDB(volume, 'Contents')["contents"]
    return render(request, 'myApp/index.html', {'volume' : volume, 'indexes' : indexes})


"""Function: delete page. """
def delete(request, volume, session):
    filepath = str(base_dir) + '/data/' + volume
    filename = session + '.json'
    path = os.path.join(filepath, filename)
    os.remove(path)
    contentpath = str(base_dir) + '/data/' + volume + '/' + 'Contents.json'
    with open(contentpath, mode="r", encoding='UTF-8') as newContent:
        data = json.load(newContent)
        temp = data["contents"]
        temp.remove(session)
    with open(contentpath, mode="w", encoding='UTF-8') as newContent:
        json.dump(data, newContent)
    return render(request, 'myApp/delete.html')

"""Function: upload a new page. """
def upload(request, volume, session):
    msg = ''
    filepath = str(base_dir) + '/data/' + volume
    filename = session + '.json'
    data = readDB(volume, session)
    text = data["database"]["content"]
    length = (len(text) + 1) // 2
    if request.POST:
        paragraph = request.POST.get('paragraph')
        content = request.POST.get('content')
        if paragraph == '0':
            text.append('Description')
        else:
            text.append('\u00a7.' + paragraph)
        text.append(content)
        newdata = {
                "database":{
                "session":session,
                "year":data["database"]["year"],
                "content":text
                }
            }
        with open(os.path.join(filepath, filename), 'w') as newFile:
            json.dump(newdata, newFile)
        msg = 'Success!'
    return render(request, 'myApp/upload.html', {'year' : data["database"]["year"], 'session' : session, 'msg' : msg, 'volume' : volume})

"""Function: upload success page. """
def success(request, session, volume):
    return render(request, 'myApp/success.html', {'session' : session, 'volume' : volume})

"""Function: create new page. """
def create(request):
    msg = ''
    volumes = readvolume()["volumes"]
    if request.POST:
        volume = request.POST.get('folder')
        session = request.POST.get('session')
        year = request.POST.get('year')
        if session in readDB(volume, 'Contents')["contents"]:
            msg = 'Wrong! The same session name has existed!'
        else:
            filepath = str(base_dir) + '/data/' + volume
            filename = session + '.json'
            newdata = {
                    "database":{
                    "session":session,
                    "year":year,
                    "content":[]
                    }
                }
            with open(os.path.join(filepath, filename), 'w') as newFile:
                json.dump(newdata, newFile)
            contentpath = str(base_dir) + '/data/' + volume + '/' + 'Contents.json'
            with open(contentpath, mode="r", encoding='UTF-8') as newContent:
                data = json.load(newContent)
                temp = data["contents"]
                temp.append(session)
            with open(contentpath, mode="w", encoding='UTF-8') as newContent:
                json.dump(data, newContent)
            return redirect('success', session=session, volume=volume)
    return render(request, 'myApp/create.html',  {'volumes' : volumes, 'msg' : msg})

"""Function: search by key words. """
def search(request):
    res = []
    volumes = readvolume()["volumes"]
    keyword = ''
    if request.POST:
        keyword = request.POST.get('keyword')
        order = 1
        for volume in volumes:
            contents = readDB(volume, 'Contents')["contents"]
            for session in contents:
                data = readDB(volume, session)["database"]["content"]
                for each in range(len(data)):
                    if keyword in data[each]:
                        index = data[each].index(keyword)
                        left = max(0, index-60)
                        right = min(index+60, len(data[each]))
                        res.append({'order': order, 'volume':volume, 'session':session, 'context': '...' + data[each][left:right+1] + '...', 'paragraph':data[each-1]})
                        order += 1
                        continue
    return render(request, 'myApp/search.html',  {'res' : res, 'keyword' : keyword})

"""Function: edit. """
def edit(request, volume, session):
    sessiondata = readDB(volume, session)
    filepath = str(base_dir) + '/data/' + volume
    filename = session + '.json'
    if request.POST:
        paragraph = int(request.POST.get('paragraph'))
        content = request.POST.get('content')
        newcontent = sessiondata["database"]["content"]
        direction = (paragraph - int(newcontent[2][2:]))*2 + 3
        newcontent[direction] = content
        newdata = {
                    "database":{
                    "session":session,
                    "year":sessiondata["database"]["year"],
                    "content": newcontent
                    }
                }
        with open(os.path.join(filepath, filename), 'w') as newFile:
                json.dump(newdata, newFile)
    return render(request, 'myApp/edit.html', {'volume' : volume, 'sessiondata' : sessiondata, 'session' : session})

"""Function: source. """
def source(request, volume, session, filename):
    filepath = str(base_dir) + '/myApp/static/' + volume + '/' + session
    filelist = os.listdir(filepath)
    numdic = {}
    for v in filelist:
        right = v.index('[')
        numdic[v] = v[4:right]
    res = dict(sorted(numdic.items(), key=lambda item: int(item[1])))
    filelist = res.keys()
    file = volume + '/' + session + '/' + filename
    return render(request, 'myApp/source.html', {'volume' : volume, 'filelist' : filelist, 'session' : session, 'filename' : filename, 'file' : file})