# Import required libraries
import os
import datetime
import requests

# Function to download a PDF from a URL and save it to a specified filepath
def download_pdf(url, filepath, today, yesterday):
    # Send a GET request to the URL
    response = requests.get(url)

    # If the response is a 404 error and the URL is for WSJ.pdf,
    # try downloading the PDF with yesterday's date in the URL
    if response.status_code == 404 and 'WSJ.pdf' in url:
        # Replace today's day with yesterday's day in the URL
        url_yesterday = url.replace(str(today.day), str(yesterday.day))
        # Send a GET request to the updated URL
        response = requests.get(url_yesterday)

    # If the response status code is 200 (successful), write the content to the specified filepath
    if response.status_code == 200:
        with open(filepath, 'wb') as f:
            f.write(response.content)
    # Otherwise, print an error message
    else:
        print(f"Failed to download {url}: {response.status_code}")

# Function to download PDFs from the specified URLs
def download_pdfs():
    # Get the current date and time
    current_date = datetime.datetime.now()
    # Get yesterday's date by subtracting one day from the current date
    yesterday = current_date - datetime.timedelta(days=1)

    # List of URLs to download PDFs from, with the day of the month inserted into the URL
    urls = [
        f"https://cdn.freedomforum.org/dfp/pdf{current_date.day}/IL_CT.pdf",
        f"https://cdn.freedomforum.org/dfp/pdf{current_date.day}/IN_IS.pdf",
        f"https://cdn.freedomforum.org/dfp/pdf{current_date.day}/CA_LAT.pdf",
        f"https://cdn.freedomforum.org/dfp/pdf{current_date.day}/NY_NYT.pdf",
        f"https://cdn.freedomforum.org/dfp/pdf{current_date.day}/WSJ.pdf",
    ]

    # Define the download directory
    download_directory = os.path.expanduser("~/Library/Mobile Documents/com~apple~CloudDocs/@0 Inbox/FrontPages")

    # If the download directory does not exist, create it
    if not os.path.exists(download_directory):
        os.makedirs(download_directory)

    # Format the current date as a string in the format "YYYY-MM-DD"
    formatted_date = current_date.strftime("%Y-%m-%d")

    # Iterate through the list of URLs
    for url in urls:
        # Generate a filename with the current date and the PDF's name
        filename = f"{formatted_date}_{url.split('/')[-1].split('.')[0]}.pdf"
        # Generate the full filepath by combining the download directory and filename
        filepath = os.path.join(download_directory, filename)
        # Call the download_pdf function with the URL, filepath, current date, and yesterday's date
        download_pdf(url, filepath, current_date, yesterday)

# If this script is being run as the main module, call the download_pdfs function
if __name__ == "__main__":
    download_pdfs()
