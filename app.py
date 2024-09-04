from flask import Flask, render_template, jsonify, request
from langchain_groq import ChatGroq
from src.config import *
from src.utils import *
from src.schema import Person, Data
from src.extractor import prompt
import pandas as pd
import nest_asyncio


app = Flask(__name__)

# Initialize the LLM with model and API key
llm = ChatGroq(model=model_name, groq_api_key=GROQ_API_KEY)

@app.route('/')
def index():
    return render_template('index.html')  # Render a simple form for input

@app.route('/process', methods=['POST'])
def process():
    # Get the URL from the form submission
    nest_asyncio.apply()
    url = request.form['url']
    # Load and process the document from the provided URL
    docs = load_urls([url])
    save_html_content(docs)
    
    docs_transformed = transform_html(docs)
    splits = text_split(docs_transformed)
    
    # Process the text using the LLM
    runnable = prompt | llm.with_structured_output(schema=Data)
    result = runnable(splits)
    
    # Create a DataFrame from the result
    df = create_people_dataframe(result)
    
    # Convert the DataFrame to JSON for easy return
    df_json = df.to_json(orient='records')
    
    return jsonify(df_json)  # Return the DataFrame as JSON

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
