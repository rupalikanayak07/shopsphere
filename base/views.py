from django.shortcuts import render,redirect

from .models import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):

    if request.user.is_authenticated:
        cartproducts_count=cartmodel.objects.filter(host=request.user).count()
    else:
        cartproducts_count =False

    #search op if no record are present 
    
    nomatch=False

    # for trending and offer button
    trend= False
    offer=False


    # for search
    if 'q' in request.GET:
        q=request.GET['q']
        data= product.objects.filter(Q(pname__icontains = q)| Q(pdesc__icontains = q) | Q(pcategory__icontains=q))
        if len(data)==0:
            nomatch=True

    # for category
    elif 'cat' in request.GET:
        cat=request.GET['cat']
        data=product.objects.filter(pcategory=cat)


    # for trending

    elif 'trending' in request.GET:
        data=product.objects.filter(trending=True)
        trend=True


    # for offer
    elif 'offer' in request.GET:
        data=product.objects.filter(offer= True)
        offer=True
    
    else:
        data= product.objects.all()

    category=[]
    
    for i in product.objects.all():
        if i.pcategory not in category:
            category+=[i.pcategory]


    return render(request,'home.html',{'data':data,'nomatch':nomatch,'category':category,'cartproducts_count':cartproducts_count,'offer':offer,'trend':trend})

login_required(login_url='login_')
def addtocart(request,pk):

    item= product.objects.get(id=pk)

    try:
        cp=cartmodel.objects.get(pname=item.pname,host=request.user)
        cp.quantity+=1
        cp.totalprice+=item.price
        cp.save()
        return redirect('cart')
    
    except:
        cartmodel.objects.create(
            product=item,
            pname=item.pname,
            price=item.price,
            pcategory=item.pcategory,
            quantity=1,
            totalprice = item.price,
            host=request.user
        )

    return redirect('cart')

login_required(login_url='login_')
def cart(request):
    cartproducts_count=cartmodel.objects.filter(host=request.user).count()
    cartproducts= cartmodel.objects.filter(host=request.user)
    TA=0
    for i in cartproducts:
        TA+=i.totalprice
       

    return render(request,'cart.html',{'cartproducts':cartproducts,'TA':TA,'profile_nav':True,'cartproducts_count':cartproducts_count})

def remove(request,pk): 
    cartproduct= cartmodel.objects.get(id=pk)
    cartproduct.delete()
    return redirect('cart')


def increase(request,pk):
    a= cartmodel.objects.get(id=pk) 
    
    a.quantity+=1
    a.totalprice+=a.price
    a.save()
    return redirect('cart')
   

def decrease(request,pk):
    a= cartmodel.objects.get(id=pk)

    if a.quantity>1:
        a.quantity-=1
        a.totalprice-=a.price
        a.save()
        return redirect('cart')
    else:
        a.delete()
        return redirect('cart')

def details(request):
    return render (request,'details.html')

def orderplaced(request):
    cartproducts = cartmodel.objects.filter(host=request.user)
    total_amount = sum(item.totalprice for item in cartproducts)

    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
       

        
        full_address = f"{address}, {city}, {state} - {pincode}"

        order = Order.objects.create(
            user=request.user,
            name=name,
            phone=phone,
            address=full_address,
            total_amount=total_amount,
            status='Placed'
        )

        #  SAVE ITEMS
        for item in cartproducts:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                pname=item.pname,
                price=item.price,
                quantity=item.quantity,
                totalprice=item.totalprice
            )

        cartproducts.delete()
        return render(request, 'orderplace.html', {'order': order})

    return redirect('checkout')
def orderhistory(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render (request,'orderhistory.html', {
        'orders': orders
    })


def productdetails(request,pk):
    item= product.objects.get(id=pk)
    print(item)
    print(item.pname)

    return render(request,'productdetails.html',{'item':item})
