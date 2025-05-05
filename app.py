from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging
from dotenv import load_dotenv
import io
from PIL import Image
# from azure.core.credentials import AzureKeyCredential
# from azure.ai.vision.imageanalysis import ImageAnalysisClient
# from azure.ai.vision.imageanalysis.models import VisualFeatures
# import openai
# from langchain_openai import AzureChatOpenAI
from agentFlow import compiled_carbon_emmission_agent
from supportUDFs import CustomerSupportState
import uuid
import pandas as pd
# from llmCall import toolCall

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# azure_openai_key = os.getenv("AZURE_OPENAI_KEY")
# azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
# azure_openai_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

# #Configure Azure Vision API
# vision_key = os.getenv("AZURE_VISION_KEY")
# vision_endpoint = os.getenv("AZURE_VISION_ENDPOINT")
# # Configure OpenAI with Azure settings
# openai.api_type = "azure"
# openai.api_key = azure_openai_key
# openai.api_base = azure_openai_endpoint
# openai.api_version = "2024-12-01-preview"

# llm = AzureChatOpenAI(azure_deployment=azure_openai_deployment,
# # api_version="2024-05-01-preview",
# temperature=0,
# max_tokens=None,
# timeout=None,
# max_retries=2,)

# Global variables
UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER,exist_ok=True)

@app.route('/api/chat', methods=['POST'])
def langgraph_chat():
    # try:
        # Capture Data
        csv_file = request.files.get('csv_file')
        # file1 = request.files['image1'].read()
        # file2 = request.files['image2'].read()
        file1 = request.files.get('image1')
        file2 = request.files.get('image2')
        query = request.form.get("query")

        # print("FILE 1 : ",file1)
        # # convert bytes to image
       

        #Initialization of states
        img1_path = None
        img2_path = None
        csv_path = None
        addresses = []
        # print(query)
        if csv_file and csv_file.filename:
            csv_path = os.path.join(UPLOAD_FOLDER, csv_file.filename)
            csv_file.save(csv_path)
            df = pd.read_csv(csv_path)
            addresses = df['address'].dropna().to_list()
            
        # Save Image 1 if present
        # print("IMAGE NAMES : ", image1.filename, image2.filename)
        if file1 and file1.filename:
            image1 = Image.open(io.BytesIO(file1.read()))
        
            img1_path = os.path.join(UPLOAD_FOLDER, file1.filename)
            image1 = image1.convert('RGB')
            print("IMAGE 1 Path : ", img1_path)
            image1.save(img1_path)
           

        # Save Image 2 if present
        if file2 and file2.filename:
            image2 = Image.open(io.BytesIO(file2.read()))
            img2_path = os.path.join(UPLOAD_FOLDER, file2.filename)
            image2 = image2.convert("RGB")
            image2.save(img2_path)

        if not query:
            return jsonify({"error": "No message provided"}), 400

        # Initialize LangGraph state
        state = CustomerSupportState(
            customer_query=query,
            query_category="",
            query_sentiment="",
            final_response="",
            img1_path=img1_path,
            img2_path=img2_path,
            file_path=csv_path,
            addresses=addresses,
            parcels=None,
            distance_matrix=[],
            tsp_route=[],
            organized_parcels=None,
            packing_summary=None,
        )
        # print("STATE : ", state)
        # Run the LangGraph workflow
        final_state = compiled_carbon_emmission_agent.invoke(
            state,
            config={"configurable": {"thread_id": f"user-session-{str(uuid.uuid4())}"}})

        print("FINAL RESPONSE : ",final_state["final_response"])
        return jsonify({
            "response": final_state.get("final_response"),
        })

    # except Exception as e:
    #     logger.error(f"Error in langgraph endpoint: {str(e)}")
    #     return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    # if not all([azure_openai_key, azure_openai_endpoint, azure_openai_deployment, 
    #             vision_key, vision_endpoint]):
        # logger.warning("Some Azure credentials are missing. Please set them in .env file.")
    
    app.run(debug=True, port=5000)
