import tornado.ioloop
import tornado.web
import tornado.websocket
import random
import json

current_chats = []
chat_dict = {}


class Chats:

    def __init__(self):
        self.chats = 0
        self.chat_dict = {}
        self.current_connections = set()

    @staticmethod
    def create_hash():
        return ''.join(str(random.randint(0, 9)) for _ in range(5))

ChatsInstance = Chats()

class MainHandler(tornado.web.RequestHandler):

    def data_received(self, chunk):
        pass

    def get(self):
        self.render(r'templates/index.html')


class ChatSocket(tornado.websocket.WebSocketHandler):

    def __init__(self, application, request):
        super().__init__(application, request)
        self.hash = None

    def data_received(self, chunk):
        pass

    def open(self):
        self.hash = ChatsInstance.create_hash()
        ChatsInstance.current_connections.add(self.hash)
        ChatsInstance.chat_dict[self.hash] = self
        print('user:', self.hash, 'joined')

    def on_message(self, message):
        print("we got a message", message)
        # todo we want to change the behavior based on who sent the chat
        for key in ChatsInstance.current_connections:
            ChatsInstance.chat_dict[key].write_message(message)

    def on_close(self):
        print("WebSocket closed")


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/chat", ChatSocket)
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("running on port 8888")
    tornado.ioloop.IOLoop.current().start()
