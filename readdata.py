import os,sys
import json
import csv
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


#returns a vector with 2 features
def extractFeatures(directory,filename):
    # yaaaaafe
    fp = FeaturePlan(sample_rate=44100, resample=True)
    fp.addFeature('mfcc: MFCC blockSize=512 stepSize=256 CepsNbCoeffs=1')
    fp.addFeature('psp: PerceptualSpread blockSize=512 stepSize=256')
    df = fp.getDataFlow()
    engine = Engine()
    engine.load(df)
    afp = AudioFileProcessor()

    afp.processFile(engine,os.path.join(directory, filename))
    featureVector = engine.readAllOutputs()

    return featureVector
