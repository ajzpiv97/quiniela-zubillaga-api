import unittest
from flaskr.utils.local_utils import get_score


class SimpleTest(unittest.TestCase):

    #test same score
    def test(self):
        self.assertEqual(5,get_score("1-1","1-1"),"test1")
        self.assertEqual(5, get_score("1-2", "1-2"), "test2")
        self.assertEqual(5, get_score("3-1", "3-1"), "test3")
        self.assertEqual(5, get_score("0-0", "0-0"), "test4")

    def test_match_winner(self):
        ## team a wins by differnt score
        self.assertEqual(3, get_score("3-1", "6-1"))
        self.assertEqual(3, get_score("4-5", "1-2"))
        ## tied but different score than predicted
        self.assertEqual(3, get_score("2-2", "3-3"))

    def test_total_goals_predicted(self):
        ## goals but not winner
        self.assertEqual(2, get_score("2-1", "1-2"))
        ## goals and winner
        self.assertEqual(5, get_score("3-1", "4-0"))
        ## no goals scored
        self.assertEqual(0, get_score("7-1", "1-1"))
        self.assertEqual(0, get_score("0-1", "2-0"), "test1")

if __name__ == '__main__':
    unittest.main()