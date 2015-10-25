import unittest
import changrab as cgr

class changrabTest(unittest.TestCase):
    def setUp(this):
        pass
    def tearDown(this):
        pass
    def test_parse_4ch_url(this):
        url = r'http://boards.4chan.org/fit/thread/17018018/this-link-covers-the-following-topics'
        expected = ('http://', 'fit', '17018018')
        actual = cgr.parse_4ch_url(url)
        this.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()