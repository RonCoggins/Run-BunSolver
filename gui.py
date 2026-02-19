import tkinter as tk
from tkinter import ttk
from pathlib import Path
from functools import cache

import numpy as np

import team as t
import pokemon as p
import random
import game_state as gs
import battle_engine as be
import opponenttrainers

PNG_DIRECTORY = Path('./png')


class GUI:
    def __init__(self, battle_engine: be.BattleEngine):

        self.battle_engine = battle_engine

        

        root = tk.Tk()
        height: int = 1500
        width: int = 1000
        root.geometry(f"{height}x{width}")
        root.resizable(False,False)

        self.battle_engine.init_game_state("Youngster Joey")

        main_frame = tk.Frame(root)
        main_frame.grid()

        self.battle_frame = BattleFrame(main_frame, battle_engine=self.battle_engine)
        self.opponent_team_frame = OpponentPokemonInfoFrame(main_frame, battle_engine=self.battle_engine,battle_frame=self.battle_frame)
        self.player_team_frame = PlayerPokemonInfoFrame(main_frame, battle_engine=self.battle_engine)
        
        self.player_team_frame.grid(row=0, column=0)
        self.opponent_team_frame.grid(row=0, column=1)
        self.battle_frame.grid(row=2)

        self.player_team_frame["padx"] = 20

        self.player_team_frame.rowconfigure(1)
        self.opponent_team_frame.rowconfigure(1)

        self.player_team_frame.columnconfigure(1)
        self.opponent_team_frame.columnconfigure(1)

        

        main_frame.rowconfigure(1)

        root.mainloop()
    

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

        self.start_battle_button: tk.Button = tk.Button(self, text="Start Battle", command=lambda: [self.battle_engine.run_one_turn(), self.update_info()], state="disabled")
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


    
class PlayerPokemonInfoFrame(tk.Frame):
    def __init__(self, parent_frame: tk.Frame, battle_engine: be.BattleEngine):
        tk.Frame.__init__(self, parent_frame)

        self.config(highlightbackground="black",highlightthickness=1, padx=10)
        self.config(height=500, width=400)
        self.grid_propagate(False)

        self.first_load:bool  = True

        self.parent_frame = parent_frame
        self.battle_engine = battle_engine

        self.create_player_pokemon_team()


    def create_player_pokemon_team(self):

        self.player_team_label = tk.Label(self, text="Player Team")
        self.player_team_label.grid(column=1,row=0)

        player_team_pokemon_obj:list[p.BattlingPokemon] = list(self.battle_engine.game_state.player_info.team.team.values())
        self.player_team_names: list[str] = [x.pokemon_name.upper() for x in player_team_pokemon_obj]

        self.player_team_info_dict: dict[str,tk.Label] = {}
                                                          
        self.stat_frame_dict: dict[str,tk.Frame] = {}

        column = 0
        row = 2
        
        for index in range(len(self.player_team_names)):
            self.player_team_info_dict[f"image{index}"] = tk.Label(self)
            self.stat_frame_dict[f"infoframe{index}"] = PokemonStatInformationFrame(self, player_team_pokemon_obj[index])
            self.stat_frame_dict[f"infoframe{index}"].config(height=64,width=64)

            self.player_team_info_dict[f"image{index}"].grid(column=column,row=row) 
            self.stat_frame_dict[f"infoframe{index}"].grid(column=column+1,row=row)

            if column < 2:
                column += 2
            else:
                column = 0
                row += 1

            

        self.load_player_pokemon_png()

    def load_player_pokemon_png(self):
    
        self.player_png_locations: dict[str, str] = {}
        self.player_photo_image_obj: dict[str, tk.PhotoImage] = {}

        for index, pokemon_name in enumerate(self.player_team_names):

            self.player_png_locations[f"image{index}"] = f"{PNG_DIRECTORY}/{pokemon_name}.png"
            self.player_photo_image_obj[f"image{index}"] = tk.PhotoImage(file=self.player_png_locations[f"image{index}"],width=64)
            self.player_team_info_dict[f"image{index}"]["image"] = self.player_photo_image_obj[f"image{index}"]

