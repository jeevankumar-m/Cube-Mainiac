# Cube Mainiac

A retro-style 2D platformer shooter game built with Python and Pygame. Battle through waves of enemies, navigate challenging terrain, and reach the goal to claim victory.

[![Contributors](https://img.shields.io/github/contributors/jeevankumar-m/Cubemainiac?style=for-the-badge&label=CONTRIBUTORS&labelColor=2d2d2d&color=ff6b6b)](https://github.com/jeevankumar-m/Cubemainiac/graphs/contributors)
[![Forks](https://img.shields.io/github/forks/jeevankumar-m/Cubemainiac?style=for-the-badge&label=FORKS&labelColor=2d2d2d&color=ff6b6b)](https://github.com/jeevankumar-m/Cubemainiac/network/members)
[![Stars](https://img.shields.io/github/stars/jeevankumar-m/Cubemainiac?style=for-the-badge&label=STARS&labelColor=2d2d2d&color=ff6b6b)](https://github.com/jeevankumar-m/Cubemainiac/stargazers)
[![Issues](https://img.shields.io/github/issues/jeevankumar-m/Cubemainiac?style=for-the-badge&label=ISSUES&labelColor=2d2d2d&color=ff6b6b)](https://github.com/jeevankumar-m/Cubemainiac/issues)
[![License](https://img.shields.io/github/license/jeevankumar-m/Cubemainiac?style=for-the-badge&label=LICENSE&labelColor=2d2d2d&color=ff6b6b)](https://github.com/jeevankumar-m/Cubemainiac/blob/main/LICENSE)
[![LinkedIn](https://img.shields.io/badge/LINKEDIN-Profile-blue?style=for-the-badge&labelColor=2d2d2d&logo=linkedin)](https://www.linkedin.com/in/jeevan-kumar06)

---

## Table of Contents

- [About](#about)
- [Features](#features)
- [Gameplay](#gameplay)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Built With](#built-with)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)
- [Technical Details](#technical-details)
- [Contributing](#contributing)
- [License](#license)

---

## About

Cube Mainiac is an action-packed platformer where you control a cube character fighting against enemy cubes across a dynamically generated battlefield. Your mission is simple yet challenging: eliminate all enemies and reach the victory point. The game features smooth platforming mechanics, shooting combat, AI-driven enemies, and a dynamic health system that keeps you on your toes.

## Features

- **Smooth Platforming**: Jump and move through a tile-based level with precise collision detection and physics
- **Combat System**: Shoot projectiles to defeat enemies with satisfying combat mechanics
- **Intelligent Enemy AI**: Enemies that actively chase and shoot at the player, creating dynamic encounters
- **Health System**: Visual health bars for both player and enemies to track your progress
- **Multiple Enemy Waves**: Battle through 10 randomly spawned enemies across the map
- **Parallax Background**: Beautiful layered background system for visual depth
- **Immersive Audio**: Background music and sound effects for jump, shoot, damage, and enemy death
- **Win/Lose Conditions**: Clear victory and defeat states with animated game over screens
- **Retro Aesthetic**: Pixel art style with custom pixel font for that nostalgic feel

## Gameplay

### Objective
Your goal is to eliminate all 10 enemies scattered across the map, then navigate to the goal point to claim victory. Watch your health, manage your resources, and survive the onslaught.

### Controls
- **Left/Right Arrow Keys**: Move your character horizontally
- **Up Arrow Key**: Jump (only works when on ground)
- **Spacebar**: Shoot projectiles in the direction you're facing

### Game Mechanics
- Enemies spawn at random locations and will chase you when you're within range
- Each enemy has 100 health points and takes 25 damage per hit
- You have 100 health points and take 15 damage from enemy projectiles
- Falling too fast will result in instant death
- Defeat all enemies to unlock the goal point

## Installation

### Prerequisites
- Python 3.6 or higher
- Pygame library

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/cubemainiac.git
   cd cubemainiac
   ```

2. **Install Pygame**
   ```bash
   pip install pygame
   ```
   
   Or if you're using pip3:
   ```bash
   pip3 install pygame
   ```

3. **Run the game**
   ```bash
   python main.py
   ```
   
   Or on some systems:
   ```bash
   python3 main.py
   ```

## Project Structure

```
Cubemainiac/
│
├── main.py              # Main game logic and game loop
├── map.txt              # Primary level map data
├── map2.txt             # Alternative level map
├── pixel-operator.ttf   # Custom pixel font file
│
├── assets/              # Game visual assets
│   ├── player.png       # Player sprite
│   ├── enemy.png        # Enemy sprite
│   ├── dirt.png         # Ground tile texture
│   ├── dirt2.png       # Alternative ground tile
│   └── gameover.png     # Game over indicator tile
│
└── sfx/                 # Sound effects and music
    ├── background.mp3   # Background music track
    ├── jump.wav         # Jump sound effect
    ├── shoot.wav        # Shooting sound effect
    ├── damage_sound.mp3 # Player damage sound
    └── enemy_death.mp3  # Enemy death sound effect
```

## Built With

<div align="center">

![Python](https://img.shields.io/badge/PYTHON-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white&labelColor=2d2d2d)
![Pygame](https://img.shields.io/badge/PYGAME-2.x-57C2D1?style=for-the-badge&logo=pygame&logoColor=white&labelColor=2d2d2d)

</div>

### Technologies & Libraries

- **Python 3.x** - The core programming language powering the game
- **Pygame** - Game development framework for graphics rendering, audio playback, and input handling
- **Random Module** - Standard library module for enemy spawn randomization
- **Sys Module** - System-specific parameters and functions for game termination

## Customization

### Adjusting Difficulty

**Change Enemy Count**
Edit line 115 in `main.py`:
```python
enemy_creation_count = 10  # Modify this number to change total enemies
```

**Modify Health Values**
- Player max health: Line 108 (`player_max_health = 100`)
- Enemy max health: Line 110 (`enemy_max_health = 100`)

**Adjust Damage Values**
- Enemy damage per hit: Line 301 (`enemy_health -= 25`)
- Player damage per hit: Line 316 (`player_health -= 15`)

### Switching Maps
Change line 77 in `main.py`:
```python
game_map = load_map('map2')  # Change to 'map' or 'map2'
```

### Map Tile System
The game uses a text-based tile map where:
- `0` = Empty space (air)
- `1` = Dirt tile (ground)
- `2` = Alternative dirt tile (variation)
- `3` = Goal/End tile (victory point)

## Troubleshooting

**Game won't start?**
- Ensure all asset files are present in the correct directories (`assets/` and `sfx/`)
- Verify Pygame installation: `pip show pygame` or `python -m pygame --version`
- Check that `pixel-operator.ttf` is in the root directory

**No sound playing?**
- Verify all sound files exist in the `sfx/` folder
- Check your system's audio settings and volume
- Ensure audio drivers are properly installed

**Performance issues?**
- The game runs at 60 FPS by default (line 417: `clock.tick(60)`)
- Lower the FPS cap if experiencing lag: `clock.tick(30)`
- Close other resource-intensive applications

**Enemies not spawning?**
- Check that `enemy_creation_count` is greater than 0
- Verify the map file is properly formatted
- Ensure spawn locations are within map boundaries

## Technical Details

### Game Architecture
- **Physics Engine**: Custom gravity and momentum system with collision detection
- **Collision System**: Rectangle-based collision detection with tile map
- **Enemy AI**: Distance-based chasing algorithm with shooting cooldown
- **Camera System**: Smooth scrolling camera that follows the player
- **Spawn System**: Random coordinate generation for enemy placement
- **State Management**: Game states for playing, game over, and victory

### Performance
- Target FPS: 60 frames per second
- Display resolution: 700x500 pixels (scaled from 350x250 internal resolution)
- Tile size: 16x16 pixels (based on asset dimensions)

## Contributing

Contributions are welcome! Whether it's bug fixes, new features, or improvements to the codebase, your input is valuable. Please feel free to:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is open source and available under the MIT License. See the LICENSE file for more details.

## Acknowledgments

- Built with the Pygame community in mind
- Inspired by classic 2D platformer games
- Thanks to all contributors and testers

---

**Ready to become a Cube Mainiac? Start playing and see if you can defeat all enemies!**

