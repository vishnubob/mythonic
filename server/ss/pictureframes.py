import mmath
import pictureframe

class SSPictureFrame(pictureframe.PictureFrame):

    def __init__(self, address, lead_tracks=[], drum_tracks=[]):
        self.lead_tracks = list(lead_tracks)
        self.drum_tracks = list(drum_tracks)
        super(SSPictureFrame, self).__init__(address)

    def pattern_hint(self, t, span=0.5):
        on = int(t / (span * 2.0)) % 2 == 0
        self.uv = self.MAX_UV if on else self.MIN_UV

    @property
    def tracks(self):
        return self.lead_tracks + self.drum_tracks

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
        pf.fade_rgb(t, span, 255, 255, 0)

class RedFinishesBat(SSPictureFrame):
    """
    Red finishes creation, sense of accomplishment
    """
    @staticmethod
    def mood(pf, t, span):
        pf.fade_rgb(t, span, 0, 255, 0)

class RedHugsBat(SSPictureFrame):
    """
    Love, hugging creation
    """
    @staticmethod
    def mood(pf, t, span):
        pf.fade_rgb(t, span, 255, 0, 0)

class RedPlaysWithBat(SSPictureFrame):
    """
    Playing with bat toy, having fun
    """
    @staticmethod
    def mood(pf, t, span):
        # magenta
        pf.fade_rgb(t, span, 255, 0, 255)

class RedHangsBat(SSPictureFrame):
    """
    Hangs bat in the tree
    """
    @staticmethod
    def mood(pf, t, span):
        pf.fade_rgb(t, span, 160, 32, 240)

class BatFliesAway(SSPictureFrame):
    """
    Bat flies away
    """
    @staticmethod
    def mood(pf, t, span):
        pf.fade_rgb(t, span, 0, 0, 255)

class BatTakesOff(SSPictureFrame):
    """
    Bat takes off, sense of adventure
    """
    @staticmethod
    def mood(pf, t, span):
        pf.fade_rgb(t, span, 255, 165, 0)

class BatEatsStars(SSPictureFrame):
    """
    Bat eating stars adventure
    """
    @staticmethod
    def mood(pf, t, span):
        """
        Yellow to purple
        """
        if pf.fade_rgb(t, span, 255, 165, 0):
            return
        pf.fade_rgb(t, span, 160, 32, 240)

class BatTripsBalls(SSPictureFrame):
    """
    Bat glowing sparkly showoff
    """
    @staticmethod
    def mood(pf, t, span):
        """
        Really fucking trippy
        """
        pf.randomize_hsv()

class RedIsSad(SSPictureFrame):
    """
    Red is sad
    """
    @staticmethod
    def mood(pf, t, span):
        pf.fade_rgb(t, span, 0, 0, pf.MAX_BLUE / 2.0)

class PlanetTapsShoulder(SSPictureFrame):
    """
    Planet taps on shoulder to console
    """
    @staticmethod
    def mood(pf, t, span):
        pf.fade_rgb(t, span, 0, 128, 128)

class PlanetHangout(SSPictureFrame):
    """
    Red and Planet friendship, hanging out
    """
    @staticmethod
    def mood(pf, t, span):
        pf.fade_rgb(t, span, 255, 0, 255)

