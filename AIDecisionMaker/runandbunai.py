import move as m
import pokemon as p
import game_state as gs
import damagecalc as dc

import numpy as np
import numpy.typing as npt

from collections import Counter
from functools import reduce

import AIDecisionMaker.runandbunaiconstants as constants

class RunAndBunAI:

    def __init__(self, game_state: gs.GameState, player: bool):

        self.player = player

        if self.player:
            self.decision_making_pokemon: p.BattlingPokemon = game_state.player_info.team.active_pokemon
            self.other_pokemon: p.BattlingPokemon = game_state.opponent_info.team.active_pokemon
        else:
            self.decision_making_pokemon: p.BattlingPokemon = game_state.opponent_info.team.active_pokemon
            self.other_pokemon: p.BattlingPokemon = game_state.player_info.team.active_pokemon

        self.damage_ranges: dict[str,npt.ArrayLike] = {"move1" : [],
                                                    "move2" : [],
                                                    "move3" : [],
                                                    "move4" : [],}

        self.possible_scores : dict[str, list[list[int|float]]] = {"move1" : [[]],
                                                                    "move2" : [[]],
                                                                    "move3" : [[]],
                                                                    "move4" : [[]],}
        
        self.move_scores :dict[str,int] = {"move1" : 0,
                                           "move2" : 0,
                                           "move3" : 0,
                                           "move4" : 0,}

        self.get_damage_ranges()
        self.get_highest_damage_rolls()
        

        self.score_damaging_moves()
        self.get_highest_scoring_move()
        print(self.move_scores)
        self.highest_scoring_move = max(self.move_scores, key=self.move_scores.get)
        self.selected_move = self.decision_making_pokemon.moveset[self.highest_scoring_move]

    def get_damage_ranges(self):

        for move_index, move_obj in self.decision_making_pokemon.moveset.items():
            self.damage_ranges[move_index] = dc.DamageCalculation(
                self.decision_making_pokemon, self.other_pokemon, move_obj, final_calc=False
            ).damage_range

    def get_highest_damage_rolls(self):

        range_matrix: npt.ArrayLike = np.zeros((4,16))

        for index, damage_range in enumerate(self.damage_ranges.values()):
            range_matrix[index] = damage_range
        
        highest_damage_array = np.max(range_matrix, axis=0)

        print(highest_damage_array)
        
        overlapping_rolls :dict[str,int]= {"move1" : 0,
                                            "move2" : 0,
                                            "move3" : 0,
                                            "move4" : 0,}
        
        for index, damage_range in self.damage_ranges.items():
            for damage_value in damage_range:
                if damage_value in highest_damage_array:
                    print(f"Move Index: {index} {damage_value} in {damage_range}")
                    overlapping_rolls[index] += 1
        
        print(overlapping_rolls)





        






    def score_damaging_moves(self):
        
        print(self.damage_ranges)

        highest_damage = self.damage_ranges[max(self.damage_ranges, key=self.damage_ranges.get)]

        print(f"Highest Damage {highest_damage}")

        for move_index, damage_value in damages.items():
            if damage_value == highest_damage:
                self.possible_scores[move_index] = constants.MIN_DAMAGING_MOVE_SCORE,constants.MAX_DAMAGING_MOVE_SCORE
            else:
                self.possible_scores[move_index] = [constants.DEFAULT_MOVE_SCORE]


        

    def get_highest_scoring_move(self):

        #print(self.possible_scores)
        score_index = 0
        chance_index = 1

        score_array: list[int] = []
        chance_array: list[float]= []

        for move_index, scores in self.possible_scores.items():
            for score in scores:
                score_array.append(score[score_index])
                chance_array.append(score[chance_index])
            
            random_choice = int(np.random.choice(a=score_array,p=chance_array))
            self.move_scores[move_index] = random_choice
            score_array: list[int] = []
            chance_array: list[float]= []
            

                



            


            





        



