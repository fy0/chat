import tornado.ioloop
import tornado.web

from settings import application

if __name__ == "__main__":
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()

