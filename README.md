# NEAT-Visualize
A script for visualizing NEAT-Python genomes in Pygame

Usage:
```python
drawNetwork(
        config: neat.Config,
        genome: neat.DefaultGenome,
        size: tuple,
        node_names: list[list[str]] = None,
        show_disabled: bool = True,
        colors: list[tuple[int, int, int]] = None) -> pygame.Surface:
```

Dependencies:
- Pygame
- NEAT-Python


TODO:
- Make the input node descriptions fit better
- Add output note descriptions
- Add logic for sorting and placing the hidden layer nodes better
- Add feature for saving as PNG or JPEG
