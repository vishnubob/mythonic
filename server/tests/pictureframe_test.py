import unittest
from pictureframe import PictureFrame

class TestPictureFrame(unittest.TestCase):

    def test_set_red(self):
        p = PictureFrame(0, None)
        self.assertRaises(ValueError, p.set_red, PictureFrame.MAX_RED + 1)
        self.assertRaises(ValueError, p.set_red, PictureFrame.MIN_RED - 1)
        p.red = 23
        self.assertEqual(23, p.red)

    def test_set_green(self):
        p = PictureFrame(0, None)
        self.assertRaises(ValueError, p.set_green, PictureFrame.MAX_GREEN + 1)
        self.assertRaises(ValueError, p.set_green, PictureFrame.MIN_GREEN - 1)
        p.green = 23
        self.assertEqual(23, p.green)

    def test_set_blue(self):
        p = PictureFrame(0, None)
        self.assertRaises(ValueError, p.set_blue, PictureFrame.MAX_BLUE + 1)
        self.assertRaises(ValueError, p.set_blue, PictureFrame.MIN_BLUE - 1)
        p.blue = 23
        self.assertEqual(23, p.blue)

    def test_set_uv(self):
        p = PictureFrame(0, None)
        self.assertRaises(ValueError, p.set_uv, PictureFrame.MAX_UV + 1)
        self.assertRaises(ValueError, p.set_uv, PictureFrame.MIN_UV - 1)
        p.uv = 23
        self.assertEqual(23, p.uv)

    def test_set_white(self):
        p = PictureFrame(0, None)
        self.assertRaises(ValueError, p.set_white, PictureFrame.MAX_WHITE + 1)
        self.assertRaises(ValueError, p.set_white, PictureFrame.MIN_WHITE - 1)
        p.white = 23
        self.assertEqual(23, p.white)

if __name__ == '__main__':
    unittest.main()
