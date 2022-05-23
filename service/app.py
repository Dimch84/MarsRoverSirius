from flask import Flask, request
from hashlib import sha256
from json import dumps, loads
from sqlalchemy.orm import Session
from sqlalchemy import delete, select
from service.database import engine, Service


app = Flask(__name__)


@app.route('/services/', methods=['GET', 'POST'])
def process_services():
    """
    This page allows to get the list of all the fields or post a new field.

    :return:
    """
    session = Session(engine)
    if request.method == 'POST':
        service_data = loads(request.json)
        service_name = service_data['name']
        service_password = sha256(str.encode(
            service_data['password'])).hexdigest()
        service_url = service_data['url']
        new_service = Service(name=service_name,
                              password=service_password, url=service_url)
        service = session.execute(select(Service).
                                  where(Service.name == service_name)).scalar()
        if service and service.password != service_password:
            session.close()
            return dumps({'answer': 'Incorrect password'})
        session.execute(delete(Service).where(
            Service.name == new_service.name))
        session.add(new_service)
        session.flush()
        session.commit()
        session.close()
        return dumps({'answer': 'OK'})
    if request.method == 'GET':
        services = session.execute(select(Service)).all()
        services = list(map(lambda x: x[0], services))
        session.close()
        return dumps([{'name': service.name, 'url': service.url}
                      for service in services])


@app.route('/services/<service_name>', methods=['GET', 'DELETE'])
def get_service(service_name):
    """
    This page allows to get the url of the chosen service or delete it.

    :param service_name: service name.
    :return:
    """
    session = Session(engine)
    if request.method == 'DELETE':
        password = sha256(str.encode(
            loads(request.json)['password'])).hexdigest()
        service = session.execute(select(Service).
                                  where(Service.name == service_name)). \
            scalar()
        if service and service.password != password:
            session.close()
            return dumps({'answer': 'Incorrect password'})
        session.execute(delete(Service).where(Service.name == service_name))
        session.flush()
        session.commit()
        session.close()
        return dumps({'answer': 'OK'})
    if request.method == 'GET':
        service = session.execute(select(Service).
                                  where(Service.name == service_name)).scalar()
        session.close()
        if service is None:
            return dumps({'answer': 'Unknown service name'})
        return dumps({'name': service.name, 'url': service.url})
