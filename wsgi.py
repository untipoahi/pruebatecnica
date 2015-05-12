#!/usr/bin/env python
import os
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.paster import get_app

#app = config.make_wsgi_app()
path = '/'.join(os.path.abspath(__file__).split('/')[0:-1])
application = get_app(path + '/development.ini', 'main')

#
# Below for testing only
#
if __name__ == '__main__':
	from wsgiref.simple_server import make_server
	httpd = make_server('0.0.0.0', 6543, application)
	
	httpd.serve_forever()