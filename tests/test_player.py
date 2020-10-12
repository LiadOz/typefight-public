# import unittest
# from unittest.mock import MagicMock
# from common.utility import WordType
# from backend.players import (IPlayer, executor_factory, PlayerQueueAndMode,
#                              PlayerMediator)

# class TestDuelMediator(unittest.TestCase):
#     def setUp(self):
#         self.executor = executor_factory(2)
#         self.p1 = IPlayer(self.executor, 0)
#         self.p2 = IPlayer(self.executor, 1)
#
#     def test_register(self):
#         self.assertEqual(self.p1, self.executor.player_1)
#         self.assertEqual(self.p2, self.executor.player_2)
#         self.assertEqual(self.executor.registered, 2)
#
#     def test_opponent(self):
#         self.assertEqual(self.executor.get_opponent(self.p1), self.p2)
#         self.assertEqual(self.executor.get_opponent(self.p2), self.p1)
#         with self.assertRaises(Exception):
#             p3 = IPlayer()
#             self.executor.get_opponent(p3)
#
#     def test_p1_to_p2(self):
#         self.p2.recieve_action = MagicMock()
#         self.p1.executor.send_action(self.p1, 'a')
#         self.p2.recieve_action.assert_called_once_with('a')
#
#     def test_p2_to_p1(self):
#         self.p1.recieve_action = MagicMock()
#         self.p2.executor.send_action(self.p2, 'a')
#         self.p1.recieve_action.assert_called_once_with('a')
#
#
# class TestPlayer(unittest.TestCase):
#     def setUp(self):
#         self.player = PlayerQueueAndMode(PlayerMediator(), 0)
#
#     def test_remove(self):
#         self.player.remove_previous()
#         self.assertEqual(self.player.current_word.get_text(), '')
#
#         self.player.type_key('a')
#         self.player.remove_previous()
#         self.assertEqual(self.player.current_word.get_text(), '')
#
#     def test_type(self):
#         self.player.type_key('a')
#         self.player.type_key('A')
#         self.assertEqual(self.player.current_word.get_text(), 'aA')
#
#
# class TestPlayerQueueAndMode(unittest.TestCase):
#     def setUp(self):
#         self.player = PlayerQueueAndMode(PlayerMediator(), 0)
#
#     def test_publish(self):
#         self.player.add_word(WordType.ATTACK, 'a')
#         self.player.add_word(WordType.DEFEND, 'b')
#
#         self.player.type_key('a')
#         self.player.publish_word()
#         self.assertEqual(self.player.get_data()[WordType.ATTACK], ['a'])
#         self.assertEqual(self.player.get_data()[WordType.DEFEND], ['b'])
#
#         self.player.toggle_mode()
#         self.player.publish_word()
#         self.assertEqual(self.player.get_data()[WordType.ATTACK], [])
#         self.assertEqual(self.player.get_data()[WordType.DEFEND], ['b'])
#
#         self.player.type_key('b')
#         self.player.publish_word()
#         self.assertEqual(self.player.get_data()[WordType.ATTACK], [])
#         self.assertEqual(self.player.get_data()[WordType.DEFEND], ['b'])
#
#         self.player.toggle_mode()
#         self.player.publish_word()
#         self.assertEqual(self.player.get_data()[WordType.ATTACK], [])
#         self.assertEqual(self.player.get_data()[WordType.DEFEND], [])
