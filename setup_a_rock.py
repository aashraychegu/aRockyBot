from app_vars import *
from bs4 import BeautifulSoup as bs
import random as r


def get_gallery_image_list_from_rock_id(chosen_rock_id):
    system(
        f'{curl_invoker} -A "Mozilla/5.0 (platform; rv:geckoversion) Gecko/geckotrail Firefox/firefoxversion" -o "{rs}/app_data/html/index.html" https://www.mindat.org/gm/{chosen_rock_id}')

    with open(f"{rs}\\app_data\\html\\index.html", "rb") as f:
        soup = bs(f, 'html.parser')

    image_list = []
    for i in (soup.find_all("img")):
        image_list.append("https://www.mindat.org" + i.get("src"))
    if image_list == []:
        return None
    return (image_list)


try:
    rl = load(
        open(f"{rs}/app_data/rock_urls_list.json"))
except:
    print("Error loading rock_urls_list.json\n Setting it up now... \n Restart the application for the updated list.")
    system("python setup_rock_urls_list.py")


def download_image(filename, url):
    return system(
        f'{curl_invoker} -sA "Mozilla/5.0 (platform; rv:geckoversion) Gecko/geckotrail Firefox/firefoxversion" --output "{rs}/{images_dir}/{filename}" {url}')


def rm_prev_image():
    for i in list((rp / images_dir).iterdir()):
        remove(str(i.absolute()))


def get_random_single_image_url(crid):
    url = r.choice(get_gallery_image_list_from_rock_id(crid))
    return url, url.split("/")[-1]


def download_image_from_crid(crid):
    try:
        rm_prev_image()
    except IndexError as e:
        pass
    url, filename = get_random_single_image_url(crid)
    download_image(filename, url)


def download_image_from_url(url):
    try:
        rm_prev_image()
    except IndexError as e:
        pass
    filename = url.split("/")[-1]
    download_image(filename, url)


def setup_new_rock():
    def rand_rock_key():
        return (r.choice(list(rl.keys())))
    rock_name = rand_rock_key()

    def rand_rock_url_of_rock():
        return r.choice(rl[rock_name])
    rval = True

    try:
        download_image_from_url(rand_rock_url_of_rock())
    except Exception as e:
        print(e)
        rval = False
    return rock_name, rval


def get_rock_path():
    try:
        return str(list((rp / images_dir).iterdir())[0].absolute())
    except IndexError as e:
        return None


def try_getting_new_rock():
    while True:
        name, rval = setup_new_rock()
        if rval:
            return name, get_rock_path()


if __name__ == "__main__":
    print(try_getting_new_rock())
