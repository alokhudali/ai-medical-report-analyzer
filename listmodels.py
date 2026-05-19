from google import genai

# Create client with your API key
client = genai.Client(api_key="AIzaSyDNpzYcOQihFM4Gil668tBsvFGf70fNIrY")

# List all available models
for model in client.models.list():
    print(f"Name: {model.name}")
    
    # Some models may not expose supported actions
    if hasattr(model, "supported_actions"):
        print(f"Capabilities: {model.supported_actions}")
    
    print("-" * 20)