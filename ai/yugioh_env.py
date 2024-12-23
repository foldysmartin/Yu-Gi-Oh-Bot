from enum import Enum
import random
from pettingzoo.utils import wrappers
from gymnasium.spaces import Dict, MultiDiscrete, Discrete, Box
import numpy as np
import gymnasium as Gym

from Player import Player
from abstract_field import Zone
from ai.opponent import Opponent
from ai.ring_buffer import WinBuffer
from battling.to_battle import AttackTarget, ToBattle
from cards.load_card import find_card
from field_half import OutOfCards
from game import Game, ToNextPhase
from summoning.normal.to_normal_summon import ToNormalSummon


def env():
    env = YugiohEnv()
    env = wrappers.TerminateIllegalWrapper(env, illegal_reward=-1)
    env = wrappers.AssertOutOfBoundsWrapper(env)
    env = wrappers.OrderEnforcingWrapper(env)
    return env


def fill_monster(name):
    cards = []
    for i in range(3):
        cards.append(find_card(name))
    return cards


def create_deck():
    cards = []
    names = [
        "Mystical Elf",
        "Feral Imp",
        "Winged Dragon, Guardian of the Fortress #1",
        "Beaver Warrior",
        "Celtic Guardian",
        "Mammoth Graveyard",
        "Great White",
        "Silver Fang",
        "Giant Soldier of Stone",
        "Dragon Zombie",
        "Witty Phantom",
        "Claw Reacher",
        "Mystic Clown",
        "Ancient Elf",
        "Magical Ghost",
        "Neo the Magic Swordsman",
        "Baron of the Fiend Sword",
        "Man-Eating Treasure Chest",
        "Sorcerer of the Doomed",
    ]
    for name in names:
        cards = cards + fill_monster(name)
    random.shuffle(cards)
    return cards


class Actions(Enum):
    next_phase = 0
    play_card_1 = 1
    play_card_2 = 2
    play_card_3 = 3
    play_card_4 = 4
    play_card_5 = 5
    play_card_6 = 6
    play_card_7 = 7
    attack_1_1 = 8
    attack_1_2 = 9
    attack_1_3 = 10
    attack_1_4 = 11
    attack_1_5 = 12
    attack_1_direct = 13
    attack_2_1 = 14
    attack_2_2 = 15
    attack_2_3 = 16
    attack_2_4 = 17
    attack_2_5 = 18
    attack_2_direct = 19
    attack_3_1 = 20
    attack_3_2 = 21
    attack_3_3 = 22
    attack_3_4 = 23
    attack_3_5 = 24
    attack_3_direct = 25
    attack_4_1 = 26
    attack_4_2 = 27
    attack_4_3 = 28
    attack_4_4 = 29
    attack_4_5 = 30
    attack_4_direct = 31
    attack_5_1 = 32
    attack_5_2 = 33
    attack_5_3 = 34
    attack_5_4 = 35
    attack_5_5 = 36
    attack_5_direct = 37


actions = [
    (Actions.next_phase, ToNextPhase()),
    (Actions.play_card_1, ToNormalSummon(0)),
    (Actions.play_card_2, ToNormalSummon(1)),
    (Actions.play_card_3, ToNormalSummon(2)),
    (Actions.play_card_4, ToNormalSummon(3)),
    (Actions.play_card_5, ToNormalSummon(4)),
    (Actions.play_card_6, ToNormalSummon(5)),
    (Actions.play_card_7, ToNormalSummon(6)),
    (Actions.attack_1_1, ToBattle(Zone.First, AttackTarget.First)),
    (Actions.attack_1_2, ToBattle(Zone.First, AttackTarget.Second)),
    (Actions.attack_1_3, ToBattle(Zone.First, AttackTarget.Third)),
    (Actions.attack_1_4, ToBattle(Zone.First, AttackTarget.Fourth)),
    (Actions.attack_1_5, ToBattle(Zone.First, AttackTarget.Fith)),
    (Actions.attack_1_direct, ToBattle(Zone.First, AttackTarget.Direct)),
    (Actions.attack_2_1, ToBattle(Zone.Second, AttackTarget.First)),
    (Actions.attack_2_2, ToBattle(Zone.Second, AttackTarget.Second)),
    (Actions.attack_2_3, ToBattle(Zone.Second, AttackTarget.Third)),
    (Actions.attack_2_4, ToBattle(Zone.Second, AttackTarget.Fourth)),
    (Actions.attack_2_5, ToBattle(Zone.Second, AttackTarget.Fith)),
    (Actions.attack_2_direct, ToBattle(Zone.Second, AttackTarget.Direct)),
    (Actions.attack_3_1, ToBattle(Zone.Third, AttackTarget.First)),
    (Actions.attack_3_2, ToBattle(Zone.Third, AttackTarget.Second)),
    (Actions.attack_3_3, ToBattle(Zone.Third, AttackTarget.Third)),
    (Actions.attack_3_4, ToBattle(Zone.Third, AttackTarget.Fourth)),
    (Actions.attack_3_5, ToBattle(Zone.Third, AttackTarget.Fith)),
    (Actions.attack_3_direct, ToBattle(Zone.Third, AttackTarget.Direct)),
    (Actions.attack_4_1, ToBattle(Zone.Fourth, AttackTarget.First)),
    (Actions.attack_4_2, ToBattle(Zone.Fourth, AttackTarget.Second)),
    (Actions.attack_4_3, ToBattle(Zone.Fourth, AttackTarget.Third)),
    (Actions.attack_4_4, ToBattle(Zone.Fourth, AttackTarget.Fourth)),
    (Actions.attack_4_5, ToBattle(Zone.Fourth, AttackTarget.Fith)),
    (Actions.attack_4_direct, ToBattle(Zone.Fourth, AttackTarget.Direct)),
    (Actions.attack_5_1, ToBattle(Zone.Fith, AttackTarget.First)),
    (Actions.attack_5_2, ToBattle(Zone.Fith, AttackTarget.Second)),
    (Actions.attack_5_3, ToBattle(Zone.Fith, AttackTarget.Third)),
    (Actions.attack_5_4, ToBattle(Zone.Fith, AttackTarget.Fourth)),
    (Actions.attack_5_5, ToBattle(Zone.Fith, AttackTarget.Fith)),
    (Actions.attack_5_direct, ToBattle(Zone.Fith, AttackTarget.Direct)),
]

