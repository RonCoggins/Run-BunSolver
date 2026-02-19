import move as m
import pokemon as p
import game_state as gs
import damagecalc as dc

from itertools import combinations

import numpy as np
import numpy.typing as npt

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

        self.move_category = {name: ("damaging" if move_object.base_power != None else "setup") for name, move_object in self.decision_making_pokemon.moveset.items()}


        self.damage_ranges: dict[str,npt.ArrayLike] = {}

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
        

        self.score_moves()
        print(self.move_scores)
        self.highest_scoring_move = max(self.move_scores, key=self.move_scores.get)
        print(self.highest_scoring_move)
        self.selected_move = self.decision_making_pokemon.moveset[self.highest_scoring_move]    

    def get_damage_ranges(self):
        
        damaging_moves = [key for key, value in self.move_category.items() if value == "damaging"]
        

        for move_index, move_obj in self.decision_making_pokemon.moveset.items():
            if move_index in damaging_moves:
                self.damage_ranges[move_index] = dc.DamageCalculation(
                    self.decision_making_pokemon, self.other_pokemon, move_obj, final_calc=False
                ).damage_range

    def get_highest_damage_rolls(self):

        damaging_moves = [key for key, value in self.move_category.items() if value == "damaging"]

        range_matrix: npt.ArrayLike = np.zeros((len(damaging_moves),16))

        for index, damage_range in enumerate(self.damage_ranges.values()):
            range_matrix[index] = damage_range
        
        highest_damage_array = np.max(range_matrix, axis=0)
        
        overlapping_rolls :dict[str,int]= {}

        total_rolls = 0

        for index, damage_range in self.damage_ranges.items():
            overlapping_rolls[index] = 0
            for damage_value in damage_range:
                
                if damage_value in highest_damage_array:
                    overlapping_rolls[index] += 1
                    total_rolls += 1
        
        self.damaging_move_selection_chance :dict[str,float]= {name: value/total_rolls for name, value in overlapping_rolls.items()}

    def score_moves(self):

        move_selection_probability_list = [x for x in self.damaging_move_selection_chance.values()]
        damaging_move_list = [key for key, value in self.move_category.items() if value == "damaging"]

        selected_highest_damage_move: str = np.random.choice(damaging_move_list, p=move_selection_probability_list)

        self.move_scores[selected_highest_damage_move] = self.highest_damage_move_score()


    def highest_damage_move_score(self):

        score_index = 0
        chance_index = 1

        possible_scores = [constants.MAX_DAMAGING_MOVE_SCORE[score_index],constants.MIN_DAMAGING_MOVE_SCORE[score_index]]
        scores_chances = [constants.MAX_DAMAGING_MOVE_SCORE[chance_index],constants.MIN_DAMAGING_MOVE_SCORE[chance_index]]

        print(possible_scores)
        print(scores_chances)
        
        selected_score = np.random.choice(possible_scores, p=scores_chances)

        return selected_score









            

            



        

                
        
        

                
            


    
        
    
        
        
            

                



            


            





        



