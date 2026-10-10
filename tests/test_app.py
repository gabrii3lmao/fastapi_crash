from http import HTTPStatus
from fastapi.testclient import TestClient
from tests.conftest import client


def test_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá mundo!'}


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'john',
            'email': 'john@email.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'john',
        'email': 'john@email.com',
        'id': 1,
    }


def test_read_user(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [{
            'username': 'john',
            'email': 'john@email.com',
            'id': 1,
        }]}


def test_update_user(client):
    response = client.put('/users/1', json={
        'username': 'Douglas',
        'email': 'douglas@email.com',
        'password': 'secret',
    },)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'Douglas',
        'email': 'douglas@email.com',
    }


def test_should_return_an_error_if_user_not_found_in_put(client):
    response = client.put('/users/999', json={
        'username': 'Douglas',
        'email': 'douglas@email.com',
        'password': 'secret',
    },)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'success'}

def test_should_return_an_error_if_user_not_found_in_delete(client):
    response = client.delete('/users/999')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
