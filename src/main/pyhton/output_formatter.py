import os
from fpdf import FPDF

def format_as_markdown(data, content, review_result):
    """Format the press kit as Markdown"""
    markdown = f"""# Press Kit: {data['company_info']['name']}

## Press Release: {data['press_kit_info']['topic']}
{content['press_release']}

## Company Overview
{content['company_overview']}

## PR Message
{content['pr_message']}

## Email Draft
{content['email_draft']}

"""
    
    if data['supplementary_data']:
        markdown += "## Supplementary Materials\n"
        for item in data['supplementary_data']:
            markdown += f"- {item['title']} (Source: {item['source']})\n"
    
    markdown += "\n## Quality Review Summary\n"
    for category, score in review_result["scores"].items():
        category_name = " ".join(word.capitalize() for word in category.split("_"))
        markdown += f"- {category_name}: {score}/10\n"
    
    markdown += f"\n### Overall Feedback\n{review_result['overall_feedback']}\n"
    
    return markdown

def format_as_pdf(data, content, review_result):
    """Format the press kit as PDF"""
    pdf = FPDF()
    pdf.add_page()
    
    # Set up font
    pdf.set_font("Arial", "B", 16)
    
    # Title
    pdf.cell(0, 10, f"Press Kit: {data['company_info']['name']}", 0, 1, "C")
    pdf.ln(10)
    
    # Press Release
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, f"Press Release: {data['press_kit_info']['topic']}", 0, 1)
    pdf.set_font("Arial", "", 12)
    
    # Break down the press release into paragraphs to avoid overflow
    paragraphs = content['press_release'].split('\n\n')
    for paragraph in paragraphs:
        pdf.multi_cell(0, 10, paragraph)
        pdf.ln(5)
    pdf.ln(10)
    
    # Company Overview
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Company Overview", 0, 1)
    pdf.set_font("Arial", "", 12)
    
    # Break down the company overview into paragraphs
    paragraphs = content['company_overview'].split('\n\n')
    for paragraph in paragraphs:
        pdf.multi_cell(0, 10, paragraph)
        pdf.ln(5)
    pdf.ln(10)
    
    # PR Message
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "PR Message", 0, 1)
    pdf.set_font("Arial", "", 12)
    
    # Break down the PR message into paragraphs
    paragraphs = content['pr_message'].split('\n\n')
    for paragraph in paragraphs:
        pdf.multi_cell(0, 10, paragraph)
        pdf.ln(5)
    pdf.ln(10)
    
    # Email Draft
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Email Draft", 0, 1)
    pdf.set_font("Arial", "", 12)
    
    # Break down the email draft into paragraphs
    paragraphs = content['email_draft'].split('\n\n')
    for paragraph in paragraphs:
        pdf.multi_cell(0, 10, paragraph)
        pdf.ln(5)
    pdf.ln(10)
    
    # Supplementary Materials
    if data['supplementary_data']:
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Supplementary Materials", 0, 1)
        pdf.set_font("Arial", "", 12)
        for item in data['supplementary_data']:
            pdf.multi_cell(0, 10, f"- {item['title']} (Source: {item['source']})")
        pdf.ln(10)
    
    # Quality Review
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Quality Review Summary", 0, 1)
    pdf.set_font("Arial", "", 12)
    for category, score in review_result["scores"].items():
        category_name = " ".join(word.capitalize() for word in category.split("_"))
        pdf.cell(0, 10, f"{category_name}: {score}/10", 0, 1)
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Overall Feedback:", 0, 1)
    pdf.set_font("Arial", "", 12)
    
    # Break down the overall feedback into paragraphs
    paragraphs = review_result['overall_feedback'].split('\n\n')
    for paragraph in paragraphs:
        pdf.multi_cell(0, 10, paragraph)
        pdf.ln(5)
    
    return pdf

def format_as_text(data, content, review_result):
    """Format the press kit as plain text"""
    text = f"PRESS KIT: {data['company_info']['name']}\n\n"
    
    text += f"PRESS RELEASE: {data['press_kit_info']['topic']}\n"
    text += f"{content['press_release']}\n\n"
    
    text += "COMPANY OVERVIEW\n"
    text += f"{content['company_overview']}\n\n"
    
    text += "PR MESSAGE\n"
    text += f"{content['pr_message']}\n\n"
    
    text += "EMAIL DRAFT\n"
    text += f"{content['email_draft']}\n\n"
    
    if data['supplementary_data']:
        text += "SUPPLEMENTARY MATERIALS\n"
        for item in data['supplementary_data']:
            text += f"- {item['title']} (Source: {item['source']})\n"
        text += "\n"
    
    text += "QUALITY REVIEW SUMMARY\n"
    for category, score in review_result["scores"].items():
        category_name = " ".join(word.capitalize() for word in category.split("_"))
        text += f"{category_name}: {score}/10\n"
    
    text += "\nOVERALL FEEDBACK\n"
    text += f"{review_result['overall_feedback']}\n"
    
    return text

def save_output(data, content, review_result, output_format="markdown"):
    """Save the press kit in the specified format"""
    
    # Create output directory if it doesn't exist
    if not os.path.exists("output"):
        os.makedirs("output")
    
    company_name = data['company_info']['name'].replace(" ", "_").lower()
    file_name = f"press_kit_{company_name}"
    
    if output_format == "markdown":
        markdown_content = format_as_markdown(data, content, review_result)
        with open(f"output/{file_name}.md", "w") as f:
            f.write(markdown_content)
        print(f"\nPress kit saved as output/{file_name}.md")
        return f"output/{file_name}.md"
    
    elif output_format == "pdf":
        pdf = format_as_pdf(data, content, review_result)
        pdf_path = f"output/{file_name}.pdf"
        pdf.output(pdf_path)
        print(f"\nPress kit saved as {pdf_path}")
        return pdf_path
    
    elif output_format == "text":
        text_content = format_as_text(data, content, review_result)
        with open(f"output/{file_name}.txt", "w") as f:
            f.write(text_content)
        print(f"\nPress kit saved as output/{file_name}.txt")
        return f"output/{file_name}.txt"
    
    else:
        print(f"Unsupported output format: {output_format}. Defaulting to markdown.")
        return save_output(data, content, review_result, "markdown")