import os
import datetime
import requests

# Function to download a PDF from a URL and save it to a specified filepath.
# If the URL results in a 404 error, it tries downloading the PDF with yesterday's date in the URL.
def download_pdf(url, filepath, single_digit_day):
    response = requests.get(url)
    
    if response.status_code == 404 and 'WSJ.pdf' in url:
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        single_digit_day_yesterday = yesterday.strftime("%d")
        url = url.replace(single_digit_day, single_digit_day_yesterday)
        response = requests.get(url)

    if response.status_code == 200:
        with open(filepath, 'wb') as f:
            f.write(response.content)
    else:
        print(f"Failed to download {url}: {response.status_code}")

# Function to download PDFs from the specified URLs, and save the new PDFs with today's date prepended.
def download_pdfs():
    current_date = datetime.datetime.now()
    date_str = current_date.strftime("%y%m%d")
    single_digit_day = current_date.day

    # List of URLs to download PDFs from
    urls = [
        f"https://cdn.freedomforum.org/dfp/pdf{single_digit_day}/IL_CT.pdf",
        f"https://cdn.freedomforum.org/dfp/pdf{single_digit_day}/IN_IS.pdf",
        f"https://cdn.freedomforum.org/dfp/pdf{single_digit_day}/CA_LAT.pdf",
        f"https://cdn.freedomforum.org/dfp/pdf{single_digit_day}/NY_NYT.pdf",
        f"https://cdn.freedomforum.org/dfp/pdf{single_digit_day}/WSJ.pdf",
    ]

    # Define the download directory
    download_directory = os.path.expanduser("~/Library/Mobile Documents/com~apple~CloudDocs/@0 Inbox/FrontPages")

    # Create the download directory if it doesn't exist.
    if not os.path.exists(download_directory):
        os.makedirs(download_directory)

    # Format the current date as a string
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")

    # Download PDFs and save them with today's date prepended.
    for url in urls:
        filename = f"{current_date}_{url.split('/')[-1].split('.')[0]}.pdf"
        filepath = os.path.join(download_directory, filename)
        download_pdf(url, filepath, single_digit_day)

if __name__ == "__main__":
    download_pdfs()
