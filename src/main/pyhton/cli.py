import click
from config import OUTPUT_FORMATS, DEFAULT_FORMAT
from data_collector import collect_all_data
from content_generator import generate_all_content
from quality_reviewer import review_press_kit, display_review_report
from output_formatter import save_output

@click.command()
@click.option('--output-format', '-f', type=click.Choice(OUTPUT_FORMATS), default=DEFAULT_FORMAT,
              help='Output format for the press kit')
def main(output_format):
    """PressAgent: Automatic Press Kit Generation and Quality Review"""
    print("\nWelcome to PressAgent: Press Kit Generator\n")
    
    try:
        # Step 1: Collect all necessary data
        data = collect_all_data()
        
        # Step 2: Generate content
        content = generate_all_content(data)
        
        # Step 3: Present final configuration
        print("\n[Final Configuration Confirmation]\n")
        print("[Final Structure Preview]")
        print("- Press Release (Draft)")
        print("- Company Overview")
        print("- PR Message")
        print("- Email Draft")
        if data['supplementary_data']:
            print("- Supplementary Materials")
        
        confirmation = input("\nDo you confirm this final configuration? (Y/N): ")
        if confirmation.upper() != 'Y':
            print("Process cancelled by user.")
            return
        
        # Step 4: Review the generated press kit
        review_result = review_press_kit(content)
        need_modifications = display_review_report(review_result)
        
        if need_modifications:
            print("\nModification functionality would be implemented here in a complete solution.")
            print("For now, we'll proceed with the current version.")
        
        # Step 5: Save the final output
        output_file = save_output(data, content, review_result, output_format)
        print(f"\nPress kit generation complete! File saved at: {output_file}")
    
    except KeyboardInterrupt:
        print("\nProcess interrupted by user. Exiting...")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()