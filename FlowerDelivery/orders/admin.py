from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Order, OrderItem
import csv
import datetime
from django.http import HttpResponse


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    content_disposition = f'attachment; filename={opts.verbose_name}.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition
    writer = csv.writer(response)
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    # Записываем первую строку с информацией заголовка
    writer.writerow([field.verbose_name for field in fields])
    # Записываем строки данных
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response


export_to_csv.short_description = 'Сохранить заказ в CSV'


def order_detail(obj):
    url = reverse('orders:admin_order_detail', args=[obj.id])
    return mark_safe(f'<a href="{url}">View</a>')


def make_status_new(modeladmin, request, queryset):
    queryset.update(status='new')


make_status_new.short_description = "Отметить как 'Оформлен'"


def make_status_accepted(modeladmin, request, queryset):
    queryset.update(status='accepted')


make_status_accepted.short_description = "Отметить как 'Принят к работе'"


def make_status_processing(modeladmin, request, queryset):
    queryset.update(status='processing')


make_status_processing.short_description = "Отметить как 'Находится в работе'"


def make_status_shipped(modeladmin, request, queryset):
    queryset.update(status='shipped')


make_status_shipped.short_description = "Отметить как 'В доставке'"


def make_status_completed(modeladmin, request, queryset):
    queryset.update(status='completed')


make_status_completed.short_description = "Отметить как 'Выполнен'"


def make_status_cancelled(modeladmin, request, queryset):
    queryset.update(status='cancelled')


make_status_cancelled.short_description = "Отметить как 'Отменён'"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # list_display = ['id', 'first_name', 'last_name', 'email',
    #                 'address', 'postal_code', 'city', 'paid',
    #                 'created', 'updated']
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'address', 'city', 'paid',
                    'created', 'status', order_detail]

    # list_filter = ['paid', 'created', 'updated']
    list_filter = ['paid', 'created', 'status']

    inlines = [OrderItemInline]
    # actions = [export_to_csv]
    actions = [export_to_csv, make_status_new, make_status_processing, make_status_accepted,
               make_status_shipped, make_status_completed, make_status_cancelled]
