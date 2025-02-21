# Pygame Wrapper

Pygame Wrapper is a lightweight Python module that streamlines game development with Pygame. By encapsulating common boilerplate code and exposing a clear set of overridable methods, developers can concentrate on game logic without delving into low-level Pygame details.

## Features

- Simple Setup: Configure your game with a settings dictionary.
- Customizable Hooks: Override `on_init`, `on_event`, `on_update`, `on_render`, and `on_cleanup` to define behavior.
- Hierarchical Game Components: Create reusable game objects by subclassing `GameObject`.
- Separation of Concerns: Distinguish framework code from game-specific logic.

## Installation

Clone the repository:

```bash
git clone https://github.com/talhaorak/pygame-wrapper.git
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Examples
```bash
python -m examples.[folder].main
```

Ex:
```bash
python -m examples.assets.main
```

## Usage

Subclass `Game` and override its methods to implement your game logic. You can also subclass `GameObject` to create modular game components.

```python
from pygame_wrapper.wrapper import Game
from pygame_wrapper.game_object import GameObject
import pygame

class MyGame(Game):
    def on_init(self):
        # Initialize game components.
        pass

    def on_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.running = False

    def on_update(self, dt):
        # Update game logic.
        pass

    def on_render(self):
        # Render game elements.
        pass

if __name__ == '__main__':
    settings = {
        'width': 800,
        'height': 600,
        'caption': 'My Game',
        'fps': 60,
        'bg_color': (30, 30, 30)
    }
    MyGame(settings).run()
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.
