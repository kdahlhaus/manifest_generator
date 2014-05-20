from manifestgen.app import convert_filenames_to_urls

import unittest

class TestConvertFilenamesToUrls(unittest.TestCase):
    
    def test_cannonical(self):
        result = convert_filenames_to_urls( [ '/usr/proj/index.html', '/usr/proj/js/util.js'], '/usr/proj', '/sample/static' )
        self.assertEqual( result, [ '/sample/static/index.html', '/sample/static/js/util.js' ])

