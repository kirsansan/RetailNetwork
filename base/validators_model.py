from rest_framework.exceptions import ValidationError
from config.config import HIERARCHY_MODE


def validate_complex_case(instance):
    if instance.node_type != 0:
        if instance.factory_link is not None and instance.retail_network_link is not None:
            message = "Don't use both links for Factory and RetailNetwork"
            raise ValidationError({'__all__': [message]})
        # check links and their types
        if instance.factory_link is not None:
            if instance.factory_link.node_type != 0:
                message = "Factory link meaning to non-factory object"
                raise ValidationError({'__all__': [message]})
        if instance.retail_network_link is not None:
            if instance.retail_network_link.node_type != 1:
                message = "RetailNetwork link meaning to non-RetailNetwork object"
                raise ValidationError({'__all__': [message]})
        # Hard checking if HIERARCHY_MODE
        if HIERARCHY_MODE:
            if instance.node_type == 2 \
                    and instance.factory_link is not None:
                message = "IndividualEntrepreneur can work only with RetailNetworks"
                raise ValidationError({'__all__': [message]})
            if instance.node_type == 1 \
                    and instance.retail_network_link is not None:
                message = "RetailNetwork can work only with Factories"
                raise ValidationError({'__all__': [message]})

    else:  # Factory
        if instance.factory_link is not None or instance.retail_network_link is not None:
            message = "Factory mustn't have other links"
            raise ValidationError({'__all__': [message]})
            # raise ValidationError("Factory mustn't have other links")
