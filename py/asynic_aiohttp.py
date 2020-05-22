import asyncio
import aiohttp
import time
import requests

async def download(url):
    print("get %s" % url)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            print(resp.status)

def download2(url):
    print("get %s" % url)
    resp = requests.get(url)
    print(resp.status_code)

def main2():
    start = time.time()
    download2("http://www.163.com")
    download2("http://www.mi.com")
    download2("http://www.baidu.com")
    end = time.time()
    print("complete in %s sec." % str(end - start))

loop = asyncio.get_event_loop()
task1 = loop.create_task(download("http://www.163.com"))
task2 = loop.create_task(download("http://www.mi.com"))
task3 = loop.create_task(download("http://www.baidu.com"))

async def main():
    start = time.time()
    await task1
    await task2
    await task3
    end = time.time()
    print("complete in %s sec." % str(end - start))


if __name__ == '__main__':
    loop.run_until_complete(main())
    print("#------------------------#")
    main2()
