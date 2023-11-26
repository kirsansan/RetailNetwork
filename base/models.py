from django.db import models


class Counterparty(models.Model):
    name = models.CharField(max_length=100, verbose_name='name')
    email = models.EmailField(verbose_name='email')
    country = models.CharField(max_length=100, verbose_name='country')
    city = models.CharField(max_length=100, verbose_name='city')
    street = models.CharField(max_length=100, verbose_name='street')
    house_number = models.CharField(max_length=20, verbose_name='house number')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Counterparty'
        verbose_name_plural = 'Counterpartys'
        ordering = ['pk']


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='product name')
    model = models.CharField(max_length=100, verbose_name='product model')
    release_date = models.DateField(verbose_name='product release date')
    supplier = models.ForeignKey(Counterparty, on_delete=models.CASCADE, verbose_name='supplier')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['supplier', 'pk']


class NetworkNode(models.Model):
    NODE_TYPES = (
        ('Factory', 'Factory'),
        ('RetailNetwork', 'Retail Network'),
        ('IndividualEntrepreneur', 'Individual Entrepreneur'),
    )

    name = models.CharField(max_length=100, verbose_name='node name')
    node_type = models.CharField(max_length=22, choices=NODE_TYPES, verbose_name='node type')
    contacts = models.OneToOneField(Counterparty, on_delete=models.CASCADE, verbose_name='contacts', related_name='contacts_link')
    products = models.ManyToManyField(Product, verbose_name='products')
    factory_link = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='factorylink')
    retail_network_link = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    debt = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, verbose_name='debt node-to-node')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'node'
        verbose_name_plural = 'nodes'
        ordering = ['pk']

    # @property
    # def supp(self):
    #     if self.retail_network is not None:
    #         return self.retail_network
    #     else:
    #         return self.supplier
