# -*- coding: utf-8 -*-

__author__ = "mRt (martincerdeira@gmail.com)"
__version__ = "0.03"
__date__ = "$Date: 4/2/2012$"
__license__ = "GPL v3"

from bottle import run, route, error, request, response, get, post, request, template, debug, static_file, url, HTTPResponse
from PIL import Image
from PIL import ImageOps
from random import shuffle
import urllib, cStringIO
import uuid
import urlparse, os
import ImageFilter
import mimetypes

_cache = dict() # This is a toy cache handler, replace it with better stuff

@route('/')
def default():
    return template('main', result = '', original = '', actions = sorted(_actions.keys()))
    
@route('/css/:filename')
def css_file(filename):
    return static_file(filename, root=os.getcwd() + '/css/')
    
@route('/img/:filename')
def img_file(filename):
    return static_file(filename, root=os.getcwd() + '/img/')
    
@post('/submited/')
def submited():     
    action = action_string(request.forms)
    url = request.forms.get('url')
    web = request.url.replace('/submited', '')  
    result = web + url + action
    return template('main', result = result, original = url, actions = sorted(_actions.keys()))
        

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
        elif a == "shred":
            img = img_shred(url, img)
        elif a == "addborder":
            img = img_addborder(url, img)
        elif a == 'light':
            img = img_light(url, img)
        elif a == 'getred':
            img = img_getred(url, img)
        elif a == 'getgreen':
            img = img_getgreen(url, img)
        elif a == 'getblue':
            img = img_getblue(url, img)
        elif a == 'invertrgb':
            img = img_invertrgb(url, img)
            
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
    
def img_shred(url, img):    
    SHREDS = 10 
    shredded = Image.new("RGBA", img.size)
    width, height = img.size
    shred_width = width/SHREDS
    sequence = range(0, SHREDS)
    shuffle(sequence)

    for i, shred_index in enumerate(sequence):
        shred_x1, shred_y1 = shred_width * shred_index, 0
        shred_x2, shred_y2 = shred_x1 + shred_width, height
        region =img.crop((shred_x1, shred_y1, shred_x2, shred_y2))
        shredded.paste(region, (shred_width * i, 0))

    return shredded
    
def img_addborder(url, img):
    #TODO, replace hardcoded fill and border for parameters
    r = ImageOps.expand(img, border=5, fill='red')
    return r
    
def img_light(url, img):
    tilesize=50
    WIDTH, HEIGHT = img.size
    for x in xrange(0, WIDTH, tilesize):
        for y in xrange(0, HEIGHT, tilesize):
            br = int(255 * (1 - x / float(WIDTH) * y /float(HEIGHT)))
            tile = Image.new("RGBA", (tilesize, tilesize), (255,255,255,128))
            img.paste((br,br,br), (x, y, x + tilesize, y + tilesize), mask=tile)
    
    return img
    
def img_getred(url, img):    
    rimg = img.convert("RGB")
    r,g,b = img.split()
    return Image.merge('RGB',(r,r,r))    

def img_getgreen(url, img):
    rimg = img.convert("RGB")
    r,g,b = img.split()
    return Image.merge('RGB',(g,g,g))    
    
def img_getblue(url, img):
    rimg = img.convert("RGB")
    r,g,b = rimg.split()
    return Image.merge('RGB',(b,b,b))    
    
def img_invertrgb(url, img):    
    rimg = img.convert("RGB")
    r,g,b = rimg.split()
    return Image.merge('RGB',(b,g,r))     

def img_write(url, img):
    pass
    # def draw_text(text, size, angle=0, fill=None):
    # font = ImageFont.truetype(
        # 'path/to/font.ttf', size
    # )
    # size = font.getsize(text) # Returns the width and height of the given text, as a 2-tuple.
    # im = Image.new('RGBA', size, (0, 0, 0, 0)) # Create a blank image with the given size
    # draw = ImageDraw.Draw(im)
    # draw.text((0, 0), text, font=font, fill=fill) #Draw text
    # return im.rotate(angle, expand=True)
 
# img = draw_text('Google', 30, 45, (82, 124, 178)) 
    
    # http://stackoverflow.com/questions/7698231/python-pil-draw-multiline-text-on-image 
    

def save_tmp(url, img2):
    headers = dict()
    #Extract extension
    ext = set_ext(url)
    #Guess mime type and encoding
    mimetype, encoding = mimetypes.guess_type(url)
    if mimetype: headers['Content-Type'] = mimetype
    if encoding: headers['Content-Encoding'] = encoding
    headers['Cache-control'] = 'public; max-age=28800'
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
    'sharpen' : img_sharpen,
    'write' : img_write,
    'shred' : img_shred,
    'addborder': img_addborder,
    'light' : img_light,
    'getred' : img_getred,
    'getgreen' : img_getgreen,
    'getblue' : img_getblue,
    'invertrgb' : img_invertrgb
}


    
run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000))) #This is needed to work on Heroku (extracted from bottle recipes http://bottlepy.org/docs/dev/recipes.html)
