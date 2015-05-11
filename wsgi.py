#!/usr/bin/env python
import os
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.paster import get_app

#app = config.make_wsgi_app()

app = get_app('pyramidapp/development.ini', 'main')

#
# Below for testing only
#
if __name__ == '__main__':
	from wsgiref.simple_server import make_server
	httpd = make_server('0.0.0.0', 3000, app)
	
	httpd.serve_forever()