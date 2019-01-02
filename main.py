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
