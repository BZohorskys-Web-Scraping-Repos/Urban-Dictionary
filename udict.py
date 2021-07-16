import requests
import sys
import webbrowser
import logging
from lxml import etree

SITE = 'https://www.urbandictionary.com/define.php?term='

logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)-15s [%(levelname)s] %(funcName)s: %(message)s',
)

def main():
    if len(sys.argv) != 2:
        if len(sys.argv) < 2:
            print('Error: Not enough arguments provided. Please provide a search term.')
            return
        else:
            print('Error: Too many arguments provided.')
            return
    
    query_string = sys.argv[1]
    search_url = ''.join([SITE, query_string])
    r = requests.get(search_url)
    if r.status_code == 200:
        page_html = etree.HTML(r.content)
        definitions = page_html.xpath('//div[@class="def-panel "]')
        for definition in definitions:
            header = definition.xpath('./div[@class="row"]/descendant-or-self::*/text()')
            word = definition.xpath('./div[@class="def-header"]/descendant-or-self::*/text()')
            meaning = definition.xpath('./div[@class="meaning"]/descendant-or-self::*/text()')
            example = definition.xpath('./div[@class="example"]/descendant-or-self::*/text()')
            example = ''.join(example).replace('\r','\n         ')
            print(''.join(header).strip())
            print(f"{''.join(word).strip().title()} - {''.join(meaning).strip()}")
            print(f"Example: {example}")
            user_response = input('Next or Quit? (ENTER/q): ')
            if user_response == 'q':
                break
    else:
        print(f'Recieved {r.status_code} response code.')

def is_paragraph_empty(paragraph):
    return True if paragraph.strip() == '' else False


if __name__ == '__main__':
    main()
