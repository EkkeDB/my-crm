from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db import connection
import json
from django.views.decorators.csrf import csrf_protect
from django.core.management import call_command



from .forms import CreateUserForm, LoginForm, CustomForm, TableSelectForm

from crm.apps.webapp.models import   Cryptocurrency, HistoricalCryptocurrency, Cost_Center, Sociedad, Trader, Commodity_Group, Commodity_Type, Commodity_Subtype, Commodity, Delivery_Format, Additive, Counterparty, Counterparty_Facility, Broker, Currency, ICOTERM, Trade_Operation_Type, Contract





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
    if request.method == 'GET':
        try:
            # Call fetch_crypto_data command to update cryptocurrency data
            call_command('fetch_crypto_data')
        except Exception as e:
            # Handle any errors that occur during data fetch
            return JsonResponse({'status': 'error', 'message': str(e)})
        
    # Retrieve all Cryptocurrency objects from the database
    cryptos = Cryptocurrency.objects.all()
    
    # Render the template with the cryptocurrency data
    return render(request, 'webapp/mycrypto.html', {'cryptos': cryptos})


@login_required(login_url='my-login')
def fetch_crypto_data_view(request):
    if request.method == 'POST':
        call_command('fetch_crypto_data')
        return JsonResponse({'status': 'success', 'message': 'Data fetched successfully.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})




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





@login_required(login_url='my-login')
def update_row(request):
    if request.method == 'POST':
        id_trader = request.POST.get('id_trader')
        trader_name = request.POST.get('trader_name')

        if id_trader:
            trader = get_object_or_404(Trader, pk=id_trader)
            trader.trader_name = trader_name
            trader.save()

            return redirect('table_view')  # Redirect to a suitable page

    return render(request, 'webapp/your_template.html')




@csrf_protect
def upload_csv(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        rows = data.get('rows', [])
        # Process rows and insert into the database
        for row in rows:
            # Assuming you have a model named `YourModel`
            Trader.objects.create(**row)
        return JsonResponse({'message': 'CSV data uploaded successfully!'})
    return JsonResponse({'error': 'Invalid request'}, status=400)


# To search in MODAL


# Mapping table names to model classes
model_mapping = {
    'sociedad': Sociedad,
    'counterparty': Counterparty,
    'commodity': Commodity,
    'trade_operation_type': Trade_Operation_Type,
    'cryptocurrency': Cryptocurrency,
    'historical_cryptocurrency': HistoricalCryptocurrency,
    'cost_center': Cost_Center,
    'trader': Trader,
    'commodity_group': Commodity_Group,
    'commodity_type': Commodity_Type,
    'commodity_subtype': Commodity_Subtype,
    'delivery_format': Delivery_Format,
    'additive': Additive,
    'broker': Broker,
    'currency': Currency,
    'icoterm': ICOTERM,
    'contract': Contract,
    'counterparty_facility': Counterparty_Facility
}

def fetch_data(request, table_name):
    model = model_mapping.get(table_name)
    if model is None:
        return JsonResponse({'error': 'Invalid table name'}, status=400)

    data = list(model.objects.values())
    return JsonResponse({'data': data})



def search_autocomplete(request, input_type):
    query = request.GET.get("q", "").strip()

    if len(query) >= 3:
        if input_type == "trader":
            results = Trader.objects.filter(trader_name__icontains=query)[:10]
            data = [{"id": t.id_trader, "name": t.trader_name} for t in results]
        elif input_type == "counterparty":
            results = Counterparty.objects.filter(counterparty_name__icontains=query)[:10]
            data = [{"id": c.id_counterparty, "name": c.counterparty_name} for c in results]
        else:
            data = []
    else:
        data = []

    return JsonResponse(data, safe=False)