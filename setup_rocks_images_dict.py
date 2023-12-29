from unicodedata import name
from load_rock import get_gallery_image_list_from_rock_id as ggilfr
from json import load, dump
import asyncio
import goodpath
cp = goodpath.root_path_as_str()

urlslist = {}
async_task_list = []
with open(cp+"/app_data/rock_id_list.json", "r") as f:
    rock_info = load(f)


async def get_rock_id(i):
    print("started getting the urls for "+i)
    got_rock = ggilfr(rock_info["name_to_mdid"][i])
    urlslist[i] = got_rock
    print("ended getting the urls for " + i +
          ". They have been stored in memory")


async def main():
    for i in rock_info["name_to_mdid"]:

        async_task_list.append(asyncio.create_task(get_rock_id(i)))
    asyncio.gather(*async_task_list)

asyncio.run(main())

with open(f'{cp}\\app_data\\rock_urls_list.json', "w") as f:
    print("dumping urls into rock_urls_list.json")
    dump(urlslist, f)
