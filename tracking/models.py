from django.db import models
from django.contrib.auth.models import AbstractUser
import qrcode
from io import BytesIO
from django.core.files import File


class ProfileUser (AbstractUser):
    ROLE_CHOICES= [
        ('farmer', 'Petani'),
        ('trader', 'Pengepul'),
        ('factory', 'Pabrik'),
        ('distributor', 'Distributor'),
        ('customer', 'Customer'),
    ]
    Role            = models.CharField (max_length=20, choices= ROLE_CHOICES)
    def __str__(self):
        return f"{self.username} ({self.Role})"
    

class Farmer (models.Model):
    Desa = [
        ("Laturake", "Laturake"),
        ("Morekao", "Morekao"),
        ("Ariate", "Ariate"),
        ("Kawa", "Kawa"),
        ("Alang Saude", "Alang Saude"),
        ("Waisala", "Waisala"),
        ("Kamal", "Kamal"),
        ("Buria", "Buria"),
        ("Lokki", "Lokki"),
        ("Nagalema", "Nagalema"),
        ("Tehoru", "Tehoru"),
        ("Piru", "Piru"),
        ("Taniwel", "Taniwel"),
        ("Leimu", "Leimu"),
        ("Lainnya", "Lainnya"),
    ]
    user            = models.OneToOneField ('ProfileUser', on_delete= models.CASCADE, related_name= 'Farmer')
    Name            = models.CharField (max_length = 100)
    FarmerGroup     = models.CharField (max_length= 100)
    AsalDesa        = models.CharField (max_length= 100, choices= Desa, default= "Pilih Desa")
    Location        = models.CharField (max_length=100, default= "test")
    
class Product (models.Model):
    ProductFarmers = [
        ("Pala Batok", "Pala Batok"),
        ("Pala Bulat", "Pala Bulat"),
        ("Pala Lonjong", "Pala Lonjong"),
        ("Daging Pala", "Daging Pala"),
        ("Fuli", "Fuli"),
        ("Cengkeh", "Cengkeh"),
        ("Kenari", "Kenari"),
        ("Vanila", "Vanila"),
        ("Kopi Tuni", "Kopi Tuni"),
        ("Buah Pala Utuh", "Buah Pala Utuh"),
    ]
    Grade = [
        ('basah', 'Basah'),
        ('kering', 'Kering'),
        ('campur', 'Campur'),
        ('abcd', 'ABCD atau AB'),
        ('bwp', 'BWP'),
        ('ss', 'SS'),
        ('whole', 'Whole'),
        ('broken', 'Broken'),
        ('tua', 'Tua'),
        ('muda', 'Muda'),
        ('lainnya', 'Lainnya')
    ]
    ProductFarmers  = models.CharField (choices= ProductFarmers, max_length=100, default= 'Tidak ada produk')
    Varietas        = models.CharField (max_length=100, blank= True, null= True)
    Grade           = models.CharField (max_length=20, choices= Grade, blank= True, null=True, default= 'Kualitas')
    Volume          = models.FloatField ()
    HarvestAge      = models.CharField (max_length=100)
    HarvestMethod   = models.CharField (max_length=100)
    WaterContent    = models.CharField (max_length=100)
    Owner           = models.ForeignKey ('ProfileUser', on_delete= models.CASCADE)
    QR_Code         = models.ImageField (upload_to = 'qrcodes/', blank= True, null= True)
    
    def save (self, *args, **kwargs):
        super().save(*args, **kwargs)
        qr_info = f"{self.id}"
        qr_img = qrcode.make (qr_info)

        buffer = BytesIO()
        qr_img.save(buffer, format = 'PNG')
        file_name = f'qr{self.Varietas}_{self.id}.png'
        self.QR_Code.save (file_name, File(buffer), save=False)

        super ().save (*args, **kwargs)
    def __str__(self):
        return f"{self.Varietas} - (Pemilik: {self.Owner.username})"


class History (models.Model):
    Seller          = models.ForeignKey ('ProfileUser', on_delete = models.CASCADE, related_name= 'Seller')
    Buyer           = models.ForeignKey ('ProfileUser', on_delete= models.CASCADE, related_name= 'Buyer')
    Product         = models.ForeignKey (Product, on_delete= models.CASCADE, related_name= 'History')
    Date            = models.DateTimeField (auto_now_add= True)
    def __str__(self):
        return f"{self.Product.Varietas} dari {self.Seller.username if self.Seller else '-'} Ke {self.Buyer.username if self.Buyer else '-'}" 

class Trader (models.Model):
    user            = models.OneToOneField ('ProfileUser', on_delete= models.CASCADE, related_name= 'Trader')
    Name            = models.CharField (max_length= 100)
    Location        = models.CharField (max_length= 100, default= "test")

#yang atas blm inggris
class Factory (models.Model):
    user            = models.OneToOneField ('ProfileUser', on_delete= models.CASCADE, related_name= 'Factory')
    FactoryName    = models.CharField (max_length= 100)
    Location        = models.CharField (max_length= 100, default= "test")

class Distributor (models.Model):
    user            = models.OneToOneField ('ProfileUser', on_delete= models.CASCADE, related_name= 'Distributor')
    Name            = models.CharField (default= 'Distributor Baru')
    Location        = models.CharField (max_length= 100, default= "test")


class Customer (models.Model):
    user            = models.OneToOneField ('ProfileUser', on_delete= models.CASCADE, related_name= 'Customer')
    Name            = models.CharField (max_length=100)
    Location        = models.CharField (max_length= 200, default= "test")

#ADDING
class ProductFactory (models.Model):
    product        = models.OneToOneField ('Product', on_delete= models.CASCADE, related_name= 'ProductFactory')
    ProductionCode = models.CharField (max_length=100, blank= True, null=True)
    DryingStart    = models.DateTimeField(null=True, blank=True)
    DryingEnd      = models.DateTimeField(null=True, blank=True)
    PressingDate   = models.DateField(null=True, blank=True)
    PackagingDate  = models.DateField(null=True, blank=True)
    PackagingType  = models.CharField(max_length=100, blank=True)


    def __str__(self):
        return f"Factory data for {self.product.Varietas}"

