import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("Error: GEMINI_API_KEY not found in environment variables or .env file.")
    print("Please create a .env file with GEMINI_API_KEY=your_key_here")
    exit(1)

genai.configure(api_key=API_KEY)

generation_config = {
  "temperature": 0.1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "application/json",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  system_instruction="""You are an aggressive but professional Special Education Attorney. Your goal is to analyze IEP drafts for parents and identify weak, vague, or legally unenforceable language. You are on the parent's side.

Input: A section of an IEP (goals, accommodations, etc.).
Output: A JSON object with three keys:
1. 'red_flags': A list of strings. Identify specific phrases that are 'weasel words' (e.g., 'try', 'attempt', 'encouraged', 'as needed', 'opportunities to'). Explain WHY it is bad in one sentence.
2. 'fixes': A list of objects. Each object should have 'original_text' and 'rewritten_text'. Rewrite the goals to be SMART (Specific, Measurable, Achievable, Relevant, Time-bound). Use concrete numbers and removal of vague qualifiers.
3. 'action_plan': A short, professional email draft to the Case Manager from the parent, politely but firmly requesting these changes, referencing that the current goals are not 'reasonably calculated to enable the child to make progress appropriate in light of the child's circumstances' (Endrew F. standard)."""
)

def analyze_iep(text):
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(text)
    return response.text

if __name__ == "__main__":
    try:
        with open("bad_iep.txt", "r") as f:
            iep_text = f.read()
            
        print("Analyzing IEP...")
        analysis = analyze_iep(iep_text)
        print(analysis)
        
        # Save to file for inspection
        with open("analysis_result.json", "w") as f:
            f.write(analysis)
            
    except FileNotFoundError:
        print("Error: bad_iep.txt not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
