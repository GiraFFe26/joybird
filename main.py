import requests
import os
from fake_useragent import UserAgent
import json
from json.decoder import JSONDecodeError
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from requests.exceptions import ChunkedEncodingError


def collect_data():
    ua = UserAgent()
    http_proxyf = 'http://login:password@ip:port'
    os.environ["http_proxy"] = http_proxyf
    os.environ["https_proxy"] = http_proxyf
    retry_strategy = Retry(
        total=15,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    sess = requests.Session()
    sess.mount("https://", adapter)
    sess.mount("http://", adapter)
    # maybe need sess.trust_env = True
    for id in range(12000):
        print(id)
        cookies = {
            'connect.sid': 's%3AkkKnU7oeWxFmsmb9fDhD_U8-Rwk6VWrq.DHh8UZKL5T1A9wyJwuY4dNG8XNv%2BPEcm9vsJxayrwWE',
            'hero-session-555e9e99-2289-4b83-b89a-358e93a981cd': 'author=client&expires=1690556773119&visitor=cecc8796-94e1-4d50-adc2-380f62ea4f65',
            '__cf_bm': 'pXtmeFZkyULTGOa1_J4cj4ExlzJ0TqJtVMtT33Q2OLE-1659024551-0-AZmMqqQ4VP+wjaVnvl77Udo3x46KChF7FzO+cY7JVPAx7Q3sQgiC9OzxuaNXcE1TGxIPv9SsrkhHXFf3uJzo6JcnuFAHK0hTMMFfvZjcWO6nw3/iS+sSh3uwhDSiaWVE8w==',
        }

        headers = {
            'authority': 'api.prod.nest.joybird.com',
            'accept': '*/*',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            # Already added when you pass json=
            # 'content-type': 'application/json',
            # Requests sorts cookies= alphabetically
            # 'cookie': 'connect.sid=s%3AkkKnU7oeWxFmsmb9fDhD_U8-Rwk6VWrq.DHh8UZKL5T1A9wyJwuY4dNG8XNv%2BPEcm9vsJxayrwWE; hero-session-555e9e99-2289-4b83-b89a-358e93a981cd=author=client&expires=1690556773119&visitor=cecc8796-94e1-4d50-adc2-380f62ea4f65; __cf_bm=pXtmeFZkyULTGOa1_J4cj4ExlzJ0TqJtVMtT33Q2OLE-1659024551-0-AZmMqqQ4VP+wjaVnvl77Udo3x46KChF7FzO+cY7JVPAx7Q3sQgiC9OzxuaNXcE1TGxIPv9SsrkhHXFf3uJzo6JcnuFAHK0hTMMFfvZjcWO6nw3/iS+sSh3uwhDSiaWVE8w==',
            'origin': 'https://joybird.com',
            'referer': 'https://joybird.com/',
            'sec-ch-ua': '"Opera GX";v="89", "Chromium";v="103", "_Not:A-Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': ua.random,
        }

        json_data = {
            'operationName': 'getProductBasicDetails',
            'variables': {
                'id': id
            },
            'query': 'query getProductBasicDetails($slug: String, $id: Int, $productSku: String) {\n  basicDetails: getProduct(slug: $slug, id: $id, productSku: $productSku) {\n    id\n    sku\n    slug\n    name\n    discontinued\n    default_option_value\n    default_option_image\n    first_popular_image\n    type {\n      name\n      __typename\n    }\n    family {\n      name\n      __typename\n    }\n    efg_flag\n    exp_wood_product\n    difficulty\n    is_external\n    category_ids\n    attributes_min {\n      dimensions\n      urlKey\n      __typename\n    }\n    attributes {\n      code\n      label\n      name\n      value\n      __typename\n    }\n    additional_attributes {\n      fet_left_img\n      fet_right_img\n      showpiece_desc\n      __typename\n    }\n    hero_image_count\n    hero_images {\n      sort_order\n      img {\n        url\n        cropData\n        __typename\n      }\n      upholstery_name\n      upholstery_type\n      __typename\n    }\n    variation_photos_count\n    custom_properties {\n      dimensional_image_desktop\n      dimensional_image_mobile\n      selling_attributes\n      product_label\n      intro_video_1x1\n      intro_video_16x9\n      ar_asset\n      ar_asset_upholstery\n      display_option_images\n      default_angle\n      cylindo_product\n      cylindo_scale_up\n      option_selector\n      __typename\n    }\n    meta {\n      id\n      price {\n        discount_percent\n        final_price\n        original_price\n        max_discount_percent\n        __typename\n      }\n      reviews {\n        average_score\n        count\n        sample_reviews {\n          title\n          comment\n          rate\n          date\n          full_name\n          __typename\n        }\n        __typename\n      }\n      promotion {\n        discount\n        endDate\n        tiers {\n          min_cart\n          discount\n          __typename\n        }\n        __typename\n      }\n      collectionSlug\n      __typename\n    }\n    __typename\n  }\n}\n',
        }

        resp = sess.post('https://api.prod.nest.joybird.com/graphql', cookies=cookies, headers=headers,
                                 json=json_data)
        try:
            src = json.loads(resp.text)
        except JSONDecodeError:
            resp = sess.post('https://api.prod.nest.joybird.com/graphql', cookies=cookies, headers=headers,
                             json=json_data)
            src = json.loads(resp.text)
        if src['data']['basicDetails'] != None:
            for i in src['data']['basicDetails']['attributes']:
                if i['code'] == 'item_availability' and i['value'] == '0':
                    try:
                        main_url = 'https://joybird.com' + src['data']['basicDetails']['attributes_min']['urlKey']
                    except TypeError:
                        break
                    print(main_url)
                    category, name = main_url.split('/')[3], src['data']['basicDetails']['name'].replace('"', '').replace('/', '')
                    path_category = f'F:/data/{category}'
                    try:
                        os.mkdir(path_category)
                    except FileExistsError:
                        pass
                    path_product = f'{path_category}/{name.strip()} {id}'
                    os.mkdir(path_product)
                    resp = sess.get(main_url, headers={'user-agent': ua.random})
                    soup = BeautifulSoup(resp.text, 'lxml')
                    try:
                        a = json.loads(soup.find('div', id='apollo-state').find('script').text.split('.__APOLLO_STATE__=')[-1][:-1])
                    except AttributeError:
                        resp = sess.get(main_url, headers={'user-agent': ua.random})
                        soup = BeautifulSoup(resp.text, 'lxml')
                        try:
                            a = json.loads(
                                soup.find('div', id='apollo-state').find('script').text.split('.__APOLLO_STATE__=')[-1][
                                :-1])
                        except AttributeError:
                            continue
                    for i in a:
                        if a[i]['__typename'] == 'OptionValue':
                            color, sku = a[i]['value'].lower().strip().replace(' ', '_'), a[i]['sku']
                            path_color = f'{path_product}/{sku}'
                            try:
                                os.mkdir(path_color)
                            except (FileExistsError, OSError):
                                break
                            url = f'{main_url}?fabric={color}'
                            print(url)
                            try:
                                resp = sess.get(url, headers={'user-agent': ua.random})
                            except ChunkedEncodingError:
                                resp = sess.get(url, headers={'user-agent': ua.random})
                            soup = BeautifulSoup(resp.text, 'lxml')
                            images = soup.find_all('img', class_='PDPDesktopHeroThumbnail__image')
                            for k, image in enumerate(images):
                                image_url = image.get('src').split('?auto')[0]
                                resp = sess.get(image_url, headers={'user-agent': ua.random})
                                with open(f'{path_color}/image{k}.jpg', "wb") as f:
                                    f.write(resp.content)
                            try:
                                dism_image = soup.find('div', class_='PDPDimensionsContentUI').find('img').get('data-src').split('?auto')[0]
                            except AttributeError:
                                continue
                            resp = sess.get(dism_image, headers={'user-agent': ua.random})
                            with open(f'{path_color}/dismensions.jpg', "wb") as f:
                                f.write(resp.content)
                    else:
                        path_color = f'{path_product}/default'
                        os.mkdir(path_color)
                        url = main_url
                        print(url)
                        try:
                            resp = sess.get(url, headers={'user-agent': ua.random})
                        except ChunkedEncodingError:
                            resp = sess.get(url, headers={'user-agent': ua.random})
                        soup = BeautifulSoup(resp.text, 'lxml')
                        images = soup.find_all('img', class_='PDPDesktopHeroThumbnail__image')
                        for k, image in enumerate(images):
                            image_url = image.get('src').split('?auto')[0]
                            resp = sess.get(image_url, headers={'user-agent': ua.random})
                            with open(f'{path_color}/image{k}.jpg', "wb") as f:
                                f.write(resp.content)
                        try:
                            dism_image = \
                            soup.find('div', class_='PDPDimensionsContentUI').find('img').get('data-src').split(
                                '?auto')[0]
                        except AttributeError:
                            continue
                        resp = sess.get(dism_image, headers={'user-agent': ua.random})
                        with open(f'{path_color}/dismensions.jpg', "wb") as f:
                            f.write(resp.content)

                    break


def main():
    collect_data()


if __name__ == '__main__':
    main()
