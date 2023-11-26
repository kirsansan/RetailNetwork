from datetime import time

from rest_framework.exceptions import ValidationError

from base.models import NetworkNode


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
    print('validaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaator')
    if value.get('node_type') is None:
        raise ValidationError('You must specify node_type')
    if value.get('factory_link') and value.get('retail_network_link'):  # both exist
        raise ValidationError('You must specify only one mention - factory_link or retail_network_link')
    # if value.get('factory_link') and value.get('retail_network_link'):  # both exist
    #     raise ValidationError('You must specify only one mention - factory_link or retail_network_link')

    if value.get('factory_link'):
        temp_obj = NetworkNode.objects.get(pk=value.get('factory_link'))
        if temp_obj.node_type != 'Factory':
            raise ValidationError('Factory field mention to the non-factory object')
    if value.get('retail_network_link'):
        temp_obj = NetworkNode.objects.get(pk=value.get('retail_network_link'))
        if temp_obj.node_type != 'retail_network_link':
            raise ValidationError('retail_network_link field mention to the non-retail_network object')
