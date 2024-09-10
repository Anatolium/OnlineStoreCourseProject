from decimal import Decimal
from django.conf import settings
from FlowerDelivery.shop.models import Product


class Cart:
    def __init__(self, request):
        """
        Инициализируем корзину
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Сохраняем пустую корзину в текущем сеансе
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        """
        Прокручиваем товарные позиции корзины в цикле и получаем товары из БД
        """
        product_ids = self.cart.keys()
        # Получаем объекты Product и добавляем их в корзину
        products = Product.objects.filter(id__in=product_ids)
        #  Копируем текущую корзину в переменную cart
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Определяем общее число товаров в корзине
        """
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product, quantity=1, override_quantity=False):
        """
        Добавляем товар в корзину либо обновляем его количество
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # Отмечаем сеанс как "измененный", сообщая Django, что сеанс необходимо сохранить
        self.session.modified = True

    def remove(self, product):
        """
        Удаляем товар из корзины
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            # Обновляем корзину в текущем сеансе
            self.save()

    def clear(self):
        # Удаляем корзину из сеанса
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
