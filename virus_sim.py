#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist

class Corona:
    """
    Very basic virus spread simulation
    Robert Noakes 2020
    """    
    
    def __init__(self, people, area):
        """
        Initialises the class 

        Parameters
        ----------
        people : TYPE = int
            Number of people in the simulation.
        area : TYPE
            Area in which the people are enclosed.

        Returns
        -------
        None.

        """
        self.people = people
        self.area = area
        self.length = np.sqrt(self.area)
        self.start_positions = np.random.uniform(-self.length/2, self.length/2, 
                                                 (self.people, 2))
        self.pos_state = np.empty((self.people, 2))
        self.inf_state = np.empty(self.people, dtype=object)
        for i in np.arange(self.people):
            self.pos_state[i] = np.array(self.start_positions[i])
            self.inf_state[i] = "susceptable"
        s = np.random.randint(1, self.people)
        self.inf_state[s] = "infected"
        self.infected = np.count_nonzero(self.inf_state == "infected")
        self.susceptable = np.count_nonzero(self.inf_state == "susceptable")
        self.dead = np.count_nonzero(self.inf_state == "dead")
        self.recovered = np.count_nonzero(self.inf_state == "recovered")
        
    def walk(self, stride=20):
        """
        Takes every person and walks them in a random direction 
        by a number of strides within the bounds of the area
        
        Parameters
        ----------
        stride : TYPE, optional int
            Meters to move per walk, the default is 20.

        Returns
        -------
        None.

        """
        self.new_pos_state = np.empty((self.people, 2))
        for i in np.arange(self.people):
            if self.inf_state[i] != "dead":
                angle = np.random.uniform(0, 2*np.pi)
                dx = stride*np.cos(angle)
                dy = stride*np.sin(angle)
                dr = np.array([dx,dy])
                new = self.pos_state[i]+dr
                if -np.sqrt(self.area)/2 < new[0] < np.sqrt(self.area)/2:
                    if -np.sqrt(self.area)/2 < new[1] < np.sqrt(self.area)/2:
                        self.new_pos_state[i] = new
                    else:
                        self.new_pos_state[i] = self.pos_state[i]
                else:
                    self.new_pos_state[i] = self.pos_state[i]
            else:
                    self.new_pos_state[i] = self.pos_state[i]
                
        self.pos_state = self.new_pos_state
    
    def proximity(self):
        """
        Calculates the proximity between any given infected person and nearest
        all other susceptable people

        Returns
        -------
        Proximities, TYPE = numpy.ndarray
              Array of dimension n x m where n is the number of infected people
              and m is the number of susceptable people

        """
        self.positions_infected = self.pos_state[self.inf_state == "infected"]
        self.positions_susceptable = self.pos_state[self.inf_state == "susceptable"]
        self.index_infected = np.argwhere(self.inf_state == "infected")
        self.index_susceptable = np.argwhere(self.inf_state == "susceptable") 
        try:
            return cdist(self.positions_infected, self.positions_susceptable)
        except ValueError:
            return "All infected"
        
    def normal(self, stride=20):
        """
        Simulates normal random movement conditions inside the area.
        Calls a walk and calculates proximities
        
        If a susceptable personis within 2m of an infected person, infection
        probability = 0.25
        
        If a susceptable personis within 1m of an infected person, infection
        probability = 0.75
        
        Parameters
        ----------
        stride : TYPE, optional int
            Meters to move per walk, the default is 20.

        Returns
        -------
        None.

        """
        for i in range(5):
            self.walk(stride)
        p = self.proximity()
        close = np.argwhere((p != 0) & (p < 2) & (p > 1))
        vclose = np.argwhere((p != 0) & (p < 1))
        if len(vclose) > 0:
            for i in vclose:   
                if np.random.rand(1) < 0.75:
                    self.inf_state[self.index_susceptable[i[1]]] = "infected"
        if len(close) > 0:
            for i in close:
                if np.random.rand(1) < 0.25:
                    self.inf_state[self.index_susceptable[i[1]]] = "infected" 
                    
        self.infected = np.count_nonzero(self.inf_state == "infected")
        self.susceptable = np.count_nonzero(self.inf_state == "susceptable")
        self.dead = np.count_nonzero(self.inf_state == "dead")
        self.recovered = np.count_nonzero(self.inf_state == "recovered")
        self.index_infected = np.argwhere(self.inf_state == "infected")

    def anim(self, stride=20):
        """
        Generates an animation of the positions of each person and uses a
        colour scheme to show infections, susceptibility, recoveries and deaths

        Parameters
        ----------
        stride : TYPE, optional int
            Meters to move per walk, the default is 20.

        Returns
        -------
        None.

        """
        counter = 0
        self.index_infected = int(np.argwhere(self.inf_state == "infected")[0])
        self.inf_times = {}
        self.inf_times[str(self.index_infected)] = counter
        self.counter = np.arange(1)
        self.I_counter = np.arange(1)+1
        self.S_counter = np.arange(1)+self.people-1
        self.D_counter = np.arange(1)
        self.R_counter = np.arange(1)
        
        col = np.where(self.inf_state == "infected","r", 
                       np.where(self.inf_state == "susceptable","b", 
                                np.where(self.inf_state == "recovered", "y", 
                                         np.where(self.inf_state == "dead", "k", "m"))))
        plt.ion()
        fig, ax = plt.subplots()
        plt.xlim(-self.length/2, self.length/2)
        plt.ylim(-self.length/2, self.length/2)
        plt.title("Virus Simulation")
        plt.axis("off")
        xdata = self.pos_state.T[0]
        ydata = self.pos_state.T[1]
        points = ax.scatter(xdata, ydata, color=col, s=2, label="Number infected = {0}".format(self.infected))
        plt.draw()
        while self.infected > 0:
            counter +=1
            OI = np.argwhere(self.inf_state == "infected")
            self.normal(stride)
            new_inf_index = np.setdiff1d(self.index_infected, OI)
            for i in new_inf_index:
                self.inf_times[str(i)] = counter
            for i in self.index_infected:
                if counter - self.inf_times[str(*i)] == 14:
                    if np.random.rand(1) < 0.1:
                        self.inf_state[i] = "dead"
                    else:
                        self.inf_state[i] = "recovered"
                        
            self.counter = np.concatenate((self.counter, np.arange(1)+counter))
            self.I_counter= np.concatenate((self.I_counter, np.arange(1)+self.infected))
            self.S_counter = np.concatenate((self.S_counter, np.arange(1)+self.susceptable))
            self.D_counter = np.concatenate((self.D_counter, np.arange(1)+self.dead))
            self.R_counter = np.concatenate((self.R_counter, np.arange(1)+self.recovered))
            col = np.where(self.inf_state == "infected","r", 
                           np.where(self.inf_state == "susceptable","b", 
                                    np.where(self.inf_state == "recovered", "y", 
                                             np.where(self.inf_state == "dead", "k", "m"))))
            xdata = self.pos_state.T[0]
            ydata = self.pos_state.T[1]
            points.set_offsets(np.c_[xdata,ydata])
            points.set_color(col)
            points.set_label("Infected = {}, Susceptable = {}, Recovered = {}. Dead = {}".format(self.infected, self.susceptable, self.recovered, self.dead))
            plt.legend(loc="upper left")
            fig.canvas.draw_idle()
            plt.pause(0.001)
    
    def run(self, stride):
        """
        Runs the animation until no people are infected and then generates
        a plot of infections, susceptibility, recoveries and deaths with time.
        People stay infected for 14 "days" the either die with 10% probability
        or recover with 90% probability 

        Parameters
        ----------
        stride : TYPE = int
            Meters to move per walk

        Returns
        -------
        None.

        """
        self.anim(stride)
        plt.figure()
        xdata = self.counter
        I = self.I_counter
        S = self.S_counter
        D = self.D_counter
        R = self.R_counter
        plt.plot(xdata, I, label="Infections = {}".format(self.people - np.min(self.S_counter)), color="m")
        plt.plot(xdata, S, label="Susceptable = {}".format(self.susceptable), color="g")
        plt.plot(xdata, D, label="Dead = {}".format(self.dead), color="k")
        plt.plot(xdata, R, label="Recovered = {}".format(self.recovered), color="y")
        plt.xlabel("Time")
        plt.ylabel("People")
        plt.legend()
        plt.show()
    
    def run_light(self, stride):
        """
        Runs the simulation without animation
        
        Parameters
        ----------
        stride : TYPE = int
            Meters to move per walk

        Returns
        -------
        None.

        """
        counter = 0
        self.index_infected = int(np.argwhere(self.inf_state == "infected")[0])
        self.inf_times = {}
        self.inf_times[str(self.index_infected)] = counter
        self.counter = np.arange(1)
        self.I_counter = np.arange(1)+1
        self.S_counter = np.arange(1)+self.people-1
        self.D_counter = np.arange(1)
        self.R_counter = np.arange(1)
        
        while self.infected > 0:
            print(self.infected)
            OI = np.argwhere(self.inf_state == "infected")
            counter+=1
            self.normal(stride)
            new_inf_index = np.setdiff1d(self.index_infected, OI)
            for i in new_inf_index:
                self.inf_times[str(i)] = counter
            for i in self.index_infected:
                if counter - self.inf_times[str(*i)] == 14:
                    if np.random.rand(1) < 0.1:
                        self.inf_state[i] = "dead"
                    else:
                        self.inf_state[i] = "recovered"
                    
            self.counter = np.concatenate((self.counter, np.arange(1)+counter))
            self.I_counter= np.concatenate((self.I_counter, np.arange(1)+self.infected))
            self.S_counter = np.concatenate((self.S_counter, np.arange(1)+self.susceptable))
            self.D_counter = np.concatenate((self.D_counter, np.arange(1)+self.dead))
            self.R_counter = np.concatenate((self.R_counter, np.arange(1)+self.recovered))
        
        
        xdata = self.counter
        I = self.I_counter
        S = self.S_counter
        D = self.D_counter
        R = self.R_counter
        plt.figure()
        plt.plot(xdata, I, label="Infections = {}".format(self.people - np.min(self.S_counter)), color="m")
        plt.plot(xdata, S, label="Susceptable = {}".format(self.susceptable), color="g")
        plt.plot(xdata, D, label="Dead = {}".format(self.dead), color="k")
        plt.plot(xdata, R, label="Recovered = {}".format(self.recovered), color="y")
        plt.xlabel("Time")
        plt.ylabel("People")
        plt.legend()
        plt.show()
        
C = Corona(10000, 100000)
C.run(20)

                   