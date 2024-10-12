from django.shortcuts import render
from django.http import JsonResponse
from tomatoes.models import Product, ProductReview

# Create your views heree.
def checkout(request):
    return render(request, 'checkout.html')

def shop_detail(request):
    product = Product.objects.all()

    context = {
        "products" : product,
    }

    return render(request,'shop-detail.html', context)

def product_detail(request, pid):
    product = Product.objects.get(pid=pid)

    p_image = product.p_image.all()
    context = {
        "p" : product,
        "p_image" : p_image
    }

    return render(request, "product-detail.html", context)

def add_to_cart(request):
    product_id = str(request.GET['id'])
    product_quantity = int(request.GET['quant'])
    product_title = request.GET['title']
    product_price = request.GET['price']

    cart_product = {
        product_id: {
            'title': product_title,
            'quant': product_quantity,
            'price': product_price
        }
    }

    if 'cart_data_obj' in request.session:
        cart_data = request.session['cart_data_obj']

        if product_id in cart_data:
            cart_data[product_id]['quant'] += product_quantity
        else:
            cart_data.update(cart_product)

        request.session['cart_data_obj'] = cart_data
    else:
        request.session['cart_data_obj'] = cart_product

    return JsonResponse({"data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj'])})

# def cart(request):
#     cart_total_amount = 0

#     if 'cart_data_obj' in request.session:
#         for p_id, item in request.session['cart_data_obj'].items():
            
#     return render(request, 'cart.html')