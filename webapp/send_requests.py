import requests
import uuid
import datetime

def standart_tests(endpoints, methods_list, request_url, body={'key': 'value'}):
    for endpoint in endpoints:
        print(f'Endpoints {endpoints[endpoint]} Methods_list {methods_list}')
        method405list = list(set(methods_list) ^ set(endpoints[endpoint]))
        # method405list.reverse()
        method405 = method405list[0]
        print(f'XOR LISTS {method405}')
        url = request_url + endpoint

        headers = {'Authorization': 'Bearer ' + get_uid('jti'), 'RqUID': get_uid('rquid')}

        try:
            if method405 == 'GET':
                result = requests.get(url, headers=headers)
            elif method405 == 'POST':
                result = requests.post(url, headers=headers, data=body)
            elif method405 == 'PUT':
                result = requests.put(url, headers=headers, data=body)
            elif method405 == 'DELETE':
                result = requests.delete(url, headers=headers)
            elif method405 == 'PATCH':
                result = requests.patch(url, headers=headers, data=body)
            else:
                print('Запрос с методом ', method405, ' не реализован')
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
