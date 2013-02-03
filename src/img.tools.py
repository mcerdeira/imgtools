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
    img2 = img.convert('L')
    return img2
    #return save_tmp(url, img2)

def img_rotate(url, img, degrees):
    img2 = img.rotate(degrees)
    return img2
    #return save_tmp(url, img2)

def img_blur(url, img):
    img2 = img.filter(ImageFilter.BLUR)
    return img2
    #return save_tmp(url, img2)

def img_detail(url, img):
    img2 = img.filter(ImageFilter.DETAIL)
    return img2
    #return save_tmp(url, img2)

def img_contour(url, img):
    img2 = img.filter(ImageFilter.CONTOUR)
    return img2
    #return save_tmp(url, img2)

def img_edge_enhance(url, img):
    img2 = img.filter(ImageFilter.EDGE_ENHANCE)
    return img2
    #return save_tmp(url, img2)

def img_edge_enhance_more(url, img):
    img2 = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return img2
    #return save_tmp(url, img2)

def img_emboss(url, img):
    img2 = img.filter(ImageFilter.EMBOSS)
    return img2
    #return save_tmp(url, img2)

def img_find_edges(url, img):
    img2 = img.filter(ImageFilter.FIND_EDGES)
    return img2
    #return save_tmp(url, img2)

def img_smooth(url, img):
    img2 = img.filter(ImageFilter.SMOOTH)
    return img2
    #return save_tmp(url, img2)

def img_smooth_more(url, img):
    img2 = img.filter(ImageFilter.SMOOTH_MORE)
    return img2
    #return save_tmp(url, img2)

def img_sharpen(url, img):
    img2 = img.filter(ImageFilter.SHARPEN)
    return img2
    #return save_tmp(url, img2)

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
    
def start_server():    
    debug(True)
    run(host='localhost', port=8000)

if __name__ == '__main__':
    start_server()
