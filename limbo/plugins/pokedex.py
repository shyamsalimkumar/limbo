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

    message = ":monkey: Sorry, no matching pokemon found :monkey:"
    heading = name[0].upper() + name[1:]

    try:
        description = soup.find("div", attrs={"class": "col desk-span-8 lap-span-6"}).text.strip()
        basic_tabs = soup.find("ul", attrs={"class": "svtabs-panel-list"})
        tabs = basic_tabs.findAll("li", attrs={"class": "svtabs-panel"})
        current_tab = tabs[0]
        img_url = current_tab.find("div", attrs={"class": "col desk-span-4 lap-span-6 figure"}).find("img").get("src")
        vitals_table = current_tab.find("table", attrs={"class": "vitals-table"})
        trs = vitals_table.findAll("tr")
        keys = []
        vitals = {}

        for x in range(0, 6):
            current_tr = trs[x]
            key = "Id" if x == 0 else current_tr.find("th").text
            keys.append(key)

            if x == 0:
                vitals[key] = current_tr.find("strong").text
            elif x == 1 or x == 5:
                vitals[key] = ",".join([link.text for link in current_tr.findAll("a")])
            else:
                vitals[key] = current_tr.find("td").text

        message = Template("*$heading*\nDescription: $description\n$img\n$vital")\
            .substitute(heading=heading, description="_" + description + "_", img=img_url,
                        vital="\n".join([": ".join([x, vitals[x]]) for x in keys]))
    except AttributeError:
        print("Page parsing failed. 404 or API change")
    finally:
        return message

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!(?:pokedex|pokemon) (.*)", text)
    if not match:
        return
    
    pokemon_name = match[0]
    return pokedex(pokemon_name.encode("utf-8"))
