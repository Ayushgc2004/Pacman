Consider following PacMan problem:

Layout: The Pac-Man map is now divided into two halves: blue (right) and red (left). Red agents (which all have even indices) must defend the red food while
trying to eat the blue food. When on the red side, a red agent is a ghost. When crossing into enemy territory, the agent becomes a Pac-Man.

Scoring: When a Pac-Man eats a food dot, the food is permanently removed and one point is scored for that Pac-Man's team. Red team scores are positive, while Blue team scores are negative. Eating Pac-Man: When a Pac-Man is eaten by an opposing ghost, the Pac-Man returns to its starting position (as a ghost). No points are awarded for eating an opponent. Ghosts can never be eaten.

Winning: A game ends when one team eats all but two of the opponents' dots. Games are also limited to 3000 agent moves. If this move limit is reached, whichever team has eaten the most food wins. Computation Time: Each agent has 1 second to return each action. Each move which does not return within one second will incur a warning. After three warnings, or any single move taking more than 3 seconds, the game is forfeit. There will be an initial start-up allowance of 15 seconds.

Observations: Agents can only observe an opponent's configuration (position and direction) if they or their teammate is within 5 squares (Manhattan
distance). In addition, an agent always gets a noisy distance reading for each agent on the board, which can be used to approximately locate unobserved
opponents.

Find out the winner of the game and time required for complete computations.

Develop a GUI to show the execution.
