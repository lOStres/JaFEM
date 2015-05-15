import os,sys
import json
import csv
import soundfile as sf
from scipy.fftpack import dct
from features import mfcc,fbank,sigproc,logfbank

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


#returns a vector with (currently)  4 features
def extractFeatures(directory,filename):
	try:
		data,samplerate=sf.read(os.path.join(directory, filename))
	except (IOError, RuntimeError):
		print("Could not open file ", filename)
		print("Exiting...")
		sys.exit()
	#if file was opened succesfully proceed with feature extraction
	#win is the size of window for mfcc extraction AND step size
	win=data.size/(4*samplerate)
	featureVector=mfcc(data,samplerate,win,win,1)
	#featureVector is of type numpy_array
	return featureVector
