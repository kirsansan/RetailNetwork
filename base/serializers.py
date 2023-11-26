from django.db import transaction
from rest_framework import serializers

from base.models import NetworkNode, Counterparty, Product
from base.validators import node_create_validator, debt_api_validator


class CounterpartySerializer(serializers.ModelSerializer):
    class Meta:
        model = Counterparty
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class NetworkNodeSerializer(serializers.ModelSerializer):
    contact_set = CounterpartySerializer(source='contacts', many=False, allow_null=False)

    class Meta:
        model = NetworkNode
        # fields = '__all__'
        exclude = ['contacts']
        validators = [node_create_validator, debt_api_validator]
        # validators = [habit_mass_validator,
        #               HabitActionTimeValidator(field='time_for_action'), ]

    def create(self, validated_data):
        debt = validated_data.pop('debt')
        contact_data = validated_data.pop('contacts')
        product_data = validated_data.pop('products')

        with transaction.atomic():  # many tables will be saved in one moment
            if contact_data:
                new_contact = Counterparty.objects.create(**contact_data)
                validated_data['contacts'] = new_contact

            new_node = NetworkNode.objects.create(debt=0.0, **validated_data)

            for product_info in product_data:
                # product = Product.objects.create(**product_info)
                new_node.products.add(product_info)  # add products in ManyToMany
        return new_node

class NetworkNodeCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkNode
        fields = '__all__'
        validators = [node_create_validator, debt_api_validator]
