from flask import Flask,redirect
import pprint
app = Flask(__name__)
meme1="https://images.app.goo.gl/yNfV9D2SgC86eESG8"
@app.route("/")
def hello_world():
    return redirect("https://www.youtube.com/", code=302)
#"<p>Hi,\nI am Flaskiano,gonna unload you :D</p>"
class LoggingMiddleware(object):
    def __init__(self, app):
        self._app = app

    def __call__(self, env, resp):
        errorlog = env['wsgi.errors']
        pprint.pprint(('REQUEST', env), stream=errorlog)

        def log_response(status, headers, *args):
            pprint.pprint(('RESPONSE', status, headers), stream=errorlog)
            return resp(status, headers, *args)

        return self._app(env, log_response)
    
if __name__=='__main__':
    app.wsgi_app = LoggingMiddleware(app.wsgi_app)
    app.run()
