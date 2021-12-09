from lxml import etree
import aiohttp
import asyncio
import logging
import itertools
import requests
import sys
import time
import webbrowser

SITE = 'https://www.urbandictionary.com/define.php?term='

logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)-15s [%(levelname)s] %(funcName)s: %(message)s',
)

async def get_webpage(url):
    async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                code = response.status
                html = await response.text()
                return {'code':code,'html':html}

async def idleAnimation(task):
    for frame in itertools.cycle(r'-\|/-\|/'):
        if task.done():
            print('\r', '', sep='', end='', flush=True)
            break;
        print('\r', frame, sep='', end='', flush=True)
        await asyncio.sleep(0.2)

async def main():
    if len(sys.argv) != 2:
        if len(sys.argv) < 2:
            print('Error: Not enough arguments provided. Please provide a search term.')
            return
        else:
            print('Error: Too many arguments provided.')
            return

    query_string = sys.argv[1]
    search_url = ''.join([SITE, query_string])
    webRequestTask = asyncio.create_task(get_webpage(search_url))
    await idleAnimation(webRequestTask)
    if webRequestTask.result()['code'] == 200:
        page_html = etree.HTML(webRequestTask.result()['html'])
        definitions = page_html.xpath('//div[@class="def-panel "]')
        for definition in definitions:
            header = definition.xpath('./div[@class="row"]/descendant-or-self::*/text()')
            word = definition.xpath('./div[@class="def-header"]/descendant-or-self::*/text()')
            meaning = definition.xpath('./div[@class="meaning"]/descendant-or-self::*/text()')
            example = definition.xpath('./div[@class="example"]/descendant-or-self::*/text()')
            example = ''.join(example).replace('\r','\n         ')
            print(f"{''.join(word).strip().title()} - {''.join(meaning).strip()}")
            print(f"Example: {example}")
            user_response = input('Next or Quit? (ENTER/q): ')
            if user_response == 'q':
                break
    else:
        print(f'Recieved {webRequestTask.result()["code"]} response code.')

def is_paragraph_empty(paragraph):
    return True if paragraph.strip() == '' else False


if __name__ == '__main__':
    asyncio.run(main())
