import unittest
import naukri
import io
from pathlib import Path
from pypdf import PdfWriter


class Test(unittest.TestCase):
    def setUp(self):
        self.mock_account = {
            "username": "test_user",
            "password": "test_password",
            "original_resume_path": "test_resume.pdf",
            "modified_resume_path": "test_resume_modified.pdf"
        }

    def test_naukri(self):
        """Smoke test for login initialization (expected to fail without credentials)"""
        status, driver = naukri.naukriLogin(self.mock_account, headless=True)
        naukri.tearDown(driver)
        # We expect failure given current 'your_naukri_username' in constants
        self.assertFalse(status)

    
    def test_update_resume(self):
        """Verify PDF modification logic"""
        original_resume_path = Path(self.mock_account["original_resume_path"])
        modified_resume_path = Path(self.mock_account["modified_resume_path"])
        
        # Ensure directories exist
        original_resume_path.parent.mkdir(parents=True, exist_ok=True)
        modified_resume_path.parent.mkdir(parents=True, exist_ok=True)

        # Create a dummy PDF file
        writer = PdfWriter()
        writer.add_blank_page(width=72, height=72)
        with open(original_resume_path, "wb") as f:
            writer.write(f)

        result_path = naukri.UpdateResume(self.mock_account)
        
        # Verification
        self.assertTrue(Path(result_path).exists())
        self.assertIn(str(modified_resume_path), str(result_path))

        # Cleanup dummy files
        if original_resume_path.exists():
            original_resume_path.unlink()
        if modified_resume_path.exists():
            modified_resume_path.unlink()



if __name__ == "__main__":
    unittest.main()
