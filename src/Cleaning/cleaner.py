import subprocess
import os


def clean_pdf_to_md(
        doc_path : str, 
        export_path : str,
        start_page : int = 2,       # Optional: page that the cleaning will start on
        batch_multiplier: int = 2,  # Optional: how much to multiply default batch sizes by if you have extra VRAM
        max_pages: int = 5,         # Optional: max number of pages to clean
        langs: str = 'en'           # Optional: languages that the pdf contains (multiple separated by commas)
    ) -> str:


    # Check if pdf has already been cleaned
    if os.path.exists(export_path):
        return f'Duplicate: pdf has already been cleaned at: {export_path}'

    if not os.path.exists(doc_path):
        raise FileNotFoundError(f"The input document path does not exist: {doc_path}")

    command = f'marker_single "{doc_path}" "{export_path}" --batch_multiplier {batch_multiplier} --start_page {start_page} --langs {langs} --max_pages {max_pages}'
    
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Print stdout line by line
    for line in process.stdout:
        print(line, end='')

    # Check for errors
    if process.returncode != None:
        for line in process.stderr:
            print(line, end='')
        return f"Error: Command failed with return code {process.returncode}"

    return f"Success: PDF cleaned and saved to {export_path}"


if __name__ == "__main__":
    # Determine the base directory of the project
    base_dir = os.path.dirname(os.path.abspath('AI-Data-Prep'))
    
    # Construct the paths relative to the base directory
    document_path = os.path.join(base_dir, "Data/Raw Data/Flash/FCM4 Flash Core Modules.pdf")
    export_location = os.path.join(base_dir, "Data/Clean Data/Flash/")
    
    print(clean_pdf_to_md(document_path, export_location, max_pages=1000))