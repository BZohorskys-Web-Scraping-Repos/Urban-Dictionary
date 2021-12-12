from lxml import etree
import aiohttp
import asyncio
import curses
import logging
import itertools
import requests
import sys
import time

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

def interactive_console(screen, definitionHtmlList):
    pos = 0
    while pos < len(definitionHtmlList):
        screen.clear()
        word = definitionHtmlList[pos].xpath('./div[@class="def-header"]/descendant-or-self::*/text()')
        meaning = definitionHtmlList[pos].xpath('./div[@class="meaning"]/descendant-or-self::*/text()')
        example = definitionHtmlList[pos].xpath('./div[@class="example"]/descendant-or-self::*/text()')
        example = ''.join(example).replace('\r','\n         ')

        word = ''.join(word).strip().title()
        meaning = ''.join(meaning).strip()
        screen.addstr("({0}/{1}) {2} - {3}\n".format(pos+1, len(definitionHtmlList), word, meaning))
        screen.addstr("Example: {0}\n".format(example))
        screen.addstr("Next, Previous, or Quit? (j,k,q)")
        user_response = screen.getkey()
        valid_response = False
        while not valid_response:
            if user_response == 'j':
                valid_response = True
                pos += 1
            elif user_response == 'k':
                if pos != 0:
                    valid_response = True
                    pos  -= 1
                else:
                    user_response = screen.getkey()
            elif user_response == 'q':
                valid_response = True
                pos = len(definitionHtmlList)
            else:
                user_response = screen.getkey()

def is_paragraph_empty(paragraph):
    return True if paragraph.strip() == '' else False

async def search(query_string):
    search_url = ''.join([SITE, query_string])
    webRequestTask = asyncio.create_task(get_webpage(search_url))
    await idleAnimation(webRequestTask)
    if webRequestTask.result()['code'] == 200:
        page_html = etree.HTML(webRequestTask.result()['html'])
        definitions = page_html.xpath('//div[@class="def-panel "]')
        curses.wrapper(interactive_console, definitions)
    else:
        print(f'Recieved {webRequestTask.result()["code"]} response code.')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        if len(sys.argv) < 2:
            print('Error: Not enough arguments provided. Please provide a search term.')
            sys.exit()
        else:
            print('Error: Too many arguments provided.')
            sys.exit()

    query_string = sys.argv[1]
    sys.exit(asyncio.run(search(query_string)))
