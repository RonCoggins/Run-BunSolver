from textual.app import App, ComposeResult
from textual.widgets import Label, ListView, ListItem
from textual.containers import HorizontalGroup




class OpponentTrainerSelection(HorizontalGroup):

    def compose(self) -> ComposeResult:
        yield ListView(
            ListItem("Pikachu"),
            ListItem("Wartortle")
        )



class TUI(App):


    def compose(self) -> ComposeResult:

        yield OpponentTrainerSelection(self)




