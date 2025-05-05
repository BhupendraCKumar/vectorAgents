
import requests, base64
import cv2
# from langchain_core.output_parsers import PydanticOutputParser
# from typing import Dict
from supportUDFs import CustomerSupportState

# Set up a parser + inject instructions into the prompt template.
# parser = PydanticOutputParser(pydantic_object=QueryResponse)

def analyze_images(state: CustomerSupportState)->CustomerSupportState:
  
  cv2.imwrite(r".\temp1.png",cv2.resize(cv2.imread(state["img1_path"]),(100,100)))
  cv2.imwrite(r".\temp2.png",cv2.resize(cv2.imread(state["img2_path"]),(100,100)))

  invoke_url = "https://integrate.api.nvidia.com/v1/chat/completions"
  stream = True

  with open(r".\temp1.png", "rb") as f:
    image1_b64 = base64.b64encode(f.read()).decode()
  # print(len(image1_b64))
  assert len(image1_b64) < 180_000, \
    "To upload larger images, use the assets API (see docs)"
    
  with open(r".\temp2.png", "rb") as f:
    image2_b64 = base64.b64encode(f.read()).decode()
  # print(len(image1_b64))
  assert len(image2_b64) < 180_000, \
    "To upload larger images, use the assets API (see docs)"
  

  headers = {
    "Authorization": "Bearer <API TOKEN>",
    "Accept": "text/event-stream" if stream else "application/json"
  }

  payload = {
    "model": 'meta/llama-4-maverick-17b-128e-instruct',
    "messages": [
      {
        "role": "user",
        "content": f'''You are a quality check agent. Your job is to reject or accept the product manufactured.
                Consider the first image as good quality image. Find the differences in the second image
          compare the edges similarity, color similarity(consider the fact it can be in different lighting condition).
           Finally return the output as discarded or accepted. 
            Discarded: If the difference is huge on the edges/curves.
            Accepted: If Minor/No differences on the color. 
            Input images: <img src="data:image/png;base64,{image1_b64}" /> <img src="data:image/png;base64,{image2_b64}" />
            Output must be in a dictionary format with keys as shown below:
               description : Descritption
               differences: Explain the differences
               similarity': Explanation of similarity
               conclusion': Single word conclussion. approved or rejected
            NOTE: No coding/technical details must be mentioned
            '''
      }
    ],
    "max_tokens": 512,
    "temperature": 1.00,
    "top_p": 1.00,
    "stream": stream
  }

  response = requests.post(invoke_url, headers=headers, json=payload)
  import json
  resp = ''
  if stream:
      for line in response.iter_lines():
          if line:
              try:
                  l = line.decode()
                  d = json.loads(l[l.index('{'):])
                  resp+=d['choices'][0]['delta']['content']
              except Exception as e:
                  continue
          
  else:
      print(response.json())
  state["final_response"] = resp
  
  return state
