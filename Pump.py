import numpy as np


class Pump() :
    def __init__(self) :
        #ordre à envoyer
        self.order="%"
        #état actuel
        self.state="OFF"
        # Transition matrix
        self.transition_matrix= np.array([["^","on","off"],["ON","%","OFF"],["OFF","ON","%"]])

    def Run(self):
        colonne=self.transition_matrix[0,:].tolist()
        if self.order in colonne :
            y=colonne.index(self.order)
            row = self.transition_matrix[:, 0].tolist()
            if self.state in row :
                x=row.index(self.state)
                new_state=self.transition_matrix[x,y]#get new state from the transition matrix
                if new_state!="%":
                    self.action(new_state)
                    self.state=new_state
        self.order="%"


    def action(self,new_state):
        print("turn "+new_state)
pump=Pump()
pump.order='on'
pump.Run()

