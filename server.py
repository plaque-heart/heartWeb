import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from bottle import route,default_app,run,static_file,response
from bottle import mako_template as template
from datetime import datetime
from siteSettings import Site

hellostr= """<h1>Hello {}</h1>"""

SQLBase = automap_base()

engine = sqlalchemy.create_engine("sqlite:///dbase.db", echo=True)
session=sessionmaker(bind=engine)()

SQLBase.prepare(engine, reflect=True)
People=SQLBase.classes.people

@route('/static/<path:path>')
def static(path):
    return static_file(path,root=Site.staticRoot)

@route('/people')
@route('/people/<who>')
def theTeam(who=None):
    if who:
        people=session.query(People).filter(People.group==who).all()
    else:
        people=session.query(People).all()
    return template('team.html',people=people)

@route('/image/people/<name>')
def picture(name):
    rows=session.query(People).filter(People.name==name)
    if rows:
        response.set_header('content_type', 'image/jpeg')
        return rows[0].picture
    else:
        raise bottle.HTTPError(500,'No picture')
    

@route('/hello/')
def hellohide():
    return hello('anon')
@route("/hello/<name>")
#@route("/hello")
def hello(name='nobody'):
    return hellostr.format(name.capitalize())

@route('/')
@route('/<path:path>')
def nothing(path='index'):
    now=datetime.now().strftime('%A %d-%b-%Y %H:%M:%S')
    if path.endswith('.html'):
        pass
    else:
        path+='.html'
        
    return template(path,time=now)

application = default_app()

if __name__ == '__main__':
    print("Hello")
    run(port=8000,host="0.0.0.0",debug=True)