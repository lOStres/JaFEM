import wave,sys,struct
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
import json
import soundfile as sf
import psycopg2
from soundfile import SoundFile



for i in range(6901,6904):
	try:
		filename=str(i)+'.wav'
		data,samplerate=sf.read(filename)
		print(samplerate)
		
	except (IOError, RuntimeError):
		print "File does not exist, continuing1..."

	try:
		filename=str(i)+".ogg"
		data,samplerate=sf.read(filename)
		print(samplerate)
		
	except (IOError, RuntimeError):
		print "File does not exist, continuing2..."
	try:
		filename=str(i)+".aif"
		data,samplerate=sf.read(filename)
		print(samplerate)
		
	except (IOError, RuntimeError):
		print "File does not exist, continuing3..."
	try:
		filename=str(i)+".flac"
		data,samplerate=sf.read(filename)
		print(samplerate)
		
	except (IOError, RuntimeError):
		print "File does not exist, continuing4..."




def extract_features(data,samplerate):
	win=data.size/(8*samplerate)
	mfcc_feat=mfcc(data,samplerate,win,win,1)
	return mfcc_feat


