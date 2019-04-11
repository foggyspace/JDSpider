import asyncio
from pprint import pprint

import aiohttp
from pyquery import PyQuery as pq


TIMEOUT = 5



headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36"
}


async def fetch(url, session):
    async with session.get(url) as resp:
        return await resp.text()


async def parse_jd_python_data(response):
    doc = pq(response)

    book_dict = {}

    books = doc("div#J_goodsList ul.gl-warp.clearfix li").items()

    for book in books:
        title = book.find('div.p-name.p-name-type-2 a').attr('title')
        price = book.find('div.p-price strong i').text()
        name = book.find('div.p-name.p-name-type-2 a em').text()
        publish = book.find('span.J_im_icon a').text()
        book_dict["title"] = title.strip()
        book_dict["price"] = price
        book_dict["name"] = name.strip()
        book_dict["publish"] = publish.strip()
        pprint(book_dict)


async def crawl(url, headers):
    try:
        timeout = aiohttp.ClientTimeout(total=TIMEOUT)
        async with aiohttp.ClientSession(headers=headers, timeout=timeout) as session:
            html = await fetch(url, session)
            await parse_jd_python_data(html)
    except (aiohttp.ClientConnectionError, asyncio.TimeoutError) as e:
        print('[*] exception '.format(e))
        return await crawl(url, headers)




if __name__ == '__main__':
    root_url = 'https://search.jd.com/Search?keyword=python&enc=utf-8&page={}'
    urls = [root_url for page in range(100)]
    loop = asyncio.get_event_loop()
    tasks = [asyncio.ensure_future(crawl(url, headers)) for url in urls]
    tasks = asyncio.gather(*tasks)
    loop.run_until_complete(tasks)
