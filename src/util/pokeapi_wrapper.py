import requests
import json

base_url = "https://pokeapi.co/api/v2/"

class PokemonInfoRetrieval():
    
    def __init__(self, pokemon_name):
        self.pokemon_name = pokemon_name
        self.URL = str(base_url + "pokemon/" + pokemon_name)

    #STATS

    def get_hp_stat(self):
        hp_API_index = 0
        return requests.get(self.URL).json()["stats"][hp_API_index]["base_stat"]
    
    def get_atk_stat(self):
        attack_API_index = 1
        return requests.get(self.URL).json()["stats"][attack_API_index]["base_stat"]
    
    def get_def_stat(self):
        defence_API_index = 2
        return requests.get(self.URL).json()["stats"][defence_API_index]["base_stat"]
    
    def get_spa_stat(self):
        spa_API_index = 3
        return requests.get(self.URL).json()["stats"][spa_API_index]["base_stat"]
    
    def get_spd_stat(self):
        spd_API_index = 4
        return requests.get(self.URL).json()["stats"][spd_API_index]["base_stat"]

    def get_spe_stat(self):
        speed_API_index = 5
        return requests.get(self.URL).json()["stats"][speed_API_index]["base_stat"]

    #typing
    
    def get_typing(self, type_number):

        try:
            return requests.get(self.URL).json()["types"][type_number]["type"]["name"]

        except:
            return "none"


class MoveInfoRetrieval():
    
    def __init__(self, move_number):
        self.move_number = move_number
        
        self.URL = str(base_url + "move/" + str(move_number))

        self.move_name = requests.get(self.URL).json()["name"]

    def get_move_typing(self):
        return requests.get(self.URL).json()["type"]["name"]

    def get_move_base_power(self):
        return requests.get(self.URL).json()["power"]
    
    def get_move_category(self):
        return requests.get(self.URL).json()["damage_class"]["name"]
    
    def add_data_to_json(self):
        json_content = {"base_power": self.get_move_base_power(),
                        "move_category": self.get_move_category(),
                        "typing" : self.get_move_typing(),
                        }
        
        
        current_data = {}

        
        with open("movestats.json", mode="r") as file:
            current_data = json.load(file)
        
        with open("movestats.json", mode="w") as file:
            current_data[self.move_name] = json_content
            json.dump(current_data, file, indent=4)

tries = []

number_of_moves = 919

# for num in range(312,number_of_moves):
#     test = MoveInfoRetrieval(num)
#     try:
#         test.add_data_to_json()
#         print(f"Completed: {num}/{number_of_moves} - {num/number_of_moves}% Complete")
#     except:
#         tries.append(num)

# print(tries)
        
    



