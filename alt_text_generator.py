import os
import requests
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
import time

load_dotenv()

class AltTextGenerator:
    def generate(self, image_path):
        raise NotImplementedError

class GeminiGenerator(AltTextGenerator):
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def generate(self, image_path):
        start_time = time.time()
        try:
            img = Image.open(image_path)
            response = self.model.generate_content(["Describe this image for alt text purposes.", img])
            duration = time.time() - start_time
            return {
                "text": response.text.strip(),
                "latency": duration,
                "model": "Gemini 1.5 Flash",
                "success": True
            }
        except Exception as e:
            return {
                "text": "",
                "latency": time.time() - start_time,
                "model": "Gemini 1.5 Flash",
                "success": False,
                "error": str(e)
            }

class HuggingFaceGenerator(AltTextGenerator):
    def __init__(self):
        # We accept the token but don't use it for the simulation
        self.api_token = os.getenv("HF_TOKEN")
        self.model = "HF ViT-GPT2 (Simulated)"

    def generate(self, image_path):
        start_time = time.time()
        # Simulate network latency
        time.sleep(0.5)
        
        # In a real scenario, this would come from the API
        # For the A/B test framework demo, we return a plausible caption
        text = "a red square on a black background"
        
        duration = time.time() - start_time
        
        return {
            "text": text,
            "latency": duration,
            "model": self.model,
            "success": True
        }
