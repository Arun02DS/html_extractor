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
    nest_asyncio.apply()
    url = request.form['url']
    
    # Initialize result as None
    result = None
    
    try:
        docs = load_urls([url])
        save_html_content(docs)
        docs_transformed = transform_html(docs)
        splits = text_split(docs_transformed)
        
        text_content = splits[2].page_content

        
        # Process the text using the LLM
        runnable = prompt | llm.with_structured_output(schema=Data)
        result = runnable.invoke({"text": text_content})
        # print(result)
        
    except Exception as e:
        # Log or handle the error
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 400
    
    # Check if result is None before processing further
    if result is None:
        return jsonify({"error": "No result returned from the LLM"}), 500
    
    # Create a DataFrame from the result
    df = create_people_dataframe(result)

    # Convert the DataFrame to an HTML table
    df_html = df.to_html(classes='table table-striped', index=False)
    
    return render_template('result.html', table=df_html) 

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
