from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from base.models import NetworkNode, Counterparty, Product


@admin.action(description="Clear debt summ")
def clear_summ(modeladmin, request, queryset):
    """Admin action, which allows you to reset node debt to 0"""
    queryset.update(debt=0)


@admin.register(Counterparty)
class CounterpartyListAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'email', 'country',
                    'city', 'street', 'house_number',)
    # readonly_fields = ('pk', 'name', 'email', 'country', 'city', 'street', 'house_number',)
    list_filter = ('name',)


@admin.register(Product)
class ProductsListAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'model', 'release_date',)


list_filter = ('name',)


@admin.register(NetworkNode)
class NodesListAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'node_type', 'contacts',
                    'supplier_ref', 'debt', 'city')
    list_filter = ('name', 'node_type', 'contacts__city')
    actions = [clear_summ]

    def city(self, obj):
        if obj.contacts:
            return obj.contacts.city
        return None

    city.short_description = 'city'

    # Custom field
    # def supplier(self, obj):
    #     """custom field for find local supplier"""
    #     if obj.retail_network_link is not None:
    #         return obj.retail_network_link
    #     else:
    #         return obj.factory_link
    # supplier.short_description = 'Supplier'

    @staticmethod
    def supplier_ref(obj):
        """custom field for create local supplier href"""
        if obj.supplier_link:
            # return u'<a href="{0}">{1}</a>'.format(reverse('admin:base_Counterparty_change', args=(obj.contacts.pk,)), obj.contacts)
            url = (reverse("admin:base_networknode_change", args=(obj.supplier_link.pk,)))
            return format_html('<a href="{}">{}</a>', url, obj.supplier_link)
        else:
            if obj.node_type == 0:  # factory
                #     url = (reverse("admin:base_networknode_change", args=(obj.factory_link.pk,)))
                #     return format_html('<a href="{}">{}</a>', url, obj.factory_link)
                # else:
                return "Factories have no links"

    # def deep_hierarchy_supplier(self, obj):
    #     """deep supplier finding"""
    #     if obj.retail_network_link is not None:
    #         return obj.retail_network_link
    #     else:
    #         return obj.factory_link
    #
    #     deep_hierarchy_supplier.short_description = 'Hierarchy Supplier'

#     list_filter = ('creator', 'contacts.city', )

# def time_display(self, obj):
#     return obj.time.strftime("%HH:%M:%S")


# @admin.register(SenderDailyLog)
# class LogAdmin(admin.ModelAdmin):
#     list_display = ('habit_id', 'daily_status')
