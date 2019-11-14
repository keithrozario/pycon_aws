import asyncio
import time
import aiohttp


async def download_site(session, url):
    timeout = aiohttp.ClientTimeout(sock_connect=5)

    try:
        async with session.get(f"http://{url}/robots.txt",
                               timeout=timeout) as response:
            text = await response.text()
            return text
    except Exception as e:
        print(f"{url}: {e}")


async def download_all_sites(sites):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False), headers=headers) as session:
        tasks = []
        for url in sites:
            task = asyncio.ensure_future(download_site(session, url))
            tasks.append(task)
        print("Awaiting response")
        return await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == "__main__":
    with open('sites.csv', 'r') as site_csv:
        sites  = site_csv.read().split('\n')
    start_time = time.time()
    results = asyncio.get_event_loop().run_until_complete(download_all_sites(sites[700:800]))
    print(f"{len(results)} results")
    duration = time.time() - start_time
    print(f"Downloaded {len(sites)} sites in {duration} seconds")