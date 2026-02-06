import tkinter as tk
import team as t
import pokemon as p
import random
import game_state as gs
import battle_engine as be
import opponenttrainers



class GUI:
    def __init__(self, battle_engine: be.BattleEngine):

        self.battle_engine = battle_engine

        root = tk.Tk()
        height: int = 600
        width: int = 600
        root.geometry(f"{height}x{width}")

        main_frame = tk.Frame(root)
        main_frame.grid()

        battle_frame = tk.Frame(
            main_frame, highlightthickness=1, highlightbackground="Black"
        )
        battle_frame.grid(row=0, column=0, padx=50)

        stats_display_frame = tk.Frame(
            main_frame, highlightthickness=1, highlightbackground="Black"
        )
        stats_display_frame.grid(row=1, column=0, padx=50)

        ### PLAYER POKEMON LIST BOX

        ### Start Battle Button
        
        tk.Button(battle_frame, text="Start Battle", command=lambda: [self.battle_engine.run_one_turn(), self.update_labels()]).grid(row=4)
        tk.Button(battle_frame, text="Simulate Full Battle", command=lambda: [self.battle_engine.finish_battle(), self.update_labels()]).grid(row=5)
        tk.Button(battle_frame, text="Reset Battle", command=lambda: [self.battle_engine.reset_battle(), self.update_labels()]).grid(row=6)


        self.turn_var = tk.StringVar()
        self.turn_var.set("Turn Number: " + str(self.battle_engine.game_state.turn_info.turn_number)) 
        tk.Label(battle_frame, textvariable=self.turn_var).grid(row=0, column=0)

        self.player_pokemon_var = tk.StringVar()
        self.player_pokemon_var.set("Player Pokemon: " + str(self.battle_engine.game_state.player_info.team.active_pokemon).title()) 
        tk.Label(battle_frame, textvariable=self.player_pokemon_var).grid(row=1,column=0)

        self.opponent_pokemon_var = tk.StringVar()
        self.opponent_pokemon_var.set("Opponent Pokemon: " + str(self.battle_engine.game_state.opponent_info.team.active_pokemon).title()) 
        tk.Label(battle_frame, textvariable=self.opponent_pokemon_var).grid(row=2,column=0)

        tk.Label(battle_frame, text="HP").grid(row=0, column=1)

        self.player_pokemon_health_var = tk.StringVar()
        self.player_pokemon_health_var.set(str(self.battle_engine.game_state.player_info.team.active_pokemon.current_HP)) 
        tk.Label(battle_frame, textvariable=self.player_pokemon_health_var).grid(row=1,column=1)

        self.opponent_pokemon_health_var = tk.StringVar()
        self.opponent_pokemon_health_var.set(str(self.battle_engine.game_state.opponent_info.team.active_pokemon.current_HP)) 
        tk.Label(battle_frame, textvariable=self.opponent_pokemon_health_var).grid(row=2,column=1)

        tk.Label(battle_frame, text="Last Move Used").grid(row=0, column=2)

        self.player_pokemon_move_used_var = tk.StringVar()
        self.player_pokemon_move_used_var.set(str(self.battle_engine.game_state.player_info.current_move)) 
        tk.Label(battle_frame, textvariable=self.player_pokemon_move_used_var).grid(row=1,column=2)

        self.opponent_pokemon_move_used_var = tk.StringVar()
        self.opponent_pokemon_move_used_var.set(str(self.battle_engine.game_state.opponent_info.current_move)) 
        tk.Label(battle_frame, textvariable=self.opponent_pokemon_move_used_var).grid(row=2,column=2)

        self.player_pokemon_remaining_var = tk.StringVar()
        self.player_pokemon_remaining_var.set(str(self.battle_engine.game_state.player_info.team.team))
        tk.Label(stats_display_frame, textvariable=self.player_pokemon_remaining_var,wraplength=100,justify="left").grid(row=2,column=2)
        
        self.available_trainers = self.create_available_trainers_list(stats_display_frame)
        self.available_trainers.grid(row=5, column=2)

        self.opponent_pokemon_remaining_var = tk.StringVar()
        self.opponent_pokemon_remaining_var.set(str(self.battle_engine.game_state.opponent_info.team.team))
        tk.Label(stats_display_frame, textvariable=self.opponent_pokemon_remaining_var,wraplength=100,justify="left").grid(row=3,column=2)

        self.update_opponent_pictures():
        

        root.mainloop()
    
    def update_labels(self) -> None:
        self.turn_var.set("Turn Number: " + str(self.battle_engine.game_state.turn_info.turn_number)) 

        self.player_pokemon_var.set("Player Pokemon: " + str(self.battle_engine.game_state.player_info.team.active_pokemon).title()) 
        self.opponent_pokemon_var.set("Opponent Pokemon: " + str(self.battle_engine.game_state.opponent_info.team.active_pokemon).title())

        self.player_pokemon_health_var.set(str(self.battle_engine.game_state.player_info.team.active_pokemon.current_HP)) 
        self.opponent_pokemon_health_var.set(str(self.battle_engine.game_state.opponent_info.team.active_pokemon.current_HP))

        self.player_pokemon_move_used_var.set(str(self.battle_engine.game_state.player_info.current_move))
        self.opponent_pokemon_move_used_var.set(str(self.battle_engine.game_state.opponent_info.current_move))

        self.player_pokemon_remaining_var.set(str(self.battle_engine.game_state.player_info.team.team))

    def create_available_trainers_list(self,parent_frame: tk.Frame):
        available_trainers = list(opponenttrainers.opponent_trainers.keys())
        list_variable = tk.Variable(value=available_trainers)
        listbox = tk.Listbox(parent_frame, listvariable=list_variable)
        listbox.bind("<<ListboxSelect>>", self.update_trainer_selection)
        return listbox
    
    def update_trainer_selection(self, event):
        #this loooks horrible, curselection was returning a tuple so work around
        selection = event.widget.curselection()
        selection = selection[0]
        selected_trainer = list(opponenttrainers.opponent_trainers.keys())[selection]
        self.update_opponent_pokemon(selected_trainer)
        

    def update_opponent_pokemon(self, selected_trainer):
        opponent_team = t.BattlingTeam(False,selected_trainer)
        self.opponent_pokemon_remaining_var.set(str(opponent_team.team))

        


    
