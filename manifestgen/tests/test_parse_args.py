from html5_cache_manifest_gen.args import parse_args

import unittest

class ParseArgsTests(unittest.TestCase):
    
    def test_cannonical(self):
        command_line =  "-c *.py -c *.img -c *.png -nc temp.py -n counter.html form.html -f / fallback.html -f /form fallbackform.html"
        args = parse_args(command_line.split())
        #self.assertEqual(args, Namespace(cache=[['*.py'], ['*.img'], ['*.png']], fallback=[['/', 'fallback.html '], ['/form', 'fallbackform.html']], network=[['counter.html', 'form.html']], no cache=[['temp.py']]))

        self.assertEqual( args.cache, [['*.py'], ['*.img'], ['*.png']])
        self.assertEqual( args.nocache, [['temp.py']])
        self.assertEqual( args.fallback, [['/', 'fallback.html'], ['/form', 'fallbackform.html']])






