# gridsim

2D gridworld simulation. Keywords: grid world, grid-world, pygame, sim, girdworld, simulation, 2D.

# Dependencies

Install pygame

# Documentation

## Instantiating:

Simulation(configFile = None, matrixFile = None)

Parameters:

Returns:

Usage:

sim = Simulation('path/to/config_file','path/to/MDP_file')

## Moving Agents:

Simulation.move_agent(number = None, action = None)

Parameters:

Returns:

Usage:

sim.move_agent(0,'east')

## Getting Current State:

Simulation.get_state()

Parameters:

None

Returns:

Usage:

state = sim.get_state()

## Update simulation

Simulation.update()

Parameters:

None

Returns:

Usage:

done = sim.update()

## Getting the log:

Simulation.log()

Parameters:

Returns:

Usage:

# Usage Example: