import pathlib as pl
from json import load
from goodpath import root_path_as_plPath as Grp
from goodpath import root_path_as_str as Grs
from os import system, remove

try:
    rl = load(
        open(f"{str(pl.Path(__file__).parent.resolve())}/app_data/rock_urls_list.json"))
except:
    print("Error loading rock_urls_list.json\n Setting it up now... \n Restart the application for the updated list.")
    system("python setup_rock_urls_list.py")

rs = Grs()
rp = Grp()
curl_invoker = "curl"
code = 23
images_dir = "app_images"
