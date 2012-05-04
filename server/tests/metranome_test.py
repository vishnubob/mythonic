import unittest
from metranome import Metranome
import time

class TestMetranome(unittest.TestCase):

    def test_init(self):
        m = Metranome(120)
        self.assertIsNone(m.current_beat, "current_beat should be None before start")
    def test_seconds_per_beat(self):
        m = Metranome(120)
        self.assertEqual(2, m.seconds_per_beat, "Incorrect seconds per beat")

    def test_start(self):
        m1 = Metranome(120)
        m1.start()
        self.assertEqual(1, m1.current_beat, "start() should start on beat 1")

        m2 = Metranome(120)
        self.assertEqual(1, m2.start(), "start() should return 1")

    def test_time(self):
        m = Metranome(30)
        m.start()

        # Two beats should pass in this time
        time.sleep(1)
        self.assertTrue(m.time() < 2, "time should not continue until next_beat call")
        m.next_beat()
        self.assertTrue(m.time() > 2 and m.time() < 3, "time should continue after next_beat call, but only by one beat")


    def test_can_increment(self):
        m = Metranome(30)
        self.assertTrue(m.can_increment, "Metranome should be able to increment before start")
        m.start()
        self.assertFalse(m.can_increment, "Metranome should not be able to increment before sufficient time has passed")
        

    def test_next_beat(self):
        m = Metranome(30)
        print m.seconds_per_beat
        # Note, starts on 1
        m.start()
        self.assertIsNone(m.next_beat(), "next_beat should be None before time passes")
        time.sleep(1)
        self.assertEqual(2, m.next_beat(), "next_beat should increment one at a time")

if __name__ == '__main__':
    unittest.main()
