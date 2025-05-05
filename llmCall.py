import os
from dotenv import load_dotenv
# from azure.core.credentials import AzureKeyCredential
# from azure.ai.vision.imageanalysis import ImageAnalysisClient
# from azure.ai.vision.imageanalysis.models import VisualFeatures
import openai
from langchain_openai import AzureChatOpenAI

# Load environment variables
load_dotenv()

azure_openai_key = os.getenv("AZURE_OPENAI_KEY")
azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
azure_openai_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

# #Configure Azure Vision API
# vision_key = os.getenv("AZURE_VISION_KEY")
# vision_endpoint = os.getenv("AZURE_VISION_ENDPOINT")
# Configure OpenAI with Azure settings
openai.api_type = "azure"
openai.api_key = azure_openai_key
openai.api_base = azure_openai_endpoint
openai.api_version = "2024-12-01-preview"

llm = AzureChatOpenAI(
    api_key=azure_openai_key,
    api_version="2024-12-01-preview",
    azure_endpoint=azure_openai_endpoint,
    azure_deployment=azure_openai_deployment,
)
# llm = AzureChatOpenAI(azure_deployment=azure_openai_deployment,
# # api_version="2024-05-01-preview",
# temperature=0,
# max_tokens=None,
# timeout=None,
# max_retries=2,)

def toolCall(prompt, cat=False, QueryCategory=None):
    if cat:

        response = llm.with_structured_output(QueryCategory).invoke(prompt)
        print("RESPONSE ", response)
    else:
        response = llm.invoke(prompt)
        response = response.content

    return response