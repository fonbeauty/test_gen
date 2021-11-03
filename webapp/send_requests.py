import requests
import uuid
import datetime


def standart_tests(endpoints, methods_list, request_url, body={'key': 'value'}):
    for endpoint in endpoints:
        print(f'Endpoints {endpoints[endpoint]} Methods_list {methods_list}')
        method405list = list(set(methods_list) ^ set(endpoints[endpoint]))
        method = method405list[0]
        print(f'XOR LISTS {method}')
        url = request_url + endpoint
        jti = get_uid('jti')
        headers = {'Authorization': 'Bearer ' + jti, 'RqUID': get_uid('rquid')}
        tests_execute(url, method, headers, body)

        method = methods_list[0]
        headers = {'Authorization': 'Bearer ' + jti}
        tests_execute(url, method, headers, body)
        headers = {'Authorization': 'Bearer ' + jti, 'RqUID': ''}
        tests_execute(url, method, headers, body)
        headers = {'Authorization': 'Bearer ' + jti, 'RqUID': 'd864bd8b912e4c2d9cf11b2ce8f7e31'}
        tests_execute(url, method, headers, body)
        headers = {'Authorization': 'Bearer ' + jti, 'RqUID': 'd864bd8b912e4c2d9cf11b2ce8f7e6c33'}
        tests_execute(url, method, headers, body)
        headers = {'Authorization': 'Bearer ' + jti, 'RqUID': 'd864bd8b912e4c2d9cf11b2ce8f7e6cz'}
        tests_execute(url, method, headers, body)

        headers = {'RqUID': get_uid('rquid')}
        tests_execute(url, method, headers, body)
        headers = {'Authorization': '', 'RqUID': get_uid('rquid')}
        tests_execute(url, method, headers, body)
        headers = {'Authorization': 'Bearer 77d3073c-5987-4dd0-83f3-e21c0771c029', 'RqUID': get_uid('rquid')}
        tests_execute(url, method, headers, body)


def tests_execute(url, method, headers, body):
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
        print_request(result)
        return result
    except(requests.RequestException, ValueError) as e:
        print(f'Получена ошибка {e} статус код {result.status_code}')
        return False


def print_request(result):
    time = datetime.datetime.now().time()
    print('---Request---')
    print(f'{time}: {result.request.method} {result.request.url}')
    print(f'Headers: {result.request.headers}')
    print(f'Payload: {result.request.body}')
    print('---END---')


def get_uid(type):
    uid = str(uuid.uuid4())
    if type == 'rquid':
        return uid.replace('-', '')
    else:
        return uid
