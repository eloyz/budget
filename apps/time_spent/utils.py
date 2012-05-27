

# Warm to cool colors
# Ideally this list could be generated
EXPENSE_COLORS = (
    '#AB2F27',  # red
    '#D08021',  # orange
    '#D19919',  # yelloworange
    '#EFC443',  # yellow
    '#A7B929',  # olive
    '#84BB3B',  # lime
    '#57A336',  # green
    '#45A388',  # bluegreen
    '#4784A3',  # teal
    '#668ADE',  # blue
)


def get_budget_hours(budget):
    return float(budget) / 24


def get_expense_hours(expense):
    return float(expense) / 24


def get_total_expense(expenses):
    """
    get_total_expense:
        Required: List of expense objects.
        Returns the total amount of expenses
        for this month.
    """
    total_expense = 0
    for expense in expenses:
        total_expense += expense.amount

    return float(total_expense)


def next_month(month, year):
    """
    next_month(month_int, year_int):
        Returns next month tuple.
        i.e. (next_month_int, next_year_int)
    """
    next_month = (month + 1) % 13
    next_year = year
    if next_month == 0:
        next_month = 1
        next_year += 1
    return (next_month, next_year)


def prev_month(month, year):
    """Returns previous month tuple"""
    prev_month = (month - 1) % 13
    prev_year = year
    if prev_month == 0:
        prev_month = 12
        prev_year -= 1
    return (prev_month, prev_year)


def work_days(month_int=None, month=None):
    """List of workdays"""
    import calendar

    work_days = []
    for week in month:
        for day in week:
            if day.month == month_int and day.weekday() < calendar.SATURDAY:
                work_days.append(day)
    return work_days


def desktop_context(**kwargs):
    """
    Returns context for for desktop response.
    Ideally you're not being redirected based
    on what device or stage you are within this
    application.

    Ideally the application shows
    you exactly what you need and we remove
    the linkage factor. Some would frown at this.

    I think my limiting people's resources, it's
    easier to keep them focused and have them appreciate
    the interface.
    """
    import calendar
    from datetime import datetime
    from itertools import cycle, count
    from django.core.urlresolvers import reverse
    from time_spent.models import Income, Expense
    from time_spent.utils import EXPENSE_COLORS

    request = kwargs['request']
    month = kwargs['month']
    year = kwargs['year']

    user = request.user
    calendar_dt = today = datetime.today()

    if month and year:
        calendar_dt = datetime(day=1, month=int(month), year=int(year))

    calendar.setfirstweekday(calendar.SUNDAY)
    days_of_week = calendar.weekheader(10).split()
    month = calendar.Calendar(calendar.SUNDAY).monthdatescalendar(
        calendar_dt.year,
        calendar_dt.month
    )

    expenses = Expense.objects.filter(creator=user).order_by('pk')

    try:
        income = Income.objects.get(creator=user)
    except:
        income = Income.objects.create(
            label=unicode(),
            amount=3000,
            creator=user,
        )

    num_workdays = len(work_days(calendar_dt.month, month))
    # hourly_income = income.per_hour(num_workdays)
    # daily_income = income.per_day(num_workdays)

    income_hourly = income.amount / (num_workdays * 24)
    income_daily = income.amount / num_workdays

    colors = cycle(EXPENSE_COLORS)
    counter = count(0)

    expense_list = []
    for i in range(10):
        expense_list.append({
            'pk': 0,
            'label': u'',
            'amount': 0,
            'color': colors.next(),
            'hours': 0,
            'days': 0,
            'per_month': u'',
            'per_year': u'',
        })

    colors = cycle(EXPENSE_COLORS)

    for expense in expenses[:10]:

        expense_list[counter.next()] = {
            'pk': expense.pk,
            'label': expense.label,
            'amount': expense.amount,
            'color': colors.next(),
            'hours': expense.amount / income_hourly,
            'days': expense.amount / income_daily,
            'per_month': u'12days/mo',
            'per_year': u'43days/yr',
        }

    if request.method == "POST":
        expense_list = []

        income.amount = request.POST.get('income-amount', None)
        income.save()

        post_items = ['stock-item-pk', 'stock-item-label', 'stock-item-amount', 'stock-item-color']
        expense_tuples = zip(*[dict(request.POST)[item] for item in post_items])

        counter = count(0)

        for expense_tuple in expense_tuples:
            pk, label, amount, color = expense_tuple[:4]

            if amount:
                amount = float(amount)
            else:
                amount = 0

            if pk:
                pk = int(pk)
            else:
                pk = 0

            if pk or amount > 0:
                try:
                    expense = Expense.objects.get(pk=pk)
                except:
                    expense = Expense()

                expense.dt = calendar_dt
                expense.label = label
                expense.amount = unicode(amount)
                expense.creator = user
                expense.save()

                pk = expense.pk

            expense_list.append({
                "pk": pk,
                "label": label,
                "amount": amount,
                "color": color,
                "hours": float(amount) / income_hourly,
                "days": float(amount) / income_daily,
                'per_month': u'12days/mo',
                'per_year': u'',
            })

    total_expense = get_total_expense(expenses)
    expense_hourly = total_expense / (num_workdays * 24)
    expense_daily = total_expense / num_workdays

    net_income = income.amount - total_expense
    month_name = calendar.month_name[calendar_dt.month]

    net_hours = net_income / (num_workdays * 24)
    net_days = net_income / num_workdays

    next_month_url = reverse('time-spent', args=next_month(calendar_dt.month, calendar_dt.year))
    prev_month_url = reverse('time-spent', args=prev_month(calendar_dt.month, calendar_dt.year))

    # this is how many work hours are available
    # not how many work hours you've worked this month
    survive_hours = (num_workdays * 8) - net_hours
    survive_percentage = survive_hours / (num_workdays * 8) * 100
    enjoy_percentage = net_hours / (num_workdays * 8) * 100

    print num_workdays

    return {
        'calendar': calendar,
        'days_of_week': days_of_week,  # list
        'month': month,  # list
        'today': today,  # datetime
        'month_int': calendar_dt.month,
        'year_int': calendar_dt.year,
        'next_month_url': next_month_url,
        'prev_month_url': prev_month_url,
        'total_expense': total_expense,
        'expense_hourly': expense_hourly,
        'expense_daily': expense_daily,
        'income_hourly': income_hourly,
        'income_daily': income_daily,
        'month_name': month_name,
        'stock_list': expense_list,
        'income': income,
        'net_income': net_income,
        'num_work_hours': num_workdays * 8,
        'num_work_days': num_workdays,
        'net_hours': net_hours,
        'net_days': net_days,
        'survive_percentage': survive_percentage,
        'enjoy_percentage': enjoy_percentage,
    }


def mobile_context(**kwargs):
    return desktop_context(**kwargs)
