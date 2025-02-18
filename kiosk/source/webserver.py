



import tornado.web
import tornado.ioloop
import threading
import elcsoft.controller.websocket
import wikismartdoor as wikismartdoor

clients = []

if __name__ == "__main__":
    obj = wikismartdoor.WikiSmartdoor()
    th = threading.Thread(target=obj.run, daemon=True).start()

    handlers = [
        (r'/ws', elcsoft.controller.websocket.WebsocketHandler, { 'wikismartdoor': obj, 'clients': clients })
    ]

    settings = {
        "cookie_secret": "elcsoft"
    }

    app = tornado.web.Application(handlers, **settings)
    app.listen(8080)

    mainLoop = tornado.ioloop.IOLoop.instance()

    try:
        mainLoop.start()  # mainLoop를 사용하여 서버 시작
        print("Webserver Started!")
    except KeyboardInterrupt:
        mainLoop.stop()  # mainLoop를 사용하여 서버 중지
        print("Webserver Stopped!")










