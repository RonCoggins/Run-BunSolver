import json

import constants

constants.POKEMON_STATS
class ShowdownParser():
    def __init__(self):
        
        self.data: list[str] = []
        self.pokemon_names = [x for x in constants.POKEMON_STATS.keys()]

        self.team = {}

        self.parse_showdown()

    def parse_showdown(self):
        self.open_team_file()
        self.get_pokemon_names()

        for pokemon_names in self.team.keys():
            self.get_relevant_data(pokemon_names)

    def open_team_file(self):
        with open("team.txt", "r") as file:
            for line in file:
                self.data.append(line.strip().lower())

    def get_pokemon_names(self):
        for content in self.data:
            if content in self.pokemon_names:
                if "@" in content:
                    match = content.index("@")-1
                    without_atsign = content[0:match]
                    self.team[without_atsign] = {}
                else:
                    self.team[content] = {}

    def get_relevant_data(self, pokemon_name):

        for content in self.data:
            if pokemon_name in content:
                index_position = self.data.index(content)
                ability = self.get_ability(self.data[index_position+1])
                level = self.get_level(self.data[index_position+2])
                nature = self.get_nature(self.data[index_position+3])
                ivs = self.get_ivs(self.data[index_position+4])
                move1 = self.get_moves(self.data[index_position+5])
                move2 = self.get_moves(self.data[index_position+6])
                move3 = self.get_moves(self.data[index_position+7])
                move4 = self.get_moves(self.data[index_position+8])

                self.team[pokemon_name] = {"ability": ability,
                                            "level": level,
                                            "nature": nature,
                                            "ivs": ivs,
                                                "moves":[move1,
                                                         move2,
                                                         move3,
                                                         move4]

                                            }


    def get_ability(self, string):

        without_ability_word = ""
        match = string.index(" ")+1
        without_ability_word = string[match:]
        
        return without_ability_word.replace(" ","-")

    def get_level(self,string):

        without_level_word = ""
        match = string.index(" ")+1
        without_level_word = string[match:]
        
        return int(without_level_word)

    def get_nature(self,string):

        without_nature_word = ""
        match = string.index(" ")
        without_nature_word = string[:match]
        
        return without_nature_word        

    def get_ivs(self,string):

        iv_dict = {}
        
        cleaned_string = string.replace("ivs: ", " ").replace("hp"," ").replace("atk"," ").replace("def"," ").replace("spa"," ").replace("spd"," ").replace("spe"," ").replace("   /"," ").strip()
        
        string_as_list = cleaned_string.split()

        iv_dict = (int(string_as_list[0]),
                int(string_as_list[1]),
                int(string_as_list[2]),
                int(string_as_list[3]),
                int(string_as_list[4]),
                int(string_as_list[5]),
        )
        
        return iv_dict

    def get_moves(self, string):
            
        try:
            return string [2:].replace(" ","-")
        except:
            return None    