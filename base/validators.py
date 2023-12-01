from rest_framework.exceptions import ValidationError
from base.models import NetworkNode


def node_create_validator(value):
    """Validate all fields in a given"""

    ref: NetworkNode = value.get('supplier_link')

    if ref is not None:
        if value.get('node_type') == 0:
            raise ValidationError('Factory cannot have reference')
        else:  # non-factory
            if ref.node_type > value.get('node_type'):
                raise ValidationError('You cannot reference a node with a higher hierarchy level')
    else:
        if value.get('node_type') != 0:
            raise ValidationError('Non Factory object must have a reference')


def debt_api_create_validator(value):
    if value.get('debt') is not None:
        if float(value.get('debt')) != 0.0:
            raise ValidationError('You must not specify non-zero debt through API')


def debt_api_update_validator(value):
    if value.get('debt') is not None:
        raise ValidationError('You must not specify debt through API')

# def check_same_contact(value):
#     same_contact = Counterparty.objects.filter(name=value.get('contacts')['name']).order_by('pk').all()
#     if len(same_contact) > 0:
#         raise ValidationError('Same contact has already exist. You must specify unique contacts')
