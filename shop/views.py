from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Cart, CartItem
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

# def add_to_cart(request):
#     product_id = str(request.POST['id'])
#     product_quantity = int(request.POST['quant'])
#     product_title = request.POST['title']
#     product_price = request.POST['price']

#     # fetech the item from DB

#     # cart status complete -> get the current cart

#     # Cart table
#     # cart id, user id, status [in progress, compete]

#     # cart items table
#     # cart, product id, product qty

#     # return - cart id

#     cart_product = {
#         product_id: {
#             'title': product_title,
#             'quant': product_quantity,
#             'price' : product_price
#         }
#     }

#     if 'cart_data_obj' in request.session:
#         cart_data = request.session['cart_data_obj']

#         if product_id in cart_data:
#             cart_data[product_id]['quant'] += product_quantity
#         else:
#             cart_data.update(cart_product)

#         request.session['cart_data_obj'] = cart_data
#     else:
#         request.session['cart_data_obj'] = cart_product

#     return JsonResponse({"data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj'])})

from django.shortcuts import get_object_or_404
from .models import Product, Cart, CartItem

def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('id')  # This is the pid
        product_quantity = int(request.POST.get('quant'))
        product_title = request.POST.get('title')

        # Fetch the product using the pid
        product = get_object_or_404(Product, pid=product_id)

        # Create or get the user's cart
        cart, created = Cart.objects.get_or_create(user=request.user, status='in_progress')

        # Check if the product already exists in the user's cart
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

        if item_created:
            cart_item.quantity = product_quantity
            cart_item.price = product.price  # Set the price when creating a new item
        else:
            cart_item.quantity += product_quantity  # Update quantity for existing item
            cart_item.price = product.price  # Ensure the price is set, can adjust if needed

        cart_item.save()  # Save the cart item

        total_items = CartItem.objects.filter(cart=cart).count()  # Get total item count

        return JsonResponse({'status': 'success', 'totalcartitems': total_items})

    return JsonResponse({'status': 'error'}, status=400)

<<<<<<< HEAD
# def cart(request):
#     cart_total_amount = 0

#     if 'cart_data_obj' in request.session:
#         for p_id, item in request.session['cart_data_obj'].items():
            
#     return render(request, 'cart.html')
=======
def cart(request):
    cart = Cart.objects.get(user=request.user, status='in_progress')
    return render(request, 'cart.html', {'cart': cart})
>>>>>>> e0c5fe100126254891168e73a1553bfccd46ad30
