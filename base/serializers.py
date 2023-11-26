from rest_framework import serializers

from base.models import NetworkNode, Counterparty, Product
from base.validators import node_create_validator


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
        validator = [node_create_validator]
        # validators = [habit_mass_validator,
        #               HabitActionTimeValidator(field='time_for_action'), ]

    def create(self, validated_data):
        debt = validated_data.pop('debt')
        contact_data = validated_data.pop('contacts')
        product_data = validated_data.pop('products')
        if contact_data:
            new_contact = Counterparty.objects.create(**contact_data)
            validated_data['contacts'] = new_contact
        new_node = NetworkNode.objects.create(**validated_data)
        # course.owner =
        if product_data:
             for product in product_data:
                 print(product)
                 Product.objects.create(**product, course_id=course)
        return new_node


class NetworkNodeCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkNode
        fields = '__all__'
        validator = [node_create_validator]
