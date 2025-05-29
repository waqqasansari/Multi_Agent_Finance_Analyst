import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

# API Configuration
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
FINANCIAL_MODELING_PREP_API_KEY = os.getenv("FINANCIAL_MODELING_PREP_API_KEY")