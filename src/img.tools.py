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
import ImageFilter


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
		elif a == "blur":
			return img_blur(file, url, img)
		elif a == "detail":
			return img_detail(file, url, img)
		elif a == "contour":
			return img_contour(file, url, img)
		elif a == "edge_enhance":
			return img_edge_enhance(file, url, img)
		elif a == "edge_enhance_more":
			return img_edge_enhance_more(file, url, img)
		elif a == "emboss":
			return img_emboss(file, url, img)
		elif a == "find_edges":
			return img_find_edges(file, url, img)
		elif a == "smooth":
			return img_smooth(file, url, img)
		elif a == "smooth_more":
			return img_smooth_more(file, url, img)
		elif a == "sharpen":
			return img_sharpen(file, url, img)
			
@error(404)
def error_hdl(error):
    return "<b>Ups, this is bad...</b>" 
	

def get_img_id():
	return str(uuid.uuid1())
	
# IMAGE PROCESS FUNCTIONS	

def img_bw(file, url, img):
	img2 = img.convert('L')
	return save_tmp(file, url, img2)	
	
def img_rotate(file, url, img, degrees):
	img2 = img.rotate(degrees)
	return save_tmp(file, url, img2)		

def img_blur(file, url, img):
	img2 = img.filter(ImageFilter.BLUR)
	return save_tmp(file, url, img2)

def img_detail(file, url, img):
	img2 = img.filter(ImageFilter.DETAIL)
	return save_tmp(file, url, img2)	
	
def img_contour(file, url, img):
	img2 = img.filter(ImageFilter.CONTOUR)
	return save_tmp(file, url, img2)
	
def img_edge_enhance(file, url, img):
	img2 = img.filter(ImageFilter.EDGE_ENHANCE)
	return save_tmp(file, url, img2)

def img_edge_enhance_more(file, url, img):
	img2 = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
	return save_tmp(file, url, img2)

def img_emboss(file, url, img):
	img2 = img.filter(ImageFilter.EMBOSS)
	return save_tmp(file, url, img2)

def img_find_edges(file, url, img):
	img2 = img.filter(ImageFilter.FIND_EDGES)
	return save_tmp(file, url, img2)

def img_smooth(file, url, img):
	img2 = img.filter(ImageFilter.SMOOTH)
	return save_tmp(file, url, img2)

def img_smooth_more(file, url, img):
	img2 = img.filter(ImageFilter.SMOOTH_MORE)
	return save_tmp(file, url, img2)

def img_sharpen(file, url, img):
	img2 = img.filter(ImageFilter.SHARPEN)
	return save_tmp(file, url, img2)
	
def save_tmp(file, url, img2):
	tmp = get_img_id() + os.path.splitext(url)[1]
	img2.save('tmp/' + tmp)
	return static_file(tmp, 'tmp')	

def start_server():
    debug(True)
    run(host='localhost', port=8000)

if __name__ == '__main__':
	start_server()