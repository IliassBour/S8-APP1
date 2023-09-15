# Copyright (c) 2018, Simon Brodeur
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#  - Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#  - Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES LOSS OF USE, DATA,
# OR PROFITS OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

# Université de Sherbrooke
# Code for Artificial Intelligence module
# Adapted by Audrey Corbeil Therrien for Artificial Intelligence module

import Genetic
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from Player import *
from Maze import *


class GenSim:
    numparams = 2
    popsize = 1000
    nbits = 8
    numGenerations = 20
    mutationProb = 0.1
    crossoverProb = 0.8
    monster = 0

    def __init__(self, numparams, popsize, nbits, numGenerations, mutationProb, crossoverProb, monster):
        self.numparams = numparams
        self.popsize = popsize
        self.nbits = nbits
        self.numGenerations = numGenerations
        self.mutationProb = mutationProb
        self.crossoverProb = crossoverProb
        self.monster = monster

    def fitness_function(self, cvalues):
        attributes = self.getattributes(cvalues)
        fitness = np.zeros(self.popsize)
        for i in range(self.popsize):
            tmpPlayer = Player()
            tmpPlayer.set_attributes(attributes[i])
            fitness[i] = self.monster.mock_fight(tmpPlayer)[1]
        return fitness

    def getattributes(self, cvalues):
        scale = np.zeros((self.popsize, self.numparams))

        for i in range(self.popsize):
            for j in range(self.numparams):
                if cvalues[i][j] > 0.5:
                    factor = ((cvalues[i][j]-0.5) / 0.5)
                    scale[i][j] = MAX_ATTRIBUTE * factor
                else:
                    factor = (((cvalues[i][j])*(-1)) / 0.5)
                    scale[i][j] = MAX_ATTRIBUTE * factor

        return scale
    # Produces the 3D surface plot of the fitness function
    def init_plot(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_title('Function landscape')
        xymin = -3.0
        xymax = 3.0
        x, y = np.meshgrid(np.linspace(xymin, xymax, 100),
                           np.linspace(xymin, xymax, 100))
        z = self.fitness_function(x, y)

        ax.plot_surface(x, y, z, cmap=plt.get_cmap('coolwarm'),
                        linewidth=0, antialiased=False)

        e = np.zeros((self.popsize,))
        sp, = ax.plot(e, e, e, markersize=10, color='k', marker='.', linewidth=0, zorder=10)

        ax.set_xlim(-3, 3)
        ax.set_ylim(-3, 3)
        ax.set_zlim(-1, 4)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        # fig.show()
        return fig, sp


    # Displays the progress of the fitness over all the generations
    def display_generations(self, ga_sim):
        fig = plt.figure()
        n = np.arange(self.numGenerations)
        ax = fig.add_subplot(111)
        ax.plot(n, ga_sim.maxFitnessRecord, '-r', label='Generation Max')
        ax.plot(n, ga_sim.overallMaxFitnessRecord, '-b', label='Overall Max')
        ax.plot(n, ga_sim.avgMaxFitnessRecord, '--k', label='Generation Average')
        ax.set_title('Fitness value over generations')
        ax.set_xlabel('Generation')
        ax.set_ylabel('Fitness value')
        ax.legend()
        fig.tight_layout()

        plt.show()


    def simulation(self):
        # Fix random number generator seed for reproducible results
        np.random.seed(0)

        # Enables realtime plotting of landscape and population.
        # Disabling plotting is much faster!
        SHOW_LANDSCAPE = False

        ga_sim = Genetic.Genetic(self.numparams, self.popsize, self.nbits)
        ga_sim.set_crossover_modulo(self.nbits)
        ga_sim.init_pop()
        ga_sim.set_fit_fun(self.fitness_function)

        if SHOW_LANDSCAPE:
            # Plot function to optimize
            fig, sp = self.init_plot()

        ga_sim.set_sim_parameters(self.numGenerations, self.mutationProb, self.crossoverProb)

        for i in range(ga_sim.num_generations):
            ga_sim.decode_individuals()
            ga_sim.eval_fit()
            ga_sim.print_progress()

            if SHOW_LANDSCAPE:
                # Plot landscape
                sp.set_data(ga_sim.cvalues[:, 0], ga_sim.cvalues[:, 1])
                sp.set_3d_properties(ga_sim.fitness)
                fig.canvas.draw()
                plt.pause(0.02)

            ga_sim.new_gen()

        # Display best individual
        print('#########################')
        print('Best individual (encoded values):')
        print(ga_sim.get_best_individual())
        print('#########################')

        self.display_generations(ga_sim)
        return ga_sim.get_best_individual()


