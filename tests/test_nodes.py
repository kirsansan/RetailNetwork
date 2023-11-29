import json
from json import loads, dumps

import pytest

from base.serializers import CounterpartySerializer, ProductSerializer
from config.config import MAX_NODE_PER_PAGE
from base.models import NetworkNode
from tests.factories import NetworkNodeFactory
from users.models import User


@pytest.mark.django_db
def test_get_nodes_list(authenticated_user):
    auth_client = authenticated_user.get('client')
    # NetworkNodeFactory.create()
    [NetworkNodeFactory.create_batch(MAX_NODE_PER_PAGE) for _ in range(0, 7)]
    response = auth_client.get('/nodes/all/')
    assert response.status_code == 200
    assert len(response.data['results']) == MAX_NODE_PER_PAGE


@pytest.mark.django_db
def test_get_nodes_list_diff_users(authenticated_user, non_active_user):
    auth_client = authenticated_user.get('client')
    non_active_client = non_active_user.get('client')
    nodes = NetworkNodeFactory.create_batch(2)  # two default

    # we will see 2 objects  - both nodes for active
    response = auth_client.get('/nodes/all/')
    assert response.status_code == 200
    assert len(response.data['results']) == 2

    # we will not be able to see anything - all nodes are not public
    response = non_active_client.get('/nodes/all/')
    assert response.status_code == 403
    # assert len(response.data['results']) == 2


@pytest.mark.django_db
def test_get_node_detail(authenticated_user):
    auth_client = authenticated_user.get('client')
    nodes: list[NetworkNode] = NetworkNodeFactory.create_batch(2)  # two default
    node = nodes[0]
    serializer_obj = CounterpartySerializer()
    contact = serializer_obj.to_representation(node.contacts)

    # make new response
    response = auth_client.get(f'/nodes/detail/{node.pk}/')
    expected_response_wo_contact = {
        "id": node.pk,
        "name": node.name,
        "node_type": node.node_type,
        "debt": '0.00',
        "supplier_link": node.supplier_link,
        "products": []
    }
    assert response.status_code == 200
    resp_contact = response.data.pop('contact_set')

    assert response.data == expected_response_wo_contact
    assert resp_contact == contact


@pytest.mark.django_db
def test_create_node(authenticated_user, random_product, random_contact):
    auth_client = authenticated_user.get('client')
    tmp_node = NetworkNodeFactory()
    # cont_serializer_obj = CounterpartySerializer()
    # prod_serializer_obj = ProductSerializer()
    # contact = cont_serializer_obj.to_representation(random_contact)
    # product = prod_serializer_obj.to_representation(random_product)

    new_data = {
        "name": "Emirates airlines",
        "node_type": 1,
        "debt": '0',
        "supplier_link": tmp_node.pk,
        "contacts": random_contact.pk,
        "products": [random_product.pk, ]
    }
    response = auth_client.post('/nodes/create/', new_data, format='json')
    assert response.status_code == 201
    response.data.pop('id')
    expected_response_wo_products = {
        "name": "Emirates airlines",
        "node_type": 1,
        "debt": '0.00',
        "supplier_link": tmp_node.pk,
        "contacts": random_contact.pk,
    }
    # resp_contact = response.data.pop('contacts')
    resp_prod = response.data.pop('products')
    # print("RP=", resp_prod)
    # print("P=", product)

    assert response.data == expected_response_wo_products
    assert resp_prod == [random_product.pk]


@pytest.mark.django_db
def test_create_plus_node(authenticated_user, random_product, random_contact):
    auth_client = authenticated_user.get('client')
    tmp_node = NetworkNodeFactory()
    # cont_serializer_obj = CounterpartySerializer()
    # prod_serializer_obj = ProductSerializer()
    # contact = cont_serializer_obj.to_representation(random_contact)
    # product = prod_serializer_obj.to_representation(random_product)

    new_data = {
        "name": "Emirates airlines",
        "node_type": 1,
        "debt": '0.00',
        "supplier_link": tmp_node.pk,
        "products": [random_product.pk, ],
        "contact_set": {
                    "name": "Airbus office",
                    "email": "office@airbus.com",
                    "country": "Netherlands",
                    "city": "Linden",
                    "street": "3th Builders street",
                    "house_number": "22"
                    }
    }
    response = auth_client.post('/nodes/create_plus/', new_data, format='json')
    assert response.status_code == 201
    response.data.pop('id')
    resp_contact = response.data.pop('contact_set')
    resp_prod = response.data.pop('products')

    expected_response_wo_contact_products = {
        "name": "Emirates airlines",
        "node_type": 1,
        "debt": '0.00',
        "supplier_link": tmp_node.pk,
    }

    print("RC=", resp_contact)
    # print("P=", product)

    assert response.data == expected_response_wo_contact_products
    assert resp_prod == [random_product.pk]



@pytest.mark.django_db
def test_update_node(authenticated_user, random_product):
    auth_client = authenticated_user.get('client')
    node: NetworkNode = NetworkNodeFactory()

    response = auth_client.get(f'/nodes/detail/{node.pk}/')
    assert response.status_code == 200
    new_data = {
        "name": "NEWstring",
        "node_type": node.node_type,
        "debt": node.debt,
        "contacts": node.contacts.pk,
        "supplier_link": node.supplier_link,
        "products": [random_product.pk]
    }
    response = auth_client.put(f'/nodes/update/{node.pk}/', data=new_data, format='json')
    assert response.status_code == 200
    node.refresh_from_db()
    assert node.name == 'NEWstring'


@pytest.mark.django_db
def test_delete_node(authenticated_user):
    auth_client = authenticated_user.get('client')
    node = NetworkNodeFactory()

    response = auth_client.get(f'/nodes/detail/{node.pk}/')
    assert response.status_code == 200
    response = auth_client.delete(f'/nodes/delete/{node.pk}/')
    assert response.status_code == 204

    # Check that the node was deleted from the database
    with pytest.raises(NetworkNode.DoesNotExist):
        node.refresh_from_db()
