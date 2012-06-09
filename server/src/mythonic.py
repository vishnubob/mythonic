from biscuit import Manager
from pictureframe import PictureFrame
from math import floor

class SSManager(Manager):
    """
    Runner for Sonic Storyboard.
    """

    def __init__(self, hc, number_of_boxes):
        self.picture_frames = []
        for idx in range(number_of_boxes):
            self.picture_frames.append(PictureFrame(idx, hc))


    def cook_intensity(offset=0, pace=10):
        """
        Return an intensity staggered by "offset", changing at "pace"
        """
        seed = time.time() * pace
        return floor(seed + offset % 255)

    def think(self):
        seconds = floor(time.time())

        for picture_frame, idx in self.picture_frames:
            offset = idx * 10
            picture_frame.set_red(self.cook_intensity(0 + offset))
            picture_frame.set_green(self.cook_intensity(85 + offset))
            picture_frame.set_blue(self.cook_intensity(170 + offset))
            picture_frame.set_uv(self.cook_intensity(0 + offset, 20))
        
