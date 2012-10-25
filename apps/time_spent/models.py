from django.db import models
from django.contrib.auth.models import User


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

    # def hours_per_day(self):
    #     return self.hours / 7

    # def hours_per_month(self, month=None):
    #     return self.hours_per_day() * (month.days() or 30)

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
        self.creator = kwargs.get('creator')

    def daily(self):
        return self.yearly() / (52 * 7)  # 52wks 7days

    def monthly(self):
        income = Income.objects.get(creator=self.creator).amount
        expense = Expense.total(self.creator)
        return income - expense

    def yearly(self):
        return self.monthly() * 12

    def percent(self):
        """
        Percent of monthly income is net income
        """
        income = Income.objects.get(creator=self.creator).amount * 100

        if income <= 0:
            return 0

        return self.monthly() / income

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
    label = models.CharField(max_length=200)
    amount = models.FloatField()
    creator = models.ForeignKey(User)

    def __unicode__(self):
        return '%s %s' % (self.label, self.amount)

    def __init__(self, *args, **kwargs):
        super(Wish, self).__init__(*args, **kwargs)

        if hasattr(self, 'creator'):
            self.net_income = NetIncome(creator=self.creator)

    @classmethod
    def total_amount(cls, creator):
        wishes = cls.objects.filter(
            creator=creator).values_list('amount', flat=True)

        return sum(wishes)

    @classmethod
    def total_time(cls, creator):
        from math import ceil, floor

        net = NetIncome(creator=creator)
        total = cls.total_amount(creator) * 1.0825  # tax

        if not net.monthly():
            return {
                'years': 0,
                'months': 0,
                'days': 0,
            }

        years = floor(total / net.yearly())
        months = floor((total - (net.yearly() * years)) / net.monthly())
        paid = (net.monthly() * months) + (net.yearly() * years)
        days = ceil((total - paid) / net.daily())

        return {
            'years': years,
            'months': months,
            'days': days,
        }

    def amount_with_tax(self):
        return self.amount * 1.0825

    def time(self):
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
        from math import floor
        return floor(self.amount_with_tax() / self.net_income.yearly())

    def months(self):
        from math import floor
        return floor(self.amount_with_tax() / self.net_income.monthly())

    def days(self):
        from math import floor
        return floor(self.amount_with_tax() / self.net_income.daily())
