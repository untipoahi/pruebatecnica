from pyramid.config import Configurator
from sqlalchemy import *
from sqlalchemy.engine.url import URL
from .models import DBSession, Base
import dbSettings

def main(global_config, **settings):
	engine = create_engine(URL(**dbSettings.DATABASE))
	DBSession.configure(bind=engine)
	Base.metadata.bind = engine
	config = Configurator(settings = settings)
	config.add_route('personsapi', 'api/persons')
	config.add_route('personsapione', 'api/persons/{id}')
	config.scan();
	return config.make_wsgi_app()