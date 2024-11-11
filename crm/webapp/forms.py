from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput, DateInput  
from django.db import connection
from django.apps import apps
from datetime import date

from crispy_forms.layout import Layout, Div, Field
from crispy_forms.helper import FormHelper
from bootstrap_datepicker_plus.widgets import DatePickerInput


from .models import Contract, Trader

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
            'date':                     DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control' 'customInput',
                    'id': 'date-input',
                    'max': date.today().isoformat(),
                
            }),
        }



def get_table_choices():
    # Get all models in the installed apps
    models = apps.get_models()
    
    # Extract table names from models
    model_table_names = {model._meta.db_table for model in models}
    
    # Get all tables in the current database schema
    with connection.cursor() as cursor:
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
        all_tables = cursor.fetchall()
    
    # Filter out tables that are not managed by Django models
    
    table_choices = [

                ('webapp_trader', 'Trader'),
                ('webapp_trade_operation_type', 'Trade Operation Type'),
                ('webapp_sociedad', 'Sociedad'),
                ('webapp_counterparty', 'Counterparty'),
                ('webapp_commodity', 'Commodity'),
                ('webapp_commodity_group', 'Commodity Group'),
                ('webapp_delivery_format', 'Delivery Format'),
                ('webapp_additive', 'Additive'),
                ('webapp_broker', 'Broker'),                
                ('webapp_broker_fee_currency', 'Broker Currency'),
                ('webapp_icoterm', 'Icoterm'),
                ('webapp_entrega', 'Entrega'),                
                ('webapp_cost_center', 'Cost Center'),                
                ('webapp_trade_currency', 'Trade Currency'),
                ('webapp_delivery_period', 'Delivery Period'),

    ]
    
    return table_choices


    table_choices = [

                ('webapp_trader', 'Trader'),
                ('webapp_trade_operation_type', 'Trade Operation Type'),
                ('webapp_sociedad', 'Sociedad'),
                ('webapp_counterparty', 'Counterparty'),
                ('webapp_commodity', 'Commodity'),
                ('webapp_commodity_group', 'Commodity Group'),
                ('webapp_delivery_format', 'Delivery Format'),
                ('webapp_additive', 'Additive'),
                ('webapp_broker', 'Broker'),
                ('webapp_broker_fee', 'Broker Fee'),
                ('webapp_broker_fee_currency', 'Broker Currency'),
                ('webapp_icoterm', 'Icoterm'),
                ('webapp_entrega', 'Entrega'),
                ('webapp_freight_cost', 'Freight Cost'),
                ('webapp_cost_center', 'Cost Center'),
                ('webapp_forex', 'Forex'),
                ('webapp_payment_days', 'Payment Days'),
                ('webapp_price', 'Price'),
                ('webapp_trade_currency', 'Trade Currency'),
                ('webapp_delivery_period', 'Delivery Period'),

    ]


class TableSelectForm(forms.Form):
    table = forms.ChoiceField(choices=get_table_choices())



class TraderForm(forms.ModelForm):
    class Meta:
        model = Trader
        fields = ['trader_name']