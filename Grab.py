import numpy as np

class Stock() :
    def __init__(self) :
        self.count_red=0.
        self.count_green=0
        self.position_stock_matrix=np.array([["^","red","green"],
                                             ["1", "red", "green"]
                                             ["2", "red", "green"]
                                             ["3", "red", "green"]
                                             ["4", "red", "green"]])

class Grab(Stock) :
    def __init__(self) :
        super().__init__()
        #ordre à envoyer
        self.order="%"
        self.order_color="%" #will be usefull to sort the glass
        #état actuel
        self.state="OFF"
        # Transition matrix
        self.transition_matrix= np.array([["^","launch","%","red1","red2","green1","green2"],
                                          ["OFF","P_B_C","%","%","%","%","%"],
                                          ["P_B_C","%","P_H_C","%","%","%","%"],
                                          ["P_H_C","%","%","P_H_L1","P_H_L2","P_H_R1","P_H_R2"],
                                          ["P_H_L1","%","/P_H_X","%","%","%","%"],
                                          ["P_H_L2","%","/P_H_X","%","%","%","%"],
                                          ["P_H_R1","%","/P_H_X","%","%","%","%"],
                                          ["P_H_R2","%","/P_H_X","%","%","%","%"],
                                          ["/P_H_X","%","/P_H_C","%","%","%","%"],
                                          ["/P_H_C","%","OFF","%","%","%","%"]])




    def Run(self):
        colonne=self.transition_matrix[0,:].tolist()
        if self.order in colonne :
            y=colonne.index(self.order)
            row = self.transition_matrix[:, 0].tolist()
            if self.state in row :
                x=row.index(self.state)
                new_state=self.transition_matrix[x,y]#get new state from the transition matrix

                if new_state!="%":
                    if self.order_color!="%":# check if a color has been specify and that there is still a place in the robot for this color
                        self.action(new_state)#call the Move method to move the Servo
                        self.state=new_state
                        if new_state == 'OFF':  # reset of order_color
                            self.order_color = "%"

        self.order="%"
        if self.state=='P_H_C':
            self.order=self.order_color #indicate the spot to put the class



    def action(self,output):
        output_data=output.split("_")
        print(output_data)

    def grab_color(self,color):
        self.order="launch"
        result="%"
        if color=="red":
            if self.count_red<3 :
                result="red2"
                self.count_red+=1
            elif self.count_red<5 :
                result="red1"
                self.count_red += 1
        else :
            if self.count_green<3 :
                result="green2"
                self.count_green+=1
            elif self.count_green<5 :
                result="green1"
                self.count_green+=1


        self.order_color=result



grab=Grab()
grab.grab_color("red")
print(grab.order_color)
ct=0
while 1 :
    print(grab.order)

    grab.Run()
    ct+=1
    if ct%10==1 :
        grab.grab_color("red")



