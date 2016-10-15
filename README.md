# GUI

##### Launching GUI

```bash
python config_gui.py [configFile]
```

The GUI prompts for inputs on the command line while running

##### Parameters:

configFile (optional) - open a config file to edit


# gridsim

2D gridworld simulation, grid world, grid-world, pygame, sim, girdworld, simulation, 2D.

## Dependencies

* Python 2.7
* Pygame

## Documentation

### Instantiating

```python
Simulation(configFile = None)
```

##### Parameters:

configFile: String

##### Returns:

An instance of Simulation()

##### Usage:
```python
sim = Simulation('path/to/config_file')
```

### Uploading matrix file

```python
Simulation.load_matrix_file('path/to/matrix_file')
```

##### Parameters:

matrixFile: String

##### Returns:

Nothing

### Uploading slip file

```python
Simulation.load_slip_file('path/to/slip_file')
```

##### Parameters:

slipFile: String

##### Returns:

Nothing

##### Slip file structure:
```python
x_pos y_pos action x_result y_result probability
```

### Moving Agents

```python
Simulation.move_agent(actions = None)
```

##### Parameters:

actions: List of actions. There are 7 actions to choose from. 'east', 'west', 'north', 'south', 'keyboard', 'matrix'.

The fist four actions are self-explanatory. 'keyboard' takes the input from they keyboard keys to move the agent. 'matrix' moves the agent according to the matrix file used during instantiating the simulation.

##### Returns:

Boolean: flag whether to terminate simulation. True if terminate, False if not.

Dictionary: Contains the state of the simulation.

##### Usage:
```python
done, state = sim.move_agent(['east','keyboard'])
```
### Getting Current State

```python
Simulation.get_state()
```

##### Parameters:

None

##### Returns:

Dictionary

##### Usage:
```python
state = sim.get_state()
```
### Update simulation

```python
Simulation.update()
```

##### Parameters:

None

##### Returns:

Boolean

##### Usage:

```python
done = sim.update()
```
### Getting the log

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

### Getting history

```python
Simulation.get_history(time_steps)
```

##### Parameters:

time_steps

##### Returns

Dictionary of last [time_steps] time steps

#####Usuage:

```python
histroy_1 = sim.get_log(1)
history_2 = sim.get_log(2)
agents_2_history = sim.get_log(2)["agents"]
```

### Generating agent matrix

```python
Simulation.generate_agent_matrix(file = None)
```

##### Parameters:

String: String

##### Returns:

None

##### Usage:

```python
sim.generate_agent_matrix("agent_matrix.txt")
```

## Usage Example

```python
from environment import Simulation

sim = Simulation("config.txt", "matrix.txt")

state = sim.get_state()

done = False
while not done:

    done, state = sim.move(["matrix", "stay"])
        
sim.generate_agent_matrix("agent_matrix.txt")

```

## Developers

* [@LaufferN](https://github.com/LaufferN)
* [@sahabi](https://github.com/sahabi)
