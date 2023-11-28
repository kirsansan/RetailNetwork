from rest_framework.exceptions import ValidationError
from config.config import HIERARCHY_MODE


def validate_complex_case(instance):
    if instance.node_type != 0:  # non factory
        # check links and their types
        if instance.supplier_link is not None:
            if instance.supplier_link.node_type > instance.node_type:
                message = "You cannot reference a node with a higher hierarchy level"
                raise ValidationError({'__all__': [message]})
        else:
            message = "You must reference to supplier"
            raise ValidationError({'__all__': [message]})
        # Hard checking if HIERARCHY_MODE
        if HIERARCHY_MODE:
            pass
            # if instance.node_type == 2 \
            #         and instance.factory_link is not None:
            #     message = "IndividualEntrepreneur can work only with RetailNetworks"
            #     raise ValidationError({'__all__': [message]})
            # if instance.node_type == 1 \
            #         and instance.retail_network_link is not None:
            #     message = "RetailNetwork can work only with Factories"
            #     raise ValidationError({'__all__': [message]})

    else:  # Factory
        if instance.supplier_link is not None:
            message = "Factory mustn't have supplier links"
            raise ValidationError({'__all__': [message]})
