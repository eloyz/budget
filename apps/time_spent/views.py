from django.conf import settings
from lazysignup.decorators import allow_lazy_user

# create method that returns context
# put context together with template
# return result

# home page could return multiple interfaces
# introduction version
# desktop version
# mobile version


@allow_lazy_user
def detail(request, month=0, year=0):
    """
    We're building the response and then sending it via this view.
    Rather than going the more traditional route, we're opting for
    returning variable responses depending on device.
    """
    from django.template import RequestContext
    from django.shortcuts import render_to_response
    from time_spent.utils import mobile_context, desktop_context

    if request.flavour == 'mobile':
        context = mobile_context(
            request=request, month=month, year=year)
    else:
        context = desktop_context(
            request=request, month=month, year=year)

    return render_to_response(
        'details.html', context,
        context_instance=RequestContext(request)
    )


@allow_lazy_user
def income(request, month=0, year=0):
    """
    We're building the response and then sending it via this view.
    Rather than going the more traditional route, we're opting for
    returning variable responses depending on device.
    """
    from django.template import RequestContext
    from django.core.urlresolvers import reverse
    from django.shortcuts import render_to_response, HttpResponseRedirect
    from time_spent.models import Income

    default_income = settings.BUDGET_DEFAULTS['income']

    try:
        income = Income.objects.get(creator=request.user)
    except:
        income = Income.objects.create(
            label=unicode(),
            amount=default_income,
            creator=request.user,
        )

    if request.method == "POST":
        income.amount = request.POST.get('income-amount')

        if not len(income.amount):
            income.amount = 0
        elif not income.amount.isalpha():
            income.amount = float(income.amount)
        else:  # is non-numeric
            income.amount = 0

        income.save()

        return HttpResponseRedirect(reverse('homepage'))

    return render_to_response(
        'income.html',
        {'income': income},
        context_instance=RequestContext(request)
    )


@allow_lazy_user
def expenses(request, month=0, year=0):
    """
    We're building the response and then sending it via this view.
    Rather than going the more traditional route, we're opting for
    returning variable responses depending on device.
    """
    from django.template import RequestContext
    from django.shortcuts import render_to_response
    from time_spent.utils import expense_context

    return render_to_response(
        'expenses.html',
        expense_context(request=request, month=month, year=year),
        context_instance=RequestContext(request)
    )


@allow_lazy_user
def net_income(request, month=0, year=0):
    """
    We're building the response and then sending it via this view.
    Rather than going the more traditional route, we're opting for
    returning variable responses depending on device.
    """
    from django.template import RequestContext
    from django.shortcuts import render_to_response
    from time_spent.models import Income, Expense
    from time_spent.utils import get_total_expense

    income = Income.objects.get(creator=request.user)
    expenses = Expense.objects.filter(creator=request.user).order_by('pk')
    expense_monthly = get_total_expense(expenses)
    net_monthly = income.amount - expense_monthly

    mbp = 1700

    months = mbp / net_monthly
    days = mbp % 30

    return render_to_response(
        'net-income.html', {
        'net_income': net_monthly,
        'months': months,
        'days': days,
        }, context_instance=RequestContext(request)
    )
