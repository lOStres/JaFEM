import json


data=[]
def readvalues(files):
	lista=[]
	#open all files that end with .json in <path> directory
	#and store certain attributes
	if files.endswith(".json"):
		json_data=open(files)
		data=json.load(json_data)
		lista.append(data['filesize'])
		lista.append(data['duration'])
		lista.append(data['samplerate'])
		lista.append(data['tags'])
		lista.append(data['type'])
		lista.append(data['geotag'])
		
	return lista

		

