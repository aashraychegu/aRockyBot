from app_vars import *
from bs4 import BeautifulSoup as bs
import random as r
from urllib.request import urlretrieve


def get_gallery_image_list_from_rock_id(chosen_rock_id):
    system(
        f'{curl_invoker} -A "Mozilla/5.0 (platform; rv:geckoversion) Gecko/geckotrail Firefox/firefoxversion" -o "{rs}/app_data/html/index.html" https://www.mindat.org/gm/{chosen_rock_id}'
    )

    with open(f"{rs}\\app_data\\html\\index.html", "rb") as f:
        soup = bs(f, "html.parser")

    image_list = []
    for i in soup.find_all("img"):
        image_list.append("https://www.mindat.org" + i.get("src"))
    return image_list


rl = load(open(f"{rs}/app_data/rock_urls_list.json"))
rl_keys = list(rl.keys())


def rand_rock_key():
    return r.choice(rl_keys)


def url_of_rock(rock_name):
    return r.choice(rl[rock_name])


def get_rock_name_url():
    name = rand_rock_key()
    url = url_of_rock(name)
    # url, _ = urlretrieve(url)
    return name, url
