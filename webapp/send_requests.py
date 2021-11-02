import requests


def standart_tests(endpoints, methods_list, request_url, body={'key': 'value'}):
    for endpoint in endpoints:
        print(f'Endpoints {endpoints[endpoint]} Methods_list {methods_list}')
        method405list = list(set(methods_list) ^ set(endpoints[endpoint]))
        # method405list.reverse()
        method405 = method405list[0]
        url = request_url + endpoint
        print(f'XOR LISTS {method405}')
        try:
            if method405 == 'GET':
                result = requests.get(url)
            elif method405 == 'POST':
                result = requests.post(url, body)
                print(result)
            elif method405 == 'PUT':
                result = requests.put(url, body)
            elif method405 == 'DELETE':
                result = requests.delete(url)
            elif method405 == 'PATCH':
                result = requests.patch(url, body)
            else:
                print('Запрос с методом ', method405, ' не реализован')
                return False
            # result.raise_for_status()
            return result
        except(requests.RequestException, ValueError) as e:
            print(f'Получена ошибка {e} статус код {result.status_code}')
            return False

    pass
