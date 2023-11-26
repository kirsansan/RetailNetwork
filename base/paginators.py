from rest_framework.pagination import PageNumberPagination

from config.config import MAX_NODE_PER_PAGE


class AllListsPaginator(PageNumberPagination):
    page_size = MAX_NODE_PER_PAGE
