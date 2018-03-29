# -*- coding: UTF-8 -*-
"""
hello_flask: First Python-Flask webapp
"""
from flask import Flask  # From module flask import class Flask
from flask import request
import requests

from db import DB
from flask.helpers import make_response
from flask_cors import CORS
from urllib.parse import urlparse, parse_qs,urlencode
import urllib
import collections
from flask import Response
from django.db.backends.dummy.base import ignore

# 出现的问题的解决方案
# https://www.ntu.edu.sg/home/ehchua/programming/webprogramming/Python3_Flask.html
# https://www.ntu.edu.sg/home/ehchua/programming/webprogramming/Python2_Apps.html#virtualenv

db = DB()
# db.createTable()

app = Flask(__name__)    # Construct an instance of Flask class for our webapp
CORS(app)

@app.route('/<path>', methods=['GET','POST'])   # URL '/' to be handled by main() route handler
def main(path):
	
	paramdict = getparamdict()
	cachekey = request.path + "?" + urlencode(paramdict)
	
# 	urlencode(querydict)
	
	data = db.getdatabyurl(cachekey)
# 	parsere = urlparse(request.url)
	
# 	return r.text
	remote = "https://dev-trade.sbifxt.co.jp/api_fxt/HttpApi/"
	dataresp = None
	if(data == None):
		
		if(request.method == "GET"):
			url = remote + request.path + "?" + request.query_string.decode("utf-8")
			r = requests.get(url,verify=False)
		elif(request.method  == "POST"):
			r = requests.post(remote + request.path, data=request.form, verify=False)
			
		if(r.status_code == 200):
			data = parseResult(r.text)
			if(data["status"] == "0"):
				db.savetocache(cachekey, r.text)
				dataresp = make_response(r.text)
		else:
# 			make_response(r.content.decode("utf-8"), r.status_code)
			dataresp =  Response(r.content.decode("utf-8"), status=r.status_code)
		
	else:
# 		get data from cache 
		dataresp = make_response(data[1])
# 	resp.headers["Access-Control-Allow-Origin"] = "*"
# 	resp.headers["Access-Control-Allow-Credentials"] = "*"
	return dataresp

def useCache():
	querydict = parse_qs(urlparse(request.url).query)
	return "TRUE". querydict["cache"] == True
		

def parseResult(data):
	strlist = data.splitlines()
	result = {}
	result["data"] = []
	
	for i in range(0,len(strlist)):
		cols = strlist[i].split("\t")		
		if(i == 0):
			if(len(cols) < 4):
				result["status"] = "2"
				result["message"] = "API data format error"
				continue
			result["name"] = cols[0]
			result["status"] = cols[1]
			result["message"] = cols[2]
			result["timestamp"] = cols[3]
			result["headers"] = cols
		else:
			result["data"].append(cols)
	return result
		
def getparamdict():
	ignoreparams = ['SESN', 'GUID']
	if(request.method == "GET"):
		querydict = parse_qs(urlparse(request.url).query)
		map(lambda m: querydict.pop(m, None), ignoreparams)
		sortedquerydict = collections.OrderedDict(sorted(querydict.items()))
		return sortedquerydict
	elif(request.method == "POST"):
		querydict = dict(request.form)
		querydict = parse_qs(urlparse(request.url).query)
		sortedquerydict = collections.OrderedDict(sorted(querydict.items()))
		return sortedquerydict
		
if __name__ == '__main__':  # Script executed directly?
	app.run(debug=True)  # Launch built-in web server and run this Flask webapp
