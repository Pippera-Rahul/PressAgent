import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_MODEL, STYLE_OPTIONS

# Configure the Gemini API
genai.configure(api_key=GEMINI_API_KEY)

def get_gemini_model():
    """Get the Gemini model instance"""
    return genai.GenerativeModel(GEMINI_MODEL)

def generate_press_release(data, style="professional"):
    """Generate press release draft using Gemini"""
    model = get_gemini_model()
    
    prompt = f"""
    Generate a press release for {data['company_info']['name']} about {data['press_kit_info']['topic']}.
    
    Company Information:
    - Name: {data['company_info']['name']}
    - Product/Service: {data['company_info']['product']}
    - Achievements: {data['company_info']['achievements']}
    - Brand Attributes: {data['company_info']['brand_attributes']}
    
    Target Media: {data['press_kit_info']['target_media']}
    Desired Tone: {data['press_kit_info']['tone']}
    Style: {style}
    
    Include any relevant supplementary data:
    {[item['title'] for item in data['supplementary_data']]}
    """
    
    response = model.generate_content(prompt)
    
    return response.text

def generate_company_overview(data):
    """Generate company overview using Gemini"""
    model = get_gemini_model()
    
    prompt = f"""
    Write a comprehensive company overview for {data['company_info']['name']}.
    
    Include information about:
    - Their flagship product/service: {data['company_info']['product']}
    - Major achievements: {data['company_info']['achievements']}
    - Brand attributes: {data['company_info']['brand_attributes']}
    
    Make it professional and informative, suitable for a press kit.
    """
    
    response = model.generate_content(prompt)
    
    return response.text

def generate_pr_message(data):
    """Generate PR message using Gemini"""
    model = get_gemini_model()
    
    prompt = f"""
    Write a concise PR message for {data['company_info']['name']} regarding {data['press_kit_info']['topic']}.
    
    The message should be suitable for {data['press_kit_info']['target_media']} and use a {data['press_kit_info']['tone']} tone.
    
    Keep it brief but impactful.
    """
    
    response = model.generate_content(prompt)
    
    return response.text

def generate_email_draft(data):
    """Generate email draft using Gemini"""
    model = get_gemini_model()
    
    prompt = f"""
    Write an email draft that could be sent to media contacts about {data['press_kit_info']['topic']} for {data['company_info']['name']}.
    
    Target: {data['press_kit_info']['target_media']}
    Tone: {data['press_kit_info']['tone']}
    
    Include a brief introduction, the key points about the announcement, and contact information placeholder.
    """
    
    response = model.generate_content(prompt)
    
    return response.text

def generate_style_options(data):
    """Generate multiple style options for press release"""
    style_drafts = {}
    
    for style in STYLE_OPTIONS:
        print(f"\nGenerating {style} draft...")
        draft = generate_press_release(data, style)
        preview = draft.split('\n\n')[0] if '\n\n' in draft else draft[:200] + "..."
        
        style_drafts[style] = {
            "full_text": draft,
            "preview": preview
        }
    
    return style_drafts

def present_style_options(style_drafts):
    """Present style options to user and get selection"""
    print("\n[Draft Previews]\n")
    
    for style, content in style_drafts.items():
        print(f"[Draft Preview – Style: {style.capitalize()}]")
        print(content["preview"])
        print("\n")
    
    selected_style = input("Which style do you prefer? (Enter style name or 'request modification'): ")
    
    if selected_style.lower() == 'request modification':
        modification = input("What modifications would you like to request? ")
        return "request_modification", modification
    
    if selected_style.lower() in [s.lower() for s in STYLE_OPTIONS]:
        for style in STYLE_OPTIONS:
            if style.lower() == selected_style.lower():
                return style, style_drafts[style]["full_text"]
    
    print("Invalid selection. Please try again.")
    return present_style_options(style_drafts)

def generate_all_content(data):
    """Generate all content for the press kit"""
    # Generate and present style options for press release
    style_drafts = generate_style_options(data)
    selected_style, press_release = present_style_options(style_drafts)
    
    if selected_style == "request_modification":
        # Handle modification request
        print(f"Applying requested modifications: {press_release}")
        # In a real implementation, you would modify the draft based on the request
        style_drafts = generate_style_options(data)
        selected_style, press_release = present_style_options(style_drafts)
    
    # Generate other content
    company_overview = generate_company_overview(data)
    pr_message = generate_pr_message(data)
    email_draft = generate_email_draft(data)
    
    content = {
        "press_release": press_release,
        "company_overview": company_overview,
        "pr_message": pr_message,
        "email_draft": email_draft,
        "selected_style": selected_style
    }
    
    return content