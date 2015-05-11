import os
import json


def parseJson(directory, filename):
    data=[]
    jsonMetaList=[]
    #open all files that end with .json in <path> directory
    #and store certain attributes
    if filename.endswith(".json"):
        json_data=open(os.path.join(directory, filename))
        data=json.load(json_data)
        jsonMetaList.append(data['filesize'])
        jsonMetaList.append(data['duration'])
        jsonMetaList.append(data['samplerate'])
        jsonMetaList.append(data['tags'])
        jsonMetaList.append(data['type'])

    return jsonMetaList

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

