# gridsim

2D gridworld simulation, grid world, grid-world, pygame, sim, girdworld, simulation, 2D.

# Dependencies

* Python 2.7
* Pygame

# Documentation

## Instantiating

Simulation(configFile = None, matrixFile = None)

##### Parameters:

configFile: String

matrixFile: String

##### Returns:

An instance of Simulation()

##### Usage:
```python
sim = Simulation('path/to/config_file','path/to/MDP_file')
```
## Moving Agents

Simulation.move_agent(number = None, action = None)

##### Parameters:

number: Integer

action: String

##### Returns:

None

##### Usage:
```python
sim.move_agent(0,'east')
```
## Getting Current State

Simulation.get_state()

##### Parameters:

None

##### Returns:

Dictionary

##### Usage:
```python
state = sim.get_state()
```
## Update simulation

Simulation.update()

##### Parameters:

None

##### Returns:

Boolean

##### Usage:
```python
done = sim.update()
```
## Getting the log

Simulation.get_log()

##### Parameters:

None

##### Returns:

Dictionary

##### Usage:

```python
log = sim.get_log()
agents_log = sim.get_log()["agents"]
agent_0_log = sim.get_log()["agents"][0]
```

# Usage Example

```python
from environment import Simulation

sim = Simulation("config.txt", "matrix.txt")

done = False
while not done:

    sim.move_agent(0, "east")
    sim.move_agent(1, "south")
    
    agent1 = sim.get_state()["agents"][0]
    print "agent1: {}".format(agent1)

    obstacle1 = sim.get_state()["moving_obstacles"][0]
    print "obstacle1: {}".format(obstacle1)

    done = sim.update()

for line in sim.get_log()["agents"][0]:
    print line
```

# Developers

* @LaufferN
* @sahabi