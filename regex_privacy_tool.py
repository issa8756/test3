import re
import argparse
import logging

# Setup logging configuration
logging.basicConfig(filename='replacements.log', level=logging.INFO, 
                    format='%(asctime)s - %(message)s')

def replace_patterns(text, find_phone, find_email, find_date):
    # Define regular expressions for each pattern
    phone_pattern = r'\b07\d{8}\b'  # Example pattern for Swedish phone number
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'  # General email pattern
    date_pattern = (
        r'\b(\d{2}[-/]\d{2}[-/]\d{4}|\d{4}[-/]\d{2}[-/]\d{2}|\d{2}/\d{2}/\d{4})\b'
    )  # Multiple date formats: DD-MM-YYYY, YYYY-MM-DD, MM/DD/YYYY, etc.

    replacements_count = {
        'phone': 0,
        'email': 0,
        'date': 0
    }
    
    # Replace patterns based on user options
    if find_phone:
        new_text, count = re.subn(phone_pattern, '"PHONE_NUMBER"', text)
        text = new_text
        replacements_count['phone'] += count

    if find_email:
        new_text, count = re.subn(email_pattern, '"EMAIL_ADDRESS"', text)
        text = new_text
        replacements_count['email'] += count

    if find_date:
        new_text, count = re.subn(date_pattern, '"DATE"', text)
        text = new_text
        replacements_count['date'] += count

    return text, replacements_count

def main():
    # Setup argparse to handle command line arguments
    parser = argparse.ArgumentParser(description="Replace specific patterns in text with predefined words.")
    parser.add_argument("input_file", help="Path to the input text file")
    parser.add_argument("output_file", help="Path to save the modified text file with replacements")
    
    # Add options for patterns to find (phone, email, date)
    parser.add_argument("-p", "--phone", action="store_true", help="Find and replace phone numbers")
    parser.add_argument("-e", "--email", action="store_true", help="Find and replace email addresses")
    parser.add_argument("-d", "--date", action="store_true", help="Find and replace dates")
    
    args = parser.parse_args()
    
    # Read the content of the input text file
    try:
        with open(args.input_file, 'r') as file:
            text = file.read()
    except FileNotFoundError:
        print(f"File {args.input_file} not found.")
        return
    
    # Replace patterns in the text based on user selection
    updated_text, replacements_count = replace_patterns(text, args.phone, args.email, args.date)
    
    # Write the modified content to the output file
    with open(args.output_file, 'w') as file:
        file.write(updated_text)
    
    # Log the changes made
    log_message = f"Replacements made: {replacements_count['email']} email(s), {replacements_count['phone']} phone number(s), {replacements_count['date']} date(s)."
    logging.info(log_message)
    
    print(log_message)
    print(f"Patterns replaced and saved to {args.output_file}")

if __name__ == "__main__":
    main()
