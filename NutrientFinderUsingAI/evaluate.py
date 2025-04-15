import google.generativeai as genai 
from app.models import APIKey

api_key = APIKey.objects.last().key  

genai.configure(api_key=api_key)

def upload_file(path,mime_type=None):
	file = genai.upload_file(path,mime_type=mime_type)
	return file


generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config,
) 

def generate_nutrient(path):
    files = [upload_file(path, mime_type='image/png')]

    response = model.generate_content([
        files[0],
        """
        You are a professional nutrition analyst.
        Look at the attached food image carefully and:
        - Identify the food name.
        - Provide a JSON output with the following format:
        {
            "food_name": "<name>",
            "fat": "<value in grams>",
            "protein": "<value in grams>",
            "carbohydrates": "<value in grams>",
            "calories": "<approximate value>",
            "additional_notes": "<any special ingredients or insights>"
        }
        """

































        
    ])

    return response.text