class OpponentPokemonInfoFrame(tk.Frame):

    def __init__(self, parent_frame: tk.Frame, battle_engine: be.BattleEngine, battle_frame: BattleFrame):
        tk.Frame.__init__(self, parent_frame)

        self.config(highlightbackground="black",highlightthickness=1, padx=10)
        self.config(height=500, width=400)
        self.grid_propagate(False)

        self.grid_propagate(False)

        self.parent_frame = parent_frame
        self.battle_engine = battle_engine
        self.battle_frame : BattleFrame = battle_frame

        self.first_load:bool  = True

        self.opponent_team_info_dict: dict[str,tk.Label] = {}
        self.stat_frame_dict: dict[str,tk.Frame] = {}

        self.create_available_trainers_list()

    def create_available_trainers_list(self):
        available_trainers = list(opponenttrainers.opponent_trainers.keys())
        self.trainers_combobox = ttk.Combobox(self, values=available_trainers)
        self.trainers_combobox.set("Select Opponent Trainer")
        self.trainers_combobox.grid(column=1,row=0)
        self.trainers_combobox.bind("<<ComboboxSelected>>", self.create_opponent_pokemon_team)

    def create_opponent_pokemon_team(self, event):

        trainer_selection = self.trainers_combobox.get()
        self.battle_engine.init_game_state(trainer_selection)
        trainer_team = t.BattlingTeam(False, trainer_selection)

        self.battle_frame.start_battle_button.configure(state="active")
        self.battle_frame.update_info()

        opponent_team_pokemon_obj:list[p.BattlingPokemon] = list(trainer_team.team.values())
        self.opponent_team_names: list[str] = [x.pokemon_name.upper() for x in opponent_team_pokemon_obj]

        column = 0
        row = 2

        self.destroy_existing_frames()

        for index in range(6):
            
            if index < len(self.opponent_team_names):
                
                self.opponent_team_info_dict[f"image{index}"] = tk.Label(self)

                self.stat_frame_dict[f"infoframe{index}"] = PokemonStatInformationFrame(self, opponent_team_pokemon_obj[index])
                self.stat_frame_dict[f"infoframe{index}"].config(height=64,width=64)

                self.opponent_team_info_dict[f"image{index}"].grid(column=column,row=row) 
                self.stat_frame_dict[f"infoframe{index}"].grid(column=column+1,row=row)
            else:
                
                self.opponent_team_info_dict[f"image{index}"] = tk.Label(self)
                self.stat_frame_dict[f"infoframe{index}"] = BlankFrame(self)
                self.opponent_team_info_dict[f"image{index}"].grid(column=column,row=row)
                self.stat_frame_dict[f"infoframe{index}"].grid(column=column+1,row=row)


            if column < 2:
                column += 2
            else:
                column = 0
                row += 1
        
        self.load_opponent_pokemon_png()

    def load_opponent_pokemon_png(self):


        self.opponent_png_locations: dict[str, str] = {}
        self.opponent_photo_image_obj: dict[str, tk.PhotoImage] = {}


        for index, pokemon_name in enumerate(self.opponent_team_names):

            self.opponent_png_locations[f"image{index}"] = f"{PNG_DIRECTORY}/{pokemon_name}.png"
            self.opponent_photo_image_obj[f"image{index}"] = tk.PhotoImage(file=self.opponent_png_locations[f"image{index}"],width=64)
            self.opponent_team_info_dict[f"image{index}"]["image"] = self.opponent_photo_image_obj[f"image{index}"]

    def destroy_existing_frames(self):

        for key in self.stat_frame_dict.keys():
            self.stat_frame_dict[key].destroy()
        for key in self.opponent_team_info_dict.keys():
            self.opponent_team_info_dict[key].destroy()

class PokemonStatInformationFrame(tk.Frame):
    def __init__(self, parent_frame: tk.Frame, battling_pokemon_obj: p.BattlingPokemon):
        tk.Frame.__init__(self, parent_frame)
        self.battling_pokemon_obj = battling_pokemon_obj
        
        self.parent_frame = parent_frame

        self.pokemon_name = tk.Label(self, text=f"Name: {self.get_name()}")
        self.level = tk.Label(self, text=f"Lvl: {self.get_level()}")
        self.hp = tk.Label(self, text=f"HP: {self.get_HP()}")
        self.moveset = tk.Label(self, text=self.get_moveset())

        self.stat_mapping: dict[str,int] = {
            "name": 0,
            "lvl" : 1,
            "hp" : 2,
            "moveset" : 3,
        }

        self.pokemon_name.grid(row=self.stat_mapping["name"])
        self.level.grid(row=self.stat_mapping["lvl"])
        self.hp.grid(row=self.stat_mapping["hp"])
        self.moveset.grid(row=self.stat_mapping["moveset"])

    
    def get_name(self) -> str:

        return self.battling_pokemon_obj.pokemon_name.title()

    def get_level(self) -> int:

        return self.battling_pokemon_obj.level

    def get_HP(self) -> int:

        return self.battling_pokemon_obj.current_HP
    
    def get_moveset(self) -> list:

        moveset = list(self.battling_pokemon_obj.moveset.values())
        moveset = [x.move_name.title() for x in moveset]

        formatted_string = ""

        for movename in moveset:
           formatted_string = formatted_string + movename +"\n"
        
        return formatted_string

class BlankFrame(tk.Frame):
    def __init__(self, parent_frame: tk.Frame):
        tk.Frame.__init__(self, parent_frame)

        self.config(height=64, width=64)


            
        
        

    