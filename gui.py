import tkinter as tk
import team as t
import pokemon as p
import random
import battle_engine as gs



class GUI:
    def __init__(self):
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

        self.party_pokemon_listbox: tk.Listbox = self.create_party_pokemon_listbox()

        tk.Label(pokemon_select_frame, anchor="center").pack()

        ### Stats List

        hp_stat = tk.StringVar(value = p.PlayerPokemon("Yanmega").stats["hp"])
        self.hp_label: tk.Label = tk.Label(stats_display_frame, text=hp_stat)
        self.hp_label.pack()

        root.mainloop()

    def create_party_pokemon_listbox(self) -> tk.Listbox:
        party_pokemon_listbox = tk.Listbox()
        party_pokemon_listbox.pack()
        party_pokemon_listbox.bind('<<ListboxSelect>>',self.update_player_pokemon_stats)

        for index, pokemon in enumerate(list(p.POKEMON_STATS_PLAYER.keys())):

            party_pokemon_listbox.insert(index, pokemon)

        return party_pokemon_listbox
    
    def update_player_pokemon_stats(self,event) -> str:
        
        current_index :int = self.party_pokemon_listbox.curselection()
        
        selected_pokemon: str = str(self.party_pokemon_listbox.get(current_index))

        print(selected_pokemon)

        self.hp_label.config(text=f"HP: {p.PlayerPokemon(selected_pokemon).stats["hp"]}" +
                             f" ATK: {p.PlayerPokemon(selected_pokemon).stats["atk"]}"+
                             f" DEF: {p.PlayerPokemon(selected_pokemon).stats["def"]}"+
                             f" SPA: {p.PlayerPokemon(selected_pokemon).stats["spa"]}"+
                             f" SPD: {p.PlayerPokemon(selected_pokemon).stats["spd"]}"+
                             f" SPE: {p.PlayerPokemon(selected_pokemon).stats["spe"]}")

        return selected_pokemon
    

GUI()