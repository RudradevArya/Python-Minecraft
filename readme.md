# Minecraft-inspired Python Project

This project is a Minecraft-inspired game implemented in Python using Pyglet for graphics rendering. It aims to replicate some of the core mechanics and features of Minecraft while serving as a learning exercise in 3D graphics programming, game development, and Python.

## Project Progress Videos

<!-- [![Video Title](https://img.youtube.com/vi/VIDEO_ID/0.jpg)](https://www.youtube.com/watch?v=VIDEO_ID) -->
[![Video Title](https://img.youtube.com/vi/NTwoWGXgmiA/0.jpg)](https://www.youtube.com/watch?v=NTwoWGXgmiA)

## Features

* 3D voxel-based world generation
* Customizable block types with different textures and properties
* First-person camera and movement
* Chunk-based world loading and rendering
* Basic terrain generation
* Block placement and destruction
* Texture management system
* Shader-based rendering
* Save and load functionality for world persistence

## Task List

Here's a task list for further development of the project:

* [x] Enhance world generation
    * [x] Implement more diverse terrain features (hills, caves, etc.)
    * [x] Add different biomes
* [x] Improve block interaction mechanics
* [x] Add block variants (e.g., different wood types)
* [x] Implement more complex terrain generation
    * [x] Add biomes
    * [ ] Implement noise-based terrain generation
* [x] Add an inventory system
    * [ ] Create UI for inventory
    * [x] Implement item pickup and storage
* [x] Implement crafting mechanics
    * [ ] Design crafting recipes
    * [x] Create crafting UI
* [x] Optimize rendering for better performance
    * [ ] Implement occlusion culling
    * [x] Add level of detail (LOD) for distant chunks
* [ ] Implement multiplayer functionality
    * [ ] Set up client-server architecture
    * [ ] Implement network synchronization
* [ ] Add sound effects and music
* [ ] Implement a day/night cycle
* [ ] CUDA Parllelization
* [x] ✨**ENJOY** \- ✨

## Learning Resources

If you're new to game development or some of the concepts used in this project please go through the `reading-material.txt` files where crude logic and resources are pasted

## Requirements

* Python 3.x
* Pyglet
* OpenGL
* nbtlib (for save file handling)
* base36 (for save file path encoding)

## Project Structure

* `main.py`: Entry point of the application, sets up the game window and runs the main loop
* `world.py`: Manages the game world, chunks, and block types
* `chunk.py`: Handles individual chunks of the world
* `subchunk.py`: Manages subchunks for more efficient rendering
* `block_type.py`: Defines different types of blocks and their properties
* `camera.py`: Implements the first-person camera and movement
* `texture_manager.py`: Manages loading and handling of textures
* `shader.py`: Handles shader compilation and usage
* `matrix.py`: Provides matrix operations for 3D transformations
* `hit.py`: Implements ray casting for block selection and interaction
* `save.py`: Handles saving and loading of the world data

## How to Run

1. Clone this repository.
2. Ensure you have all the required dependencies installed.
3. Create virtual environment

``` sh
python -m venv myenv
```

``` sh
myenv\Scripts\activate
```
``` sh
pip install pyglet
```
``` sh
pip install nbtlib
```

``` sh
pip install base36
```

4. Run `python main.py` to start the game.

## Controls

* WASD: Move around
* Space: Move up
* Left Shift: Move down
* Mouse: Look around
* Left Click: Break block
* Right Click: Place block
* Middle Click: Pick block
* G: Cycle through block types
* O: Save the world
* Escape: Release mouse capture

## Customization

You can add new block types by editing the `data/blocks.mcpy` file. The format is as follows:

```
block_id: name "Block Name", texture.all "texture_name", model models.cube
```

Textures should be placed in the `textures/` directory.

## Acknowledgements

This project was inspired by Minecraft, created by Mojang Studios. It is not affiliated with or endorsed by Mojang or Microsoft.

Special thanks to the Pyglet and OpenGL communities for their excellent documentation and resources.
