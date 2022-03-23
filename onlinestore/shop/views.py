from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from . import forms
from django.db.models import Q


@login_required(login_url='/users/sign_in')
def products(request):
    category = request.GET.get('category')
    brand = request.GET.get('brand')
    search = request.GET.get('search')
    product_pk = request.GET.get("product")

    if product_pk:
        product = Product.objects.get(pk=product_pk)
        cart_item = CartItem.objects.filter(product=product)
        if not cart_item:
            cart_item = CartItem.objects.create(customer=request.user, product=product, quantity=1)
            cart_item.save()
            return redirect("shop:products")
        for item in cart_item:
            item.quantity += 1
            item.save()
    products_list = Product.objects.all()
    slides = Slide.objects.all()
    products_list = products_list.filter(category=category) if category else products_list
    products_list = products_list.filter(brand=brand) if brand else products_list
    products_list = products_list.filter(
        Q(title__icontains=search) | Q(description__icontains=search)) if search else products_list

    return render(request, "products.html", {'products': products_list, 'slides': slides})


def cart(request):
    cart_items = CartItem.objects.filter(customer=request.user)
    total_price = sum([item.total_price() for item in cart_items])
    total_quantity = sum([item.quantity for item in cart_items])

    return render(
        request,
        'cart.html',
        {'cart_items': cart_items, 'total_quantity': total_quantity, 'total_price': total_price}
    )


def delete_cart_item(request, pk):
    cart = CartItem.objects.get(pk=pk)
    if request.method == 'POST':
        cart.delete()
        return redirect('shop:cart')
    return render(request, 'delete_cart.html', {'cart': cart})


def edit_cart_item(request, pk):
    cart_item = CartItem.objects.get(pk=pk)
    action = request.GET.get("action")

    if action == 'take' and cart_item.quantity > 0:
        if cart_item.quantity == 1:
            cart_item.delete()
            return redirect('shop:cart')
        cart_item.quantity -= 1
        cart_item.save()
        return redirect("shop:cart")
    cart_item.quantity += 1
    cart_item.save()
    return redirect("shop:cart")


def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'product_detail.html', {'product': product})


def create_order(request):
    cart_items = CartItem.objects.filter(customer=request.user)
    total_price = sum([item.total_price() for item in cart_items])
    amount = sum([item.quantity for item in cart_items])
    form = forms.OrderForm(request.POST)

    if request.method == 'POST' and form.is_valid():
        order = Order.objects.create(
            address=request.POST.get('address'),
            phone=request.POST.get('phone'),
            total_price=total_price,
            customer=request.user
        )
        for cart_item in cart_items:
            OrderProduct.objects.create(
                order=order,
                product=cart_item.product,
                amount=cart_item.quantity,
                total=cart_item.total_price()
            )
        cart_items.delete()
        return redirect('shop:orders')

    form = forms.OrderForm()
    return render(request, 'order_creation_page.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'amount': amount,
        'form': form
    })


def rate_product(request, pk):
    product = Product.objects.get(pk=pk)
    reviews = Review.objects.filter(product=product)

    if request.method == 'POST':
        form = forms.RateForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = request.user
            rating.product = product
            rating.save()
            return redirect('shop:rate_product', pk=pk)
    form = forms.RateForm()
    return render(request, 'rate.html', {'form': form, 'product': product, 'reviews': reviews})


def orders(request):
    orders_list = Order.objects.filter(customer=request.user)
    return render(request, 'orders.html', {'orders': orders_list})
