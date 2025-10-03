import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define variables
ECOSYSTEM = os.getenv('ECOSYSTEM')
CHECK_SINGLE_PACKAGE = os.getenv('CHECK_SINGLE_PACKAGE')
CHECK_MULTIPLE_PACKAGES = os.getenv('CHECK_MULTIPLE_PACKAGES')
