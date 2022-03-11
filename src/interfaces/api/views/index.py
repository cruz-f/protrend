from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer

from router import BaseIndexView


class IndexView(BaseIndexView):
    """
    ProTReND database REST API. ProTReND provides open programmatic access to the Transcriptional Regulatory Network (TRN) database through a RESTful web API.

    ProTReND's REST API allows users to retrieve structured regulatory data. In addition, the web interface provides a simple yet powerful resource to visualize ProTReND.
    All data can be visualized by navigating through the several biological entities available at the API Index.

    IMPORTANT:
     - ANONYMOUS USERS PERFORMING MORE THAN 3 REQUESTS PER SECOND WILL BE BANNED!
     - REGISTERED USERS PERFORMING MORE THAN 5 REQUESTS PER SECOND WILL BE BANNED!
    Please follow the best practices mentioned in the documentation.

    The web API navigation provides detailed visualizations for each biological entity contained in the database.
    """
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer)