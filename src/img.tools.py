# -*- coding: utf-8 -*-

__author__ = "mRt (martincerdeira@gmail.com)"
__version__ = "0.01"
__date__ = "$Date: 4/2/2012$"
__license__ = "GPL v3"

from bottle import run, route, error, request, response, get, post, request, debug, static_file, url
from PIL import Image
import urllib, cStringIO
import uuid
import os.path


@route('/')
def default():
	return "<b>You are lost.</b>"

@route('<img_url:path>')
def main(img_url):
	url = img_url[1:]
	file = file = cStringIO.StringIO(urllib.urlopen(url).read())
	img = Image.open(file)
	#Todo: use callbacks to concatenate image processing funcions	
	for a in request.query.getall("action"):
		if "(" in a and ")" in a: # action with parameters
			a = a.replace("(", "|").replace(")", "|").split("|")
			if a[0] == "rotate":
				return img_rotate(file, url, img, float(a[1]))
		elif a == "black_white":
			return img_bw(file, url, img)
			
@error(404)
def error_hdl(error):
    return "<b>Ups, this is bad...</b>" 
	

def get_img_id():
	return str(uuid.uuid1())
	
# IMAGE PROCESS FUNCTIONS	

def img_flip():
	pass

def img_bw(file, url, img):
	img2 = img.convert('L')
	tmp = get_img_id() + os.path.splitext(url)[1]
	img2.save('tmp/' + tmp)
	return static_file(tmp, 'tmp')	
	
def img_rotate(file, url, img, degrees):
	img2 = img.rotate(degrees)
	tmp = get_img_id() + os.path.splitext(url)[1]
	img2.save('tmp/' + tmp)
	return static_file(tmp, 'tmp')		

def img_size(size):
	pass

def img_addtext():
	pass
	
def img_gallery():
	pass
	
def img_crop():
	pass

def start_server():
    debug(True)
    run(host='localhost', port=8000)

if __name__ == '__main__':
	start_server()