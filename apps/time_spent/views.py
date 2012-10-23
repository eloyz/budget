from django.conf import settings
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from lazysignup.decorators import allow_lazy_user

from time_spent.forms import QuickExpenseForm

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
    from time_spent.utils import expense_context

    return render_to_response(
        'expenses.html',
        expense_context(request=request, month=month, year=year),
        context_instance=RequestContext(request)
    )


@allow_lazy_user
def expenses_quick_start(request):
    """
    Shows you a form that allows you type in your total expense
    for the month and we break it down to common monthly items
    in a budget, allowing you to edit your expenses rather than
    start from scratch.
    """

    if request.method == 'POST':
        form = QuickExpenseForm(request.POST)
        if form.is_valid():
            total_expense = form.cleaned_data['total_expense']

            print 'total_expense', total_expense
            # TODO: divide total_expense into typical budget

            # http://www.gatherlittlebylittle.com/2008/02/dave-ramseys-gazelle-budget/
            expenses_with_percent = {
                'Home': 24,
                'Utils': 5,
                'Food': 15,
                'Savings': 10,
                'Transportation': 10,
                'Clothing': 6,
                'Medical/Health': 5,
                'Personal': 10,
                'Entertainment': 5,
                'Debt': 10,
            }

            print 'expense_percent', sum(expenses_with_percent.values())

    else:  # not post
        form = QuickExpenseForm()

    return render_to_response(
        'expenses-quick-start.html', {
        'form': form,
        }, context_instance=RequestContext(request)
    )


@allow_lazy_user
def net_income(request, month=0, year=0):
    """
    We're building the response and then sending it via this view.
    Rather than going the more traditional route, we're opting for
    returning variable responses depending on device.
    """
    from time_spent.models import NetIncome, Wish

    net_income = NetIncome(creator=request.user)
    wish_list = Wish.objects.filter(
        creator=request.user).order_by('amount')

    amount = Wish.total_amount(request.user)
    total_time = Wish.total_time(request.user)

    total = {
        'amount': amount * 1.0825,
        'years': 0,
        'months': 0,
        'days': 0,
    }

    return render_to_response(
        'net-income.html', {
        'net_income': net_income,
        'wish_list': wish_list,
        'total': total,
        'total_time': total_time,
        }, context_instance=RequestContext(request)
    )


@allow_lazy_user
def wish_list(request, month=0, year=0):
    """
    Returns wish list page. This page lists out your
    wishes, and the amount of time to afford those wishes.
    """
    from time_spent.models import NetIncome, Wish

    net_income = NetIncome(creator=request.user)
    wish_list = Wish.objects.filter(
        creator=request.user).order_by('amount')

    amount = Wish.total_amount(request.user)
    total_time = Wish.total_time(request.user)

    total = {
        'amount': amount * 1.0825,
        'years': 0,
        'months': 0,
        'days': 0,
    }

    return render_to_response(
        'net-income.html', {
        'net_income': net_income,
        'wish_list': wish_list,
        'total': total,
        'total_time': total_time,
        }, context_instance=RequestContext(request)
    )


@allow_lazy_user
def wish(request):
    from time_spent.forms import WishForm

    if request.method == "POST":
        form = WishForm(request.POST)
        if form.is_valid():
            wish = form.save(commit=False)
            wish.creator = request.user
            wish.save()

        return HttpResponseRedirect(reverse('net-income'))

    return render_to_response(
        'wish.html', {
            'form': WishForm()
        }, context_instance=RequestContext(request)
    )


@allow_lazy_user
def wish_change(request, pk):
    from time_spent.models import Wish
    from time_spent.forms import WishForm
    wish = get_object_or_404(Wish, pk=pk)

    if request.method == "POST":
        form = WishForm(request.POST, instance=wish)
        if form.is_valid():
            wish = form.save(commit=False)
            wish.creator = request.user
            wish.save()

        return HttpResponseRedirect(reverse('net-income'))

    form = WishForm(instance=wish)

    return render_to_response(
        'wish-change.html', {
        'wish': wish,
        'form': form,
        }, context_instance=RequestContext(request)
    )


@allow_lazy_user
def wish_remove(request, pk):
    from time_spent.models import Wish
    wish = get_object_or_404(Wish, pk=pk)

    if request.method == "POST":
        wish.delete()
        return HttpResponseRedirect(reverse('net-income'))

    return render_to_response(
        'wish-remove.html', {
        'wish': wish,
        }, context_instance=RequestContext(request)
    )
