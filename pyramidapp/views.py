from pyramid.view import view_config
import colander
from pyramid.httpexceptions import HTTPFound
from .models import (DBSession, Person)
from colander import(Email, Regex)
from pkg_resources import resource_filename
import sys
import json
from pyramid.response import Response
from sqlalchemy.orm.exc import NoResultFound

class PersonEntry(colander.MappingSchema):
	name = colander.SchemaNode(colander.String())
	lastname = colander.SchemaNode(colander.String())
	email = colander.SchemaNode(colander.String(),
								validator = colander.Email())
	phone = colander.SchemaNode(colander.String(),
								validator = colander.Regex('^\(\d{3}\) ?\d{3}( |-)?\d{4}|^\d{3}( |-)?\d{3}( |-)?\d{4}'))
	address = colander.SchemaNode(colander.String())

@view_config(route_name='home', renderer="templates/index.pt")
def index_view(request):
	return {"project": "Akhet Demo"}
	
class PersonViews(object):
	def __init__(self, request):
		self.request = request
	
	def convertTojson(self, elements):
		if type(elements) is list:
			try:
				return [e.__dict__ for e in elements if e.__dict__.pop('_sa_instance_state')]
			except:
				return [e.__dict__ for e in elements]
		else:
			result = elements.__dict__
			if '_sa_instance_state' in result:
				result.pop('_sa_instance_state')
			return result
			
	@view_config(route_name='personsapi', renderer='json', request_method='GET')
	def persons_view(self):
		try:
			persons = DBSession.query(Person).order_by(Person.lastname).all()
			return self.convertTojson(persons)
		except:
			return dict(message=sys.exc_info()[0])
		
	@view_config(route_name='personsapi', renderer='json', request_method='POST')
	def person_add(self):	
		try:
			person = PersonEntry().deserialize(self.request.json_body)
		except colander.Invalid as e:
			return self.error(e)
			
		person = Person(name = person['name'],
						lastname = person['lastname'],
						email = person['email'],
						phone = person['phone'],
						address = person['address'])
		DBSession.add(person)
		DBSession.flush()
		
		person = DBSession.query(Person).filter_by(email=person.email).one()
		return Response(status='200 Created',
						content_type='application/json; charset=UTF-8')
		
	@view_config(route_name='personsapione', renderer='json', request_method='GET')
	def person_view(self):
		id = int(self.request.matchdict['id'])
		try:
			person = DBSession.query(Person).filter_by(id=id).one()
			return self.convertTojson(person)
		except NoResultFound as e:
			return self.notfound()
	
	@view_config(route_name='personsapione', renderer='json', request_method='PUT')
	def persons_edit(self):
		id = int(self.request.matchdict['id'])
		try:
			modifiedPerson = PersonEntry().deserialize(self.request.json_body)
			person = DBSession.query(Person).filter_by(id=id).one()
			person.name = modifiedPerson['name']
			person.lastname = modifiedPerson['lastname']
			person.email = modifiedPerson['email']
			person.phone = modifiedPerson['phone']
			person.address = modifiedPerson['address']
			DBSession.flush()
		except NoResultFound as e:
			return self.notfound()
		except colander.Invalid as e:
			return self.error(e)
		return Response(status='200 Element Modified',
						content_type='application/json; charset=UTF-8')
	
	@view_config(route_name='personsapione', renderer='json', request_method='DELETE')
	def persons_delete(self):
		id = int(self.request.matchdict['id'])
		try:
			person = DBSession.query(Person).filter_by(id=id).delete()
			DBSession.flush()
		except NoResultFound as e:
			return self.notfound()
		return Response(status='200 Element Deleted',
						content_type='application/json; charset=UTF-8')
	
	def error(self, e):
		print('prueba')
		messages = e.asdict()
		print(messages)
		return Response(body=json.dumps(messages), status='500 - Server Error', content_type='application/json')
	
	def notfound(self):
		return Response(body=json.dumps({'message': '404 - Element Not Found'}),
		status='404 Not Found',
		content_type='application/json')