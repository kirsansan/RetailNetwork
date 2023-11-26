from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from base.models import NetworkNode, Contragent, Product



@admin.action(description="Clear debt summ")
def clear_summ(modeladmin, request, queryset):
    """Admin action, which allows you to reset node debt to 0"""
    queryset.update(debt=0)


@admin.register(Contragent)
class ContrageentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'email', 'country',
                    'city', 'street', 'house_number',)
    list_filter = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'model', 'release_date',)


list_filter = ('name',)


@admin.register(NetworkNode)
class NodesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'node_type', 'contacts',
                    'supp', 'supplier_link', 'debt',)
    list_filter = ('name',)
    actions = [clear_summ]

    #Кастомное поле
    def supp(self, obj):
        if obj.retail_network is not None:
            return obj.retail_network
        else:
            return obj.factory
    supp.short_description = 'Supplier'

    def supplier_link(self, obj):
        if obj.retail_network:
            #return u'<a href="{0}">{1}</a>'.format(reverse('admin:base_contragent_change', args=(obj.contacts.pk,)), obj.contacts)
            url = (reverse("admin:base_contragent_change", args=(obj.retail_network.contacts.pk,)))
            return format_html('<a href="{}">{}</a>', url, obj.retail_network)
        else:
            if obj.factory:
                url = (reverse("admin:base_contragent_change", args=(obj.factory.contacts.pk,)))
                return format_html('<a href="{}">{}</a>', url, obj.factory)
            else:
                return "Factories have no links"

#     list_filter = ('creator', 'contacts.city', )

# def time_display(self, obj):
#     return obj.time.strftime("%HH:%M:%S")


# @admin.register(SenderDailyLog)
# class LogAdmin(admin.ModelAdmin):
#     list_display = ('habit_id', 'daily_status')
