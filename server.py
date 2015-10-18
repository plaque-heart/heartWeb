from bottle import route,default_app,run,static_file
from bottle import mako_template as template
from datetime import datetime
from siteSettings import Site

hellostr= """<h1>Hello {}</h1>"""


@route('/static/<path:path>')
def static(path):
    return static_file(path,root=Site.staticRoot)

@route('/hello/')
def hellohide():
    return hello('anon')
@route("/hello/<name>")
#@route("/hello")
def hello(name='nobody'):
    return hellostr.format(name.capitalize())

@route('/')
@route('/<path:path>')
def nothing(path='index.html'):
    now=datetime.now().strftime('%A %d-%b-%Y %H:%M:%S')
    return template(path,time=now)

application = default_app()

if __name__ == '__main__':
    print("Hello")
    run(port=8000,host="0.0.0.0",debug=True)