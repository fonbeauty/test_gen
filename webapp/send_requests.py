import requests
import uuid
import datetime


def execute_standart_tests(endpoints, methods_list, request_url, security_schemes, body=None):
    if body is None:
        body = {'key': 'value'}

    type_auth = next(iter(security_schemes))
    url = request_url + next(iter(endpoints))
    print(f'Секурити секция {type_auth}')
    auth_type = security_schemes[type_auth].get('type')
    if auth_type == 'oauth2':
        scope = security_schemes.get('oauth')
        print(f'Скоуп {scope}')
        client_id = '3dbb0219-2962-4270-bc4f-33b195eae308'
        client_secret = 'b9fbc8af-875d-43a8-9a1d-f31101a6f62f'
        auth_url = 'https//some_site/oauth'
        # print(f'URL для authorization {url}')
        token = get_token(auth_type, client_id, client_secret, scope, auth_url)
        execute_authorization_tests(url, methods_list[0], token, body)

    elif security_schemes[type_auth].get('type') == 'basic':
        token = '00000000-0000-0000-0000-000000000001'
        print('Тип аутентификации basic')
    elif security_schemes[type_auth].get('type') == 'apiKey':
        token = '00000000-0000-0000-0000-000000000002'
        print('Тип аутентификации apiKey')
    else:
        token = '00000000-0000-0000-0000-000000000003'
        print('Не предусмотренный тип аутентификации')

    for endpoint in endpoints:
        print(f'Endpoints {endpoints[endpoint]} Methods list {methods_list}')
        method405list = list(set(methods_list) ^ set(endpoints[endpoint]))
        url = request_url + endpoint
        token = get_uid('jti')

        send_test_request('Method not allowed', url, method405list[0], token, body)

        send_test_request('Not found', url, methods_list[0], token, body)

        send_test_request('RqUID header is absent', url, methods_list[0], token, body)
        send_test_request('Empty RqUID header', url, methods_list[0], token, body)
        send_test_request('RqUID header less 32 symbols', url, methods_list[0], token, body)
        send_test_request('RqUID header more 32 symbols', url, methods_list[0], token, body)
        send_test_request('RqUID header consist invalid symbol', url, methods_list[0], token, body)


def execute_authorization_tests(url, method, token, body):
    headers = {'RqUID': get_uid('rquid')}
    tests_execute('Authorization header is absent', url, method, headers, body)

    headers = {'Authorization': '', 'RqUID': get_uid('rquid')}
    tests_execute('Empty Authorization header', url, method, headers, body)

    headers = {'Authorization': 'Bearer 77d3073c-5987-4dd0-83f3-e21c0771c029', 'RqUID': get_uid('rquid')}
    tests_execute('In Authorization header other token', url, method, headers, body)

    # send_test_request('Authorization header is absent', url, method, token, body)
    # send_test_request('Empty Authorization header', url, method, token, body)
    # send_test_request('In Authorization header other token', url, method, token, body)


def send_test_request(name, url, method, token, body):
    headers = {'Authorization': 'Bearer ' + token, 'RqUID': get_uid('rquid')}
    if name == 'Method not allowed':
        headers = {'Authorization': 'Bearer ' + token, 'RqUID': get_uid('rquid')}
    elif name == 'Not found':
        result = tests_execute(name, url + 'wrongpath', method, headers, body)
        return result
    elif name == 'RqUID header is absent':
        headers = {'Authorization': 'Bearer ' + token}
    elif name == 'Empty RqUID header':
        headers = {'Authorization': 'Bearer ' + token, 'RqUID': ''}
    elif name == 'RqUID header less 32 symbols':
        headers = {'Authorization': 'Bearer ' + token, 'RqUID': 'd864bd8b912e4c2d9cf11b2ce8f7e31'}
    elif name == 'RqUID header more 32 symbols':
        headers = {'Authorization': 'Bearer ' + token, 'RqUID': 'd864bd8b912e4c2d9cf11b2ce8f7e6c33'}
    elif name == 'RqUID header consist invalid symbol':
        headers = {'Authorization': 'Bearer ' + token, 'RqUID': 'd864bd8b912e4c2d9cf11b2ce8f7e6cz'}
    # elif name == 'Authorization header is absent':
    #     headers = {'RqUID': get_uid('rquid')}
    # elif name == 'Empty Authorization header':
    #     headers = {'Authorization': '', 'RqUID': get_uid('rquid')}
    # elif name == 'In Authorization header other token':
    #     headers = {'Authorization': 'Bearer 77d3073c-5987-4dd0-83f3-e21c0771c029', 'RqUID': get_uid('rquid')}

    result = tests_execute(name, url, method, headers, body)
    return result


def tests_execute(name, url, method, headers, body):
    try:
        if method == 'GET':
            result = requests.get(url, headers=headers)
        elif method == 'POST':
            result = requests.post(url, headers=headers, data=body)
        elif method == 'PUT':
            result = requests.put(url, headers=headers, data=body)
        elif method == 'DELETE':
            result = requests.delete(url, headers=headers)
        elif method == 'PATCH':
            result = requests.patch(url, headers=headers, data=body)
        else:
            print('Запрос с методом ', method, ' не реализован')
            return False
        # result.raise_for_status()
        print_request(name, result)
        return result
    except(requests.RequestException, ValueError) as e:
        print(f'Получена ошибка {e} статус код {result.status_code}')
        return False


def print_request(name, result):
    time = datetime.datetime.now().time()
    print(f'---Test {name} ---')
    print(f'{time}: {result.request.method} {result.request.url}')
    print(f'Headers: {result.request.headers}')
    print(f'Payload: {result.request.body}')
    print(f'---End test {name} ---')


def get_token(auth_type, client_id, client_secret, scope, auth_url):
    print(f'Запрос токена')
    return get_uid('token')


def get_uid(type):
    uid = str(uuid.uuid4())
    if type == 'rquid':
        return uid.replace('-', '')
    else:
        return uid
