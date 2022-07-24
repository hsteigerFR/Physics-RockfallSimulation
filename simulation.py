from tkinter import *
import math


class Interface:

    def signe(self, x):
        """This function gets the sign of a given number x. -1 if negative, 0 if zero or +1 if positive."""
        if abs(x) == 0:
            return 0
        else:
            return x / abs(x)

    def domaine(self, x):
        """This function returns the index of the domain where the rock is located."""
        for i in range(len(self.Xtalus) - 1):
            if x >= self.Xtalus[i] and x < self.Xtalus[i + 1]:
                return i

    def chute_libre(self):
        """This function simulates the free fall of the rock. The rock keeps falling as long as a surface is not reached.
           Air resistance is ignored."""
        self.Vx.append(self.Vx[-1])
        self.Vy.append(self.Vy[-1] + self.g * self.dt)
        self.X.append(self.X[-1] + self.Vx[-1] * self.dt)
        self.Y.append(self.Y[-1] + self.Vy[-1] * self.dt)

    def rebond(self):
        """This function simulates the bouncing of the rock against a surface."""
        i = self.domaine(self.X[-1])
        a = math.atan(
            (self.Ytalus[i + 1] - self.Ytalus[i]) / (self.Xtalus[i + 1] - self.Xtalus[i]))
        Vt = self.Vx[-1] * math.cos(a) + self.Vy[-1] * math.sin(a)
        Vn = -self.Vx[-1] * math.sin(a) + self.Vy[-1] * math.cos(a)
        Vn, Vt = -Vn * self.cr, Vt * self.cr
        self.Vx.append(math.cos(a) * Vt - math.sin(a) * Vn)
        self.Vy.append(math.sin(a) * Vt + math.cos(a) * Vn)
        self.X.append(self.X[-1] + self.Vx[-1] * self.dt)
        self.Y.append(self.Y[-1] + self.Vy[-1] * self.dt)

    def roulement(self):
        """This function simulates the sliding of the rock over a surface."""
        i = self.domaine(self.X[-1])
        a = math.atan(
            (self.Ytalus[i + 1] - self.Ytalus[i]) / (self.Xtalus[i + 1] - self.Xtalus[i]))
        At = (self.g) * (math.sin(a) - (self.f) * math.cos(a))
        An = 0
        Vt = At * self.dt
        Vn = 0
        if self.Vx[-1] * self.signe(a + 0.05) < 0:
            self.Vx.append(0)
            self.Vy.append(0)
        else:
            self.Vx.append(math.cos(a) * Vt - math.sin(a) * Vn + self.Vx[-1])
            self.Vy.append(math.sin(a) * Vt + math.cos(a) * Vn + self.Vy[-1])
        self.X.append(self.X[-1] + self.Vx[-1] * self.dt)
        self.Y.append(self.Y[-1] + self.Vy[-1] * self.dt)

    def test_collision(self):
        """This function checks if the rock is in the air or if there is a contact with a surface."""
        i = self.domaine(self.X[-1])
        a = math.atan(
            (self.Ytalus[i + 1] - self.Ytalus[i]) / (self.Xtalus[i + 1] - self.Xtalus[i]))
        courbe = ((self.X[-1] - self.Xtalus[i]) * ((self.Ytalus[i + 1] - self.Ytalus[i]
                                                    ) / (self.Xtalus[i + 1] - self.Xtalus[i])) + self.Ytalus[i]) - self.R
        if self.Y[-1] > courbe:
            self.Y.append(courbe)
            self.X.append(self.X[-1])
            self.impacts.append(len(self.X) - 1)
            self.amplitude_rebond()
            return True
        else:
            return False

    def choix(self):
        """This function manages the behaviour of the rock : if it should slide, bounce of free fall, according to the context."""
        if self.test_collision():
            if self.amplitudes[-1] > 20:
                self.rebond()
            else:
                if self.Vx[-1]**2 + self.Vy[-1]**2 > 1:
                    self.roulement()
        else:
            self.chute_libre()

    def amplitude_rebond(self):
        """This function calculates the amplitude of the rock bouncing, if it is below a given threshold, the rock slides and do not bounce."""
        domaineY = self.Y[self.impacts[-2]:self.impacts[-1]]
        domaineX = self.X[self.impacts[-2]:self.impacts[-1]]
        Y1 = min(domaineY)
        X1 = domaineX[domaineY.index(Y1)]
        X2 = domaineX[len(domaineX) // 2]
        i = self.domaine(X2)
        Y2 = (self.Ytalus[i + 1] - self.Ytalus[i]) * (X2 - self.Xtalus[i]
                                                      ) / (self.Xtalus[i + 1] - self.Xtalus[i]) + self.Ytalus[i]
        self.amplitudes.append(math.sqrt((X2 - X1)**2 + (Y2 - Y1)**2))

    def etape(self):
        """This function updates the Tkinter canvas with the new rock location."""
        self.choix()
        self.canvas.delete(ALL)
        self.tracer_talus()
        self.tracer_point()

    def run(self):
        """This function starts the simulation when the user clicks on the 'Run' Button. It can be stopped with the 'Stop' Button."""
        self.arret = False
        self.run_loop()
        self.bouton_anim.config(state=DISABLED)
        self.bouton_etape.config(state=DISABLED)

    def run_loop(self):
        """This function autonomously update the canvas after a 15ms tick."""
        if not self.arret:
            try:
                self.etape()
            except BaseException:
                self.arret = True
            #print("X = ",self.X[-1]," Y = ",self.Y[-1])
            #print("Vx = ",self.Vx[-1]," Vy = ",self.Vy[-1])
            self.canvas.after(15, self.run_loop)

    def stop(self):
        """The stimulation stops when the user clicks on the 'Pause' button"""
        self.arret = True
        self.bouton_anim.config(state=NORMAL)
        self.bouton_etape.config(state=NORMAL)

    def tracer_talus(self):
        """The slope / ground model is is created with this function."""
        for i in range(len(self.Xtalus) - 1):
            self.canvas.create_line(self.Xtalus[i],
                                    self.Ytalus[i],
                                    self.Xtalus[i + 1],
                                    self.Ytalus[i + 1],
                                    fill="black",
                                    width=2)
            self.canvas.create_polygon(self.Xtalus[i],
                                       self.height,
                                       self.Xtalus[i],
                                       self.Ytalus[i],
                                       self.Xtalus[i + 1],
                                       self.Ytalus[i + 1],
                                       self.Xtalus[i + 1],
                                       self.height,
                                       fill="grey",
                                       width=2)

    def tracer_point(self):
        """This function plots the rock on the canvas thanks to its location. Its speed and the time are displayed."""
        self.canvas.create_oval(self.X[-1] - self.R,
                                self.Y[-1] - self.R,
                                self.X[-1] + self.R,
                                self.Y[-1] + self.R,
                                fill="red")
        self.temps.config(
            text="t = " + str((round((len(self.X) - 1) * self.dt, 1))) + " s")

    def __init__(self):

        # Interface creation
        self.root = Tk()
        self.root.title("Python - Simple Rockfall Simulation")
        self.height = 600
        self.width = 800
        self.canvas = Canvas(
            self.root,
            height=self.height,
            width=self.width,
            bg="white")
        self.canvas.pack()

        # Quit button
        self.bouton_quitter = Button(
            self.root,
            text="Quitter",
            command=lambda: self.root.destroy())
        self.bouton_quitter.pack(side=LEFT)

        # Pause button
        self.bouton_stop = Button(
            self.root,
            text="Pause",
            command=lambda: self.stop())
        self.bouton_stop.pack(side=RIGHT)

        # Start / end pause button
        self.bouton_anim = Button(
            self.root,
            text="Animation",
            command=lambda: self.run())
        self.bouton_anim.pack(side=RIGHT)

        # Step by step button
        self.bouton_etape = Button(
            self.root,
            text="Étape par étape",
            command=lambda: self.etape())
        self.bouton_etape.pack(side=RIGHT)

        # Constants
        self.g = 9.81  # Gravitational constant, in m.s-2
        self.cr = 0.7  # Ground restitution coefficient
        self.f = 0.2  # Ground solid friction coefficient
        self.R = 10  # The rock is represented by a disk, with radius R (in m)

        # Slope profile (in m)
        # For a given index i, (Xtalus[i],Ytalus[i]) is a coordinate of a
        # vertex as regards the slope curve.
        self.Xtalus = [0, 100, 200, 300, 400, 500, 600, 700, 800]
        self.Ytalus = [150, 230, 250, 430, 500, 500, 200, 100, 0]
        # Init
        self.Vx0 = 1  # Initial X speed (in m.s-1)
        self.Vy0 = 5  # Initial Y speed (in m.s-1)
        self.x0 = 30  # Initial location X coordinate (in m)
        self.y0 = 140  # Initial location Y coordinate (in m)
        # Algo related
        self.dt = 0.05  # Time step for the simulation (in s)

        # Variables
        self.Vx = [self.Vx0]  # X speed list, for each it
        self.Vy = [self.Vy0]  # Y speed list, for each it
        self.X = [self.x0]  # X coordinate list, for each it
        self.Y = [self.y0]  # Y coordinate list, for each it
        self.arret = False
        self.impacts = [0]  # List of impact moments
        self.amplitudes = [1000]  # List of bouncing amplitude

        # Execution info
        # Display of the simulation time
        self.temps = Label(self.root, text="t = " +
                           str((round((len(self.X) - 1) * self.dt, 1))) + " s")
        self.temps.pack()

        # Once the windows initialized, the simulation is ready to start.
        self.tracer_talus()
        self.tracer_point()

        self.root.mainloop()


Interface()
