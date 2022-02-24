import os

from fastapi import FastAPI
import pandas as pd
import logging
from mangum import Mangum

from utils import WordProcessor

stage = os.environ.get('STAGE', None)
openapi_prefix = f"/{stage}" if stage else "/"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Word processor api", openapi_prefix=openapi_prefix)

obj = WordProcessor()

@app.on_event('startup')
def startup():
    """
    Load the file into an object at the start of the api 
    """
    obj.load_file('word_search.tsv')

@app.get("/search")
def search(word: str) -> []:
    """
    Method to expose search functionality
    """
    return obj.search_string(word)

handler = Mangum(app)