from interfaces.api.views import IndexView
from router import Router


class APIRouter(Router):
    """
    Custom API Router
    """
    index_class = IndexView
