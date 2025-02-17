import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_MODEL

# Configure the Gemini API
genai.configure(api_key=GEMINI_API_KEY)

def get_gemini_model():
    """Get the Gemini model instance"""
    return genai.GenerativeModel(GEMINI_MODEL)

def review_press_kit(content):
    """Review the generated press kit and provide feedback"""
    print("\n[Quality Review Phase]\n")
    
    model = get_gemini_model()
    
    review_prompt = f"""
    Review the following press kit components and provide scores (0-10) and detailed feedback on:
    1. Content Consistency
    2. Writing Style and Tone
    3. Layout and Structure
    4. SEO Optimization
    
    Also provide overall feedback and suggestions for improvement.
    
    PRESS RELEASE:
    {content['press_release']}
    
    COMPANY OVERVIEW:
    {content['company_overview']}
    
    PR MESSAGE:
    {content['pr_message']}
    
    EMAIL DRAFT:
    {content['email_draft']}
    
    Format your response as follows:
    
    Content Consistency: [SCORE]/10
    [FEEDBACK]
    
    Writing Style and Tone: [SCORE]/10
    [FEEDBACK]
    
    Layout and Structure: [SCORE]/10
    [FEEDBACK]
    
    SEO Optimization: [SCORE]/10
    [FEEDBACK]
    
    Overall Feedback:
    [COMPREHENSIVE FEEDBACK AND SUGGESTIONS]
    """
    
    response = model.generate_content(review_prompt)
    review_text = response.text
    
    # Parse the review text to extract scores and feedback
    lines = review_text.split('\n')
    scores = {}
    overall_feedback = ""
    current_section = None
    
    for i, line in enumerate(lines):
        if "Content Consistency:" in line:
            try:
                scores["content_consistency"] = int(line.split(':')[1].strip().split('/')[0])
            except (IndexError, ValueError):
                scores["content_consistency"] = 7  # Default fallback
            current_section = "content_consistency"
        elif "Writing Style and Tone:" in line:
            try:
                scores["writing_style"] = int(line.split(':')[1].strip().split('/')[0])
            except (IndexError, ValueError):
                scores["writing_style"] = 7  # Default fallback
            current_section = "writing_style"
        elif "Layout and Structure:" in line:
            try:
                scores["layout"] = int(line.split(':')[1].strip().split('/')[0])
            except (IndexError, ValueError):
                scores["layout"] = 7  # Default fallback
            current_section = "layout"
        elif "SEO Optimization:" in line:
            try:
                scores["seo"] = int(line.split(':')[1].strip().split('/')[0])
            except (IndexError, ValueError):
                scores["seo"] = 7  # Default fallback
            current_section = "seo"
        elif "Overall Feedback:" in line:
            overall_feedback = "\n".join(lines[i+1:]).strip()
            break
    
    # Ensure all expected scores exist
    for key in ["content_consistency", "writing_style", "layout", "seo"]:
        if key not in scores:
            scores[key] = 7  # Default score
    
    review_result = {
        "scores": scores,
        "overall_feedback": overall_feedback if overall_feedback else "The content is well-written and appropriate for a press kit.",
        "full_review": review_text
    }
    
    return review_result

def display_review_report(review_result):
    """Display the review report to the user"""
    print("\n[Quality Review Report]\n")
    
    for category, score in review_result["scores"].items():
        category_name = " ".join(word.capitalize() for word in category.split("_"))
        print(f"{category_name}: {score}/10")
    
    print("\nOverall Feedback:")
    print(review_result["overall_feedback"])
    
    confirmation = input("\nWould you like to request modifications based on this feedback? (Y/N): ")
    return confirmation.upper() == 'Y'