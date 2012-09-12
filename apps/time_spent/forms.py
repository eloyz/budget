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
