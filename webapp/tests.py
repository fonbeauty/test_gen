import requests


def test_execute(request_url, method, query, header, path):
    method = str(method).capitalize()
    if method == 'GET':
        result = requests.get(request_url)
    elif method == 'POST':
        result = requests.post(request_url)
    elif method == 'PUT':
        result = requests.put(request_url)

    return result

if __name__ == '__main__':
    s = send()
    print(s)