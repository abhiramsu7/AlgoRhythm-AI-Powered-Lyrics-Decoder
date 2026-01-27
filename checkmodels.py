from google import genai

# PASTE YOUR *NEW* KEY HERE
client = genai.Client(api_key="AIzaSyCWao1Xy93vza5a4g7y_vW08Eh_3DEoXYA")

print("--- AVAILABLE MODELS ---")
try:
    # We are just going to print the name directly. No filtering.
    for model in client.models.list():
        print(f"Found: {model.name}")
            
except Exception as e:
    print(f"Error: {e}")