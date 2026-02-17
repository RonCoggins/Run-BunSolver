import move as m
import pokemon as p
import game_state as gs
import damagecalc as dc


class MaxDamageAI:

    def __init__(self, game_state: gs.GameState, player: bool):

        self.player = player

        if self.player:
            self.decision_making_pokemon: p.BattlingPokemon = game_state.player_info.team.active_pokemon
            self.other_pokemon: p.BattlingPokemon = game_state.opponent_info.team.active_pokemon
        else:
            self.decision_making_pokemon: p.BattlingPokemon = game_state.opponent_info.team.active_pokemon
            self.other_pokemon: p.BattlingPokemon = game_state.player_info.team.active_pokemon

        self.highest_damage_move: m.Move = self.get_highest_damage_move()


    def get_highest_damage_move(self):
        
        moves_obj_unsanitised: list[m.Move | None] = list(
            self.decision_making_pokemon.moveset.values()
        )

        moves_obj_list: list[m.Move] = [
            x for x in moves_obj_unsanitised if type(x) == m.Move
        ]

        move_damages: list[int] = []

        print("\tSelecting highest damage move")

        for move in moves_obj_list:

            damage: int = dc.DamageCalculation(
                self.decision_making_pokemon, self.other_pokemon, move, final_calc=False
            ).final_damage

            move_damages.append(damage)

        highest_damaging_move_index = move_damages.index(max(move_damages))

        print(f"\t\t{self.decision_making_pokemon} damages:{move_damages}")

        print(
            f"\t\t{self.decision_making_pokemon} highest damaging move is {moves_obj_list[highest_damaging_move_index].move_name}\n\n"
        )

        return moves_obj_list[highest_damaging_move_index]