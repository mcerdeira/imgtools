# -*- coding: utf-8 -*-

__author__ = "mRt (martincerdeira@gmail.com)"
__version__ = "0.03"
__date__ = "$Date: 4/2/2012$"
__license__ = "GPL v3"

from bottle import run, route, error, request, response, get, post, request, template, debug, static_file, url, HTTPResponse
from PIL import Image
import urllib, cStringIO
import uuid
import urlparse, os
import ImageFilter
import mimetypes

_cache = dict() # This is a toy cache handler, replace it with better stuff

@route('/')
def default():
    return template('main', result = '', original = '', actions = _actions.keys())
    
    
@post('/submited/')
def submited():     
    action = action_string(request.forms)
    url = request.forms.get('url')
    web = request.url.replace('/submited', '')  
    result = web + url + action
    return template('main', result = result, original = url, actions = _actions.keys())
        

@route('<img_url:path>')
def main(img_url):
    url = img_url[1:]
    action = request.query.getall("action")
    return handle_request(url, action)
    

@error(404)
def error_hdl(error):
    return "<b>Ups, this is bad...</b>"
    

def action_string(web_actions):
    retval = ""
    print web_actions
    for i in _actions.keys():
        if web_actions.get(i) != None:
            if retval != "":
                retval += "&action=" + i
            else:
                retval += "?action=" + i
            
    return retval
    
def handle_request(url, action):    
    try:
        file = cStringIO.StringIO(_cache[url])
    except KeyError:
        _cache[url] = urllib.urlopen(url).read()
        file = cStringIO.StringIO(_cache[url])
                
    img = Image.open(file)    
    return img_process(action, url, img)    

# IMAGE PROCESS FUNCTIONS

def img_process(actions, url, img):
    # Process all the requested transformations
    #TODO: use _actions instead...  
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
    
    
_actions = {
    'rotate' : img_rotate,
    'black_white' : img_bw,
    'blur' : img_blur,
    'detail' : img_detail,
    'contour' : img_contour,
    'edge_enhance' : img_edge_enhance,
    'edge_enhance_more' : img_edge_enhance_more,
    'emboss' : img_emboss,
    'find_edges' : img_find_edges,
    'smooth' : img_smooth,
    'smooth_more' : img_smooth_more,
    'sharpen' : img_sharpen
}
    
run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000))) #This is needed to work on Heroku (extracted from bottle recipes http://bottlepy.org/docs/dev/recipes.html)
