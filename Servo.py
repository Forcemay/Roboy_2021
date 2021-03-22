import numpy as np


class Servo() :
    def __init__(self) :
        #ordre à envoyer
        self.order="%"
        #état actuel
        self.state="Center"
        # Transition matrix
        self.transition_matrix= np.array([["^","left2","left1","center","right1","right2"],
                                          ["Left2","%","Left1","Center","Right1","Right2"],
                                          ["Left1","Left2","%","Center","Right1","Right2"],
                                          ["Center","Left2","Left1","%","Right1","Right2"],
                                          ["Right1","Left2","Left1","Center","%","Right2"],
                                          ["Right2","Left2","Left1","Center","Right1","%"]])

        self.output_matrix=np.array([["^","left2","left1","center","right1","right2"],
                                     ["Left2","0,0","0,0","0,0","0,0","0,0"],
                                     ["Left1","0,0","0,0","0,0","0,0","0,0"],
                                     ["Center","0,0","90,0","0,0","0,0","0,0"],
                                     ["Right1","0,0","0,0","0,0","0,0","0,0"],
                                     ["Right2","0,0","0,0","0,0","0,0","0,0"]])

    def Run(self):
        colonne=self.transition_matrix[0,:].tolist()
        if self.order in colonne :
            y=colonne.index(self.order)
            row = self.transition_matrix[:, 0].tolist()
            if self.state in row :
                x=row.index(self.state)
                new_state=self.transition_matrix[x,y]#get new state from the transition matrix
                if new_state!="%":
                    output=self.output_matrix[x,y]#get output matrix result
                    self.Move(output)#call the Move method to move the Servo
                    self.state=new_state
        self.order="%"


    def Move(self,output):
        output_data=output.split(",")
        x=output_data[0]
        y=output_data[1]
        print(x,y)
servo=Servo()
servo.order="left1"
servo.Run()
print(servo.state)