from langchain_groq import ChatGroq
from src.config import *
from src.utils import *
from src.schema import Person,Data
from src.extractor import prompt
import nest_asyncio


nest_asyncio.apply()

url = ["https://www.iitk.ac.in/me/people/faculty"]

llm = ChatGroq(model=model_name,groq_api_key=GROQ_API_KEY)

docs = load_urls(url)

save_html_content(docs)

docs_transformed = transform_html(docs)

splits=text_split(docs_transformed)

runnable = prompt | llm.with_structured_output(schema=Data)

result = runnable.invoke({"text": splits[2].page_content})

df = create_people_dataframe(result)


Person = namedtuple('Person', ['Name', 'Position', 'Research_interest'])
people_dicts = [{'Name': person.Name, 'Position': person.Position, 'Research_interest': person.Research_interest} for person in result.people]
df = pd.DataFrame(people_dicts)
print(df)

