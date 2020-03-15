import unittest
from app.faebooks import Faebooks
import pdb

# tests are designed to run from within the root directory

class FaebooksTests(unittest.TestCase):
   def setUp(self):
       self.faebooks = Faebooks()

   
   def test_error_on_archive_not_found (self):
        archive_filename="faebooks/test/test_material_not_found.csv"
        with self.assertRaises(FileNotFoundError): self.faebooks.verify_archive(archive_filename)

   def test_error_on_empty_archive (self):
        archive_filename="faebooks/test/test_material_blank.csv"
        with self.assertRaises(Exception): self.faebooks.verify_archive(archive_filename)

   def test_first_line_proper_headers(self):
        archive_filename="faebooks/test/test_material_short_improper_header.csv" 
        with self.assertRaises(Exception): self.faebooks.parse_archive(archive_filename)

  #   def test_first_line_improperly_formatted (self):
  #      archive_filename="faebooks/test/test_material_short_first_line_broken.csv"
   #     with self.assertRaises(Exception): self.faebooks.parse_archive(archive_filename) """
