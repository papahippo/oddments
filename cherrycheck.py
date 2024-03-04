import cherrypy

class Root(object):
    @cherrypy.expose
    def default(self, **kwargs):
        print (kwargs)
        return '''<form action="" method="POST">
Host Availability:
<input type="checkbox" name="goal" value="cpu" / checked=0> CPU idle
<input type="checkbox" name="goal" value="lighttpd" /> Lighttpd Service
<input type="checkbox" name="goal" value="mysql" /> Mysql Service
<input type="submit">
</form>'''

cherrypy.quickstart(Root())
