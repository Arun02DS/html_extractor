from src.logger import logging
from src.exception import HtmlExtractor
import os,sys
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from src.config import chunk_overlap,chunk_size,TEXT_FILE_NAME
from collections import namedtuple
import pandas as pd
from datetime import datetime



def load_urls(url):
    """
    Description: This function extract html content in raw format.

    Return: list of documents

    """
    try:
        logging.info("Url are being loading")
        loader = AsyncChromiumLoader(url)
        docs = loader.load()
        logging.info("Docs are created")
        return docs
    except Exception as e:
        raise HtmlExtractor(e,sys)


def save_html_content(docs):
    """
    Description: This function save extrated html into text file for reference.

    Return: None
    
    """
    try:
        artifact_dir=os.path.join(os.getcwd(),"artifacts",f"{datetime.now().strftime('%d%m%Y__%H%M%S')}")
        os.makedirs(artifact_dir,exist_ok=True)
        filepath = os.path.join(artifact_dir, TEXT_FILE_NAME)
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(str(docs[0].page_content))
        logging.info(f"Page content has been saved to url_langchain_html.txt")
    except Exception as e:
        raise HtmlExtractor(e,sys)
    
def transform_html(docs):
    """
    Description: This function transfrom HTML page with required tags.

    Return: transformed docs
    
    """
    try:
        bs_transformer = BeautifulSoupTransformer()
        docs_transformed = bs_transformer.transform_documents(docs, 
                                                              tags_to_extract=["h3", "p"])
        logging.info("HTML page transformed.")
        return docs_transformed
    except Exception as e:
        raise Exception(e,sys)
    
def text_split(docs_transformed):
    """
    Definition:This function split text into chucks with some overlap.

    Return:List of Object of text in chunks.
    
    """
    try:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size = chunk_size, chunk_overlap = chunk_overlap)
        text_chunks = text_splitter.split_documents(docs_transformed)
        logging.info(f"length of splits: {len(text_chunks)}")
        logging.info(f"split[1]: {text_chunks[1]}")
        return text_chunks
    
    except Exception as e:
        raise HtmlExtractor(e,sys)
    
def create_people_dataframe(result):
    """
    Converts a list of Person namedtuples into a pandas DataFrame and return DtaFrame.

    Args:
        result: An object with a 'people' attribute that is a list of Person namedtuples.
    """
    try:
        Person = namedtuple('Person', ['Name', 'Position', 'Research_interest'])
        people_dicts = [{'Name': person.Name, 'Position': person.Position, 'Research_interest': person.Research_interest} for person in result.people]
        df = pd.DataFrame(people_dicts)
        logging.info("Dataframe created")
        return df
    except Exception as e:
        raise HtmlExtractor(e,sys)
