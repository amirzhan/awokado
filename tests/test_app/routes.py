import falcon

from awokado.documentation import (
    SwaggerResource,
    SwaggerUIResource,
    RedocViewResource,
)
from awokado.middleware import HttpMiddleware
from awokado.utils import api_exception_handler

try:
    from .resources import *
except ImportError:
    from resources import *


api = falcon.API(middleware=[HttpMiddleware()])

###############################################################################
# Add API routes here #########################################################
###############################################################################
api.add_route("/v1/author/", AuthorResource())
api.add_route("/v1/author/{resource_id}", AuthorResource())
api.add_route("/v1/book/", BookResource())
api.add_route("/v1/book/{resource_id}", BookResource())
api.add_route("/v1/forbidden_book/", ForbiddenBookResource())
api.add_route("/v1/forbidden_book/{resource_id}", ForbiddenBookResource())
api.add_route("/v1/store/", StoreResource())
api.add_route("/v1/store/{resource_id}", StoreResource())
api.add_route("/v1/store_stats/", StoreStatsResource())
api.add_route("/v1/store_stats/{resource_id}", StoreStatsResource())
api.add_route("/v1/tag/", TagResource())
api.add_route("/v1/tag/{resource_id}", TagResource())
api.add_route("/v1/tag_stats/", TagStatsResource())
api.add_route("/v1/tag_stats/{resource_id}", TagStatsResource())
api.add_route("/v1/healthcheck/", HealthCheckResource())

api.add_route(
    "/swagger.yaml",
    SwaggerResource(api=api, project_name="Example Documentation"),
)
api.add_route("/doc", SwaggerUIResource("/swagger.yaml"))
api.add_route("/redoc", RedocViewResource("/swagger.yaml"))

###############################################################################
###############################################################################
api.add_error_handler(Exception, api_exception_handler)

# In falcon 1.4.1 this param was True by default, but in 2.0.0 (current)
# they changed it to False, so now we need to manually set it to True
# to utilize coma-separated value parsing in querystring.
api.req_options.auto_parse_qs_csv = True
