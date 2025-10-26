import argparse
import os
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv


def is_shorten_link(link, access_token):
    url = 'https://api.vk.com/method/utils.checkLink'

    payload = {
        'access_token': access_token,
        'url': link,
        'v': '5.199'
    }

    response = requests.post(url, params=payload)
    response.raise_for_status()
    response_data = response.json()
    is_short_link = response_data['response']['link'] != link
    return is_short_link


def shorten_link(access_token, link):
    url = 'https://api.vk.com/method/utils.getShortLink'

    payload = {
        'access_token': access_token,
        'url': link,
        'v': '5.199'
    }

    response = requests.post(url, params=payload)
    response.raise_for_status()
    response_data = response.json()
    short_link = response_data['response']['short_url']
    return short_link


def count_clicks(access_token, link):
    url = 'https://api.vk.com/method/utils.getLinkStats'
    parsed_link = urlparse(link)
    path = parsed_link.path[1:]

    payload = {
        'access_token': access_token,
        'key': path,
        'v': '5.199',
        'interval': 'forever',
        'extended': '0'
    }

    response = requests.post(url, params=payload)
    response.raise_for_status()
    response_data = response.json()
    clicks = response_data['response']['stats'][0]['views']
    return clicks


def main():
    load_dotenv()
    access_token = os.environ['VK_ACCESS_TOKEN']
    parser = argparse.ArgumentParser(
        description='Введите ссылку для сокращения'
    )
    parser.add_argument('link')
    args = parser.parse_args()
    link = args.link
    link_is_short = is_shorten_link(link, access_token)

    if link_is_short:
        try:
            clicks = count_clicks(access_token, link)
            print("Количество переходов по ссылке: ", clicks)
        except NameError:
            print('Не удалось сократить ссылку')
    else:
        try:
            short_link = shorten_link(access_token, link)
            print('Короткая ссылка: ', short_link)
        except KeyError:
            print('Некорректная ссылка')


if __name__ == '__main__':
    main()