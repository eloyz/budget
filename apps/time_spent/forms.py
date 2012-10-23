from django import forms
from time_spent.models import Wish


# class StockForm(forms.ModelForm):
#     class Meta:
#         model = Stock
#         fields = (
#             'dt',
#             'label',
#             'cost',
#             'slug',
#         )


class WishForm(forms.ModelForm):
    class Meta:
        model = Wish
        fields = (
            'label',
            'amount',
        )


class QuickExpenseForm(forms.Form):
    """
    This form takes has one field called
    total_expense.  We take the total_expense
    and divide it out into several expense items.
    """

    total_expense = forms.FloatField()
