"""!pokemon <name> will return pokemon description for that name (!pokedex is an alias)"""
from bs4 import BeautifulSoup
from string import Template
import re
try:
    from urllib import quote, unquote
except ImportError:
    from urllib.request import quote, unquote
import requests


def pokedex(name):
    name = name.lower()
    url = "http://pokemondb.net/pokedex/{0}".format(name)
    soup = BeautifulSoup(requests.get(url).text)

    heading = name[0].upper() + name[1:]
    description = soup.find("div", attrs={"class": "col desk-span-8 lap-span-6"}).text \
        .encode("utf8").replace("Pok\xc3\x83\xc2\xa9mon", "Pokemon").replace("\n", "").replace("\t", "")
    basic_tabs = soup.find("ul", attrs={"class": "svtabs-panel-list"})
    tabs = basic_tabs.findAll("li", attrs={"class": "svtabs-panel"})
    current_tab = tabs[0]
    img_url = current_tab.find("div", attrs={"class": "col desk-span-4 lap-span-6 figure"}).find("img").get("src") \
        .encode("utf8")
    vitals_table = current_tab.find("table", attrs={"class": "vitals-table"})
    trs = vitals_table.findAll("tr")
    vitals = {}

    for x in range(0, 6):
        current_tr = trs[x]
        key = "id" if x == 0 else current_tr.find("th").text.encode("utf8")

        if x == 0:
            vitals[key] = current_tr.find("strong").text.encode("utf8")
        elif x == 1 or x == 5:
            vitals[key] = ",".join([link.text.encode("utf8") for link in current_tr.findAll("a")])
        else:
            vitals[key] = current_tr.find("td").text.encode("utf8")

    if not description:
        return ":monkey: Sorry, no matching pokemon found :monkey:"

    message = Template("*$heading*\nDescription: _$description_\n$img\n$vital")\
        .substitute(heading=heading, description=description, img=img_url,
                    vital="\n".join([":".join([x, vitals[x]]) for x in vitals]))
    return message


def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!(?:pokedex|pokemon) (.*)", text)
    if not match:
        return
    
    pokemon_name = match[0]
    return pokedex(pokemon_name.encode("utf-8"))
