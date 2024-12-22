from dotenv import load_dotenv
import os

# load .env file
load_dotenv()

# Load Auth0 configuration from environment variables
AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
API_IDENTIFIER = os.getenv('API_IDENTIFIER')
ALGORITHMS = os.getenv('ALGORITHMS')

DATABASE_URL = os.getenv('DATABASE_URL')

print(f"AUTH0_DOMAIN {AUTH0_DOMAIN}")
print(f"API_IDENTIFIER {API_IDENTIFIER}")
print(f"ALGORITHMS {ALGORITHMS}")
print(f"DATABASE_URL {DATABASE_URL}")