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
        fields = '__all__'
        # validators = [habit_mass_validator,
        #               HabitActionTimeValidator(field='time_for_action'), ]


class NetworkNodeCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkNode
        fields = '__all__'
        validator = [node_create_validator]
