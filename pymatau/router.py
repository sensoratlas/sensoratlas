from __future__ import unicode_literals
from rest_framework.routers import Route, DynamicRoute, DefaultRouter, \
    APIRootView
import re
from django.urls import NoReverseMatch
from rest_framework.response import Response
from rest_framework.reverse import reverse
from collections import OrderedDict


# override NestedMixin from
# https://github.com/alanjds/drf-nested-routers/blob/master/rest_framework_nested/routers.py
IDENTIFIER_REGEX = re.compile(r"^[^\d\W]\w*$", re.UNICODE)


class NestedMixin:
    def __init__(self, parent_router, parent_prefix, *args, **kwargs):
        self.parent_router = parent_router
        self.parent_prefix = parent_prefix
        self.nest_count = getattr(parent_router, 'nest_count', 0) + 1
        self.nest_prefix = kwargs.pop('lookup', self.parent_prefix) + '_'

        super(NestedMixin, self).__init__(*args, **kwargs)
        if 'trailing_slash' not in kwargs:
            self.trailing_slash = parent_router.trailing_slash

        parent_registry = [registered for registered
                           in self.parent_router.registry
                           if registered[0] == self.parent_prefix]
        try:
            parent_registry = parent_registry[0]
            parent_prefix, parent_viewset, parent_basename = parent_registry
        except RuntimeError:
            raise RuntimeError('parent registered resource not found')

        self.check_valid_name(self.nest_prefix)

        nested_routes = []
        parent_lookup_regex = parent_router.get_lookup_regex(parent_viewset,
                                                             self.nest_prefix)

        self.parent_regex = '{parent_prefix}\({parent_lookup_regex}\)/'.format(
            parent_prefix=parent_prefix,
            parent_lookup_regex=parent_lookup_regex
        )

        if not self.parent_prefix and self.parent_regex[0] == '/':
            self.parent_regex = self.parent_regex[1:]
        if hasattr(parent_router, 'parent_regex'):
            self.parent_regex = parent_router.parent_regex + self.parent_regex

        for route in self.routes:
            route_contents = route._asdict()
            escaped_parent_regex = self.parent_regex.replace(
                '{', '{{').replace('}', '}}')
            route_contents['url'] = route.url.replace(
                '^', '^' + escaped_parent_regex)
            nested_routes.append(type(route)(**route_contents))

        self.routes = nested_routes

    def check_valid_name(self, value):
        if IDENTIFIER_REGEX.match(value) is None:
            raise ValueError("lookup argument '{}' needs to be valid python \
                identifier".format(value))


class SensorThingsAPI(APIRootView):
    """
    Welcome to the Sensor Things API implementation for Sensor Atlas.
    """
    def get(self, request, *args, **kwargs):
        namespace = request.resolver_match.namespace
        ret_list = []
        for key, url_name in self.api_root_dict.items():
            ret = OrderedDict()
            if namespace:
                url_name = namespace + ':' + url_name
            try:
                ret["name"] = key
                ret["url"] = reverse(
                    url_name,
                    args=args,
                    kwargs=kwargs,
                    request=request,
                    format=kwargs.get('format', None)
                )
                ret_list.append(ret)
            except NoReverseMatch:
                continue
        res = {
            'value': ret_list
        }

        return Response(res)


class SensorThingsRouter(DefaultRouter):
    """A router that has the lookup field in parentheses."""
    APIRootView = SensorThingsAPI
    routes = [
        Route(
            url=r'^{prefix}$',
            mapping={
                'get': 'list',
                'post': 'create'
            },
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        DynamicRoute(
            url=r'^{prefix}/{url_path}$',
            name='{basename}-{url_name}',
            detail=False,
            initkwargs={}
        ),
        Route(
            url=r'^{prefix}\({lookup}\)$',
            mapping={
                'get': 'retrieve',
                'put': 'update',
                'patch': 'partial_update',
                'delete': 'destroy'
            },
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Instance'}
        ),
        DynamicRoute(
            url=r'^{prefix}\({lookup}\)/{url_path}$',
            name='{basename}-{url_name}',
            detail=True,
            initkwargs={}
        ),
    ]


class NestedSimpleRouter(NestedMixin, SensorThingsRouter):
    """ Create a NestedSimpleRouter nested within `parent_router`
    Args:
    parent_router: Parent router. Maybe be a SimpleRouter or another nested
        router.
    parent_prefix: The url prefix within parent_router under which the
        routes from this router should be nested.
    lookup:
        The regex variable that matches an instance of the parent-resource
        will be called '<lookup>_<parent-viewset.lookup_field>'
        In the example above, lookup=domain and the parent viewset looks up
        on 'pk' so the parent lookup regex will be 'domain_pk'.
        Default: 'nested_<n>' where <n> is 1+parent_router.nest_count
    """
    pass


class Router:
    router = SensorThingsRouter()
