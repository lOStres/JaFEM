import os
import json
import csv


def parseJSON(directory, filename):
    data=[]
    jsonMeta=[]
    #open all files that end with .json in <path> directory
    #and store certain attributes
    try:
        json_data=open(os.path.join(directory, filename))
    except(IOError, RuntimeError ):
        print("Cannot open ", filename)

    data=json.load(json_data)
    jsonMeta.append(data['filesize'])
    jsonMeta.append(data['duration'])
    jsonMeta.append(data['samplerate'])
    jsonMeta.append(data['tags'])
    jsonMeta.append(data['type'])

    return jsonMeta

def parseCSV(directory, filename):
    with open(os.path.join(directory, filename)) as csvfile:
        csvMeta = csv.reader(csvfile, delimiter=",")
        return list(csvMeta)[0]
