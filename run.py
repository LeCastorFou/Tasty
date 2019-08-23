from tasty import create_app
import socket
from tasty.controller import  pwa

app = create_app()

app.register_blueprint(pwa.bp)
# Pour ne pas passer par les variables d'environement

app.jinja_env.cache = {}


if socket.gethostname() in ['CFT-AZURE-LX004','CFT-AZURE-LX005']:
    if __name__ == '__main__':
        app.run(debug=True,host= '0.0.0.0', port = 5000)
else:
    if __name__ == '__main__':
        app.run(debug=True, port = 5000)
