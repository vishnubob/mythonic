import unittest
from schedule import Schedule

class TestSchedule(unittest.TestCase):

    def test_schedule(self):
        s = Schedule()
        s.schedule(lambda : None, 1)
        self.assertEqual(s.insertion_point, 1, "Scheduling should advance insertion point")
        s.schedule(lambda : None, 0)
        self.assertEqual(s.insertion_point, 1, "Scheduling should not advance insertion point if would cause decrease")
        s.schedule(lambda : None, 5)
        self.assertEqual(s.insertion_point, 5, "Scheduling should advance insertion point after multiple inserts")

    def test_append(self):
        s = Schedule()
        s.append(lambda : None)
        self.assertIn(0, s._entries)
        s.append(lambda : None, 2)
        self.assertIn(2, s._entries)
        s.append(lambda : None, 2)
        self.assertIn(4, s._entries)

    def test_pop_due(self):
       s = Schedule()
       self.assertEqual(len(s.pop_due(1, 0)), 0)
       s.schedule(lambda : None, 2)
       self.assertEqual(len(s.pop_due(1, 0)), 0)
       self.assertEqual(len(s.pop_due(1, 2)), 1)
       s.schedule(lambda : None, 2)
       s.schedule(lambda : None, 2)
       self.assertEqual(len(s.pop_due(2, 2)), 2)
       s.schedule(lambda : None, 2)
       self.assertEqual(len(s.pop_due(2, 2)), 1)
       s.schedule(lambda : None, 1)
       self.assertEqual(len(s.pop_due(1, 2)), 1)

if __name__ == '__main__':
    unittest.main()
