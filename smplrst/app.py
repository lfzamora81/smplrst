import falcon

from .cat import CatEndpoint
from .history import HistoryEndpoint

api = application = falcon.API()

cat = CatEndpoint()
history = HistoryEndpoint()

api.add_route('/cat', cat)
api.add_route('/history', history)
