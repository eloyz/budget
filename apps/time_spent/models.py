from django.db import models
from django.contrib.auth.models import User


class Income(models.Model):
    """Income"""
    label = models.CharField(max_length=200)
    amount = models.FloatField()
    creator = models.ForeignKey(User)
    session_hash = models.CharField(max_length=200)
    # hours = models.FloatField()

    def per_day(self, num_workdays):
        return float(self.amount) / float(num_workdays)

    def per_hour(self, num_workdays):
        return self.per_day(num_workdays) / 8.0  # self.hours

    # def hours_per_day(self):
    #     return self.hours / 7

    # def hours_per_month(self, month=None):
    #     return self.hours_per_day() * (month.days() or 30)

    def __unicode__(self):
        return "%s %s" % (self.label, self.amount)


class Expense(models.Model):
    dt = models.DateTimeField()
    label = models.CharField(max_length=200)
    amount = models.FloatField()
    creator = models.ForeignKey(User)
    session_hash = models.CharField(max_length=200)

    def __unicode__(self):
        return "%s %s" % (self.label, self.amount)


