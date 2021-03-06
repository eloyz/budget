from django.db import models
from django.contrib.auth.models import User

TAX_RATE = 1.0825


class Income(models.Model):
    """Income"""
    label = models.CharField(max_length=200)
    amount = models.FloatField()
    creator = models.ForeignKey(User)
    session_hash = models.CharField(max_length=200)
    hours = models.FloatField(default=(7 * 24))

    def per_day(self, num_workdays):
        return float(self.amount) / float(num_workdays)

    def per_hour(self, num_workdays):
        return self.per_day(num_workdays) / 8.0  # self.hours

    def __unicode__(self):
        return '%s %s' % (self.label, self.amount)


class Expense(models.Model):
    dt = models.DateTimeField()
    label = models.CharField(max_length=200)
    amount = models.FloatField()
    creator = models.ForeignKey(User)
    session_hash = models.CharField(max_length=200)

    def __unicode__(self):
        return '%s %s' % (self.label, self.amount)

    @classmethod
    def total(cls, creator):
        expenses = cls.objects.filter(
            creator=creator).values_list('amount', flat=True)

        return sum(expenses)

    def percent(self):
        return self.amount / Income.objects.get(creator=self.creator).amount * 100.0


class NetIncome(object):

    def __init__(self, *args, **kwargs):
        """
        Returns a net income object, calculates
        net income filterd by creator.
        """
        self.creator = kwargs.get('creator')

    def hourly(self):
        """
        Returns the amount of income made hourly.
        """
        return self.daily() / 24

    def daily(self):
        """
        Returns the amount of income made daily.
        """
        return self.yearly() / (52 * 7)  # 52wks 7days

    def monthly(self):
        """
        Returns the amount of income made monthly.
        """
        income = Income.objects.get(creator=self.creator).amount
        expense = Expense.total(self.creator)
        return income - expense

    def yearly(self):
        """
        Returns the amount of income made yearly.
        """
        return self.monthly() * 12

    def on_date(self, dt):
        """
        Returns the amount of income you would have
        made by the specified date.
        """

    def percent(self):
        """
        Percent of monthly income is net income
        """
        income = Income.objects.get(creator=self.creator).amount

        if income <= 0:
            return 0

        return self.monthly() / income * 100

    def is_positive(self):
        """
        Returns a boolean value of whether your monthly
        income is negative or positive.
        """
        return self.monthly() > 0

    def is_zero(self):
        """
        Returns a boolean value of whether your monthly
        income is negative or positive.
        """
        return self.monthly() == 0


class Wish(models.Model):
    label = models.CharField(max_length=200, default=u'')
    amount = models.FloatField()
    creator = models.ForeignKey(User)

    def __init__(self, *args, **kwargs):
        super(Wish, self).__init__(*args, **kwargs)

        if hasattr(self, 'creator'):
            self.net_income = NetIncome(creator=self.creator)

    def __unicode__(self):
        return '%s %s' % (self.label, self.amount)

    @classmethod
    def total_amount(cls, creator):
        wishes = cls.objects.filter(
            creator=creator).values_list('amount', flat=True)

        return sum(wishes)

    @classmethod
    def total_time(cls, creator):
        """
        Returns the amount of time it would
        take the end-user to save for their wishlist.
        """
        from math import ceil, floor

        net = NetIncome(creator=creator)
        wishlist_total = cls.total_amount(creator) * TAX_RATE  # tax

        if not net.monthly():
            return {
                'years': 0,
                'months': 0,
                'days': 0,
            }

        years = floor(wishlist_total / net.yearly())
        months = floor(wishlist_total / net.monthly()) % 12

        # basic accounting
        paid = sum([net.yearly() * years, net.monthly() * months])
        balance = wishlist_total - paid

        # months aren't divided evenly [e.g. 29-31 days in month]
        # more accurate estimation
        days = ceil(balance / net.daily())

        return {
            'total': wishlist_total,
            'years': years,
            'months': months,
            'days': days,
        }

    def amount_with_tax(self):
        """
        Returns the amount for the wish list item
        once tax is included.
        """
        return self.amount * TAX_RATE

    def time(self):
        """
        Returns the amount of time it would take to purchase
        this wishlist item.  Returns dictionary with keys
        (e.g. years, months, days)
        """
        from math import ceil, floor

        years = self.years()
        months = floor((self.amount_with_tax() - \
            (self.net_income.yearly() * years)) / self.net_income.monthly())
        paid = (self.net_income.monthly() * months) + (self.net_income.yearly() * years)
        days = ceil((self.amount_with_tax() - paid) / self.net_income.daily())

        return {
            'years': years,
            'months': months,
            'days': days,
        }

    def years(self):
        """
        Returns the number of years it would take to pay
        for this wish list item.
        """
        from math import floor
        return floor(self.amount_with_tax() / self.net_income.yearly())

    def months(self):
        """
        Returns the number of months it would take to pay
        for this wish list item.
        """
        from math import floor
        return floor(self.amount_with_tax() / self.net_income.monthly())

    def days(self):
        """
        Returns the number of days it would take to pay
        for this wish list item.
        """
        from math import floor
        return floor(self.amount_with_tax() / self.net_income.daily())
