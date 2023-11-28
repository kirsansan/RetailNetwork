from datetime import time

from rest_framework.exceptions import ValidationError

from base.models import NetworkNode, Counterparty


# class HabitActionTimeValidator:
#     """validate time for action (less 2 minutes)"""
#
#     def __init__(self, field):
#         self.field = field
#
#     def __call__(self, obj):
#         """Validate time_for_action field in a given """
#         if dict(obj).get(self.field):
#             if dict(obj).get(self.field) > time(00, 2):
#                 raise ValidationError('time_for_action must be less 2 minutes ')
#
#
# def habit_mass_validator(value):
#     """Validate all fields in a given (w/o time_for_action)"""
#     # print(value)
#     if value.get('associated_habit') and value.get('reward'):  # both exist
#         raise ValidationError('You must specify associated habit or reward. Not both at the same time')
#     if value.get('associated_habit'):
#         if not value.get('associated_habit').is_useful:  # associated is useless
#             raise ValidationError('Associated habit must have is_useful flag as True')
#     if value.get('is_useful') or 'is_useful' not in value:  # useful of default
#         if value.get('reward'):
#             raise ValidationError('Useful habit must not have reward')
#         if value.get('associated_habit'):
#             raise ValidationError('Useful habit must not have associated habit')
#     if value.get('frequency'):  # exist
#         if value.get('frequency') > 7:
#             raise ValidationError('frequency of habit must be less 7 days')

def node_create_validator(value):
    """Validate all fields in a given"""
    if value.get('node_type') is None:
        raise ValidationError('You must specify node_type')


    ref:int = value.get('supplier_link')

    if value.get('node_type') == 0 and ref is not None:
        raise ValidationError("Factory can't have reference")

    if ref > 0:  # non-factory
        temp_obj = NetworkNode.objects.get(pk=ref)
        if temp_obj.node_type > value.get('node_type'):
            raise ValidationError('You cannot reference a node with a higher hierarchy level')



def debt_api_validator(value):
    if value.get('debt') is None or value.get('debt') != 0.0:
        raise ValidationError("You mustn't specify non-zero debt through API")


def check_same_contact(value):
    same_contact = Counterparty.objects.filter(name=value.get('contacts')['name']).order_by('pk').all()
    if len(same_contact) > 0:
        raise ValidationError('Same contact has already exist. You must specify unique contacts')


