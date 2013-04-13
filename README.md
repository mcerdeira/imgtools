Glitch
========

Glitch is an image transformation service.

Its uses PIL for image processing, and bottle for webservice dispatching.

It works by calling the service url, with the image url as a parameter.


Status
========

There is an alpha version deployed on Heroku at http://powerful-savannah-5198.herokuapp.com/

You can use it, sending parameters to it.


Example
========

http://powerful-savannah-5198.herokuapp.com/http://imalbum.aufeminin.com/album/D20110627/778673_DCB4Q8R8X81U7BKJRAYFUZ6YZEONLX_leonardodavinci_H020536_S.jpg?action=black_white


Current supported commands
==========================

black_white:         Example: action=black_white

blur                 Example: action=blur           

detail               Example: action=detail

contour              Example: action=contour

edge_enhance         Example: action=edge_enhance

edge_enhance_more    Example: action=edge_enhance_more

emboss               Example: action=emboss

find_edges           Example: action=find_edges

rotate(degrees)      Example: action=rotate(45)

smooth               Example: action=smooth

smooth_more          Example: action=smooth_more

sharpen              Example: action=sharpen

shred                Example: action=shred

addborder            Example: action=addborder

light                Example: action=light

getred               Example: action=getred

getgreen             Example: action=getgreen

getblue              Example: action=getblue

invertrgb            Example: action=invertrgb

sepia				 Example: action=sepia


Also, you can combine more than one filter, like this:

http://powerful-savannah-5198.herokuapp.com/http://imalbum.aufeminin.com/album/D20110627/778673_DCB4Q8R8X81U7BKJRAYFUZ6YZEONLX_leonardodavinci_H020536_S.jpg?action=black_white&action=blur
