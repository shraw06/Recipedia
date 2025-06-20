from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
from pymongo import MongoClient
import re
import time
import random

client = MongoClient("mongodb://localhost:27017")
db = client["recipediaDB"]
collection = db["recipes"]



headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://www.google.com',
    'Connection': 'keep-alive'
}

sitemap_url = "https://www.seriouseats.com/sitemap_1.xml"
response = requests.get(sitemap_url, headers=headers)

soup_s = BeautifulSoup(response.content, "xml")

loc_tags = soup_s.find_all("loc")

all_urls = [loc.text for loc in loc_tags]

pattern = re.compile(r"-recipe-\d+$")
recipe_urls = [url for url in all_urls if pattern.search(url)]


failed_urls = [] 

for url in recipe_urls:
   try:
      rec_name = urlparse(url).path.split("-recipe")[0].strip("/")
      rec_name = rec_name.replace("-", " ").title()
      html_text = requests.get(url, headers=headers).text
      soup = BeautifulSoup(html_text, 'lxml')
      ingredients = soup.find_all('li', class_='structured-ingredients__list-item')
      ing_name = []
      ingredients_main = []
      for ing in ingredients:
          ingr = {}
          if ing.p.find('span', attrs={'data-ingredient-name': 'true'}):
           name = ing.p.find('span', attrs={'data-ingredient-name': 'true'}).text.lower()
           ing_name.append(name)
           ingr["name"] = name
          if ing.p.find('span', attrs={'data-ingredient-quantity': 'true'}):
           qty = ing.p.find('span', attrs={'data-ingredient-quantity': 'true'}).text.lower()
           ingr["quantity"] = qty
          if ing.p.find('span', attrs={'data-ingredient-unit': 'true'}):
           unit = ing.p.find('span', attrs={'data-ingredient-unit': 'true'}).text.lower()
           ingr["unit"] = unit
          ingredients_main.append(ingr)

      
      

      instructions = soup.find_all('li', class_="comp mntl-sc-block mntl-sc-block-startgroup mntl-sc-block-group--LI")

      instructions_main = []
      for ins in instructions:
          instructions_main.append(ins.find('p', class_="comp mntl-sc-block mntl-sc-block-html").text)

      total_time_div = soup.find('div', class_="total-time project-meta__total-time")
      total_time = total_time_div.find('span', class_="meta-text__data").text


      description = soup.find('div', id="article__header--project_1-0").text

      def classify_tags(rec_name, ing_name, description=""):
        text = " ".join([rec_name]+ ing_name +[description]).lower()
        tags = []

        if any(word in text for word in ["easy", "quick", "minutes", "instant"]) or (total_time.split(' ')[1]=='mins' and int(total_time.split(' ')[0])<=20):
              tags.append("quick")
        if any(word in text for word in ["salad", "grilled", "boiled", "steamed", "light"]):
              tags.append("light")
        if any(word in text for word in ["chili", "hot sauce", "spicy", "jalapeño", "pepper", "cayenne"]):
              tags.append("spicy")
        if any(word in text for word in ["sugar", "chocolate", "dessert", "honey", "sweet"]):
              tags.append("sweet")
        if any(word in text for word in ["cheese", "meat", "umami", "broth", "savory", "soy"]):
              tags.append("savory")
        if any(word in text for word in ["chips", "nuggets", "fingers", "popcorn", "fries", "snack"]):
              tags.append("snack")
        if any(word in text for word in ["curry", "rice", "pasta", "noodles", "biryani", "meal", "heavy"]):
              tags.append("meal")
        if any(word in text for word in ["cake", "cookie", "dessert", "ice cream", "pudding"]):
              tags.append("dessert")
        if any(word in text for word in ["juice", "coffee", "tea", "smoothie", "shake", "beverage", "drink", "cocktail", "mocktail"]):
              tags.append("beverage")
        if any(word in text for word in ["soup", "broth", "stew", "ramen"]):
              tags.append("soup")
        if any(word in text for word in ["salad", "lettuce", "raw", "vinaigrette"]):
              tags.append("salad")
        if not any(word in text for word in ["chicken", "fish", "lamb", "mutton", "egg", "meat", "pork", "turkey", "ham", "prawn", "lobster", "octopus"]):
              tags.append("vegetarian")

        return tags

      tags = classify_tags(rec_name, ing_name, description)


      img_tag = soup.select_one('img.primary-image__image.mntl-primary-image--blurry.loaded')

      if img_tag and img_tag.has_attr('src'):
          img_link = img_tag['src']
      else:
          img_link = None



      recipe = {
            "name": rec_name,
            "ingredients": ingredients_main,
            "instructions": instructions_main,
            "image": img_link,
            "tags": tags
      }

      collection.insert_one(recipe)
      print(f"Successfully scraped: {url}")
      time.sleep(random.uniform(1, 3))
   except Exception as e:
      print(f"Failed to scrape: {url} - Reason: {e}")
      failed_urls.append(url)

with open("failed_urls.txt", "w") as f:
    for url in failed_urls:
        f.write(url + "\n")




#loop over all recipes
#add in the database
#display in website
#style website