from django.contrib.auth.decorators import login_required


@login_required
def details(request, **kwargs):
    from time_spent.views import detail
    return detail(request, **kwargs)
