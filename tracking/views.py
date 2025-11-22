from django.shortcuts import render, redirect, get_object_or_404
from .forms import InputProduct, FactoryProcessForm
from django.http import HttpResponse
from .models import *
from django.contrib.auth.decorators import login_required 
from django.db.models import Q
from geopy.geocoders import Nominatim

#Input and Show Product
def Input(request):
    if request.method == 'POST':
        form = InputProduct(request.POST)
        if form.is_valid():
            product = form.save(commit=False)     
            product.Owner = request.user
            form.save()  
            return redirect('FarmerDashboard')
    else:
        form = InputProduct()
    return render(request, 'FarmerCase/InputProduct.html', {'form': form})


def ShowProduct (request, Role):
    user = request.user
    products = Product.objects.filter (Owner=user)
    context={
        'title':'Daftar Produk Pala',
        'Products': products
    }
 
    return render (request, 'FarmerCase/ShowProduct.html', context)


#Scan QR
def Scan_QR (request, product_id):
    product = get_object_or_404 (Product, id= product_id) 
    current_user = request.user
    old_owner = product.Owner
    role = request.user.Role

    product.Owner = current_user
    product.save ()

    History.objects.create (
        Product = product,
        Seller = old_owner,
        Buyer = current_user
    
    )
    if role == "customer":
        return redirect("RecapCustomer", product_id=product.id)
    dashboard_map = {
        "farmer": "FarmerDashboard",
        "trader": "TraderDashboard",   
        "factory": "FactoryDashboard",
        "distributor": "DistributorDashboard",
    }
    context = {
        'product' : product,
        'seller'  : old_owner,
        'buyer'   : current_user,
        "dashboard_url": dashboard_map.get(role),

    }
    

    return render (request, 'Events/Accepted.html', context)

def ScanPage(request, Role):
    return render(request, 'Events/ScanPage.html')


#History
def History_transaction(request):
    user = request.user
    riwayat = History.objects.all().order_by('Date')

    return render(request, 'Events/History.html', {'riwayat': riwayat})

#Input Process
@login_required
def factory_process_input(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user.Role != "factory":
        return HttpResponse("Unauthorized", status=401)

    # Jika proses sudah dibuat, tampilkan pesan atau bisa diarahkan ke edit
    if hasattr(product, 'ProductFactory'):
        process = product.ProductFactory
        form = FactoryProcessForm(request.POST or None, instance=process)
    else:
        form = FactoryProcessForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            process = form.save(commit=False)
            process.product = product
            process.save()
            return redirect('FactoryDashboard')
        else:
            print("FORM ERRORS:", form.errors)

    return render(request, 'FactoryCase/Process.html', {
        'form': form,
        'product': product
    })


#Costumer 
def CustomerView(request, product_id):
    product = Product.objects.get(id=product_id)
    users = ProfileUser.objects.filter(Q(Seller__Product=product)|Q(Buyer__Product=product)).distinct()
    journey = History.objects.filter(Product=product).order_by("Date")

    for u in users:
        if u.Role == "farmer":
            u.Address = GetAddress(u.Farmer.Location)
        elif u.Role == "trader":
            u.Address = GetAddress(u.Trader.Location)
        elif u.Role == "factory":
            u.Address = GetAddress(u.Factory.Location)
        elif u.Role == "distributor":
            u.Address = GetAddress(u.Distributor.Location)
        elif u.Role == "customer":
            u.Address = GetAddress(u.Customer.Location)

    for h in journey:
            seller_loc = get_user_location(h.Seller)
            buyer_loc = get_user_location(h.Buyer)
            h.SellerAddress = GetAddress(seller_loc)
            h.BuyerAddress = GetAddress(buyer_loc)


    context = {
        "product": product,
        "users": users,
        "journey": journey,
        "dashboard_url": "CustomerDashboard"
    }
    return render(request, "CustomerCase/Query.html", context)




#LOCATION   
def reverse_geocode(lat, lon):
    geolocator = Nominatim(user_agent="myapp")
    location = geolocator.reverse((lat, lon), timeout=10)
    if location:
        return location.address
    return "Alamat tidak ditemukan"

def GetAddress(coords):
    if not coords:
        return "Lokasi tidak tersedia"

    lat, lon = coords.split(",")
    geolocator = Nominatim(user_agent="myapp")
    
    try:
        location = geolocator.reverse(f"{lat}, {lon}")
        return location.address if location else coords
    except:
        return coords

def get_user_location(user):
    """Mengambil lokasi sesuai role user"""
    try:
        role = user.Role

        if role == "farmer":
            return user.Farmer.Location

        elif role == "trader":
            return user.Trader.Location

        elif role == "factory":
            return user.Factory.Location

        elif role == "distributor":
            return user.Distributor.Location

        elif role == "customer":
            return user.Customer.Location

    except:
        return None


