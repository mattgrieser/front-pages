import unittest
import os
import requests
from unittest.mock import patch
from download_pdfs import download_pdf

class TestDownloadPDF(unittest.TestCase):

    def setUp(self):
        self.sample_url = "https://www.example.com/sample.pdf"
        self.sample_filepath = "sample.pdf"
        self.nonexistent_url = "https://www.example.com/nonexistent.pdf"
        self.nonexistent_filepath = "nonexistent.pdf"

    def tearDown(self):
        if os.path.exists(self.sample_filepath):
            os.remove(self.sample_filepath)
        if os.path.exists(self.nonexistent_filepath):
            os.remove(self.nonexistent_filepath)

    def test_download_pdf_success(self):
        with patch("requests.get") as mocked_get:
            mocked_get.return_value.status_code = 200
            mocked_get.return_value.content = b"sample pdf content"

            success = download_pdf(self.sample_url, self.sample_filepath)

            self.assertTrue(success, "Download should be successful")
            self.assertTrue(os.path.exists(self.sample_filepath), "File should be saved")

            with open(self.sample_filepath, "rb") as f:
                content = f.read()
                self.assertEqual(content, b"sample pdf content", "File content should match")

    def test_download_pdf_failure(self):
        with patch("requests.get") as mocked_get:
            mocked_get.return_value.status_code = 404

            success = download_pdf(self.nonexistent_url, self.nonexistent_filepath)

            self.assertFalse(success, "Download should not be successful")
            self.assertFalse(os.path.exists(self.nonexistent_filepath), "File should not be saved")

if __name__ == "__main__":
    unittest.main()
