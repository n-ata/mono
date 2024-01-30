import json
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination,
)
from rest_framework import serializers

DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 10


class CustomPagination(PageNumberPagination):
    # page = DEFAULT_PAGE
    page_size = DEFAULT_PAGE_SIZE
    page_size_query_param = 'page_size'
    page_query_param = 'page'

    def get_paginated_response(self, data):
        return Response({
            'next': self.page.next_page_number() if self.page.has_next() else None,
            'previous': self.page.previous_page_number() if self.page.has_previous() else None,
            'recordsTotal': self.page.paginator.count,
            # can not set default = self.page
            'page': int(self.request.GET.get('page', DEFAULT_PAGE)),
            'page_size': int(self.request.GET.get('page_size', self.page_size)),
            'data': data
        })


class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 20
    limit_query_param = 'length'
    offset_query_param = 'start'
    max_limit = 1000
    min_limit = 1
    min_offset = 0
    max_offset = 1000000

    def get_paginated_response(self, data):
        return Response({
            'recordsTotal': self.count,
            'recordsFiltered': self.count,
            'next': self.get_next_link(),
            'start': int(self.request.GET.get('start', self.offset_query_param)),
            'length': int(self.request.GET.get('length', self.limit_query_param)),
            'previous': self.get_previous_link(),
            'data': data
        })

class ItemPageNumberPagination(PageNumberPagination):
    page_size = 10
