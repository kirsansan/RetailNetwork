import pytest
from base.models import NetworkNode
from tests.factories import NetworkNodeFactory


@pytest.mark.django_db
def test_create_node_validators(authenticated_user, random_product, random_contact):
    auth_client = authenticated_user.get('client')
    tmp_node = NetworkNodeFactory()

    new_data = {
        "name": "Emirates airlines",
        "node_type": 0,
        "debt": '0',
        "supplier_link": tmp_node.pk,
        "contacts": random_contact.pk,
        "products": [random_product.pk, ]
    }
    new_data.pop("node_type")
    response = auth_client.post('/nodes/create/', new_data, format='json')
    assert response.status_code == 400
    assert str(response.data) == "{'node_type': " \
                                 "[ErrorDetail(string='Обязательное поле.', " \
                                 "code='required')]}"

    new_data["node_type"] = 0
    response = auth_client.post('/nodes/create/', new_data, format='json')
    assert response.status_code == 400
    assert str(response.data) == "{'non_field_errors': " \
                                 "[ErrorDetail(string='Factory cannot have reference', " \
                                 "code='invalid')]}"

    new_data["node_type"] = 1
    new_data["supplier_link"] = None
    response = auth_client.post('/nodes/create/', new_data, format='json')
    assert response.status_code == 400
    assert str(response.data) == "{'non_field_errors': " \
                                 "[ErrorDetail(string='Non Factory object must have a reference', " \
                                 "code='invalid')]}"

    type3_node: NetworkNode = NetworkNodeFactory()
    type3_node.node_type = 2
    type3_node.save()
    new_data["supplier_link"] = type3_node.pk
    response = auth_client.post('/nodes/create/', new_data, format='json')
    assert response.status_code == 400
    assert str(response.data) == "{'non_field_errors': " \
                                 "[ErrorDetail(string='You cannot reference a node with " \
                                 "a higher hierarchy level', " \
                                 "code='invalid')]}"


@pytest.mark.django_db
def test_create_node_debt_validators(authenticated_user, random_product, random_contact):
    auth_client = authenticated_user.get('client')
    tmp_node: NetworkNode = NetworkNodeFactory()

    new_data = {
        "name": "Emirates airlines",
        "node_type": 1,
        "supplier_link": tmp_node.pk,
        "contacts": random_contact.pk,
        "products": [random_product.pk, ]
    }
    response = auth_client.post('/nodes/create/', new_data, format='json')
    assert response.status_code == 201

    new_data["debt"] = 0
    response = auth_client.post('/nodes/create/', new_data, format='json')
    assert response.status_code == 201

    new_data["debt"] = 5
    response = auth_client.post('/nodes/create/', new_data, format='json')
    assert response.status_code == 400
    assert str(response.data) == "{'non_field_errors': " \
                                 "[ErrorDetail(string='You must not specify non-zero debt through API', " \
                                 "code='invalid')]}"

    new_data["debt"] = '0.00'
    response = auth_client.post('/nodes/create/', new_data, format='json')
    assert response.status_code == 201

    tmp_node.debt = 5.05
    tmp_node.save()
    new_data["debt"] = '0.00'
    new_data["name"] = "Worcestershire sauce"
    response = auth_client.put(f'/nodes/update/{tmp_node.pk}/', data=new_data, format='json')
    assert response.status_code == 200
    tmp_node.refresh_from_db()
    assert tmp_node.name == "Worcestershire sauce"  # was changed
    assert str(tmp_node.debt) == '5.05'             # was not changed
