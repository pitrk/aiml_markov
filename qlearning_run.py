from markov_libs import World, QLearningAgent

world02 = World()
world02.load('worlds/default2q02.toml')
qla02 = QLearningAgent(world02)

world005 = World()
world005.load('worlds/default2q005.toml')
qla005 = QLearningAgent(world005)

print("Q-learning: 10 000 iterations, epsilon: 0.2")
qla02.learning(iterations=10000)
print(qla02)
world02.clean_q()

print("Q-learning: 10 000 iterations, epsilon: 0.05")
qla005.learning(iterations=10000)
print(qla005)
world005.clean_q()

print("Q-learning: 100 000 iterations, epsilon: 0.2")
qla02.learning(iterations=100000)
print(qla02)
world02.clean_q()

print("Q-learning: 100 000 iterations, epsilon: 0.05")
qla005.learning(iterations=100000)
print(qla005)
world005.clean_q()

print("Q-learning: 1 000 000 iterations, epsilon: 0.2")
qla02.learning(iterations=1000000)
print(qla02)
world02.clean_q()

print("Q-learning: 1 000 000 iterations, epsilon: 0.05")
qla005.learning(iterations=1000000)
print(qla005)
world005.clean_q()
