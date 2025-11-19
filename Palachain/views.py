from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from tracking.forms import ProfileUserRegisterForm
from django.contrib.auth.decorators import login_required
from tracking.forms import *
from tracking.models import *
from django.db.models import Q


#Login

def index (request):
    context= {
        'title':'Home',
    }    
    return render (request, 'Login/index.html', context)

def Logout_user (request):
    logout (request)
    return redirect ('/')


User = get_user_model()
def Login_user (request):
    context = {
        'title' : 'Login',
        'header' : 'Selamat datang di halaman login'
    }

    if request.method == "POST":
        username = request.POST.get ('username')
        password = request.POST.get ('password')
        user = authenticate (request, username = username, password = password)
        if user is not None:
                login (request, user)
             
                if user.Role == 'farmer':
                    return redirect ('FarmerDashboard')
                elif user.Role == 'trader':
                    return redirect ('TraderDashboard')
                elif user.Role == 'factory':
                    return redirect ('FactoryDashboard')
                elif user.Role == 'distributor':
                    return redirect ('DistributorDashboard')
                else:
                    return redirect ('CustomerDashboard')
        else:
            print ('error')
    return render (request, 'Login/Login.html', context)


#Show profile
def ShowProfile (request):
    user = request.user
    profile = None
    if user.Role == 'farmer':
        profile = Farmer.objects.filter(user=user).first()
    elif user.Role == 'trader':
        profile = Trader.objects.filter(user=user).first()
    elif user.Role == 'factory':
        profile = Factory.objects.filter(user=user).first()
    elif user.Role == 'distributor':
        profile = Distributor.objects.filter(user=user).first()
    else:
        profile = Customer.objects.filter(user=user).first()
    context = {
    'title': 'Profil Pengguna',
    'profile': profile,
    }
    return render (request, 'Login/UserProfile.html', context)

#Registration

def Register(request):
    if request.method == 'POST':
        form = ProfileUserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('complete_profile')
    else:
        form = ProfileUserRegisterForm()
    return render(request, 'Login/Register.html', {'form': form})


@login_required
def complete_profile(request):
    user = request.user
    role = user.Role

    if role == 'farmer':
        FormClass = FarmerForm
    elif role == 'trader':
        FormClass = TraderForm
    elif role == 'factory':
        FormClass = FactoryForm
    elif role == 'distributor':
        FormClass = DistributorForm
    else:
        FormClass = CustomerForm

    if request.method == 'POST':
        form = FormClass(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = user   
            profile.save()
            return redirect('Login') 
    else:
        form = FormClass()

    return render(request, 'Login/Profile.html', {'form': form, 'role': role})


#============================================================================================================================
#Dashboard

def FarmerDashboard (request):
    user = request.user
    stock = Product.objects.filter(Owner=user).count()
    total_product = History.objects. filter (Q(Seller=user)).values("Product").distinct().count() + stock
    sold_count = History.objects.filter(Seller=user).count()
    context= {
        'title':'Dashboard Petani',
        'total_product': total_product,
        'sold_count' : sold_count,
        'stock': stock
    }    
    return render (request, 'Dashboard/FarmerDashboard.html', context)


def TraderDashboard (request):
    user = request.user
    stock = Product.objects.filter(Owner=user).count()
    sold_count = History.objects.filter(Seller=user).count()
    total_product = sold_count + stock
    context= {
        'title':'Dashboard Pengepul',
        'total_product': total_product,
        'sold_count' : sold_count,
        'stock': stock
    }    
    return render (request, 'Dashboard/TraderDashboard.html', context)


def FactoryDashboard (request):
    user = request.user
    stock = Product.objects.filter(Owner=user).count()
    total_product = History.objects. filter (Q(Seller=user)).values("Product").distinct().count() + stock
    sold_count = History.objects.filter(Seller=user).count()
    context= {
        'title':'Dashboard Pabrik',
        'total_product': total_product,
        'sold_count' : sold_count,
        'stock': stock
    }    
    return render (request, 'Dashboard/FactoryDashboard.html', context)


def DistributorDashboard (request):
    user = request.user
    stock = Product.objects.filter(Owner=user).count()
    total_product = History.objects. filter (Q(Seller=user)).values("Product").distinct().count() + stock
    sold_count = History.objects.filter(Seller=user).count()
    context= {
        'title':'Dashboard Distributor',
        'total_product': total_product,
        'sold_count' : sold_count,
        'stock': stock
    }    
    return render (request, 'Dashboard/DistributorDashboard.html', context)


def CustomerDashboard (request):
    context= {
        'title':'Dashboard Konsumen',
    }    
    return render (request, 'Dashboard/CustomerDashboard.html', context)


