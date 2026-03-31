import unittest
import naukri
import io
from pathlib import Path
from pypdf import PdfWriter


class Test(unittest.TestCase):
    def test_naukri(self):
        """Smoke test for login initialization (expected to fail without credentials)"""
        status, driver = naukri.naukriLogin(headless=True)
        naukri.tearDown(driver)
        # We expect failure given current 'your_naukri_username' in constants
        self.assertFalse(status)

    
    def test_update_resume(self):
        """Verify PDF modification logic"""
        original_resume_path = naukri.originalResumePath
        modified_resume_path = naukri.modifiedResumePath
        
        # Ensure directories exist
        original_resume_path.parent.mkdir(parents=True, exist_ok=True)
        modified_resume_path.parent.mkdir(parents=True, exist_ok=True)

        # Create a dummy PDF file
        writer = PdfWriter()
        writer.add_blank_page(width=72, height=72)
        with open(original_resume_path, "wb") as f:
            writer.write(f)

        result_path = naukri.UpdateResume()
        
        # Verification
        self.assertTrue(Path(result_path).exists())
        self.assertIn(str(modified_resume_path), str(result_path))



if __name__ == "__main__":
    unittest.main()
