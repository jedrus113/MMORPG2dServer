from tornado import ioloop, websocket, gen
from tornado import web


class MainHandler(web.RequestHandler):
    def get(self):
        self.write('<script>var ws = new WebSocket("ws://localhost:8000/websocket");'
                   'sendmessage = function() {'
                   'ws.send("Hello, world");'
                   '};'
                   'ws.onmessage = function (evt) {alert(evt.data);};</script>'
                   '<button onclick="sendmessage()">Bttn</button>')


class EchoWebSocket(websocket.WebSocketHandler):
    @gen.coroutine
    def open(self):
        print("WebSocket opened")
        self.write_message(u"Open!: ")
        yield gen.sleep(10)
        self.write_message(u"You said: 22 :)")


    def on_message(self, message):
        self.write_message(u"You said: " + message)

    def on_close(self):
        print("WebSocket closed")


def make_app():
    return web.Application([
        (r"/", MainHandler),
        (r"/websocket", EchoWebSocket),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8000)
    ioloop.IOLoop.current().start()
