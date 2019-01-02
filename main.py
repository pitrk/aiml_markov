from markov_libs import World


# Markov Decision Problem
world = World()
world.load('worlds/default.toml')
# world.load('worlds/default2.toml')
world.mdp(termination_value=0.0001)
world.calculate_policy()
# world.generate_gnuplot_file('gnu2')
print(world)