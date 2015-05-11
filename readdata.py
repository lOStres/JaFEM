import os
import json


def parseJSON(directory, filename):
    data=[]
    jsonMeta=[]
    #open all files that end with .json in <path> directory
    #and store certain attributes
    json_data=open(os.path.join(directory, filename))
    data=json.load(json_data)
    jsonMeta.append(data['filesize'])
    jsonMeta.append(data['duration'])
    jsonMeta.append(data['samplerate'])
    jsonMeta.append(data['tags'])
    jsonMeta.append(data['type'])

    return jsonMeta


def loadFiles(directory):

    print("Searching in directory: ", directory)

    for file in os.listdir(directory):
        name , extension = file.rsplit('.',1);
        # parse and store meta-data to db
        if extension == "json":
            jsonMeta = parseJson(directory, file)
            print(jsonMeta)
        elif extension == "csv":
            pass    # do something
        # retrieve link to sound file and store it to db
        else:
            pass    # do something

