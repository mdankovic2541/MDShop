def isAjax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'