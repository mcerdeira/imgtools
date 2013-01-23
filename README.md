imgtools
========

Image tools (still working on a better name) is an image transformation service.

Its uses PIL for image processing, and bottle for webservice dispatching.

It works by calling the service url, with the image url as a parameter.

Example
========

Service Url: http://localhost:8000

Image Url: http://imalbum.aufeminin.com/album/test.jpg

Transformation: Black And White

You call it, this way:

http://localhost:8000/http://imalbum.aufeminin.com/album/test.jpg?action=black_white


Status
========

Proof of concept
