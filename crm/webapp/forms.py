from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from crispy_forms.layout import Layout, Div, Field
from crispy_forms.helper import FormHelper
from bootstrap_datepicker_plus.widgets import DatePickerInput


from .models import Contract

# REGISTER/CREATE A USER

class CreateUserForm(UserCreationForm):

    class Meta:

        model = User
        fields = ['username', 'email', 'password1', 'password2']


# Login a user

class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())



class CustomForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = '__all__'
        widgets = {
            'trader':                   Div(attrs={'id': 'trader-input', 'class': 'dropdown'}),
            'trade_operation_type':     TextInput(attrs={'id': 'trade-operation-type-input'}),
            'sociedad':                 TextInput(attrs={'id': 'sociedad-input'}),
            'counterparty':             TextInput(attrs={'id': 'counterparty-input'}),
            'commodity':                TextInput(attrs={'id': 'commodity-input'}),
            'commodity_group':          TextInput(attrs={'id': 'commodity-group-input'}),
            'delivery_format':          TextInput(attrs={'id': 'delivery-format-input'}),
            'additive':                 TextInput(attrs={'id': 'additive-input'}),
            'broker':                   TextInput(attrs={'id': 'broker-input'}),
            'broker_fee':               TextInput(attrs={'id': 'broker-fee-input'}),
            'broker_fee_currency':      TextInput(attrs={'id': 'broker-fee-currency-input'}),
            'icoterm':                  TextInput(attrs={'id': 'icoterm-input'}),
            'entrega':                  TextInput(attrs={'id': 'entrega-input'}),
            'freight_cost':             TextInput(attrs={'id': 'freight-cost-input'}),
            'cost_center':              TextInput(attrs={'id': 'cost-center-input'}),
            'forex':                    TextInput(attrs={'id': 'forex-input'}),
            'payment_days':             TextInput(attrs={'id': 'payment-days-input'}),
            'price':                    TextInput(attrs={'id': 'price-input'}),
            'trade_currency':           TextInput(attrs={'id': 'trade-currency-input'}),
            'delivery_period':          TextInput(attrs={'id': 'delivery-period-input'}),
            'date':                     DatePickerInput(options={
                "format": "DD/MM/YYYY",
                "locale": "en"
            }),
        }