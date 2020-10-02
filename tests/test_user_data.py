import unittest
from backend.user import UserData
from common.utility import WordType


class TestUserData(unittest.TestCase):
    def setUp(self):
        self.user = UserData()

    def test_append(self):
        def test_queue(w_type, words):
            self.user.update_words(w_type, words)
            other_words = list(self.user.get_words(w_type).queue)
            self.assertEqual(len(words), len(other_words))
            for x, y in zip(words, other_words):
                self.assertEqual(x, y)

        words = ['this', 'is', 'a', 'test']
        test_queue(WordType.ATTACK, words)
        test_queue(WordType.DEFEND, words)

    def test_remove(self):
        self.user.remove_previous()
        self.assertEqual(self.user.get_current_word(), '')

        self.user.type_key('a')
        self.user.remove_previous()
        self.assertEqual(self.user.get_current_word(), '')

    def test_type(self):
        self.user.type_key('a')
        self.user.type_key('A')
        self.assertEqual(self.user.get_current_word(), 'aA')

    def test_publish(self):
        attack = self.user.get_words(WordType.ATTACK)
        defend = self.user.get_words(WordType.DEFEND)
        self.user.update_words(WordType.ATTACK, 'a')
        self.user.update_words(WordType.DEFEND, 'b')

        self.user.type_key('a')
        self.user.publish_word()
        self.assertEqual(attack.qsize(), 1)

        self.user.toggle_mode()
        self.user.publish_word()
        self.assertEqual(attack.qsize(), 0)

        self.user.type_key('b')
        self.user.publish_word()
        self.assertEqual(defend.qsize(), 1)

        self.user.toggle_mode()
        self.user.publish_word()
        self.assertEqual(defend.qsize(), 0)
