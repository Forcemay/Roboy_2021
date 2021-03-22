import numpy as np
class Stock() :
    def __init__(self) :
        self.count_red=2
        self.count_green=1




class Slide(Stock) :
    def __init__(self) :
        super().__init__()
        self.bot_drop_position = 20
        self.bot_grab_position = 30
        self.heigh_spot = 100
        #ordre à envoyer
        self.order="%"
        #état actuel
        self.current_position=self.heigh_spot
        self.state="H"
        # Transition matrix
        self.transition_matrix= np.array([["^","bot_drop","bot_grab","drop_red","drop_green","grab_red","grab_green","heigh_spot"],
                                          ["BD","%","%","%","%","%","%","H"],
                                          ["BG","%","%","%","%","%","%","H"],
                                          ["DR", "%","%", "%", "%", "%", "%", "H"],
                                          ["DG", "%","%", "%", "%", "%", "%", "H"],
                                          ["GR", "%","%", "%", "%", "%", "%", "H"],
                                          ["GG", "%","%", "%", "%", "%", "%", "H"],
                                          ["H", "BD","BG", "DR", "DG", "GR", "GG", "%"]])

        self.position_stock_matrix = np.array(
            [["^","bot_drop","bot_grab","heigh_spot","drop_red","drop_green","grab_red","grab_green"],
             ["0", self.bot_drop_position,self.bot_grab_position,self.heigh_spot,"%","%",0,0],
             ["1", self.bot_drop_position,self.bot_grab_position,self.heigh_spot,1,1,1,1],
             ["2", self.bot_drop_position,self.bot_grab_position,self.heigh_spot,2,2,2,2],
             ["3", self.bot_drop_position,self.bot_grab_position,self.heigh_spot,3,3,3,3],
             ["4", self.bot_drop_position,self.bot_grab_position,self.heigh_spot,"%","%",4,4]])
    def Run(self):
        colonne=self.transition_matrix[0,:].tolist()
        if self.order in colonne :
            y=colonne.index(self.order)
            row = self.transition_matrix[:, 0].tolist()
            if self.state in row :
                x=row.index(self.state)
                new_state=self.transition_matrix[x,y]#get new state from the transition matrix
                if new_state!="%":
                    self.Move()#call the Move method to move the slide
                    self.state=new_state
        self.order="%"


    def Move(self):
        data=self.order.split("_")
        if data[1]=="red" :
            color="red"
        else :
            color="green"
        next_position=self.Where_to_go(color)
        if next_position>=0 :
            print("move from ",self.current_position,' to ',next_position)

            self.current_position=next_position



    def Where_to_go(self,color):
        result=-3
        if color=='red':
            number=self.count_red
        else :
            number=self.count_green

        colonne = self.position_stock_matrix[0, :].tolist()
        if self.order in colonne:
            y = colonne.index(self.order)
            row = self.position_stock_matrix[:, 0].tolist()
            if str(int(number)) in row:
                x = row.index(str(int(number)))
                result = self.position_stock_matrix[x, y]

        return int(result)

slide=Slide()

slide.order="heigh_spot"
slide.Run()
slide.order="drop_red"
slide.Run()
slide.order="heigh_spot"
slide.Run()
slide.order="drop_red"
slide.Run()