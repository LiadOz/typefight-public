import unittest
from backend.user import UsersManager
from common.utility import WordType


class TestManager(unittest.TestCase):
    def setUp(self):
        self.manager = UsersManager()
        self.manager.set_broadcast(lambda x, y: None)

    def test_not_init(self):
        with self.assertRaises(Exception):
            self.manager.type_key(None, None)
        with self.assertRaises(Exception):
            self.manager.remove_previous(None)
        with self.assertRaises(Exception):
            self.manager.publish_word(None)
        with self.assertRaises(Exception):
            self.manager.get_data(None)

    def test_game_started(self):
        self.manager.start_game()
        self.manager.get_data(self.manager.user_1.interface)

    def test_attack(self):
        m = self.manager
        m.user_1.data.update_words(WordType.ATTACK, ['t'])
        m.start_game()
        m.user_1.interface.toggle_mode()
        m.user_1.interface.type_key('t')
        m.user_1.interface.publish_word()
        val = m.user_2.data.defend.queue[0]

        self.assertEqual(val, 't')
        with self.assertRaises(IndexError):
            m.user_1.data.attack.queue[0]

    def test_defend(self):
        m = self.manager
        m.user_1.data.update_words(WordType.DEFEND, ['t'])
        m.start_game()
        m.user_1.interface.type_key('t')
        m.user_1.interface.publish_word()
        with self.assertRaises(IndexError):
            m.user_2.data.defend.queue[0]
        with self.assertRaises(IndexError):
            m.user_1.data.defend.queue[0]

    def test_get_users(self):
        man = self.manager
        p1 = man.user_1
        p2 = man.user_2
        self.assertEqual(p1.data, man._get_player(p1.interface))
        self.assertEqual(p2.data, man._get_player(p2.interface))
        self.assertEqual(p1.data, man._get_rival(p2.interface))
        self.assertEqual(p2.data, man._get_rival(p1.interface))
        with self.assertRaises(Exception):
            man._get_player(5)
        with self.assertRaises(Exception):
            man._get_rival(5)
