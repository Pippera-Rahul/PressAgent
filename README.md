# PressAgent: Press Kit Generator

An AI-powered tool for automatically generating and reviewing press kits.

## Features

- Collects company information and press kit requirements
- Gathers supplementary data from web searches using SerpAPI
- Generates multiple style options for press releases
- Creates comprehensive press kits including:
  - Press Release
  - Company Overview
  - PR Message
  - Email Draft
  - Supplementary Materials
- Performs quality review with detailed feedback using Anthropic's Claude
- Outputs in multiple formats (Markdown, PDF, text)

## Installation

1. Clone this repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file with your API keys: