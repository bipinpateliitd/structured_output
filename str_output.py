from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from pprint import pprint
from typing import Optional,Annotated,TypedDict
from langchain_core.output_parsers import StrOutputParser
import base64

load_dotenv()

llm_image = ChatOpenAI(model="gpt-4o-mini")


file_path =input("Enter the image path :")



def load_png_as_base64(file_path):
    with open(file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        return encoded_string.decode("utf-8")
    
image_url = load_png_as_base64(file_path)

image_message=HumanMessage(
    content=[
        {"type": "text", "text": "Extract the text from the  image"},
        {
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{image_url}"},
        },
    ],
    )
response = llm_image.invoke([image_message])
parsed_response = StrOutputParser().invoke(response.content)
print(parsed_response)

llm2 = ChatOpenAI(model="gpt-4o-mini")

class Data_Extraction(TypedDict):
    name: str
    age: int
    id_type: Annotated[str, "Return the type of ID either passport, Adhhar, driving license, pancard,voterid, company id, school id, other"]
    id_number: Optional[str]
    address: Optional[str]
    phone_number: Optional[int]
    email: Optional[str]
    date_of_birth: Optional[str]

llm_with_structured_output = llm2.with_structured_output(Data_Extraction)

structured_response = llm_with_structured_output.invoke(parsed_response)

pprint("Structured Response:")
pprint(structured_response)

