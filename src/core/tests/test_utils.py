# coding: utf-8

from hashlib import md5

from django.test import TestCase

from core import utils as u


class UploadToTestCase(TestCase):

    def setUp(self):
        self.filename = 'image.jpg'
        self.hash = md5(self.filename.encode('utf-8')).hexdigest()
        self.upload_path = '/'.join(
            [self.hash[:2], self.hash[2:4], self.hash + '.jpg'])

    def test_upload_to_directory(self):
        uploader = u.upload_to('dir')
        expected_dir = 'dir/' + self.upload_path
        assert uploader(instance=None, filename=self.filename) == expected_dir

    def test_upload_to_empty_directory(self):
        uploader = u.upload_to()
        assert uploader(instance=None, filename=self.filename) == self.upload_path
