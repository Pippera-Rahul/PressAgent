import json
import requests
from serpapi import GoogleSearch
from config import SERPAPI_API_KEY

def collect_company_info():
    """Collect company information from user input"""
    print("\n[User Input Stage]\n")
    company_info = {
        "name": input("Company Name: "),
        "product": input("Flagship Product/Service: "),
        "achievements": input("Major Achievements: "),
        "brand_attributes": input("Brand Attributes: ")
    }
    
    # Mid-verification phase
    print("\nCompany Information Summary:")
    for key, value in company_info.items():
        print(f"{key.capitalize()}: {value}")
    
    confirmation = input("\nIs the above information correct? (Y/N): ")
    if confirmation.upper() != 'Y':
        print("Please re-enter the information.")
        return collect_company_info()
    
    return company_info

def collect_press_kit_topic():
    """Collect press kit topic and preferences"""
    press_kit_info = {
        "topic": input("Press Kit Topic: "),
        "target_media": input("Target Media: "),
        "tone": input("Tone (e.g., professional, formal, creative): ")
    }
    
    # Mid-verification phase
    print("\nPress Kit Information Summary:")
    for key, value in press_kit_info.items():
        print(f"{key.capitalize()}: {value}")
    
    confirmation = input("\nIs the above information correct? (Y/N): ")
    if confirmation.upper() != 'Y':
        print("Please re-enter the information.")
        return collect_press_kit_topic()
    
    return press_kit_info

def search_supplementary_data(company_name, topic):
    """Search for supplementary data using SerpAPI"""
    print("\n[Supplementary Data Collection]\n")
    
    print(f"Searching for latest news about {company_name} and {topic}...")
    
    # Use SerpAPI to search for news
    params = {
        "engine": "google_news",
        "q": f"{company_name} {topic}",
        "api_key": SERPAPI_API_KEY,
        "num": 3  # Limit to 3 results
    }
    
    search = GoogleSearch(params)
    results = search.get_dict()
    
    supplementary_data = []
    if "news_results" in results and results["news_results"]:
        for item in results["news_results"][:2]:  # Take only first 2 results
            supplementary_data.append({
                "title": item["title"],
                "source": item["source"]
            })
    
    # If no results found or error occurred, use dummy data
    if not supplementary_data:
        supplementary_data = [
            {
                "title": f"{company_name} is gaining significant attention in the global market.",
                "source": "Example News"
            },
            {
                "title": f"New innovation drives data innovation at {company_name}.",
                "source": "Tech Daily"
            }
        ]
    
    # Display summary
    print("\n[Supplementary Data Summary]")
    for item in supplementary_data:
        print(f'"{item["title"]}" (Source: {item["source"]})')
    
    confirmation = input("\nDo you want to include this supplementary data in the Press Kit? (Y/N): ")
    if confirmation.upper() == 'Y':
        return supplementary_data
    return []

def collect_all_data():
    """Main function to collect all required data"""
    company_info = collect_company_info()
    press_kit_info = collect_press_kit_topic()
    supplementary_data = search_supplementary_data(company_info["name"], press_kit_info["topic"])
    
    # Combine all data
    all_data = {
        "company_info": company_info,
        "press_kit_info": press_kit_info,
        "supplementary_data": supplementary_data
    }
    
    return all_data
