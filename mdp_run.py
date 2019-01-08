import subprocess

from markov_libs import World

# Markov Decision Problem - default world
world = World()
world.load('worlds/default.toml')
world.mdp(termination_value=0.0001)
world.calculate_policy()
print(world)
world.generate_gnuplot_file('results/default')
subprocess.run(["./plotter.sh", "results/default"])

# Markov Decision Problem - second world
world2 = World()
world2.load('worlds/default2.toml')
world2.mdp(termination_value=0.0001)
world2.calculate_policy()
print(world2)
world2.generate_gnuplot_file('results/default2')
subprocess.run(["./plotter.sh", "results/default2"])

# Markov Decision Problem - second world with reward modification
world3 = World()
world3.load('worlds/default3.toml')
world3.mdp(termination_value=0.0001)
world3.calculate_policy()
print(world3)
world3.generate_gnuplot_file('results/default3')
subprocess.run(["./plotter.sh", "results/default3"])

# Markov Decision Problem - second world with action uncertainty model modified
world4 = World()
world4.load('worlds/default4.toml')
world4.mdp(termination_value=0.0001)
world4.calculate_policy()
print(world4)
world4.generate_gnuplot_file('results/default4')
subprocess.run(["./plotter.sh", "results/default4"])

# Markov Decision Problem - second world with gamma modified
world5 = World()
world5.load('worlds/default5.toml')
world5.mdp(termination_value=0.0001)
world5.calculate_policy()
print(world5)
world5.generate_gnuplot_file('results/default5')
subprocess.run(["./plotter.sh", "results/default5"])
