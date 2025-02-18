import os
from dotenv import load_dotenv

load_dotenv()

# SecurityService URL (for inter-service communication)
SECURITY_SERVICE_URL = os.getenv("SECURITY_SERVICE_URL")