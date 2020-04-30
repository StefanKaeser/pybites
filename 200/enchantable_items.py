import re

from pathlib import Path
from urllib.request import urlretrieve

from bs4 import BeautifulSoup as Soup

out_dir = "./"
html_file = f"{out_dir}/enchantment_list_pc.html"

HTML_FILE = Path(html_file)
URL = "https://www.digminecraft.com/lists/enchantment_list_pc.php"


class Enchantment:
    """Minecraft enchantment class
    
    Implements the following: 
        id_name, name, max_level, description, items
    """

    def __init__(self, id_name, name, max_level, description, items=None):
        self.id_name = id_name
        self.name = name
        self.max_level = max_level
        self.description = description
        self.items = items
        if not self.items:
            self.items = []

    def __str__(self):
        return f"{self.name} ({self.max_level}): {self.description}"


class Item:
    """Minecraft enchantable item class
    
    Implements the following: 
        name, enchantments
    """

    def __init__(self, name, enchantments=None):
        self.name = name
        self.enchantments = enchantments
        if not self.enchantments:
            self.enchantments = []

    def __str__(self):
        string = f"{self.capitalized_name}: "
        alphabetical_ordered_enchantments = sorted(
            self.enchantments, key=lambda x: x.id_name
        )
        for enchantment in alphabetical_ordered_enchantments:
            string += f"\n  [{enchantment.max_level}] {enchantment.id_name}"
        return string

    @property
    def capitalized_name(self):
        name_parts = self.name.split("_")
        name = " ".join([part.capitalize() for part in name_parts])
        return name


def generate_enchantments(soup):
    """Generates a dictionary of Enchantment objects
    
    With the key being the id_name of the enchantment.
    """
    enchantments_table = soup.find(
        "table", {"id": "minecraft_items", "class": "std_table"}
    )

    enchantments = dict()

    rows = enchantments_table.find_all("tr")
    for row in rows[1:]:
        columns = row.find_all("td")

        name = columns[0].text
        max_level_roman = columns[1].text
        description = columns[2].text
        items_imag_url = columns[4].find("img").get("data-src")

        name, id_name = extract_name_and_id_name(name)
        max_level = convert_roman_to_arabic(max_level_roman)
        items = parse_items_image_url(items_imag_url)

        enchantment = Enchantment(id_name, name, max_level, description, items)
        enchantments[id_name] = enchantment

    return enchantments


def extract_name_and_id_name(name):
    match = re.match(r"([\w ]*)\((.*)\)", name)
    name, id_name = match.groups()
    return name, id_name


def convert_roman_to_arabic(roman):
    roman_to_arabic = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5}
    return roman_to_arabic[roman]


def parse_items_image_url(image_url):
    items_string = image_url.split("/")[-1]

    sub_strings_to_remove = ["enchanted_", "iron_", ".png", "_sm"]
    for string_ in sub_strings_to_remove:
        items_string = items_string.replace(string_, "")

    items = items_string.split("_")
    if "fishing" in items:
        items.remove("fishing")
        items.remove("rod")
        items.append("fishing_rod")

    return items


def generate_items(data):
    """Generates a dictionary of Item objects
    
    With the key being the item name.
    """
    items_dict = dict()

    for enchantment in data.values():
        item_names = enchantment.items

        for item_name in item_names:
            item = items_dict.get(item_name, Item(item_name))
            item.enchantments.append(enchantment)

            items_dict[item_name] = item

    return items_dict


def get_soup(file=HTML_FILE):
    """Retrieves/takes source HTML and returns a BeautifulSoup object"""
    if isinstance(file, Path):
        if not HTML_FILE.is_file():
            urlretrieve(URL, HTML_FILE)

        with file.open() as html_source:
            soup = Soup(html_source, "html.parser")
    else:
        soup = Soup(file, "html.parser")

    return soup


def main():
    """This function is here to help you test your final code.
    
    Once complete, the print out should match what's at the bottom of this file"""
    soup = get_soup()
    enchantment_data = generate_enchantments(soup)
    minecraft_items = generate_items(enchantment_data)
    for item in minecraft_items:
        print(minecraft_items[item], "\n")


if __name__ == "__main__":
    pass
#    main()

"""
Armor: 
  [1] binding_curse
  [4] blast_protection
  [4] fire_protection
  [4] projectile_protection
  [4] protection
  [3] thorns 

Axe: 
  [5] bane_of_arthropods
  [5] efficiency
  [3] fortune
  [5] sharpness
  [1] silk_touch
  [5] smite 

Boots: 
  [3] depth_strider
  [4] feather_falling
  [2] frost_walker 

Bow: 
  [1] flame
  [1] infinity
  [5] power
  [2] punch 

Chestplate: 
  [1] mending
  [3] unbreaking
  [1] vanishing_curse 

Crossbow: 
  [1] multishot
  [4] piercing
  [3] quick_charge 

Fishing Rod: 
  [3] luck_of_the_sea
  [3] lure
  [1] mending
  [3] unbreaking
  [1] vanishing_curse 

Helmet: 
  [1] aqua_affinity
  [3] respiration 

Pickaxe: 
  [5] efficiency
  [3] fortune
  [1] mending
  [1] silk_touch
  [3] unbreaking
  [1] vanishing_curse 

Shovel: 
  [5] efficiency
  [3] fortune
  [1] silk_touch 

Sword: 
  [5] bane_of_arthropods
  [2] fire_aspect
  [2] knockback
  [3] looting
  [1] mending
  [5] sharpness
  [5] smite
  [3] sweeping
  [3] unbreaking
  [1] vanishing_curse 

Trident: 
  [1] channeling
  [5] impaling
  [3] loyalty
  [3] riptide
"""
