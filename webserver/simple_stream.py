from flask import Flask, Response, render_template, send_from_directory
from gevent.wsgi import WSGIServer
from gevent.queue import Queue

from stream.server_sent_event import ServerSentEvent

app             = Flask('simple streamer', static_url_path='/static')
subscriptions   = []

@app.route('/debug')
def debug():
    return 'Currently %i subscriptions' % len(subscriptions)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/subscribe')
def subscribe():
    def gen():
        q = Queue()
        subscriptions.append(q)

        try:
            while True:
                result = q.get()
                print(result)
        except GeneratorExit:
            subscriptions.remove(q)
    
    return Response(gen(), mimetype='text/event-stream')

def run():
    app.debug = True
    server = WSGIServer(('', 5000), app)
    server.serve_forever()
