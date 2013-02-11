# -*- coding: utf-8 -*-

__author__ = "mRt (martincerdeira@gmail.com)"
__version__ = "0.01"
__date__ = "$Date: 4/2/2012$"
__license__ = "GPL v3"

from bottle import run, route, error, request, response, get, post, request, debug, static_file, url, HTTPResponse
from PIL import Image
import urllib, cStringIO
import uuid
import urlparse, os
import ImageFilter
import mimetypes

_cache = dict() # This is a toy cache handler, replace it with better stuff


@route('/')
def default():
    return "Oops"


@route('<img_url:path>')
def main(img_url):
    url = img_url[1:]
    try:
        file = cStringIO.StringIO(_cache[url])
    except KeyError:
        _cache[url] = urllib.urlopen(url).read()
        file = cStringIO.StringIO(_cache[url])
                
    img = Image.open(file)    
    return img_process(request.query.getall("action"), url, img)
    

@error(404)
def error_hdl(error):
    return "<b>Ups, this is bad...</b>"

# IMAGE PROCESS FUNCTIONS

def img_process(actions, url, img):
    # Process all the requested transformations
    for a in actions:
        if "(" in a and ")" in a: # action with parameters
            a = a.replace("(", "|").replace(")", "|").split("|")
            if a[0] == "rotate":
                img = img_rotate(url, img, float(a[1]))
        elif a == "black_white":
            img = img_bw(url, img)
        elif a == "blur":
            img = img_blur(url, img)
        elif a == "detail":
            img = img_detail(url, img)
        elif a == "contour":
            img = img_contour(url, img)
        elif a == "edge_enhance":
            img = img_edge_enhance(url, img)
        elif a == "edge_enhance_more":
            img = img_edge_enhance_more(url, img)
        elif a == "emboss":
            img = img_emboss(url, img)
        elif a == "find_edges":
            img = img_find_edges(url, img)
        elif a == "smooth":
            img = img_smooth(url, img)
        elif a == "smooth_more":
            img = img_smooth_more(url, img)
        elif a == "sharpen":
            img = img_sharpen(url, img)
    
    #Return final result
    return save_tmp(url, img)

def img_bw(url, img):
    return img.convert('L')    

def img_rotate(url, img, degrees):
    return img.rotate(degrees)

def img_blur(url, img):
    return img.filter(ImageFilter.BLUR)

def img_detail(url, img):
    return img.filter(ImageFilter.DETAIL)

def img_contour(url, img):
    return img.filter(ImageFilter.CONTOUR)

def img_edge_enhance(url, img):
    return img.filter(ImageFilter.EDGE_ENHANCE)

def img_edge_enhance_more(url, img):
    return img.filter(ImageFilter.EDGE_ENHANCE_MORE)

def img_emboss(url, img):
    return img.filter(ImageFilter.EMBOSS)

def img_find_edges(url, img):
    return img.filter(ImageFilter.FIND_EDGES)

def img_smooth(url, img):
    return img.filter(ImageFilter.SMOOTH)

def img_smooth_more(url, img):
    return img.filter(ImageFilter.SMOOTH_MORE)

def img_sharpen(url, img):
    return img.filter(ImageFilter.SHARPEN)

def save_tmp(url, img2):
    headers = dict()
    #Extract extension
    ext = set_ext(url)
    #Guess mime type and encoding
    mimetype, encoding = mimetypes.guess_type(url)
    if mimetype: headers['Content-Type'] = mimetype
    if encoding: headers['Content-Encoding'] = encoding
    #Build response HEADER
    response_file = cStringIO.StringIO()    
    img2.save(response_file, ext)
    response_file.seek(0)
    return HTTPResponse(response_file, **headers)

def set_ext(url):
    path = urlparse.urlparse(url).path
    ext = os.path.splitext(path)[1].lower().replace('.', '')
    if ext == '' or ext == None:
        ext = 'png'
    if ext == 'jpg':
        ext = 'jpeg'
    return ext

    
run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000))) #This is needed to work on Heroku (extracted from bottle recipes http://bottlepy.org/docs/dev/recipes.html)
