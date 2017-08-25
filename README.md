django-jquery-file-uploader is a backend app for 
[jQuery-File-Upload](http://blueimp.github.io/jQuery-File-Upload/) (developed by Sebastian Tschan, with the source available on [github](https://github.com/blueimp/jQuery-File-Upload)). This code is greately based on [django-multiple-file-chunked-upload](https://github.com/tcztzy/django-multiple-file-chunked-upload) by Tang Ziya ([tcztzy on github](https://github.com/tcztzy)). I added my modifications in order to fullfill specification of jQuery-File-Upload.

This backend allows to upload and delete files. The admin panel allows to set

* maximal upload size
* maximal chunk size
* enable/disable upload
* accepted file types (via regexp)

In the future also selection of different UIs (basic, Basic Plus, Basic Plus UI) will be allowed.

Several profiles are available (diferent model entries) and always the first one enabled is takem into consideration. If no entry is enabled, the upload is disabled.

Introduction
============

This is a small example on how to setup Sebastian Tschan's jQuery File Upload in Django. He has a working demo on his [webpage](http://aquantum-demo.appspot.com/file-upload) and a [github repository](https://github.com/blueimp/jQuery-File-Upload) with an example on how to do it in PHP.

Here, you'll find a Django project with a standard (Basic Plus UI) app. You can run the example standalone by cloning the repository, running the migrations and starting the server.

Features
========

* Drag and drop files
* Select multiple files
* Cancel upload
* Delete uploaded file (from database only)
* No flash (or other browser plugins) needed
* … more at the [upstream's features page](http://aquantum-demo.appspot.com/file-upload#features)

Requirements
============

* Django

Testing
=======

* pip install -r requirements.txt (will install django)
* python manage.py migrate
* python manage.py runserver
* go to localhost:8000/ and upload some files

Installation
============

Recommended with virtualenv

* pip install .

License
=======
MIT, as the original project. See LICENSE.txt.