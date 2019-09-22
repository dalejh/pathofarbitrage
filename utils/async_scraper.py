import aiohttp
import asyncio
import async_timeout
import time
from typing import List, Union, Dict, Tuple

from URL_builder.poe_trade_url import PoeTradeUrl
from pages.transaction_page import TransactionPage


class AsyncScraper:

    """
    This class uses aiohttp and asyncio to create a grouped task list of URLs to scrape. I generate the URLs via a helper class
    which determines which currency to scrape via user input.
    Additionally, after scraping pages, returns a Dict[List[Tuple[Union[int, float]]]] of the two IDs of a currency transaction, and the weight (ratio) of trade between them
    """

    def __init__(self, league, user_orbs_list):
        self.league = league
        self.user_orb_list = user_orbs_list
        self.loop = asyncio.get_event_loop()
        self.have_want_weight_list = []
        self.orb_list_length = len(user_orbs_list)

    # request each individual page to be scraped for arbitrage computation (via event loop defined below)
    async def grab_page(self, session, url):
        page_start = time.time()
        async with async_timeout.timeout(30):
            async with session.get(url) as res:
                print(f'Page res: {res.status}')
                print(f'Page took {time.time() - page_start}')
                return await res.text()

    # grab URL list and append to async task list
    async def grab_all_pages(self, loop, *urls):
        task_list = []
        async with aiohttp.ClientSession(loop=loop) as session:
            for url in urls:
                task_list.append(self.grab_page(session, url))
            grouped_tasks = asyncio.gather(*task_list)
            return await grouped_tasks

    # grab all orbs we want to compute arbitrage for, add to async event loop
    def scrape_all_pages(self):
        urls = []
        for orb_id in self.user_orb_list:
            for second_id in self.user_orb_list:
                if second_id == orb_id:
                    continue
                urls.append(PoeTradeUrl(self.league, str(orb_id), str(second_id)).url)

        print(urls)
        pages = self.loop.run_until_complete(self.grab_all_pages(self.loop, *urls))

        for page_data in pages:
            page = TransactionPage(page_data)
            self.have_want_weight_list.append(page.start_end_weight)

        graph = {}

        #  Create adjacency list for DFS. s is 'start currency' e is 'end currency' w is 'weight'
        #  i.e. 'weight' is the ratio of their values
        for s, e, w in self.have_want_weight_list:
            if s in graph:  # if key exists, append conversion currency ID and weight, else create key
                graph[s].append((s, e, w))
            else:
                graph[s] = [(s, e, w)]
        return graph

