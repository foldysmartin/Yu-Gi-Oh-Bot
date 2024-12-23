from tkinter import Button, Label, Tk
from Player import Player
from abstract_field import Zone
from ai.bad_bot import BadBot
from battling.to_battle import AttackTarget, ToBattle
from cards.load_card import find_card
from game import Game, ToNextPhase
from summoning.normal.to_normal_summon import ToNormalSummon


def create_deck():
    return [
        find_card("Mystical Elf"),
        find_card("Feral Imp"),
        find_card("Winged Dragon, Guardian of the Fortress #1"),
        find_card("Beaver Warrior"),
        find_card("Celtic Guardian"),
        find_card("Mammoth Graveyard"),
        find_card("Great White"),
        find_card("Silver Fang"),
        find_card("Giant Soldier of Stone"),
        find_card("Dragon Zombie"),
        find_card("Witty Phantom"),
        find_card("Claw Reacher"),
        find_card("Mystic Clown"),
        find_card("Ancient Elf"),
        find_card("Magical Ghost"),
        find_card("Neo the Magic Swordsman"),
        find_card("Baron of the Fiend Sword"),
        find_card("Man-Eating Treasure Chest"),
        find_card("Sorcerer of the Doomed"),
    ]


class GameWindow(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.geometry("600x400+50+50")
        self.resizable(0, 0)
        self.cards = []
        self.game = Game.start(create_deck(), create_deck())

        self._redraw()

    def _redraw(self):
        self.actions = [action for (action, _) in self.game.avaliable_actions()]
        for card in self.cards:
            card.destroy()
        self.cards = []
        self.selected = None
        self._draw_life_points()
        self._draw_opponent_hand()
        self._draw_player_hand()
        self._draw_player_monster_zone()
        self._draw_opponent_monster_zone()
        self._draw_next_phase_button()

    def _draw_life_points(self):
        player_1_life_points = Label(
            self,
            text=f"Player 1 Life Points: {self.game.game_state.life_points(player=Player.One)}",
        )
        player_1_life_points.grid(row=6, column=0, columnspan=6)

        player_2_life_points = Label(
            self,
            text=f"Player 2 Life Points: {self.game.game_state.life_points(player=Player.Two)}",
        )
        player_2_life_points.bind(
            "<Button-1>", self._attack_lambda(AttackTarget.Direct)
        )
        player_2_life_points.grid(row=0, column=0, columnspan=6)

    def _draw_player_hand(
        self,
    ):
        for i, card in enumerate(self.game.fetch_hand(Player.One)):
            label = Label(self, text=card.name)
            label.grid(row=5, column=i)

            if ToNormalSummon(card) in self.actions:
                label.bind(
                    "<Button-1>",
                    self._action_lambda(ToNormalSummon(card)),
                )
            self.cards.append(label)

    def _draw_opponent_hand(
        self,
    ):
        for i, card in enumerate(self.game.fetch_hand(Player.Two)):
            label = Label(self, text="Hidden")
            label.grid(row=1, column=i)
            self.cards.append(label)

    def _draw_player_monster_zone(self):
        monsters = self.game.fetch_monsters(Player.One)
        for i, zone in enumerate(Zone):
            card = monsters.get(zone)
            card_name = card.name if card else "Empty"
            label = Label(self, text=card_name)
            label.grid(row=4, column=i)

            label.bind("<Button-1>", self._select_lambda(Zone(i)))
            self.cards.append(label)

    def _draw_opponent_monster_zone(self):
        monsters = self.game.fetch_monsters(Player.Two)
        for i, zone in enumerate(Zone):
            card = monsters.get(zone)
            card_name = card.name if card else "Empty"
            label = Label(self, text=card_name)
            label.grid(row=2, column=i)
            label.bind("<Button-1>", self._attack_lambda(AttackTarget(i)))
            self.cards.append(label)

    def _draw_next_phase_button(self):
        button = Button(self, text="Next Phase", command=self._next_phase)
        label = Label(self, text="Current Phase: " + str(self.game.game_state.phase))
        button.grid(
            row=7,
            column=0,
        )
        label.grid(
            row=7,
            column=1,
        )

    def _action_lambda(self, action):
        return lambda e: self._trigger_action(action)

    def _trigger_action(self, action):
        self.game.trigger_action(action)
        self._redraw()

    def _select_lambda(self, zone):
        return lambda event: self._select(event.widget, zone)

    def _select(self, widget, zone):
        widget.config(bg="red")
        self.selected = zone

    def _attack_lambda(self, target):
        return lambda event: self._attack(target)

    def _attack(self, target):
        if self.selected:
            self._trigger_action(ToBattle(self.selected, target))

    def _next_phase(self):
        self._trigger_action(ToNextPhase())

        if self.game.game_state.active_player == Player.Two:
            BadBot().play(self.game)
        self._redraw()


window = GameWindow()
window.mainloop()
