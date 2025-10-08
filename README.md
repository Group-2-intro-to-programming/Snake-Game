# 🐍 Snake Game - Group 2
This is a classic Snake game implemented in code. The project was developed collaboratively as part of a school assignment by a team of six members. Our goal was to design, implement, and document a fully functional game while practicing teamwork, version control, and clean coding practices.It was implementation in Python using Pygame, featuring graphics, sound effects, obstacles, and progressive difficulty.

## 👥 Team Members

- **Edith Agai** - Obstacles,Integrator & Main Game Loop
- **Ashley Chege** - Snake Logic
- **June Maritim** - Food System
- **Kimani Roy** - Graphics & Assets
- **Pascal Ng'ang'a** - Input Handler
- **Warren Maina** - Score System

## ✨ Features

- 🎮 Smooth snake movement with arrow key controls
- 🍎 Dynamic food spawning
- 🧱 Progressive obstacle spawning as difficulty increases
- 📊 Score tracking with high score persistence
- 🎵 Background music and sound effects
- 🖼️ Custom sprites and graphics
- 📈 Progressive difficulty (speed increases with score)
- 👤 Player name tracking
- 🎨 Polished UI with game over screen

## 📋 Prerequisites

- Python 3.7 or higher
- Pygame library

## 🚀 Installation

1. **Clone the repository:**
```bash
git clone <your-repo-url>
cd Snake-Game
```

2. **Install Pygame:**
```bash
pip install pygame
```

Or using pip3:
```bash
pip3 install pygame
```

3. **Verify assets are in place:**
```
Snake-Game/
├── app/
│   ├── main.py
│   ├── snake.py
│   ├── food.py
│   ├── graphics.py
│   ├── input_handler.py
│   ├── obstacles.py
│   ├── score.py
│   └── utils.py
└── assets/
    ├── SnakeHead.png
    ├── snakebody.png
    ├── game_over.jpg
    ├── eating.mp3
    ├── scoreup.mp3
    ├── hitwall.mp3
    ├── in-game.mp3
    └── GameOver.mp3
```

## 🎮 How to Play

1. **Start the game:**
```bash
cd app
python main.py
```

Or:
```bash
python3 app/main.py
```

2. **Enter your name** when prompted

3. **Controls:**
   - ↑ **UP Arrow** - Move up
   - ↓ **DOWN Arrow** - Move down
   - ← **LEFT Arrow** - Move left
   - → **RIGHT Arrow** - Move right
   - **ESC** - Quit game
   - **Y** - Restart after game over
   - **N** - Quit after game over

4. **Objective:**
   - Eat red apples to grow and gain points
   - Avoid hitting walls, obstacles, and yourself
   - Survive as long as possible and beat your highscore
