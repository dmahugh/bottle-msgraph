"""Launch the minroutes web app using a development server."""
import os
import bottle

import minroutes

if __name__ == "__main__":

    @bottle.route("/static/<filepath:path>")
    def server_static(filepath):
        """Handler for static files, used with the development server."""
        PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
        STATIC_ROOT = os.path.join(PROJECT_ROOT, "static").replace("\\", "/")
        return bottle.static_file(filepath, root=STATIC_ROOT)

    bottle.run(app=bottle.app(), server="wsgiref", host="localhost", port=5000)
