import os
import sys
from dotenv import load_dotenv, find_dotenv
from google import genai
from google.genai import types

# 1. SETUP: Load environment variables securely
# Use find_dotenv() to ensure it locates your .env file in the project root
load_dotenv(find_dotenv(), override=True)

api_key = os.getenv("GEMINI_API_KEY")

# Strict Honesty Check: Stop immediately if the API key is missing
if not api_key:
    print("ERROR: GEMINI_API_KEY not found in .env file.")
    sys.exit(1)

# Initialize the Gemini 2.0/3 client
client = genai.Client(api_key=api_key)

def run_carbon_audit(file_name):
    """
    Orchestrates the Marathon Agent loop: Sense -> Reason -> Act.
    """
    # 2. SENSOR LAYER: Handle file paths and upload
    # Resolve the absolute path to prevent 'File Not Found' errors
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, file_name)

    if not os.path.exists(file_path):
        print(f"ERROR: The file '{file_name}' was not found in {base_dir}")
        return

    try:
        print(f"Sensing data from: {file_name}...")
        
        # CHANGE THIS LINE: Add the config with 'text/csv'
        uploaded_file = client.files.upload(
            file=file_path,
            config={'mime_type': 'text/csv'} # Explicitly sets the correct type
        )
        # 3. REASONING LAYER: Marathon Agent Logic
        print("Reasoning through logistics path (this may take a moment)...")
        
        # Use the correct Config object for Gemini 3
        # This enables 'Thought Signatures' as per your Project Doc
        config = types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(include_thoughts=True)
        )

        response = client.models.generate_content(
            model="gemini-3-pro-preview", 
            contents=[
                "Acting as the Carbon Ledger Auditor, perform a deep audit on this file. "
                "Follow your core principles: Strict Honesty, No Sugar-coating, and Action Logic. "
                "Identify top carbon liabilities and output a Carbon Correction Plan in JSON format.",
                uploaded_file
            ],
            config=config # Pass the validated object here
        )
        # 4. ACTION LAYER: Output the results
        print("\n" + "="*30)
        print("CARBON LEDGER AUDIT RESULT")
        print("="*30)
        print(response.text)

    except Exception as e:
        print(f"An error occurred during the audit: {e}")

# 5. EXECUTION: This turns the script 'ON'
if __name__ == "__main__":
    # Ensure you have created 'test_audit.csv' in the same folder as this script
    run_carbon_audit("test_audit.csv")