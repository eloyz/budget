from lazysignup.decorators import allow_lazy_user


@allow_lazy_user
def details(request, **kwargs):
    from time_spent.views import detail
    return detail(request, **kwargs)
