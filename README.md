# gridsim
2D gridworld simulation

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

Usage

## Getting Current State:

Simulation.get_state()

Parameters:

Returns:

Usage:

sim.get_state()

## Update simulation

Simulation.update()

Parameters

Returns:

Usage:

done = sim.update()

## Getting the log:

Simulation.log()

Parameters:

Returns:

Usage:

# Usage Example:



