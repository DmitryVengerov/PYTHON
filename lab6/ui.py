from bottle import route, run, template

@route('/')
@route('/hello/<name>')
def index(name="Stranger"):
    return template('hello_template.tpl', name=name)
run(host='localhost', port=8080)