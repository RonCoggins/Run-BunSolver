class TypeMatchUp():

    def __init__(self, move_type, target_pokemon_type_1, target_pokemon_type_2):

        self.move_type = move_type

        self.target_pokemon_type_1 = target_pokemon_type_1
        self.target_pokemon_type_2 = target_pokemon_type_2

        self.matchup_dict = {
            "normal":  {'effective': [], 'non_effective': ['rock', 'steel'], 'immune': ['ghost']},

            "fire":    {'effective': ['grass', 'ice', 'bug', 'steel'],
                        'non_effective': ['fire', 'water', 'rock', 'dragon'],
                        'immune': []},

            "water":   {'effective': ['fire', 'ground', 'rock'],
                        'non_effective': ['water', 'grass', 'dragon'],
                        'immune': []},

            "electric":{'effective': ['water', 'flying'],
                        'non_effective': ['electric', 'grass', 'dragon'],
                        'immune': ['ground']},

            "grass":   {'effective': ['water', 'ground', 'rock'],
                        'non_effective': ['fire', 'grass', 'poison', 'flying', 'bug', 'dragon', 'steel'],
                        'immune': []},

            "ice":     {'effective': ['grass', 'ground', 'flying', 'dragon'],
                        'non_effective': ['fire', 'water', 'ice', 'steel'],
                        'immune': []},

            "fighting":{'effective': ['normal', 'ice', 'rock', 'dark', 'steel'],
                        'non_effective': ['poison', 'flying', 'psychic', 'bug', 'fairy'],
                        'immune': ['ghost']},

            "poison":  {'effective': ['grass', 'fairy'],
                        'non_effective': ['poison', 'ground', 'rock', 'ghost'],
                        'immune': ['steel']},

            "ground":  {'effective': ['fire', 'electric', 'poison', 'rock', 'steel'],
                        'non_effective': ['grass', 'bug'],
                        'immune': ['flying']},

            "flying":  {'effective': ['grass', 'fighting', 'bug'],
                        'non_effective': ['electric', 'rock', 'steel'],
                        'immune': []},

            "psychic": {'effective': ['fighting', 'poison'],
                        'non_effective': ['psychic', 'steel'],
                        'immune': ['dark']},

            "bug":     {'effective': ['grass', 'psychic', 'dark'],
                        'non_effective': ['fire', 'fighting', 'poison', 'flying', 'ghost', 'steel', 'fairy'],
                        'immune': []},

            "rock":    {'effective': ['fire', 'ice', 'flying', 'bug'],
                        'non_effective': ['fighting', 'ground', 'steel'],
                        'immune': []},

            "ghost":   {'effective': ['psychic', 'ghost'],
                        'non_effective': ['dark'],
                        'immune': ['normal']},

            "dragon":  {'effective': ['dragon'],
                        'non_effective': ['steel'],
                        'immune': ['fairy']},

            "dark":    {'effective': ['psychic', 'ghost'],
                        'non_effective': ['fighting', 'dark', 'fairy'],
                        'immune': []},

            "steel":   {'effective': ['ice', 'rock', 'fairy'],
                        'non_effective': ['fire', 'water', 'electric', 'steel'],
                        'immune': []},

            "fairy":   {'effective': ['fighting', 'dragon', 'dark'],
                        'non_effective': ['fire', 'poison', 'steel'],
                        'immune': []}
        }



    def multiplier(self):

        multiplier = 1

        if self.target_pokemon_type_1 in self.matchup_dict[self.move_type]['effective']:
            multiplier *= 2
        elif self.target_pokemon_type_1 in self.matchup_dict[self.move_type]['non_effective']:
            multiplier *= 0.5
        
        if self.target_pokemon_type_2 in self.matchup_dict[self.move_type]['effective']:
            multiplier *= 2
        elif self.target_pokemon_type_2 in self.matchup_dict[self.move_type]['non_effective']:
            multiplier *= 0.5
        
        if self.target_pokemon_type_1 in self.matchup_dict[self.move_type]['immune'] or self.target_pokemon_type_2 in self.matchup_dict[self.move_type]:
            multiplier *= 0

        return multiplier