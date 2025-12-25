from django.shortcuts import render,get_object_or_404,redirect,HttpResponseRedirect
from .models import Product,Brand,Customer,Order
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.views import View
from django.views.generic import TemplateView, DetailView
from django.contrib import messages
from django.template.loader import get_template
from xhtml2pdf import pisa




def index(request,brandi=None):
    products = None
    brands = Brand.objects.all()
    brandi = request.GET.get('brand')
    if brandi:
        products=Product.get_all_products_id(brandi)
    else:
        products=Product.get_all_product();
   
   
    if request.method=='POST':
        postData = request.POST
        
        email = postData.get('email')
       
        product = request.POST.get('product')
        print("cart:",product)
        print("cart:",email)
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product]  = quantity-1
                else:
                    cart[product]  = quantity+1

            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print('cart' , request.session['cart'])
        print(email)
     #   print('you are :',request.session.get('email'))
   

        return redirect('cart')
    
    data={}
    data['products']=products
    data['brands']=brands 
   # print('you are :',request.session.get('username'))
   # print('you are :',request.session.get('email'))
   
    if request.user.is_authenticated:
        username = request.user.username
        messages.info(request, f"Welcome, {username}!")
 
    return render(request, 'index.html', data,)

def index_view(request):
    
    customer_email = request.session.get('customer_email')
    return render(request, 'index.html', {'customer_email': customer_email})


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'product_detail.html', {'product': product})

def search(request):
    query = request.GET.get('q')
    results = []
    similar_results = []
    if query:
        results = Product.objects.filter(name__icontains=query)
        # Get the first product matching the query to find similar products
        if results:
            similar_results = results[0].similar_products()
    return render(request, 'search.html', {'results': results, 'query': query, 'similar_results': similar_results})


def signup(request):
    if request.method=='GET':
        return render(request,'signup.html')
    else:
        postd = request.POST
        username=postd.get('username')
        number=postd.get('number')
        email=postd.get('email')
        password=postd.get('password')
        rpassword=postd.get('rpassword')

        #vaildation


        value={
            'username':username,
            'number':number,
            'email':email,
            'password':password,
            'rpassword':rpassword
        }
        error_mess =None
        

        if(not username):
            error_mess="Username Required !!"
        elif len(username)>10:
            error_mess="Username is very long !!"
        
        if(not number):
            error_mess="number Required !!"
        elif len(number)>10:
            error_mess=" Phone number must be 10 char long !!"
        
        if(not email):
            error_mess="email Required !!"
        
        if(not password)>6:
            error_mess="password must be 6 char long  !!"

        if password == rpassword:
            True
        else :
            error_mess="password and confirm Password does not match!!"
        
       
        if Customer.objects.filter(email=email).exists():
            error_mess="Email Already Exists."
        
        if Customer.objects.filter(username=username).exists():
            error_mess="username Already Exists."
        
       
         #SAVING
    if not error_mess:       
        print(username,number,email,password)
        customer=Customer(
            username=username,
            number=number,
            email=email,
            password=password,
            rpassword=rpassword
          )
        
        customer.password=make_password(customer.password)

        customer.register()
        return redirect('index')
    
    else: 
        data1={
            'error' :error_mess ,
            'values': value
        }
       
        return render(request,'signup.html',data1)

class Login(View):
    return_url = None
    def get(self , request):
        Login.return_url = request.GET.get('return_url')
        return render(request , 'login.html')

    def post(self , request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id

                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                   
                    return redirect('index')
            else:
                error_message = 'Email or Password invalid !!'
        else:
            error_message = 'Email or Password invalid !!'

        print(email, password)
        return render(request, 'login.html', {'error': error_message})
 

def logout(request):
    request.session.clear()
    messages.success(request, 'You have successfully logged out.')
    
    return redirect('login')

class CheckOut(View):
    def post(self, request):
        name = request.POST.get('name')
       
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Product.get_products_by_id(list(cart.keys()))
        print(name,address, phone, customer, cart, products)

        for product in products:
            print(cart.get(str(product.id)))
            order = Order(customer=Customer(id=customer),
                          name=name,
                          product=product,
                          price=product.price,
                          address=address,
                          phone=phone,
                          oquantity=cart.get(str(product.id)))
            order.save()
        request.session['cart'] = {}

        return redirect('cart')

class OrderView(View):
    def get(self , request ):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)
        print(orders)
        return render(request , 'order.html'  , {'orders' : orders})


class Cart(View):
    #def get(self , request):
    #    ids = list(request.session.get('cart').keys())
    #    if ids:
    #        products = Product.get_products_by_id(ids)
    #        print(products)
    #        return render(request , 'cart.html' , {'products' : products} )
    #    
    #    else:
    #         
    #         return render(request, 'cart_empty.html')

    def get(self , request):

        cart=request.session.get('cart')
        if cart:
            ids = list(cart.keys())
            
            products = Product.get_products_by_id(ids)
            print(products)
            return render(request , 'cart.html' , {'products' : products} )
            return redirect('order_con')
           
        else:
            return render(request, 'cart_empty.html')


def generate_bill_pdf(request, order_id):
    order = Order.objects.get(id=order_id)
    template_path = 'bill_template.html'
    context = {'order': order}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=bill_{order.id}.pdf'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

    

def notification_view(request):

    customer_email = request.session.get('customer_email')
    return render(request, 'notification.html', {'customer_email': customer_email})


def order_con(request):
    return render(request,'order_confirmation.html')