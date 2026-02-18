import move as m
import pokemon as p
import game_state as gs
import damagecalc as dc

import numpy as np

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

        self.possible_scores : dict[str, list[list[int|float]]] = {"move1" : [[]],
                                                                    "move2" : [[]],
                                                                    "move3" : [[]],
                                                                    "move4" : [[]],}
        
        self.move_scores :dict[str,int] = {"move1" : 0,
                                           "move2" : 0,
                                           "move3" : 0,
                                           "move4" : 0,}

        self.score_damaging_moves()
        self.get_highest_scoring_move()
        print(self.move_scores)
        self.highest_scoring_move = max(self.move_scores, key=self.move_scores.get)
        self.selected_move = self.decision_making_pokemon.moveset[self.highest_scoring_move]

        

    def score_damaging_moves(self):
        
        damages = {}

        for move_index, move_obj in self.decision_making_pokemon.moveset.items():
            damages[move_index] = dc.DamageCalculation(
                self.decision_making_pokemon, self.other_pokemon, move_obj, final_calc=False
            ).final_damage

        highest_damage = damages[max(damages, key=damages.get)]

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
                print(score)
                score_array.append(score[score_index])
                chance_array.append(score[chance_index])
            
            
            random_choice = int(np.random.choice(a=score_array,p=chance_array))
            print(f"RANDOM CHOICE: {random_choice}")
            self.move_scores[move_index] = random_choice
            score_array: list[int] = []
            chance_array: list[float]= []
            

                



            


            





        



