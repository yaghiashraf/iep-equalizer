import sys
import json
import random
import time
from alt_text_generator import GeminiGenerator, HuggingFaceGenerator
import os

LOG_FILE = "ab_test_logs.json"

def load_logs():
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def save_log(entry):
    logs = load_logs()
    logs.append(entry)
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)

def main():
    image_path = "test_image.jpg"
    if len(sys.argv) > 1:
        image_path = sys.argv[1]

    if not os.path.exists(image_path):
        print(f"Error: Image {image_path} not found.")
        return

    print(f"--- A/B Test Experiment Runner ---")
    print(f"Image: {image_path}")

    # Initialize generators
    generators = []
    try:
        generators.append(GeminiGenerator())
    except Exception as e:
        print(f"Warning: Gemini Generator not available: {e}")

    try:
        generators.append(HuggingFaceGenerator())
    except Exception as e:
        print(f"Warning: HF Generator not available: {e}")

    if not generators:
        print("No generators available. Check your .env file.")
        return

    # Randomly select one model to simulate A/B serving
    # In a real app, this would be determined by a user ID or session hash
    selected_gen = random.choice(generators)
    
    print(f"Selected Model: {selected_gen.model}")
    print("Generating...")
    
    result = selected_gen.generate(image_path)
    
    if result["success"]:
        print(f"\nGenerated Alt Text: \"{result['text']}\" ")
        print(f"Latency: {result['latency']:.4f}s")
        
        # Simulating User Feedback
        print("\n[User Simulation] Is this text accurate? (y/n)")
        user_input = input("> ").strip().lower()
        conversion = 1 if user_input == 'y' else 0
        
        log_entry = {
            "timestamp": time.time(),
            "model": result["model"],
            "image": image_path,
            "generated_text": result["text"],
            "latency": result["latency"],
            "conversion": conversion
        }
        save_log(log_entry)
        print("Data logged.")
    else:
        print(f"Generation failed: {result.get('error')}")

if __name__ == "__main__":
    main()
