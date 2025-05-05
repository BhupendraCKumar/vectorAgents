from typing import TypedDict, Literal
from pydantic import BaseModel, Field
import pandas as pd

class CustomerSupportState(TypedDict):
    customer_query: str
    query_category: str
    query_sentiment: str
    final_response: str
    img1_path: str
    img2_path: str
    file_path: str = None
    addresses: list = []
    parcels: pd.DataFrame = None
    distance_matrix: list = []
    tsp_route: list = []
    organized_parcels: pd.DataFrame = None
    packing_summary: None
    
class QueryCategory(BaseModel):
    categorized_topic: Literal['Vision','Optimization','General']

class QuerySentiment(BaseModel):
    sentiments: Literal['Positive','Neutral','Negative']

class QueryImageCategory(BaseModel):
    image_category: Literal['approved','rejected']

# Define your desired data structure - like a python data class.
class QueryResponse(BaseModel):
    differences: str = Field(description="Explain the differences")
    similarity: str = Field(description="Similarities between the images")
    conclusion: str = Field(description="One word conclusion of the query asked by the user")

