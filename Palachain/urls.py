from django.contrib import admin
from django.urls import path, include
from .views import *
from tracking.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path ('', index, name= "index"),
    path ('Registrasi/', Register, name = 'Register'),
    path ('Profil/', complete_profile, name='complete_profile'), #Tambahkan menu untuk lengkapi data diri di dashboard
    path ('Login/', Login_user, name ="Login"),
    path ('Petani/', FarmerDashboard, name = "FarmerDashboard"),
    path ('Pengepul/', TraderDashboard, name = "TraderDashboard"),
    path ('Distributor/', DistributorDashboard, name = "DistributorDashboard"),
    path ('Pabrik/', FactoryDashboard, name = "FactoryDashboard"),
    path ('Konsumen/', CustomerDashboard, name = "CustomerDashboard"),
    path ('History/', History_transaction, name = 'History'),
    #Layer 2
    path ('Petani/Input/', include ('tracking.urls', )),
    path ('customer/<int:product_id>/', CustomerView, name='RecapCustomer'),
    path ('<str:Role>/Produk/', ShowProduct, name = 'ShowProduct'),
    path ('scan/<int:product_id>/', Scan_QR, name='scan_qr'),
    path ('<str:Role>/scan/', ScanPage, name='scanpage'),
    path ("Logout/", Logout_user, name="logout"),
    path ('factory/process/<int:product_id>/', factory_process_input, name='factory_process_input'),
    path ('admin/', admin.site.urls),

    #Show Profile
    path ('Petani/Profil/', ShowProfile, name= 'ShowProfile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
