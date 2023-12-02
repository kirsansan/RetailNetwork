from django.db import transaction
from rest_framework import serializers
from base.models import NetworkNode, Counterparty, Product
from base.validators import node_create_validator, debt_api_create_validator, debt_api_update_validator


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
        exclude = ['contacts']
        validators = [node_create_validator, debt_api_create_validator]

    def create(self, validated_data):
        new_contact_data = validated_data.pop('contacts')
        product_data = validated_data.pop('products')
        validated_data.pop('debt')

        with transaction.atomic():  # many tables will be saved in one moment
            if new_contact_data:  # WE HAVE TO use check_same_contact validator before
                new_contact = Counterparty.objects.create(**new_contact_data)
                validated_data['contacts'] = new_contact
            new_node = NetworkNode.objects.create(debt=0.0, **validated_data)
            for product_info in product_data:
                new_node.products.add(product_info)  # add products in ManyToMany
        return new_node


class NetworkNodeCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkNode
        fields = '__all__'
        validators = [node_create_validator, debt_api_create_validator]


class NetworkNodeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkNode
        exclude = ['debt']
        validators = [node_create_validator, debt_api_update_validator]
