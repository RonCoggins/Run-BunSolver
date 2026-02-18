import move as m
import pokemon as p
import game_state as gs
import damagecalc as dc

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
        

        self.score_moves()
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
        
        overlapping_rolls :dict[str,int]= {"move1" : 0,
                                            "move2" : 0,
                                            "move3" : 0,
                                            "move4" : 0,}

        total_rolls = 0
        
        for index, damage_range in self.damage_ranges.items():
            for damage_value in damage_range:
                if damage_value in highest_damage_array:
                    overlapping_rolls[index] += 1
                    total_rolls += 1
        
        self.selection_chance :dict[str,int]= {"move1" : overlapping_rolls["move1"]/total_rolls,
                                                "move2" : overlapping_rolls["move2"]/total_rolls,
                                                "move3" : overlapping_rolls["move3"]/total_rolls,
                                                "move4" : overlapping_rolls["move4"]/total_rolls,}

    def score_moves(self):

        for move_index, selection_chance in self.selection_chance.items():
            self.possible_scores[move_index] = constants.MIN_DAMAGING_MOVE_SCORE,constants.MAX_DAMAGING_MOVE_SCORE,[selection_chance]
            
    def get_highest_scoring_move(self):

        print(self.possible_scores)

        score_index = 0
        chance_index = 1

        expected_score = 0

        for index, scores in self.possible_scores.items():
            for _score in scores:
                if len(_score) > 1:
                    
                    score = _score[score_index]
                    chance = _score[chance_index]
                    expected_score += score*chance
                    print(expected_score)

                else:

                    move_selection_chance = _score[0]

                    self.move_scores[index] = expected_score * move_selection_chance
                    expected_score = 0
        
        print(self.move_scores)
        
        
            

                



            


            





        



