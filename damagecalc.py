import pokemon as p
import move as m
import type_advantage as t

import constants

import math
import numpy as np

class DamageCalculation():
    def __init__(self,
                attacking_pokemon : p.BattlingPokemon,
                target_pokemon: p.BattlingPokemon,
                move: m.Move,
                critical_hit: bool = False,
                final_calc: bool = False):

        self.move = move

        self.move_base_power = self.move.base_power
        self.move_type = self.move.move_type
        self.move_category = self.move.move_category

        self.attacking_pokemon = attacking_pokemon
        self.target_pokemon = target_pokemon

        self.critcal_hit: bool = critical_hit

        self.final_calc: bool = final_calc

        self.damage_range: np.array = self.core_damage_calculation()

        self.final_damage:int = max(self.damage_range)

        # self.max_damage = self.final_damage_calculation("max")
        # self.min_damage = self.final_damage_calculation("min")
        # self.all_damage_rolls = self.all_damage_rolls()

    
    def core_damage_calculation(self) -> np.array:

        if self.move_base_power == None:
            return 0

        level: int = self.attacking_pokemon.level
        power = self.move_base_power

        base_formula = (2 * level / 5 + 2) * power
        
        print(f"MOVE POWER: {power}")
        print(f"LEVEL: {level}")
        print(f"BASE: {base_formula}")

        if self.move_category == "physical":
            base_formula *= (self.attacking_pokemon.stats["atk"]/self.target_pokemon.stats["def"])
            
        elif self.move_category == "special":
            base_formula *= (self.attacking_pokemon.stats["spa"]/self.target_pokemon.stats["spd"])
            
        else:
            base_formula = 0

        print(f"BASE2: {base_formula}")

        base_formula /= 50
        base_formula = math.floor(base_formula)
        
        print(f"BASE3: {base_formula}")

        base_formula += 2
        base_formula = math.floor(base_formula)
        
        print(f"BASE: {base_formula}")

        #Damage=((2×Level5+2)×Power×AD50+2)×Targets×PB×Weather×GlaiveRush×Critical×random×STAB×Type×Burn×other×ZMove×TeraShield

        if self.critcal_hit == True:
            base_formula *= 1.5
            base_formula = math.floor(base_formula)

            print(f"CRIT: {base_formula}")

        base_formula *= self.apply_random_int()
        base_formula = np.floor(base_formula)
        
        print(f"RANDOM: {base_formula}")

        base_formula *= self.apply_stab()
        base_formula = np.floor(base_formula)
        
        print(f"STAB: {base_formula}")

        base_formula *= t.TypeMatchUp(self.move_type, self.target_pokemon.typing["type1"], self.target_pokemon.typing["type2"]).multiplier()
        base_formula = np.floor(base_formula)
        
        print(f"TYPE: {base_formula}")
        
        if self.final_calc == True:
            print(f"\t\tFinal damage calculation for {self.move.move_name} is {base_formula}")
        else:
            print(f"\t\tExploring max damage value for {self.move.move_name}, returning {base_formula}")

        return base_formula

    def apply_random_int(self):
        return np.array(constants.RANDOM_DAMAGE_INT)
    
    def apply_stab(self):
        
        multiplier = 1

        if self.move_type == self.attacking_pokemon.typing["type1"] or self.move_type == self.attacking_pokemon.typing["type2"]:
            multiplier = constants.STAB_MULTIPLIER
        
        
        return multiplier
     
