import openai
import time

with open('openaiapikey.txt', 'r') as infile:
    open_ai_api_key = infile.read()
openai.api_key = open_ai_api_key

def check_fine_tune_status(fine_tune_id):
    fine_tune = openai.FineTune.retrieve(fine_tune_id)
    return fine_tune.status

# Usage example
fine_tune_id = 'ft-LlSfG2m91xkQFooBCINocuFA'  # Replace this with your fine-tuning job ID
status = check_fine_tune_status(fine_tune_id)
print(f"The fine-tuning job status is: {status}")
