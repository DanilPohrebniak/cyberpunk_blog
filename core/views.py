from django.shortcuts import render


def handler_403(request, exception):
    context = {
        'title': 'Forbidden 403',
        'messages': str(exception)
    }
    return render(request,
                  'base/error.html',
                  context=context,
                  status=403)

    