import os
import datetime
import requests

def download_pdf(url, filepath):
    response = requests.get(url)

    if response.status_code == 200:
        with open(filepath, 'wb') as f:
            f.write(response.content)
    else:
        print(f"Failed to download {url}: {response.status_code}")
        return False

    return True

def download_pdfs():
    current_date = datetime.datetime.now()
    yesterday = current_date - datetime.timedelta(days=1)

    urls = [
        "IL_CT.pdf",
        "IN_IS.pdf",
        "CA_LAT.pdf",
        "NY_NYT.pdf",
        "WSJ.pdf",
    ]

    base_url = "https://cdn.freedomforum.org/dfp/pdf"
    download_directory = os.path.expanduser("~/Library/Mobile Documents/com~apple~CloudDocs/@0 Inbox/FrontPages")

    if not os.path.exists(download_directory):
        os.makedirs(download_directory)

    formatted_date = current_date.strftime("%Y-%m-%d")

    for pdf_name in urls:
        formatted_url = f"{base_url}{current_date.day}/{pdf_name}"
        filename = f"{formatted_date}_{pdf_name.split('.')[0]}.pdf"
        filepath = os.path.join(download_directory, filename)

        success = download_pdf(formatted_url, filepath)

        if not success and 'WSJ.pdf' in pdf_name:
            formatted_url_yesterday = f"{base_url}{yesterday.day}/{pdf_name}"
            download_pdf(formatted_url_yesterday, filepath)

if __name__ == "__main__":
    download_pdfs()
