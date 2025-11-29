"""Example: Using multiple AI services"""

from zektra import ZektraGateway

gateway = ZektraGateway()

# List available services
print("Available Services:")
print("="*60)
services = gateway.get_available_services()
for name, info in services.items():
    print(f"{name}: {'Available' if info.available else 'Not configured'}")

# Query different services
prompt = "What is homomorphic encryption?"

print("\n" + "="*60)
print("Querying DeepSeek...")
print("="*60)
try:
    response = gateway.query_deepseek(prompt=prompt, payment_token="ZEKTRA")
    print(f"Response: {response.text[:200]}...")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "="*60)
print("Querying OpenAI...")
print("="*60)
try:
    response = gateway.query_openai(prompt=prompt, payment_token="ZEKTRA")
    print(f"Response: {response.text[:200]}...")
except Exception as e:
    print(f"Error: {e}")

