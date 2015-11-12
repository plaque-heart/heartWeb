import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from bottle import route,default_app,run,static_file,response
from bottle import mako_template as template
from datetime import datetime
from siteSettings import Site

hellostr= """<h1>Hello {}</h1>"""

SQLBase = automap_base()

engine = sqlalchemy.create_engine(Site.engine, echo=True)
session=sessionmaker(bind=engine)()

SQLBase.prepare(engine, reflect=True)
People=SQLBase.classes.people
Resources =SQLBase.classes.resources
Resinfo = SQLBase.classes.resinfo

@route('/info-particles3.txt')
@route('/static/<path:path>')
def static(path='info-particles3.txt'):
    return static_file(path,root=Site.staticRoot)

@route('/people')
@route('/people/<who>')
def theTeam(who=None):
    people=session.query(People).order_by(People.name)
    if who:
        people=people.filter(People.group==who).all()
    else:
        people=people.all()
    return template('team.html',people=people)

@route('/Resources')
@route('/Resources/<what>')
def theRes(what='unity'):
    resources=session.query(Resources).order_by(Resources.sort)
    resinfo=session.query(Resinfo).filter(Resinfo.name==what).all()[0]
    resources=resources.all()
    return template('Resources.html',resources=resources,resinfo=resinfo)

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