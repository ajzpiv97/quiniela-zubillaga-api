import unittest
from flaskr.utils.local_utils import get_score


class ScoringRulesTesCase(unittest.TestCase):

    # test same score
    def test(self):
        self.assertEqual(5, get_score("1-1", "1-1"), "something is wrong")
        self.assertEqual(5, get_score("1-2", "1-2"), "something is wrong")
        self.assertEqual(5, get_score("3-1", "3-1"), "something is wrong")
        self.assertEqual(5, get_score("0-0", "0-0"), "something is wrong")



    def test_match_winner(self):
        # team a wins by different score
        self.assertEqual(3, get_score("3-1", "6-1"), "something is wrong")
        self.assertEqual(3, get_score("4-5", "1-2"), "something is wrong")
        # tied but different score than predicted
        self.assertEqual(3, get_score("2-2", "3-3"), "something is wrong")

    def test_total_goals_predicted(self):
        # goals but not winner
        self.assertEqual(2, get_score("2-1", "1-2"), "something is wrong")
        # goals and winner
        self.assertEqual(5, get_score("3-1", "4-0"), "something is wrong")
        # no goals scored
        self.assertEqual(0, get_score("7-1", "1-1"), "something is wrong")
        self.assertEqual(0, get_score("0-1", "2-0"), "something is wrong")

