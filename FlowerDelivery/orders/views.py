# from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from .models import OrderItem, Order
from .forms import OrderCreateForm
# from .tasks import order_created
from cart.cart import Cart
from django.contrib.auth.decorators import login_required


# def order_create(request):
#     cart = Cart(request)
#     if request.method == 'POST':
#         # Запрос POST
#         form = OrderCreateForm(request.POST)
#         if form.is_valid():
#             order = form.save()
#             for item in cart:
#                 OrderItem.objects.create(order=order,
#                                          product=item['product'],
#                                          price=item['price'],
#                                          quantity=item['quantity'])
#             # Очищаем корзину
#             cart.clear()
#             # launch asynchronous task
#             # order_created.delay(order.id)
#             return render(request,
#                           'orders/order/created.html',
#                           {'order': order})
#     else:
#         # Запрос GET
#         form = OrderCreateForm()
#     return render(request,
#                   'orders/order/create.html',
#                   {'cart': cart, 'form': form})

@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()
            return render(request, 'orders/order/created.html',
                          {'order': order})
    else:
        # Предзаполняем форму данными пользователя
        initial_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'address': request.user.profile.address,
        }
        form = OrderCreateForm(initial=initial_data)
    return render(request, 'orders/order/create.html',
                  {'cart': cart, 'form': form})


# Декоратор проверяет, что значения полей is_active и is_staff запрашивающего страницу юзера установлены True
@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html', {'order': order})


# @login_required
# def order_history(request):
#     orders = Order.objects.filter(email=request.user.email).order_by('-created')
#     return render(request, 'orders/order/order_history.html', {'orders': orders})


@login_required
def order_history(request):
    # Получаем все заказы без фильтрации
    all_orders = Order.objects.all().order_by('-created')

    # Выводим отладочную информацию
    # print(f"Всего заказов: {all_orders.count()}")
    # print(f"Email пользователя: {request.user.email}")

    # Фильтруем заказы по email пользователя
    user_orders = all_orders.filter(email=request.user.email)
    # print(f"Заказов пользователя: {user_orders.count()}")
    return render(request, 'orders/order/order_history.html', {'orders': user_orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order/order_detail.html', {'order': order})


@login_required
def reorder(request, order_id):
    old_order = get_object_or_404(Order, id=order_id)
    cart = Cart(request)

    # Добавляем товары из старого заказа в корзину
    for item in old_order.items.all():
        cart.add(product=item.product, quantity=item.quantity)

    # Перенаправляем пользователя на страницу корзины
    return redirect('cart:cart_detail')
