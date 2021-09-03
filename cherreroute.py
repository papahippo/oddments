#!/usr/bin/python3
import cherrypy
from cherrypy.process.plugins import DropPrivileges
import sys, os, subprocess, shutil, tempfile

class ReRouter:

    """ Sample request handler class. """

    # Expose the index method through the web. CherryPy will never
    # publish methods that don't have the exposed attribute set to True.
    @cherrypy.expose
    def default(self, *pp, **kw):
        # CherryPy will call this method for the root URI ("/") and send
        # its return value to the client. Because this is tutorial
        # lesson number 01, we'll just send something really simple.
        # How about...
        url = cherrypy.url()
        qs = cherrypy.request.query_string
        new_url = url.replace('http://', 'https://') + (f"?{qs}" if qs else "")
        yield f"rerouting to {new_url}"
        raise cherrypy.HTTPRedirect(new_url)

def main():
    print(f"running'main' in {__file__}")
    # need local ip address;
    # this approach works for my dev system and real garage but is not generically robust:
    #
    local_ip_address = subprocess.check_output(['hostname', '-s', '-I']).decode('utf-8').split(' ')[0]
    server_prog_name = sys.argv.pop(0) if sys.argv else '[unknown]'
    global_config = {
        'server.socket_host': local_ip_address,
        'server.socket_port': 80,
        'server.thread_pool': 10,
    }

    print(f"{server_prog_name} will start  server",
          file=sys.stderr)
    cherrypy.config.update(global_config)
    cherrypy.tree.mount(ReRouter(), '/')
    cherrypy.engine.start()
    cherrypy.engine.block()
if __name__ == '__main__':
    main()
