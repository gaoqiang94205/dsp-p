from data.app import upload_routes
from dsp.apptemplate.app import apptemplate_routes
from dsp.bigdata.api import bigdata_routes
from dsp.container.app import container_routes
from dsp.apps.app import application_routes
from dsp.image.app import image_routes
from dsp.network.app import network_routes
from dsp.node.wapp import node_routes


def load_moudle(app):
    container_routes(app)
    application_routes(app)
    image_routes(app)
    apptemplate_routes(app)
    upload_routes(app)
    bigdata_routes(app)
    network_routes(app)
    node_routes(app)