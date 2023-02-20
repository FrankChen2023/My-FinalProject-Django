from django.shortcuts import render, redirect
from PIL import Image as Im
import json
from pathlib import Path
import os

""" Read json files. """
base_dir = Path(__file__).resolve().parent.parent
def readDB(volume, minute):
    filename = str(base_dir) + '/data/' + volume + '/' + minute + '.json'
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
def data(request, volume, minute):
    minutedata = readDB(volume, minute)
    return render(request, 'myApp/data.html', {'volume' : volume, 'minutedata' : minutedata})

""" Function: list the index. """
def volume(request):
    volumes = readvolume()["volumes"]
    return render(request, 'myApp/volume.html', {'volumes' : volumes})

""" Function: list the index. """
def index(request, volume):
    indexes = readDB(volume, 'Contents')["contents"]
    return render(request, 'myApp/index.html', {'volume' : volume, 'indexes' : indexes})


"""Function: delete page. """
def delete(request, volume, minute):
    filepath = str(base_dir) + '/data/' + volume
    filename = minute + '.json'
    path = os.path.join(filepath, filename)
    os.remove(path)
    contentpath = str(base_dir) + '/data/' + volume + '/' + 'Contents.json'
    with open(contentpath, mode="r", encoding='UTF-8') as newContent:
        data = json.load(newContent)
        temp = data["contents"]
        temp.remove(minute)
    with open(contentpath, mode="w", encoding='UTF-8') as newContent:
        json.dump(data, newContent)
    return render(request, 'myApp/delete.html')

"""Function: upload a new page. """
def upload(request, volume, minute):
    msg = ''
    filepath = str(base_dir) + '/data/' + volume
    filename = minute + '.json'
    data = readDB(volume, minute)
    text = data["database"]["content"]
    length = (len(text) + 1) // 2
    if request.POST:
        content = request.POST.get('content')
        text.append('\u00a7.'+str(length))
        text.append(content)
        newdata = {
                "database":{
                "minute":minute,
                "year":data["database"]["year"],
                "content":text
                }
            }
        with open(os.path.join(filepath, filename), 'w') as newFile:
            json.dump(newdata, newFile)
        msg = 'Success!'
    return render(request, 'myApp/upload.html', {'year' : data["database"]["year"], 'minute' : minute, 'msg' : msg, 'volume' : volume})

"""Function: upload success page. """
def success(request, minute, volume):
    return render(request, 'myApp/success.html', {'minute' : minute, 'volume' : volume})

"""Function: create new page. """
def create(request):
    msg = ''
    volumes = readvolume()["volumes"]
    if request.POST:
        volume = request.POST.get('folder')
        minute = request.POST.get('minute')
        year = request.POST.get('year')
        if minute in readDB(volume, 'Contents')["contents"]:
            msg = 'Wrong! The same minute name has existed!'
        else:
            filepath = str(base_dir) + '/data/' + volume
            filename = minute + '.json'
            newdata = {
                    "database":{
                    "minute":minute,
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
                temp.append(minute)
            with open(contentpath, mode="w", encoding='UTF-8') as newContent:
                json.dump(data, newContent)
            return redirect('success', minute=minute, volume=volume)
    return render(request, 'myApp/create.html',  {'volumes' : volumes, 'msg' : msg})

"""Function: search by key words. """
def search(request):
    res = []
    volumes = readvolume()["volumes"]
    keyword = ''
    if request.POST:
        keyword = request.POST.get('keyword')
        for volume in volumes:
            contents = readDB(volume, 'Contents')["contents"]
            for minute in contents:
                data = readDB(volume, minute)["database"]["content"]
                for each in range(len(data)):
                    if keyword in data[each]:
                        index = data[each].index(keyword)
                        left = max(0, index-60)
                        right = min(index+60, len(data[each]))
                        res.append({'volume':volume, 'minute':minute, 'context': '...' + data[each][left:right+1] + '...', 'paragraph':data[each-1]})
                        continue
    return render(request, 'myApp/search.html',  {'res' : res, 'keyword' : keyword})

"""Function: edit. """
def edit(request, volume, minute):
    minutedata = readDB(volume, minute)
    filepath = str(base_dir) + '/data/' + volume
    filename = minute + '.json'
    if request.POST:
        paragraph = int(request.POST.get('paragraph'))
        content = request.POST.get('content')
        newcontent = minutedata["database"]["content"]
        newcontent[paragraph*2+1] = content
        newdata = {
                    "database":{
                    "minute":minute,
                    "year":minutedata["database"]["year"],
                    "content": newcontent
                    }
                }
        with open(os.path.join(filepath, filename), 'w') as newFile:
                json.dump(newdata, newFile)
    return render(request, 'myApp/edit.html', {'volume' : volume, 'minutedata' : minutedata, 'minute' : minute})