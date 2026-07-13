from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Category, Product, CartItem, Order, OrderItem
from django.db import transaction


def product_list(request):
    category_id = request.GET.get('category', '')
    query = request.GET.get('q', '')

    products = Product.objects.all().order_by('-created_at')

    if category_id:
        products = products.filter(category_id=category_id)

    if query:
        products = products.filter(name__icontains=query)

    categories = Category.objects.all()

    context = {
        'products': products,
        'categories': categories,
        'selected_category': category_id,
        'query': query,
    }
    return render(request, 'store/product_list.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})


def _get_user_cart_items(request):
    return CartItem.objects.filter(user=request.user)


@login_required
def cart_detail(request):
    cart_items = _get_user_cart_items(request)
    total_price = sum(item.total_price for item in cart_items)
    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })


@login_required
@require_POST
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': 1},
    )

    if not created:
        item.quantity += 1
        item.save()

    return redirect('cart_detail')


@login_required
@require_POST
def cart_update(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    action = request.POST.get('action')

    if action == 'increment':
        item.quantity += 1
        item.save()
    elif action == 'decrement':
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()
    else:
        quantity = int(request.POST.get('quantity', 1))
        if quantity <= 0:
            item.delete()
        else:
            item.quantity = quantity
            item.save()

    return redirect('cart_detail')


@login_required
@require_POST
def cart_remove(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    return redirect('cart_detail')


@login_required
def checkout(request):
    cart_items = _get_user_cart_items(request)

    if not cart_items.exists():
        return redirect('product_list')

    total_price = sum(item.total_price for item in cart_items)

    if request.method == 'POST':
        user = request.user
        with transaction.atomic():
            order = Order.objects.create(
                user=user,
                first_name=user.first_name or user.username,
                last_name=user.last_name or '',
                email=user.email or f'{user.username}@shopease.com',
                phone='',
                address='N/A',
                city='N/A',
                state='N/A',
                zip_code='N/A',
                total_amount=total_price,
            )

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.product.price,
                    quantity=item.quantity,
                )
                if item.product.stock >= item.quantity:
                    item.product.stock -= item.quantity
                    item.product.save()

            cart_items.delete()

        return render(request, 'store/order_success.html', {
            'order': order,
            'total_price': total_price,
        })

    return render(request, 'store/checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })


def register_view(request):
    if request.user.is_authenticated:
        return redirect('product_list')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_list')
    else:
        form = UserCreationForm()

    return render(request, 'store/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('product_list')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('product_list')
    else:
        form = AuthenticationForm()

    return render(request, 'store/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('product_list')
