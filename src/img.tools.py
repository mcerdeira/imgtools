# -*- coding: utf-8 -*-

__author__ = "mRt (martincerdeira@gmail.com)"
__version__ = "0.01"
__date__ = "$Date: 4/2/2012$"
__license__ = "GPL v3"

from bottle import run, route, error, request, response, get, post, request, debug, static_file, url, BaseResponse, HTTPResponse
from PIL import Image
import urllib, cStringIO
import uuid
import os.path
import ImageFilter
import mimetypes

_cache = dict()


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
    #Todo: use callbacks to concatenate image processing funcions
    for a in request.query.getall("action"):
        if "(" in a and ")" in a: # action with parameters
            a = a.replace("(", "|").replace(")", "|").split("|")
            if a[0] == "rotate":
                return img_rotate(url, img, float(a[1]))
        elif a == "black_white":
            return img_bw(url, img)
        elif a == "blur":
            return img_blur(url, img)
        elif a == "detail":
            return img_detail(url, img)
        elif a == "contour":
            return img_contour(url, img)
        elif a == "edge_enhance":
            return img_edge_enhance(url, img)
        elif a == "edge_enhance_more":
            return img_edge_enhance_more(url, img)
        elif a == "emboss":
            return img_emboss(url, img)
        elif a == "find_edges":
            return img_find_edges(url, img)
        elif a == "smooth":
            return img_smooth(url, img)
        elif a == "smooth_more":
            return img_smooth_more(url, img)
        elif a == "sharpen":
            return img_sharpen(url, img)

@error(404)
def error_hdl(error):
    return "<b>Ups, this is bad...</b>"

# IMAGE PROCESS FUNCTIONS

def img_bw(url, img):
    img2 = img.convert('L')
    return save_tmp(url, img2)

def img_rotate(url, img, degrees):
    img2 = img.rotate(degrees)
    return save_tmp(url, img2)

def img_blur(url, img):
    img2 = img.filter(ImageFilter.BLUR)
    return save_tmp(url, img2)

def img_detail(url, img):
    img2 = img.filter(ImageFilter.DETAIL)
    return save_tmp(url, img2)

def img_contour(url, img):
    img2 = img.filter(ImageFilter.CONTOUR)
    return save_tmp(url, img2)

def img_edge_enhance(url, img):
    img2 = img.filter(ImageFilter.EDGE_ENHANCE)
    return save_tmp(url, img2)

def img_edge_enhance_more(url, img):
    img2 = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return save_tmp(url, img2)

def img_emboss(url, img):
    img2 = img.filter(ImageFilter.EMBOSS)
    return save_tmp(url, img2)

def img_find_edges(url, img):
    img2 = img.filter(ImageFilter.FIND_EDGES)
    return save_tmp(url, img2)

def img_smooth(url, img):
    img2 = img.filter(ImageFilter.SMOOTH)
    return save_tmp(url, img2)

def img_smooth_more(url, img):
    img2 = img.filter(ImageFilter.SMOOTH_MORE)
    return save_tmp(url, img2)

def img_sharpen(url, img):
    img2 = img.filter(ImageFilter.SHARPEN)
    return save_tmp(url, img2)

def save_tmp(url, img2):
    headers = dict()
    mimetype, encoding = mimetypes.guess_type(url)
    if mimetype: headers['Content-Type'] = mimetype
    if encoding: headers['Content-Encoding'] = encoding
    response_file = cStringIO.StringIO()
    img2.save(response_file, 'png') # png for now, maybe take the extension from original file
    response_file.seek(0)
    return HTTPResponse(response_file, **headers)

def start_server():    
    debug(True)
    run(host='localhost', port=8000)

if __name__ == '__main__':
    start_server()
