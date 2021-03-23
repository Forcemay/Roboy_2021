class MasterTrajectory():
    def __init__(self,vitesse,format) :
        self.vitesse=vitesse
        self.format=format
        self.list_of_trajectory=[]
        self.list_of_trajectory_selected=[]
        self.list_of_trajectory_to_remove=[]


    def change_all(self):
        for trajectory in self.list_of_trajectory_selected :
            trajectory.vitesse=self.vitesse
            trajectory.format=self.format
    def create_trajectory(self):
        number=len(self.list_of_trajectory)+1
        name='trj'+str(number)
        self.list_of_trajectory.append(Trajectory(self.vitesse,self.format,name))

    def remove_trajectory(self):
        for trj in self.list_of_trajectory_to_remove :
            self.list_of_trajectory.remove(trj)

class Trajectory(MasterTrajectory):
    def __init__(self,vitesse,format,name):
        super(Trajectory, self).__init__(vitesse,format)
        self.name=name

master_trajectory = MasterTrajectory(10, "car")
for trj in range(10):
    master_trajectory.create_trajectory()

x,y,z=1,2,5
master_trajectory.list_of_trajectory_to_remove.append(master_trajectory.list_of_trajectory[x])
master_trajectory.list_of_trajectory_to_remove.append(master_trajectory.list_of_trajectory[y])
master_trajectory.list_of_trajectory_to_remove.append(master_trajectory.list_of_trajectory[z])

master_trajectory.remove_trajectory()


