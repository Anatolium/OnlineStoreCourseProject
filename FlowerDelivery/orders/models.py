from django.db import models
from shop.models import Product


class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Оформлен'),
        ('accepted', 'Принят к работе'),
        ('processing', 'Находится в работе'),
        ('shipped', 'В доставке'),
        ('completed', 'Выполнен'),
        ('cancelled', 'Отменён'),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    # postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    # Поле статуса
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return f"Заказ {self.id} от {self.first_name}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def reorder(self):
        new_order = Order.objects.create(
            user=self.user,
            status='new',
            # total_price=self.total_price,
            address=self.address
        )
        for item in self.orderitem_set.all():
            OrderItem.objects.create(
                order=new_order,
                product=item.product,
                quantity=item.quantity,
                price=item.price
            )
        return new_order


# Объект для хранения товара, количества и суммы, уплаченной за каждый товар
class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10,
                                decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} в заказе {self.order.id}"

    def get_cost(self):
        return self.price * self.quantity
