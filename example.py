from tornado.httpclient import HTTPClient
from tornado.httpclient import AsyncHTTPClient
from tornado.concurrent import Future
from tornado import gen

def synchronous_fetch(url):
    http_client = HTTPClient()
    response = http_client.fetch(url)
    return response.body


def async_fetch(url):
    http_client = AsyncHTTPClient()

    def handle_response(response):
        return response.body

    http_client.fetch(url, callback=handle_response)


def async_fetch_future(url):
    http_client = AsyncHTTPClient()
    my_future = Future()
    fetch_future = http_client.fetch(url)

    fetch_future.add_done_callback(
        lambda f: my_future.set_result(f.result())
    )

    return my_future


@gen.coroutine
def fetch_coroutine(url):
    http_client = AsyncHTTPClient()
    response = yield http_client.fetch(url)

    return response.body


async def fetch_coroutine(url):
    http_client = AsyncHTTPClient()
    response = await http_client.fetch(url)
    return response.body

# limitations
async def f():
    executor = concurrent.futures.ThreadPoolExecutor()
    await tornado.gen.convert_yielded(executor.submit(g))