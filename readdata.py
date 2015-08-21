import os,sys
import json
import csv
import numpy

from yaafelib import *

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


#returns a  13 dimensional vector with the mean values of mfccs
def extractFeatures(directory,filename):
    # yaaaaafe
    fp = FeaturePlan(sample_rate=44100, resample=True)
    fp.addFeature('mfcc: MFCC blockSize=1024 stepSize=512')
    df = fp.getDataFlow()
    engine = Engine()
    engine.load(df)
    afp = AudioFileProcessor()

    afp.processFile(engine,os.path.join(directory, filename))
    feats = engine.readAllOutputs()
    featureVector = numpy.mean(feats['mfcc'], axis=0)

    return featureVector
