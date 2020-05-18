import requests
import vcr


with vcr.use_cassette('test.yaml'):
    response = requests.get('https://example.com')

@vcr.use_cassette(record_mode='new_episodes')
def test_requests(url, *args, **kwargs):
    res = requests.get(url)
    print(res)


def run():
    url1 = 'https://example.com'
    url2 = 'https://example.com?query=test'

    test_requests(url1)
    test_requests(url2)

run()

