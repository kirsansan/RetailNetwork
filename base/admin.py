from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from base.models import NetworkNode, Counterparty, Product
from base.validators import node_create_validator


@admin.action(description="Clear debt")
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

    city.short_description = 'city_'

    # def supplier(self, obj):
    #     """Custom field supplier without creating a href link"""
    #     if obj.retail_network_link is not None:
    #         return obj.retail_network_link
    #     else:
    #         return obj.factory_link
    # supplier.short_description = 'Supplier'

    def supplier_ref(self, obj):
        """custom field for create local supplier href"""
        if obj.supplier_link:
            url = (reverse("admin:base_networknode_change", args=(obj.supplier_link.pk,)))
            return format_html('<a href="{}">{}</a>', url, obj.supplier_link)
        else:
            if obj.node_type == 0:  # factory
                return "Factories have no links"

    supplier_ref.short_description = 'Supplier Reference'

    def save_form(self, request, form, change):
        """ Validate the form before saving """
        validators = [node_create_validator]
        for validator in validators:
            validator(form.cleaned_data)
        return form.save(commit=False)
