from src.logger import logging
from src.exception import HtmlExtractor
import os,sys
from typing import List
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from src.config import model_name,chunk_overlap,chunk_size



def load_urls(urls:List):
    """
    Description: This function extract html content in raw format.

    Return: list of documents

    """
    try:
        logging.info("Url are being loading")
        loader = AsyncChromiumLoader(urls, user_agent="MyAppUserAgent")
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
        with open("url_langchain_html.txt", "w", encoding="utf-8") as file:
            file.write(str(docs[0].page_content))
        logging.inf0(f"Page content has been saved to url_langchain_html.txt/n{docs[0].page_content}")
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
                                                              tags_to_extract=["p", "h3", "div", "a"])
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
        logging.info(f"length of chucks: {len(text_chunks)}")
        logging.info(f"chuck[0]: {text_chunks[0]}")
        return text_chunks
    
    except Exception as e:
        raise HtmlExtractor(e,sys)

