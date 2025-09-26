# Anivia SkillShot Dodging (Flappy Bird Remake)
A Python/PyGame remake of Flappy Bird with added features such as modifiers, leaderboard tracking, and animated visuals.


## 🎮 Features
- **Core Gameplay**: Flappy Bird-style dodging with smooth gravity and jump mechanics.  
- **Modifiers**:  
  - Invincible, Shield, Slow Motion, Jump Boost, Reverse Gravity, Heavy Gravity, Manual Controls, Tiny Gaps, Fast Pipes, Disappearing Pipes, x2 Points.  
  - Shield lasts for 1 hit; all others last 8 seconds.  
  - Icons blink when 2 seconds away from expiration.  
- **Leaderboard**: SQLite-backed database stores top scores with player names locally.  
- **Dynamic Environment**:  
  - Moving clouds, scrolling ground, and animated bird sprites.  
- **Menus & UI**:  
  - Start, Info, Leaderboard, Game Over, and Restart menus.  
  - Input box to enter your name for leaderboard submission.  
- **Fair Difficulty Scaling**: Higher score = higher chance of modifiers and more modifiers simultaneously.

## 📂 Project Structure
- `assets/`              - Game images & sounds
- `base.py`              - Ground / scrolling background logic
- `bird.py`              - Bird class (animation, jump, gravity, shield/invincibility)
- `cloud.py`             - Cloud class (random cloud spawns for background)
- `game.py`              - Main game loop and state management
- `leaderboard.py`       - SQLite leaderboard database handling
- `main.py`              - Entry point to run the game
- `pipe.py`              - Pipe obstacle logic
- `power.py`             - Power-up object with duration & expiry handling
- `utils.py`             - Helper functions and classes (collision, random pipes, buttons, etc.)
- `requirements.txt`     - Python dependencies

## ▶️ How to Run

1. Clone this repository:
    ```
    ...> git clone https://github.com/K-Zaid/Flappy-Bird-PyGame.git
    ...> `cd anivia-skillshot-dodging`
    ```
2. Install dependencies:
    ```
    ...> pip install -r requirements.txt
    ```
3. Run game:
    ```
    ...> python main.py
    ```

## 🕹️ Controls
- **Space** → Flap
- **Up/Down Arrows** → Move bird (when "Manual" modifier* is active)
- **Mouse** → Navigate menus
*All modifiers are displayed in the info tab (top left of starting menu screen)

## 🏆 Leaderboard
- At Game Over, enter your name to save your score.
- Scores are stored locally in `leaderboard.db` (SQLite).
- Accessible through the Leaderboard menu.

## ⚙️ Requirements
- Python 3.8+
- PyGame
    - Installed via: 
    ```
    ...> pip install -r requirements.txt
    ```

## 📜 License
This project is for educational purposes and personal use.  
No copyright infringement intended for the Flappy Bird concept.




