from flask import Flask, request
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
        service_url = service_data['url']
        service = Service(name=service_name, url=service_url)
        session.execute(delete(Service).where(Service.name == service.name))
        session.add(service)
        session.flush()
        session.commit()
        session.close()
        return 'OK'
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
        print(service_name)
        session.execute(delete(Service).where(Service.name == service_name))
        session.flush()
        session.commit()
        session.close()
        return 'OK'
    if request.method == 'GET':
        service = session.execute(select(Service).
                                  where(Service.name == service_name)).scalar()
        session.close()
        if service is None:
            return 'Unknown service name'
        return dumps({'name': service.name, 'url': service.url})
