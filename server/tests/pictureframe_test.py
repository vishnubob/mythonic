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
        
    def test_increase_red(self):
        p = PictureFrame()
        p.red = 0
        self.assertTrue(p.increase_red(p.MAX_RED - 1))
        self.assertEqual(p.MAX_RED - 1, p.red)
        self.assertFalse(p.increase_red(2))
        self.assertEqual(p.MAX_RED, p.red)

    def test_decrease_blue(self):
        p = PictureFrame()
        p.blue = 0
        # Go below the minimum
        self.assertFalse(p.decrease_blue(p.MIN_BLUE + 1))
        # Make sure only the minimum was seet
        self.assertEqual(p.MIN_BLUE, p.blue)
        p.blue = p.MIN_BLUE + 4
        # Decrease by two
        self.assertTrue(p.decrease_blue(2))
        self.assertEqual(p.MIN_BLUE + 2, p.blue)

    def test_decrease_all(self):
        p = PictureFrame()
        self.assertFalse(p.decrease_all())

if __name__ == '__main__':
    unittest.main()
