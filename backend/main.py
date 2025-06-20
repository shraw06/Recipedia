from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from dotenv import load_dotenv
import os

load_dotenv() 

MONGO_URI = os.getenv("MONGODB_URI")



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

client = MongoClient(MONGO_URI)
db = client["recipediaDB"]
collection = db["recipes"]

class IngredientsRequest(BaseModel):
    ingredients: List[str]

# @app.post("/recipes")
# def get_recipes(request: IngredientsRequest):
#     ingredientsl = [ing.lower() for ing in request.ingredients]
#     matches = collection.find({"ingredients.name": {"$in": ingredientsl}})
#     result = []
#     for match in matches:
#         recipe_ingredient_names = [i["name"].lower().strip() for i in match.get("ingredients", [])]
#         match["match_count"] = len(set(recipe_ingredient_names) & set(ingredientsl))
#         match["_id"] = str(match["_id"])
#         result.append(match)
#     return jsonable_encoder(result)

@app.post("/recipes")
def get_recipes(request: IngredientsRequest):
    ingredientsl = [ing.lower().strip() for ing in request.ingredients]

    matches = collection.find()  # Get all, do fuzzy filtering in Python

    result = []
    for match in matches:
        recipe_ingredient_names = [i["name"].lower().strip() for i in match.get("ingredients", [])]
        
        matched_ings = [
            ing_name for ing_name in recipe_ingredient_names
            for user_ing in ingredientsl
            if user_ing in ing_name or ing_name in user_ing
        ]

        if matched_ings:
            match["match_count"] = len(set(matched_ings))  # avoid overcounting
            match["_id"] = str(match["_id"])
            result.append(match)


    return jsonable_encoder(result)