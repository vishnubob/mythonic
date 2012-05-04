import unittest
from pictureframe import PictureFrame

class TestPictureFrame(unittest.TestCase):

    def test_set_red(self):
        p = PictureFrame()
        self.assertRaises(ValueError, p.set_red, PictureFrame.MAX_RED + 1)
        self.assertRaises(ValueError, p.set_red, PictureFrame.MIN_RED - 1)
        p.red = 23
        self.assertEqual(23, p.red)
        

    def test_set_green(self):
        p = PictureFrame()
        self.assertRaises(ValueError, p.set_green, PictureFrame.MAX_GREEN + 1)
        self.assertRaises(ValueError, p.set_green, PictureFrame.MIN_GREEN - 1)
        p.green = 23
        self.assertEqual(23, p.green)

    def test_set_blue(self):
        p = PictureFrame()
        self.assertRaises(ValueError, p.set_blue, PictureFrame.MAX_BLUE + 1)
        self.assertRaises(ValueError, p.set_blue, PictureFrame.MIN_BLUE - 1)
        p.blue = 23
        self.assertEqual(23, p.blue)

    def test_set_uv(self):
        p = PictureFrame()
        self.assertRaises(ValueError, p.set_uv, PictureFrame.MAX_UV + 1)
        self.assertRaises(ValueError, p.set_uv, PictureFrame.MIN_UV - 1)
        p.uv = 23
        self.assertEqual(23, p.uv)

    def test_set_white(self):
        p = PictureFrame()
        self.assertRaises(ValueError, p.set_white, PictureFrame.MAX_WHITE + 1)
        self.assertRaises(ValueError, p.set_white, PictureFrame.MIN_WHITE - 1)
        p.white = 23
        self.assertEqual(23, p.white)
        
    def increase_red(self):
        p = PictureFrame()
        p.red = 0
        assertFalse(p.increase_red(p.MAX_RED - 1))
        assertEqual(p.MAX_RED - 1, p.red)
        assertTrue(p.increase_red(2))
        assertEqual(p.MAX_RED, p.red)

    def decrease_red(self):
        p = PictureFrame()
        p.red = 0
        assertFalse(p.decrease_red(p.MIN_RED + 1))
        assertEqual(p.MIN_RED + 1, p.red)
        assertTrue(p.decrease_red(2))
        assertEqual(p.MIN_RED, p.red)

if __name__ == '__main__':
    unittest.main()
