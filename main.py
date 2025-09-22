# Entry point to run the game
from game import Game
from leaderboard import init_db

# only runs game if main.py is ran
if __name__ == "__main__": 
    game = Game()
    init_db() # Create table if it does not exist
    game.run()
