from dotenv import load_dotenv
import os,sys
from datetime import datetime
from src.logger import logging
from src.exception import HtmlExtractor
from dataclasses import dataclass

load_dotenv()

GROQ_API_KEY = os.environ.get('GROQ_API_KEY')


model_name="mixtral-8x7b-32768"
chunk_size = 1000
chunk_overlap = 0

TEXT_FILE_NAME = "url_langchain_html.txt"
DATAFRAME_FILE_NAME = "people.csv"
