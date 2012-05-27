from django.contrib.auth.decorators import login_required

# create method that returns context
# put context together with template
# return result

# home page could return multiple interfaces
# introduction version
# desktop version
# mobile version


@login_required
def detail(request, month=0, year=0):
    """
    We're building the response and then sending it via this view.
    Rather than going the more traditional route, we're opting for
    returning variable responses depending on device.
    """
    from django.template import RequestContext
    from django.shortcuts import render_to_response
    from time_spent.utils import desktop_context

    return render_to_response(
        'details.html',
        desktop_context(request=request, month=month, year=year),
        context_instance=RequestContext(request)
    )


@login_required
def income(request, month=0, year=0):
    """
    We're building the response and then sending it via this view.
    Rather than going the more traditional route, we're opting for
    returning variable responses depending on device.
    """
    from django.template import RequestContext
    from django.shortcuts import render_to_response
    from time_spent.utils import desktop_context

    return render_to_response(
        'details.html',
        desktop_context(request=request, month=month, year=year),
        context_instance=RequestContext(request)
    )


@login_required
def expenses(request, month=0, year=0):
    """
    We're building the response and then sending it via this view.
    Rather than going the more traditional route, we're opting for
    returning variable responses depending on device.
    """
    from django.template import RequestContext
    from django.shortcuts import render_to_response
    from time_spent.utils import desktop_context

    return render_to_response(
        'details.html',
        desktop_context(request=request, month=month, year=year),
        context_instance=RequestContext(request)
    )


@login_required
def net_income(request, month=0, year=0):
    """
    We're building the response and then sending it via this view.
    Rather than going the more traditional route, we're opting for
    returning variable responses depending on device.
    """
    from django.template import RequestContext
    from django.shortcuts import render_to_response
    from time_spent.utils import desktop_context

    return render_to_response(
        'details.html',
        desktop_context(request=request, month=month, year=year),
        context_instance=RequestContext(request)
    )
