import game_state as gs
import damagecalc as dc

import pokemon as p
import team as t

import numpy as np


class SwitchInAI():

    def __init__(self, game_state: gs.GameState, player=True):
        
        self.game_state = game_state

        self.player = player

        if self.player:
            self.decision_making_team: t.BattlingTeam = self.game_state.player_info.team
            self.opposing_pokemon: p.BattlingPokemon = self.game_state.opponent_info.team.active_pokemon
        else:
            self.decision_making_team: t.BattlingTeam = self.game_state.opponent_info.team
            self.opposing_pokemon: p.BattlingPokemon = self.game_state.player_info.team.active_pokemon

    def get_switch_in_decision(self):

        scores = {}

        for slot_number, pokemon_obj in self.decision_making_team.remaining_pokemon.items():

            faster: bool = self.check_speed(pokemon_obj)
            canOHKO: bool = self.check_can_OHKO(pokemon_obj)
            outdamage: bool = self.check_outdamage(pokemon_obj)
            isOHKO: bool = self.check_is_OHKO(pokemon_obj)


            if canOHKO and faster:
                scores[slot_number] = 5
                continue

            if canOHKO and not faster:
                scores[slot_number] = 4
                continue

            if outdamage and faster:
                scores[slot_number] = 3
                continue

            if outdamage and not faster:
                scores[slot_number] = 2
                continue

            if faster:
                scores[slot_number] = 1
                continue

            if isOHKO:
                scores[slot_number] = -1
                continue

            scores[slot_number] = 0

        print(scores)

        return "slot_2"

            







            
        
    def check_can_OHKO(self, pokemon: p.BattlingPokemon) -> bool:

        OHKO: bool = False

        max_damage_rolls = np.array([dc.DamageCalculation(pokemon, self.opposing_pokemon, x).max_roll for x in pokemon.moveset.values()])
        
        current_opposing_pokemon_hp = self.opposing_pokemon.current_HP

        if (max_damage_rolls >= current_opposing_pokemon_hp).any():
            OHKO = True
        
        return OHKO

    def check_is_OHKO(self, pokemon: p.BattlingPokemon) -> bool:

        OHKO: bool = False

        max_damage_rolls = np.array([dc.DamageCalculation(self.opposing_pokemon, pokemon, x).max_roll for x in self.opposing_pokemon.moveset.values()])
        
        current_opposing_pokemon_hp = self.opposing_pokemon.current_HP

        if (max_damage_rolls >= current_opposing_pokemon_hp).any():
            OHKO = True
        
        return OHKO

    def check_outdamage(self, pokemon: p.BattlingPokemon) -> bool:

        outdamages: bool = False

        max_damage_roll_decision_maker = np.array([dc.DamageCalculation(pokemon, self.opposing_pokemon, x).max_roll for x in pokemon.moveset.values()])
        current_opposing_pokemon_hp = self.opposing_pokemon.current_HP

        opposing_pokemon_new_hp = current_opposing_pokemon_hp-np.max(max_damage_roll_decision_maker)
        opposing_pokemon_percentage_lost:float = abs((current_opposing_pokemon_hp - opposing_pokemon_new_hp)/current_opposing_pokemon_hp)*100

        max_roll_opposing_pokemon = np.array([dc.DamageCalculation(self.opposing_pokemon, pokemon, x).max_roll for x in self.opposing_pokemon.moveset.values()])
        current_decision_making_pokemon_hp = pokemon.current_HP

        decision_making_pokemon_new_hp = current_decision_making_pokemon_hp-np.max(max_roll_opposing_pokemon)
        decision_making_pokemon_percentage_lost:float = abs((current_decision_making_pokemon_hp - decision_making_pokemon_new_hp )/current_decision_making_pokemon_hp)*100

        if decision_making_pokemon_percentage_lost < opposing_pokemon_percentage_lost:
            outdamages = True
        
        return outdamages

    def check_speed(self, pokemon: p.BattlingPokemon) -> bool:

        faster: bool = False

        if pokemon.stats["spe"] >= self.opposing_pokemon.stats["spe"]:
            faster = True

        return faster








        

        
