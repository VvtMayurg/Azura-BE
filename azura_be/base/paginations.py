from rest_framework.pagination import PageNumberPagination


class DefaultPagination(PageNumberPagination):
    page_size = 15
    page_query_param = "page_no"
    page_size_query_param = "page_size"
    max_page_size = 500
