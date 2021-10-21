import requests


def test_execute(request_url, method, query='null', header='null',
                 path_params={'key1': 'value1', 'key2': 'value2'}, body={'key': 'value'}):
    # print('IN TEST EXECUTE')
    method = str(method).upper()
    print(method, ' ', request_url)
    payload = {'key1': 'value1', 'key2': 'value2'}
    try:
        if method == 'GET':
            result = requests.get(request_url)
        elif method == 'POST':
            result = requests.post(request_url, body, params=path_params)
            print(result)
        elif method == 'PUT':
            result = requests.put(request_url, body)
        else:
            print('Метод ', method, ' не реализован')
            return False
        # result.raise_for_status()
        return result
    except(requests.RequestException, ValueError) as e:
        print(f'Получена ошибка {e} статус код {result.status_code}')
        return False


if __name__ == '__main__':
    s = test_execute()
    print(s)
