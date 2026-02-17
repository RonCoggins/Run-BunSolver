import random

import logging
from timeit_decorator import timeit_sync

import damagecalc as dc
import move as m
import game_state as gs
import team as t
import AIDecisionMaker.maxdamage as AIMax
import AIDecisionMaker.playeraidecision as pAI
import decisiontree as dt
import pokemon as p

class BattleEngine:

    def __init__(self):

        self.game_state: gs.GameState
    
    def init_game_state(self, opponent_trainer: str):
        self.game_state = gs.GameState(opponent_trainer)
    
    def run_one_turn(self):
        
        print(f"Turn Number: {self.game_state.turn_info.turn_number}\n")

        print(
            f"\tPokemon on the field:\n \t\tPlayer: {self.game_state.player_info.team.active_pokemon.pokemon_name.title()}\n\t\tOpponent: {self.game_state.opponent_info.team.active_pokemon.pokemon_name.title()}\n"
        )

        self.move_selection()

        self.determine_first_mover()

        self.perform_actions()

        print(f"End of turn HP values are: Player{self.game_state.player_info.team.active_pokemon.current_HP}\n End of turn HP values are: Opponent{self.game_state.opponent_info.team.active_pokemon.current_HP}\n")

        self.end_turn_actions()

        self.game_state.turn_info.turn_number += 1

    def finish_battle(self):
        while self.game_state.battle_over == False:
            self.run_one_turn()
        

    def move_selection(self) -> None:
        self.player_select_move()
        self.opponent_select_move()

    def player_select_move(self) -> None:
        self.game_state.player_info.current_move = AIMax.MaxDamageAI(self.game_state, True).highest_damage_move 

    def opponent_select_move(self) -> None:
        self.game_state.opponent_info.current_move = AIMax.MaxDamageAI(self.game_state, False).highest_damage_move 

    def determine_first_mover(self) -> None:

        if (
            self.game_state.player_info.team.active_pokemon.stats["spe"]
            > self.game_state.opponent_info.team.active_pokemon.stats["spe"]
        ):
            self.game_state.turn_info.first_mover = "player"

        elif (
            self.game_state.player_info.team.active_pokemon.stats["spe"]
            > self.game_state.opponent_info.team.active_pokemon.stats["spe"]
        ):
            self.game_state.turn_info.first_mover = "opponent"
        else:
            choices = ["player","opponent"]
            self.game_state.turn_info.first_mover = random.choice(choices)

    def perform_actions(self) -> None:

        if self.game_state.turn_info.first_mover == "player":
            self.player_attack()
            if self.game_state.opponent_info.team.active_pokemon.is_fainted == False:
                self.opponent_attack()
        else:
            self.opponent_attack()
            if self.game_state.player_info.team.active_pokemon.is_fainted == False:
                self.player_attack()


    def player_attack(self):

        damage:int = dc.DamageCalculation(
            attacking_pokemon= self.game_state.player_info.team.active_pokemon,
            target_pokemon=self.game_state.opponent_info.team.active_pokemon,
            move= self.game_state.player_info.current_move,
        ).final_damage

        self.game_state.player_info.damage_dealt_last_turn = damage

        self.game_state.opponent_info.team.active_pokemon.reduce_HP(damage)

        print(
            f"Player did {damage} to {self.game_state.opponent_info.team.active_pokemon.pokemon_name.title()} using {self.game_state.player_info.current_move.move_name.title()}"
        )

    def opponent_attack(self):

        damage:int = dc.DamageCalculation(
            self.game_state.opponent_info.team.active_pokemon,
            self.game_state.player_info.team.active_pokemon,
            self.game_state.opponent_info.current_move,
        ).final_damage

        self.game_state.opponent_info.damage_dealt_last_turn = damage

        self.game_state.player_info.team.active_pokemon.reduce_HP(damage)
        print(
            f"Player did {damage} to {self.game_state.player_info.team.active_pokemon.pokemon_name.title()} using {self.game_state.opponent_info.current_move.move_name.title()}"
        )

    def end_turn_actions(self):
        self.game_state.opponent_info.team.update_fainted_pokemon()
        self.game_state.player_info.team.update_fainted_pokemon()

        self.check_game_over()

    def check_game_over(self):
        game_over = self.game_state.determine_if_winner()

        if game_over:
            print(f"Winner is {self.game_state.winner}")
        
    def reset_battle(self):
        self.game_state.reset_state()


    