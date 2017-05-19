# import json
# from django.http import JsonResponse
# from django.template.response import TemplateResponse
# from functools import wraps
#
#
# def ajax_login_required(view_func):
#     '''check user is authenticated before calling view - used for ajax calls'''
#     @wraps(view_func)
#     def wrap(request, *args, **kwargs):
#         if request.user.is_authenticated():
#             return view_func(request, *args, **kwargs)
#         return JsonResponse({'not_authenticated': True})
#     return wrap
#
#
# def ajax_logged_in(view_func):
#     '''call decorated function first - then check user is authenticated - used for ajax calls'''
#     @wraps(view_func)
#     def wrap(request, *args, **kwargs):
#         response = view_func(request, *args, **kwargs)
#         if isinstance(response, TemplateResponse):
#             response = response.render()
#
#         content = response.content
#         if isinstance(content, bytes):
#             content = content.decode('latin-1')
#
#         if not request.user.is_authenticated():
#             return JsonResponse({'not_authenticated': True, 'html': content})
#         return response
#     return wrap
