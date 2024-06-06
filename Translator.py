# Import necessary libraries
import os
import gradio as gr
from urllib.request import url2pathname
import googletrans
from googletrans import Translator, LANGUAGES
from PyPDF2 import PdfReader
import warnings

# Ignore user warnings
warnings.filterwarnings("ignore", category=UserWarning)

# Function to save translated text to a file and return the file path
def save_text_to_file(text, file_path, page_num, lang_code, file_name):
    # Create a "Pages" subdirectory in the same directory as the PDF file
    pages_folder = os.path.join(os.path.dirname(file_path), "Pages")
    os.makedirs(pages_folder, exist_ok=True)
    # Construct the output file name using the original file name, page number, and target language
    output_file_name = f"{os.path.splitext(os.path.basename(file_name))[0]}_page_{page_num}_{lang_code}.txt"
    # Construct the output file path by joining the "Pages" subdirectory and the output file name
    output_file_path = os.path.join(pages_folder, output_file_name)
    # Write the translated text to the output file
    with open(output_file_path, "w", encoding='utf-8') as output_file:
        output_file.write(text)
    # Return the output file path so that it can be used later for downloading etc.
    return output_file_path

# Function to extract and translate text from a PDF or TXT file or a sentence.
def extract_and_translate_text(text_or_file_path, start_page=0, end_page=0, target_lang='English', download=False, file_name=""):
    """Extract and translate text from a PDF or TXT file or a text sentence."""
    
    # Check if the input is a file path or a text sentence
    if not text_or_file_path:
        return "Error: Please provide a text sentence or a file path."
    
    # If the input is a file path...
    if os.path.isfile(text_or_file_path):
        # Convert the file path to a format that can be used by PyPDF2
        file_path = url2pathname(text_or_file_path.strip('\"')) if text_or_file_path.startswith('file://') else text_or_file_path
        # Get the file extension
        file_extension = os.path.splitext(file_path)[1].lower()

        # If the file is a PDF...
        if file_extension == '.pdf':
            # Open the PDF file
            with open(file_path, 'rb') as pdf_file:
                # Create a PDF reader object
                pdf_reader = PdfReader(pdf_file)
                # Initialize the translated text to an empty string
                translated_text = ""

                # Loop through the specified pages in the PDF file
                for page_num in range(start_page, end_page + 1):
                    # Extract the text from the current page
                    page = pdf_reader.pages[page_num]
                    text = page.extract_text()
                    # Translate the text to the target language using the Google Translate API
                    try:
                        translated_page_text = Translator().translate(text, dest=target_lang).text
                    except googletrans.exceptions.GoogleTranslateError:
                        return "Error: Google Translate timed out. Please try again."

                    # If the download option is selected, save the translated text to a file
                    if download:
                        save_text_to_file(translated_page_text, file_path, page_num, target_lang, file_name)

                    # Add the translated text to the overall translated text string
                    translated_text += f"Page {page_num}:\n\n{translated_page_text}\n\n---\n\n"

        # TXT file handling...
        elif file_extension == '.txt':
            # Open the TXT file and read its contents
            with open(file_path, 'r', encoding='utf-8') as txt_file:
                text = txt_file.read()
                # Translate the text to the target language using the Google Translate API
                try:
                    translated_text = Translator().translate(text, dest=target_lang).text
                except googletrans.exceptions.GoogleTranslateError:
                    return "Error: Google Translate timed out. Please try again."

                # If the download option is selected, save the translated text to a file
                if download:
                    save_text_to_file(translated_text, file_path, 0, target_lang, file_name)
        else:
            # If the file type is unsupported, return an error message
            return "Error: Unsupported file type. Please provide a PDF or TXT file."
        
    # If the input is a text sentence...
    else:
        text = text_or_file_path
        # Translate the text to the target language using the Google Translate API
        try:
            translated_text = Translator().translate(text, dest=target_lang).text
        except googletrans.exceptions.GoogleTranslateError:
            return "Error: Google Translate timed out. Please try again."

    # Return the translated text to the interface as an output
    return translated_text

# get a list of all languages for use by the user interface drop down selection input
language_choices = list(LANGUAGES.values())

# Create a Gradio interface with the extract_and_translate_text() function as the backend function
iface = gr.Interface(
    fn=extract_and_translate_text,
    # Specify the input types and labels for the Gradio interface
    inputs=[
        gr.inputs.Textbox(label='Enter a PDF or TXT file path from your local drive or "Paste" in a sentence...)'),
        gr.inputs.Slider(label='Start page (PDF only)', minimum=0, maximum=100, step=1, default=0),
        gr.inputs.Slider(label='End page (PDF only)', minimum=0, maximum=100, step=1, default=0),
        gr.inputs.Dropdown(label='Please choose translation language from list:', choices=language_choices, default='English'),
        gr.inputs.Checkbox(label="Would you like to download the translation?", default=False),
        gr.inputs.Textbox(label='Would you like to add a prefix to the file(s)', default="")
    ],
    # Specify the output types and labels for the Gradio interface
    outputs=[   
        gr.outputs.Textbox(label='Extracted and Translated Text')
    ],
    # Specify the title and description for the Gradio interface
    title='💥 Universal PDF/Text Translator 💥',
    description='Extract and translate from PDF or TXT files as well as a cut and paste snippit.',
    # Disable the "flag" button for reporting inappropriate content
    allow_flagging=False,
    # Example file for testing
    examples=[
        ['example.pdf', 1, 1, 'French', False, '']
    ],
)

# Launch the Gradio interface if the script is run as the main program
if __name__ == '__main__':
    iface.launch()
