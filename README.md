*This project has been created as part of the 42 curriculum by mbichet.*

## Description
**Fly-in** is an advanced multi-drone pathfinding and visualization system designed to solve complex routing problems in constrained network environments. The primary goal is to compute optimal routes for multiple drones from a starting hub to an ending hub while respecting strict network constraints. The system handles capacity limitations on individual hubs, maximum link capacities, zone-based restrictions, and complex topologies like dead-ends and bottlenecks. 

## Instructions

### Prerequisites
*   **Python:** Version 3.8+.
*   **Dependencies:** Raylib (for 3D visualization), flake8, and mypy.

### Installation
A Makefile is provided to easily set up a virtual environment and install all necessary dependencies:
```bash
make install
```
## Execution
To run the simulation, execute the main Python script with your desired input map and output file path:
```bash
python3 Fly-in.py input.txt output.txt
```
Alternatively, you can run it directly via the Makefile:

```Bash
make run ARGS="input.txt output.txt"
```
### Algorithm Choices and Implementation Strategy
The core routing logic relies on a Modified Dijkstra's Algorithm that is specifically adapted to handle multi-drone constraints.

* Zone-Based Cost Model: The network maps different traversal costs based on the zone type. Priority zones have a lower or standard cost (1.0), normal zones have a standard cost (1.0), and restricted zones apply a higher traversal penalty (2.0).

* Sequential Routing Strategy: Instead of attempting to solve all drone paths simultaneously (which is NP-hard), the algorithm employs a sequential greedy approach. It computes the optimal baseline paths from the goal backwards to the start.

* Constraint and Congestion Management: Drones are routed one-by-one while tracking real-time capacities. The Hub and Link classes actively track current occupancy (nb_in) against maximum allowed capacity (max_in). If a path or hub reaches its max_size limit, the drone will wait or seek alternative valid paths to prevent deadlocks.

* Object-Oriented Architecture: The backend utilizes strongly typed classes (Map, Hub, Link, and Ship_solve) to cleanly encapsulate the network state and manage the complex validation of pathfinding rules at every step.

### Visual Representation Features
To enhance the user experience and make algorithmic behaviors transparent, the project features a real-time 3D visualization built with Raylib.

* Immersive 3D Space: The environment is rendered at 60 FPS and features a space-themed skybox (skybox.jpg) with ambient white lighting.

* Hub Identification via 3D Models: Hubs are visually distinct based on their zone types to provide immediate context without reading configurations. For example, restricted zones use a Neptune model, blocked zones use a Sun model, and priority zones use a Moon model. The start and end hubs also utilize distinct custom models.

* Real-Time Drone Tracking: Each drone is represented by a custom 3D spaceship model (spaceship.glb). The ships dynamically update their position and rotation angles to face their target destinations as they smoothly traverse the calculated links.

* Interactive Camera and Controls: Users can inspect the network topology from any angle using a free 3D camera controlled by the mouse. The simulation speed can also be dynamically adjusted using the Up and Down arrow keys, and the spacebar controls the pause/play state.

## Resources
* Classic References: The algorithm builds upon fundamental Graph Theory and Dijkstra's Algorithm concepts.

* Libraries: The visualization relies entirely on Pyray (Python bindings for Raylib).

* AI Usage: Artificial Intelligence was use for do the README.