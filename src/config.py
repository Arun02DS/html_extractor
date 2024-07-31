from dotenv import load_dotenv
import os


load_dotenv()

GROQ_API_KEY = os.environ.get('GROQ_API_KEY')


model_name="mixtral-8x7b-32768"
chunk_size = 1000
chunk_overlap = 0