import json
import os
import google.generativeai as genai

def handler(event, context):
    # Handle CORS preflight
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "POST, OPTIONS"
    }
    
    if event['httpMethod'] == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': ''
        }

    if event['httpMethod'] != 'POST':
        return {
            'statusCode': 405,
            'headers': headers,
            'body': 'Method Not Allowed'
        }

    try:
        body = json.loads(event['body'])
        text = body.get('text')
        
        if not text:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': 'No text provided'})
            }

        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            # Fallback for when key is missing (so the site doesn't just crash 500)
            return {
                'statusCode': 500,
                'headers': headers,
                'body': json.dumps({'error': 'Server configuration error: Missing API Key'})
            }

        genai.configure(api_key=api_key)
        
        generation_config = {
            "temperature": 0.1,
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

        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(text)
        
        # Parse the JSON response from Gemini
        response_data = json.loads(response.text)

        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(response_data)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }
