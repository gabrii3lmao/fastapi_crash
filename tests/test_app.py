from http import HTTPStatus
from fast_zero.schemas import UserPublic


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


def _assert_user_creation_conflict(client, payload, expected_message):
    response = client.post('/users/', json=payload)

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': expected_message}


def test_create_username_conflict_error(client, user):
    _assert_user_creation_conflict(
        client,
        payload={'email': 'random@random.com',
                 'username': user.username, 'password': 'random'},
        expected_message='Username already exists'
    )


def test_create_email_conflict_error(client, user):
    _assert_user_creation_conflict(
        client,
        payload={'email': user.email,
                 'username': 'random_name', 'password': 'secret'},
        expected_message='Email already exists'
    )


def test_read_user(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_user_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')

    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user):
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


def test_update_integrity_error(client, user):
    client.post('/users', json={'username': 'fausto',
                'email': 'fausto@example.com', 'password': 'secret'})

    response_update = client.put(
        f'/users/{user.id}', json={
            'username': 'fausto',
            'email': 'fausto@example.com',
            'password': 'secret'}
    )

    assert response_update.json() == {
        'detail': 'Username or Email already exists'
    }


def test_should_return_an_error_if_user_not_found_in_put(client):
    response = client.put('/users/999', json={
        'username': 'Douglas',
        'email': 'douglas@email.com',
        'password': 'secret',
    },)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client, user):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'success'}


def test_should_return_an_error_if_user_not_found_in_delete(client):
    response = client.delete('/users/999')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
