from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_query_param = 'page'
    page_size = 10

    def get_paginated_response(self, data):
        return Response({
            'code': 2000,
            'data': data,
            'message': 'success',
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link()
        })
