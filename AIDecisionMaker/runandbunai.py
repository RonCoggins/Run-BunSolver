import move as m
import pokemon as p
import game_state as gs
import damagecalc as dc

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

        self.highest_scoring_move = max(self.move_scores)

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

        print(self.possible_scores)




        