max_id = 20
observation_space = Dict(
    {
        "opp_monsters": MultiDiscrete([max_id, max_id, max_id, max_id, max_id]),
        "own_monsters": MultiDiscrete([max_id, max_id, max_id, max_id, max_id]),
        "life_points": Box(low=0, high=8000, shape=(2,), dtype=np.int64),
        "action_mask": MultiDiscrete([2] * len(Actions)),
    }
)




class YugiohEnv(Gym.Env):
    def __init__(self, **kwargs):
        super().__init__()

        self.player = kwargs.get("player", Player.One) 
        self.opponent = Opponent(Player.Two)
        self.wins = WinBuffer(200)
        

        self.reset()
        self.action_space = Discrete(len(Actions))
        self.observation_space = observation_space

    def _opponent(self):
        return Player.Two if self.player == Player.One else Player.One
   

    def _observation(self):
        observation = {
            "opp_monsters": self._get_monsters(self._opponent()),
            "own_monsters": self._get_monsters(self.player),
            "life_points": np.array(
                [
                    self.game.game_state.life_points(
                        self.game.game_state.active_player
                    ),
                    self.game.game_state.life_points(
                        self.game.game_state.inactive_player
                    ),
                ]
            ),
            "action_mask": self.action_mask(),
        }
        return observation

    def step(self, action_index):
        self.reward = 0
        try:
            action = first(actions, lambda a: a[0] == Actions(action_index))
            self.game.trigger_action(action[1])

            if self.game.game_state.life_points(self.player) <= 0:
                self.reward = -1
                self.terminations = True
                self.wins.lose()
                print("Player", self.player, "lost: Winrate", self.wins.win_percentage())
            elif self.game.game_state.life_points(self._opponent()) <= 0:
                self.reward = 1
                self.terminations = True
                self.wins.win()
                print("Player", self.player, "won: Winrate", self.wins.win_percentage())

            self.opponent.play(self.game)

            
        except OutOfCards as e:
            self.reward= 0
            self.terminations = True
            print("Out of cards")

        except Exception as e:
            print(e)

        return self._observation(), self.reward, self.terminations, self.truncations, self.infos

    def reset(self, seed=None, options=None):
        self.reward = 0
        self.truncations = False
        self.terminations = False
        self.infos = {}
        self.game = Game.start(create_deck(), create_deck())


        return self._observation(), self.infos
          


    def action_mask(self):
        available_actions = self.game.avaliable_actions()
        mask = np.zeros(len(Actions), dtype=np.int8)

        for index, action in enumerate(actions):
            if action[1] in available_actions:
                mask[index] = 1

        return mask

    def _get_monsters(self, player):
        ids = []
        monsters = self.game.fetch_monsters(player)
        for zone in Zone:
            if zone in monsters:
                ids.append(monsters[zone].card_id)
            else:
                ids.append(0)
        return np.array(ids)


def first(iterable, condition=lambda x: True):
    return next(x for x in iterable if condition(x))
