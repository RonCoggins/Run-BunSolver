import move as m
import pokemon as p
import game_state as gs
import damagecalc as dc


class OpponentMoveAIDecision:

    def __init__(self, game_state: gs.GameState):

        self.player_pokemon: p.BattlingPokemon = game_state.player_info.team.active_pokemon
        self.opponent_pokemon: p.BattlingPokemon = game_state.opponent_info.team.active_pokemon

        self.highest_damage_move: m.Move = self.get_highest_damage_move()


    def get_highest_damage_move(self):
        moves_obj_unsanitised: list[m.Move | None] = list(
            self.opponent_pokemon.moveset.values()
        )

        moves_obj_list: list[m.Move] = [
            x for x in moves_obj_unsanitised if type(x) == m.Move
        ]

        move_damages: list[int] = []

        print("\tSelecting opponent highest damage move")

        for move in moves_obj_list:

            damage: int = dc.DamageCalculation(
                self.opponent_pokemon, self.player_pokemon, move, final_calc=False
            ).final_damage

            move_damages.append(damage)

        highest_damaging_move_index = move_damages.index(max(move_damages))

        print(f"\t\t{self.opponent_pokemon.pokemon_name} damages:{move_damages}")

        print(
            f"\t\t{self.opponent_pokemon.pokemon_name} highest damaging move is {moves_obj_list[highest_damaging_move_index].move_name}\n\n"
        )

        return moves_obj_list[highest_damaging_move_index]


class SwitchInAIDecision:
    def __init__(self, remaining_pokemon):

        self.remaining_pokemon = remaining_pokemon

        self.switch_in_decision: str = self.get_switch_in_decision()

    def get_switch_in_decision(self) -> str:

        remaining_slots:list[str] = [x for x in self.remaining_pokemon.keys()]

        first_position = 0

        switch_in_slot = (str(remaining_slots[first_position]))

        return switch_in_slot