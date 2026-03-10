import tkinter as tk
from pathlib import Path

import numpy as np

import src.RunandBunMachine.team as t
import src.RunandBunMachine.pokemon as p
import src.RunandBunMachine.game_state as gs
import src.RunandBunMachine.battle_engine as be


PNG_DIRECTORY = Path('./gui/assets/png')

class BattleFrame(tk.Frame):
    def __init__(self, parent_frame,battle_engine: be.BattleEngine):
        tk.Frame.__init__(self, parent_frame)
        self.battle_engine = battle_engine 
        self.game_state = battle_engine.game_state

        self.first_load = True

        self.player_row = 3
        self.opponent_row = 4

        self.active_pokemon = {}
        
        self.active_pokemon_data = {"player": {},
                                    "opponent": {}}

        self.add_buttons()
        self.add_headers()

    def add_buttons(self):

        self.start_battle_button: tk.Button = tk.Button(self, text="Start Battle", command=lambda: [self.battle_engine.run_one_turn(), self.update_info()])
        self.start_battle_button.grid(row=1, column =1)
        tk.Button(self, text="Simulate Full Battle", command=lambda: [self.battle_engine.finish_battle(), self.update_info()]).grid(row=1, column =2)
        tk.Button(self, text="Reset Battle", command=lambda: [self.battle_engine.reset_battle(), self.update_info()]).grid(row=1, column =3)

    def add_headers(self):
        
        self.headers = {"pos1": "Active Pokemon",
                        "pos2": "Current HP",
                        "pos3": "Move Used Last",
                        "pos4": "Damage Dealt",
                        "pos5": "Damage Ranges"}
        
        self.headers_labels = {}
        
        column = 0

        for key, value in self.headers.items():
            self.headers_labels[key] = tk.Label(self, text= value)
            self.headers_labels[key].grid(row=2, column = column)
            column += 1

    def update_info(self):

        self.active_pokemon: dict[str,str] = {"player": self.battle_engine.game_state.player_info.team.active_pokemon.pokemon_name,
                                         "opponent": self.battle_engine.game_state.opponent_info.team.active_pokemon.pokemon_name}
        
        self.update_header_info()
        self.update_active_pokemon_png()

    def update_header_info(self):

        self.set_turn_number()
        self.set_pokemon_health()
        self.set_pokemon_move_used()
        self.set_damage_dealt()
        self.set_damage_ranges()
    

    def set_turn_number(self):

        self.turn_var = tk.StringVar()
        self.turn_var.set("Turn Number: " + str(self.battle_engine.game_state.turn_info.turn_number)) 
        tk.Label(self, textvariable=self.turn_var).grid(row=0, column=0)
    
    def set_pokemon_health(self):

        self.player_pokemon_health_var = tk.StringVar()
        self.player_pokemon_health_var.set(str(f"{self.battle_engine.game_state.player_info.team.active_pokemon.current_HP} / {self.battle_engine.game_state.player_info.team.active_pokemon.UserPokemon.stats["hp"]}")) 
        tk.Label(self, textvariable=self.player_pokemon_health_var).grid(row=self.player_row,column=1)
    
        self.opponent_pokemon_health_var = tk.StringVar()
        self.opponent_pokemon_health_var.set(str(f"{self.battle_engine.game_state.opponent_info.team.active_pokemon.current_HP} / {self.battle_engine.game_state.opponent_info.team.active_pokemon.UserPokemon.stats["hp"]}"))
        tk.Label(self, textvariable=self.opponent_pokemon_health_var).grid(row=self.opponent_row,column=1)

    def set_pokemon_move_used(self):

        self.player_pokemon_move_used_var = tk.StringVar()
        self.player_pokemon_move_used_var.set(str(self.battle_engine.game_state.player_info.current_move)) 
        tk.Label(self, textvariable=self.player_pokemon_move_used_var).grid(row=self.player_row,column=2)

        self.opponent_pokemon_move_used_var = tk.StringVar()
        self.opponent_pokemon_move_used_var.set(str(self.battle_engine.game_state.opponent_info.current_move)) 
        tk.Label(self, textvariable=self.opponent_pokemon_move_used_var).grid(row=self.opponent_row,column=2)
    
    def set_damage_dealt(self):

        self.player_damage_dealt = tk.StringVar()
        self.player_damage_dealt.set(str(self.battle_engine.game_state.player_info.team.active_pokemon.current_turn_damage_dealt)) 
        tk.Label(self, textvariable=self.player_damage_dealt).grid(row=self.player_row,column=3)

        self.opponent_damage_dealt = tk.StringVar()
        self.opponent_damage_dealt.set(str(self.battle_engine.game_state.opponent_info.team.active_pokemon.current_turn_damage_dealt)) 
        tk.Label(self, textvariable=self.opponent_damage_dealt).grid(row=self.opponent_row,column=3)
    
    def set_damage_ranges(self):
        
        self.player_damage_range = tk.StringVar()
        self.player_damage_range.set(str(self.clean_damage_ranges(True))) 
        tk.Label(self, textvariable=self.player_damage_range).grid(row=self.player_row,column=4)

        self.opponent_damage_range = tk.StringVar()
        self.opponent_damage_range.set(str(self.clean_damage_ranges(False))) 
        tk.Label(self, textvariable=self.opponent_damage_range).grid(row=self.opponent_row,column=4)

    def update_active_pokemon_png(self):

        
        self.active_pokemon_data = {"player": {},
                                    "opponent": {}}

        print(self.active_pokemon)

        for key, value in self.active_pokemon.items():
            png_location = f"{PNG_DIRECTORY}/{value.upper()}.png"
            print(png_location)
            self.active_pokemon_data[key]["photo_image_obj"] = tk.PhotoImage(file=png_location,height=64,width=64)
            self.active_pokemon_data[key]["png_label"] = tk.Label(self, image=self.active_pokemon_data[key]["photo_image_obj"])

            if key == "player":
                self.active_pokemon_data[key]["png_label"].grid(row=3, column=0)
            else:
                self.active_pokemon_data[key]["png_label"].grid(row=4, column=0)


    def clean_damage_ranges(self, player=True):
        
        string = ""
        if player:
            for move_index, range in self.battle_engine.game_state.player_info.team.active_pokemon.current_turn_damage_ranges.items():
                string += f"{str(self.battle_engine.game_state.player_info.team.active_pokemon.moveset[move_index]).title()}: {np.array_str(range)}\n"
        else:
            for move_index, range in self.battle_engine.game_state.opponent_info.team.active_pokemon.current_turn_damage_ranges.items():
                string += f"{str(self.battle_engine.game_state.opponent_info.team.active_pokemon.moveset[move_index]).title()}: {np.array_str(range)}\n"

        return string


        


        if player:
            damage_ranges = [range for move_index, range in self.battle_engine.game_state.player_info.team.active_pokemon.current_turn_damage_ranges.items()]
        else:
            damage_ranges = [range for move_index, range in self.battle_engine.game_state.opponent_info.team.active_pokemon.current_turn_damage_ranges.items()]

        return damage_ranges