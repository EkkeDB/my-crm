from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db import connection




from .forms import CreateUserForm, LoginForm, CustomForm, TableSelectForm

from webapp.models import   Cryptocurrency, HistoricalCryptocurrency, Centro, Sociedad, Trader, Commodity_Group, Commodity_Type, Commodity_Subtype, Commodity, Delivery_Format, Additive, Counterparty, Counterparty_Facility, Broker, Currency, ICOTERM, Trade_Operation_Type, Contract





# Create your views here.
# from django.http import HttpResponse


@login_required(login_url='my-login')
def home(request):
    
    return render(request, 'webapp/index.html')


@login_required(login_url='my-login')
def index(request):
    
    return render(request, 'webapp/index.html')

@login_required(login_url='my-login')
def charts(request):
    
    return render(request, 'webapp/charts.html')


@login_required(login_url='my-login')
def tables(request):
    
    return render(request, 'webapp/tables.html')


@login_required(login_url='my-login')
def tables_manage(request):
    
    return render(request, 'webapp/tables-manage.html')


"""
@login_required(login_url='my-login')
def contracts(request):
    cryptos = Cryptocurrency.objects.all()
    return render(request, 'webapp/contracts.html', {'cryptos': cryptos})
"""

def login(request):
    
    return render(request, 'webapp/login.html')



# Register a user 

def register(request):

    form = CreateUserForm()

    if request.method == "POST":

        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()
            #return redirect('')
    context = {'form' : form}

    return render(request, 'webapp/register.html', context=context)



def register2(request):

    form = CreateUserForm()

    if request.method == "POST":

        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("my-login")
    context = {'form' : form}

    return render(request, 'webapp/register2.html', context=context)



# - Login a user

def my_login(request):

    form = LoginForm()

    if request.method == "POST":

        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:

                auth.login(request, user)

                return redirect("dashboard")

    context = {'form':form}

    return render(request, 'webapp/my-login.html', context=context)



# - Logout user

def user_logout(request):

    auth.logout(request)

    #messages.success(request, "Logout success!")

    return redirect("my-login")






# - Dashboard

@login_required(login_url='my-login')
def dashboard(request):

    return render(request, 'webapp/index.html')


def password(request):
    
    return render(request, 'webapp/password.html')



def unauth(request):
    
    return render(request, 'webapp/401.html')


def notfound(request):
    
    return render(request, 'webapp/404.html')

@login_required(login_url='my-login')
def crypto(request):
    cryptos = Cryptocurrency.objects.all()
    return render(request, 'webapp/display_crypto.html', {'cryptos': cryptos})

@login_required(login_url='my-login')
def mycrypto(request):
    cryptos = Cryptocurrency.objects.all()
    return render(request, 'webapp/mycrypto.html', {'cryptos': cryptos})





@login_required(login_url='my-login')
def contracts(request):
    if request.method == 'POST':
        form = CustomForm(request.POST)
        if form.is_valid():
            # Process the form data
            # Redirect or render success page
            pass
    else:
        form = CustomForm()

    return render(request, 'webapp/contracts.html', {'form': form})


def live_search(request):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        query = request.GET.get('query', '')
        results = Trader.objects.filter(trader_name__icontains=query)
        data = [{'id_trader': obj.id_trader, 'trader_name': obj.trader_name} for obj in results]
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({}, status=400)
    




def fetch_table_data(table_name):
    with connection.cursor() as cursor:
        cursor.execute(f'SELECT * FROM "{table_name}"')
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
    return columns, rows



@login_required(login_url='my-login')
def table_view(request):
    columns = []
    rows = []
    if request.method == 'POST':
        form = TableSelectForm(request.POST)
        if form.is_valid():
            table_name = form.cleaned_data['table']
            columns, rows = fetch_table_data(table_name)
    else:
        form = TableSelectForm()
    return render(request, 'webapp/table_view.html', {'form': form, 'columns': columns, 'rows': rows})

