from django.db import models
import datetime


# Create your models here.
class Brand(models.Model):
    name=models.CharField(max_length=20)
    image=models.ImageField(upload_to='uploads/products/',default='')


    @staticmethod
    def get_all_brand():
            return Brand.objects.all()

    def __str__(self):
            return  self.name

class Product(models.Model):
    name=models.CharField(max_length=25)
    price=models.IntegerField(default=0)
    sprice=models.IntegerField(default=0)
    brand=models.ForeignKey(Brand,on_delete=models.CASCADE,default=1)
    rate=models.FloatField(default=0)
    ram=models.CharField(max_length=20)
    rom=models.CharField(max_length=20)
    description=models.CharField(max_length=20000, default='',null=True,blank=True)
    f1=models.CharField(max_length=100,default='')
    f2=models.CharField(max_length=100,default='')
    f3=models.CharField(max_length=100,default='')
    f4=models.CharField(max_length=100,default='')
    f5=models.CharField(max_length=100,default='')
    image=models.ImageField(upload_to='uploads/products/',default='')
    image1=models.ImageField(upload_to='uploads/products/',default='')
    image2=models.ImageField(upload_to='uploads/products/',default='')
    image3=models.ImageField(upload_to='uploads/products/',default='')
    quantity = models.IntegerField(default=100)  # Adding quantity attribute
    
    def similar_products(self):
     return Product.objects.filter(name__icontains=self.name).exclude(id=self.id)


    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in =ids)

    @staticmethod
    def get_all_product():
        return Product.objects.all()

    @staticmethod
    def get_all_products_id(brand_id):
        if brand_id :
         return Product.objects.filter(brand = brand_id)
        else:
            return Product.get_all_products();


class Customer(models.Model):
     username=models.CharField(max_length=50)
     number=models.CharField(max_length=10)
     email=models.CharField(max_length=50,unique=True)
     password=models.CharField(max_length=6)
     rpassword=models.CharField(max_length=6)

     def register(self):
          self.save()

     def isExit(self):
        return Customer.objects.filter(email=self.email)
      
     def _str_(self):
          self.username

     @staticmethod
     def get_customer_by_email(email):
         try:
             return Customer.objects.get(email=email)
         except:
             return False
 
 
     def isExists(self):
         if Customer.objects.filter(email = self.email):
            return True

         return  False

class Order(models.Model):
    price = models.IntegerField(default=1)
   
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=50, default='', blank=True)
    
    address = models.CharField(max_length=50, default='', blank=True)
    phone = models.CharField(max_length=50, default='', blank=True)
    oquantity = models.IntegerField(default=1)
   
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def placeOrder(self):
        self.save() 
    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer=customer_id).order_by('-date') 
