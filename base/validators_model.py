from rest_framework.exceptions import ValidationError


def validate_complex_case(instance):
    """Validate fields of Model NetworkNode before saving"""
    if instance.supplier_link is not None:
        if instance.node_type == 0:
            raise ValidationError('Factory cannot have reference')
        else:  # non-factory
            if instance.supplier_link.node_type > instance.node_type:
                raise ValidationError('You cannot reference a node with a higher hierarchy level')
    else:
        if instance.node_type != 0:
            raise ValidationError('Non Factory object must have a reference')
