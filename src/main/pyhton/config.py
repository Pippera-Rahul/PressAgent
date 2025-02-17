import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

# Models
GEMINI_MODEL = "gemini-1.0-pro"

# Output formats
OUTPUT_FORMATS = ["markdown", "pdf", "text"]
DEFAULT_FORMAT = "markdown"

# Press kit sections
DEFAULT_SECTIONS = [
    "Press Release",
    "Company Overview",
    "PR Message",
    "Email Draft",
    "Supplementary Materials"
]

# Style options
STYLE_OPTIONS = ["formal", "creative", "professional"]
DEFAULT_STYLE = "professional"