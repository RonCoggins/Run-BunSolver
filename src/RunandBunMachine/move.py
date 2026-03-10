import json

def load_move_stats() -> dict[str, dict[str, str | int]]:

    move_stats: dict[str, dict[str, str | int]] = {}

    with open("src/constants/movestats.json","r") as file:
        move_stats = json.load(file)

    return move_stats

MOVE_STATS: dict[str, dict[str, str | int]] = load_move_stats()

class Move():
    
    def __init__(self, move_name: str):
        
        self.move_name: str = move_name.lower()

        self.base_power: int = MOVE_STATS[self.move_name]["base_power"]
        self.move_type: str = MOVE_STATS[self.move_name]["typing"]
        self.move_category: str = MOVE_STATS[self.move_name]["move_category"]
    
    def __repr__(self):
        return self.move_name
            