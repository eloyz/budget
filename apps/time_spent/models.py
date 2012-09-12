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

class NetIncome(object):

    def __init__(self, *args, **kwargs):
        self.creator = kwargs.get('creator')

    def income(self):
        return Income.objects.get(creator=self.creator).amount

    def expense(self):
        return Expense.total(self.creator)

    def daily(self):
        return self.yearly() / (52 * 7)  # 52wks 7days

    def monthly(self):
        return self.income() - self.expense()

    def yearly(self):
        return self.monthly() * 12

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

    def amount_with_tax(self):
        return self.amount * 1.0825

    def months(self):
        from math import floor
        return floor(self.amount_with_tax() / self.net_income.monthly())

    def days(self):
        from math import ceil
        days = (self.amount_with_tax() - (self.net_income.monthly() * self.months())) / self.net_income.daily()
        return ceil(days)
