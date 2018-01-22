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

# https://www.ntu.edu.sg/home/ehchua/programming/webprogramming/Python3_Flask.html
# https://www.ntu.edu.sg/home/ehchua/programming/webprogramming/Python2_Apps.html#virtualenv

db = DB()
# db.createTable()

app = Flask(__name__)    # Construct an instance of Flask class for our webapp
CORS(app)

@app.route('/<path>', methods=['GET','POST'])   # URL '/' to be handled by main() route handler
def main(path):
	
	paramdict = getparamdict()
	catchkey = request.path + "?" + urlencode(paramdict)
	
# 	urlencode(querydict)
	
	data = db.getdatabyurl(catchkey)
	
# 	parsere = urlparse(request.url)
	
# 	return r.text
	remote = "https://dev-trade.sbifxt.co.jp/api_fxt/HttpApi/"
	dataresp = None
	if(data == None):
		
		if(request.method == "GET"):
			url = remote + request.path + "?" + request.query_string.decode("utf-8")
			r = requests.get(url,verify=False)
			dataresp = make_response(r.text)
		elif(request.method  == "POST"):
			r = requests.post(remote + request.path, data=request.form, verify=False)
			dataresp = make_response(r.text)
			
			
		if(r.status_code == 200):
			db.exesql("insert into datacache values(?,?)",[catchkey ,r.text])
			data = r.text
			dataresp = make_response(r.text)
		else:
# 			make_response(r.content.decode("utf-8"), r.status_code)
			dataresp =  Response(r.content.decode("utf-8"), status=r.status_code)
		
	else:
		dataresp = make_response(data[1])
# 	resp.headers["Access-Control-Allow-Origin"] = "*"
# 	resp.headers["Access-Control-Allow-Credentials"] = "*"
	return dataresp

def getparamdict():
	if(request.method == "GET"):
		querydict = parse_qs(urlparse(request.url).query)
		querydict.pop('SESN', None)
		querydict.pop('GUID', None)
		sortedquerydict = collections.OrderedDict(sorted(querydict.items()))
		return sortedquerydict
	elif(request.method == "POST"):
		querydict = dict(request.form)
		querydict.pop('SESN', None)
		querydict.pop('GUID', None)
		sortedquerydict = collections.OrderedDict(sorted(querydict.items()))
		return sortedquerydict
		
if __name__ == '__main__':  # Script executed directly?
	app.run(debug=True)  # Launch built-in web server and run this Flask webapp
