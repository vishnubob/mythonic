import mmath
import pictureframe

class SSPictureFrame(pictureframe.PictureFrame):

    def __init__(self, address):
        self.address = address
        super(SSPictureFrame, self).__init__()

    def pattern_hint(self, t, span=0.5):
        on = int(t / (span * 2.0)) % 2 == 0
        self.uv = self.MAX_UV if on else self.MIN_UV

class RedSitsAlone(SSPictureFrame):
    """
    Red sitting alone bored
    """
    @staticmethod
    def mood(pf, t, span):
        pf.blue = pf.MAX_BLUE #mmath.triangle(t, span, pf.MIN_BLUE, pf.MAX_BLUE)

class RedSewsBat(SSPictureFrame):
    """
    Red sewing, making the bat
    """
    @staticmethod
    def mood(pf, t, span):
        # yellow
        pf.hsv = (1, 1, 0)

class RedFinishesBat(SSPictureFrame):
    """
    Red finishes creation, sense of accomplishment
    """
    @staticmethod
    def mood(pf, t, span):
        pf.green = pf.MAX_GREEN

class RedHugsBat(SSPictureFrame):
    """
    Love, hugging creation
    """
    @staticmethod
    def mood(pf, t, span):
        pf.red = pf.MAX_RED

class RedPlaysWithBat(SSPictureFrame):
    """
    Playing with bat toy, having fun
    """
    @staticmethod
    def mood(pf, t, span):
        # magenta
        pf.red = 255
        pf.green = 0
        pf.blue = 255

class RedHangsBat(SSPictureFrame):
    """
    Hangs bat in the tree
    """
    @staticmethod
    def mood(pf, t, span):
        pf.red = 160
        pf.green = 32
        pf.blue = 240

class BatFliesAway(SSPictureFrame):
    """
    Bat flies away
    """
    @staticmethod
    def mood(pf, t, span):
        pf.blue = pf.MAX_BLUE

class BatTakesOff(SSPictureFrame):
    """
    Bat takes off, sense of adventure
    """
    @staticmethod
    def mood(pf, t, span):
        pf.red = 255
        pf.green = 165
        pf.blue = 0

class BatEatsStars(SSPictureFrame):
    """
    Bat eating stars adventure
    """
    @staticmethod
    def mood(pf, t, span):
        """
        Yellow to purple
        """
        #TODO
        pass
        

class BatTripsBalls(SSPictureFrame):
    """
    Bat glowing sparkly showoff
    """
    @staticmethod
    def mood(pf, t, span):
        """
        Really fucking trippy
        """
        pass

class RedIsSad(SSPictureFrame):
    """
    Red is sad
    """
    @staticmethod
    def mood(pf, t, span):
        pf.blue = pf.MAX_BLUE / 2.0

class PlanetTapsShoulder(SSPictureFrame):
    """
    Planet taps on shoulder to console
    """
    @staticmethod
    def mood(pf, t, span):
        """
        TODO: teal
        """
        pf.red = 0
        pf.green = 193
        pf.blue = 255

class PlanetHangout(SSPictureFrame):
    """
    Red and Planet friendship, hanging out
    """
    @staticmethod
    def mood(pf, t, span):
        """
        TODO: fuschia
        """
        pf.red = 255
        pf.green = 192
        pf.blue = 203

