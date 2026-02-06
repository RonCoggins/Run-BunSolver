import tkinter as tk
import team as t
import pokemon as p
import random
import game_state as gs
import battle_engine as be



class GUI:
    def __init__(self, battle_engine: be.BattleEngine):

        self.battle_engine = battle_engine

        root = tk.Tk()
        height: int = 600
        width: int = 600
        root.geometry(f"{height}x{width}")

        main_frame = tk.Frame(root)
        main_frame.pack()

        pokemon_select_frame = tk.Frame(
            main_frame, highlightthickness=1, highlightbackground="Black"
        )
        pokemon_select_frame.pack(side="left", padx=50)

        stats_display_frame = tk.Frame(
            main_frame, highlightthickness=1, highlightbackground="Black"
        )
        stats_display_frame.pack(side="right", padx=50)

        ### PLAYER POKEMON LIST BOX

        ### Start Battle Button

        tk.Button(pokemon_select_frame, text="Start Battle", command=lambda: [self.battle_engine.run_one_turn(), self.update_labels()].pack()
        tk.Button(pokemon_select_frame, text="Simulate Full Battle", command=self.battle_engine.finish_battle).pack()
        tk.Button(pokemon_select_frame, text="Reset Battle", command=self.battle_engine.reset_battle).pack()


        turn_var = tk.StringVar()
        turn_var.set(str(self.battle_engine.game_state.turn_info.turn_number)) 
        tk.Label(pokemon_select_frame, text=var).pack()
        

        root.mainloop()
    
    def update_labels(self):
        label = self.battle_engine.game_state.turn_info.turn_number
        
        
    

    
