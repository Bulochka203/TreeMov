from django.http import HttpResponse


# class ViewException:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         return self.get_response(request)
#
#     def process_exception(self, request, exception):
#         print(self)
#         print(request)
#         print(exception)
#         return HttpResponse(f'<h1>Исключение:</h1>\n<p>{exception}</p>')
