import cherrypy
import sys

print("python version:", sys.version)
print("cherrpy version:", cherrypy.__version__)

class RootServer:
    @cherrypy.expose
    def index(self, **keywords):
        return "it works!"

if __name__ == '__main__':
    server_config={
        'server.socket_host': '192.168.2.39',  # 127.0.0.1',
        'server.socket_port': 4400,
        'server.ssl_module': 'builtin',
        #'server.ssl_module':'pyopenssl',
        'server.ssl_certificate':'/etc/letsencrypt/live/larry.myerscough.nl/fullchain.pem',
        'server.ssl_private_key':'/etc/letsencrypt/live/larry.myerscough.nl/privkey.pem',
                                 'tools.sessions.locking': 'early',
        'server.thread_pool': 10,
    }

    cherrypy.config.update(server_config)
    cherrypy.quickstart(RootServer())
   # cherrypy.engine.start()
   #  cherrypy.engine.block()
