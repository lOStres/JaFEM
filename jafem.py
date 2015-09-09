import sys, os
import json
import csv
import numpy

from rtree import index
from yaafelib import *


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

# perform k-NN search for file in spatial index
def similarity(directory, filename, k):
    # first extract features from query file
    featureVector = extractFeatures(directory,filename)

    # then open and query spatial index
    p = index.Property()
    p.dat_extension = 'data'
    p.idx_extension = 'index'
    p.dimension = 13

    rtree = index.Index('rtreez', properties=p, interleaved=True)
    similar = list(rtree.nearest((featureVector[0], featureVector[1],
        featureVector[2], featureVector[3], featureVector[4],featureVector[5],
        featureVector[6], featureVector[7], featureVector[8], featureVector[9],
        featureVector[10], featureVector[11], featureVector[12],
        featureVector[0], featureVector[1], featureVector[2], featureVector[3],
        featureVector[4], featureVector[5], featureVector[6], featureVector[7],
        featureVector[8], featureVector[9], featureVector[10],
        featureVector[11], featureVector[12]), k))
    return similar

