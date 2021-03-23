from rplidar import RPLidar
from rplidar import RPLidarException
from math import cos, sin, pi, floor,sqrt
max_distance=0
import pygame
import os
from threading import Thread
import time
class Point():
    def __init__(self,x,y,label) :
        self.x=x
        self.y=y
        self.label=label
        self.current_state=[]

def distance_points(x,y,x2,y2):
    result=sqrt((x-x2)**2+(y-y2)**2)
    return result

class LYDAR(Thread) :
    def __init__(self,number_turn,distance_max_view,show_result=False) :
        Thread.__init__(self)
        self.show_result=show_result
        self.current_state=[]
        self.number_turn=number_turn
        self.distance_max_view=distance_max_view
        # Set up pygame and the display
        if show_result :
            os.putenv('SDL_FBDEV', '/dev/fb1')
            pygame.init()
            self.lcd = pygame.display.set_mode((1200,1000))
            pygame.mouse.set_visible(False)
            self.lcd.fill((0,0,0))
            pygame.display.update()
        self.port='/dev/ttyUSB0'
        try :
            self.lidar = RPLidar('/dev/ttyUSB0')
        except :
            self.lidar = RPLidar('/dev/ttyUSB1')
            self.port='/dev/ttyUSB1'


        self.lidar.stop_motor()
        self.lidar.start_motor()
    def run(self) :
        turn=0
        scan_data = [0]*360

        self.data=[]
        
        while 1:
            try :
                for i, scan in enumerate(self.lidar.iter_scans()):
                    for (_, angle, distance) in scan:
                        
                        scan_data[min([359, floor(angle)])] = distance
                    self.data.append(scan_data)
                    scan_data = [0]*360
                    turn+=1
                    if turn==self.number_turn :                            
                        self.process_data()
                        self.data=[]
                        turn=0
                    self.lidar.clear_input()

            except RPLidarException:
                self.lidar.stop_motor()
                self.lidar.stop()
                self.lidar.disconnect()
                self.lidar = RPLidar(self.port)
                
                
            
        lidar.stop()
        lidar.stop_motor()
        lidar.disconnect()
    def process_data(self):
        global max_distance
        list_points_object=[]
        label=0
        new_data=self.data
        if self.show_result :
            self.lcd.fill((0,0,0))
        if new_data!=[] :
            for angle in range(360):
                for x in range(self.number_turn):
                    distance = new_data[x][angle]
                    if 0<distance<self.distance_max_view: # ignore initially ungathered data points
                        max_distance = max([min([5000, distance]), max_distance])
                        radians = angle * pi / 180.0
                        x = distance * cos(radians)
                        y = distance * sin(radians)
                        if len(list_points_object)==0 :                        
                            x_prec=x
                            y_prec=y
                        else :
                            if distance_points(x_prec,y_prec,x,y)>50:
                                label+=1
                                x_prec=x
                                y_prec=y

                                
                                
                        list_points_object.append(Point(x,y,label))

            
            if len(list_points_object)>0:
                if distance_points(list_points_object[0].x,list_points_object[0].y,list_points_object[-1].x,list_points_object[-1].y)<50 :
                    label=list_points_object[-1].label
                    for point in list_points_object:
                        if point.label==label:
                            point.label=0

            
            ct=1
            label=0
            list_point_to_remove=[]
            size_cluster=1
            prec_label=0
            
            for point in list_points_object :
                if point.label!=prec_label :
                    if size_cluster<5 :
                        for value in list_points_object :
                            if value.label==prec_label :
                                list_point_to_remove.append(value)
                    prec_label=point.label
                    size_cluster=1
                else :
                    size_cluster+=1
            if size_cluster<5:
                for value in list_points_object :
                    if value.label==prec_label :
                        list_point_to_remove.append(value)

            for point_remove in list_point_to_remove :
                if point_remove in list_points_object :
                    list_points_object.remove(point_remove)

                
        l_color=[[0,153,153],[255,0,0],[0,255,0],[0,0,255],[153,0,153],[0,255,255],[153,0,0],[0,153,0],[255,255,0],[255,0,255]]

        self.current_state=list_points_object
        
        cpt_label=0
        prec_label=0
        if self.show_result :

            for index in range(len(list_points_object)) :
                x=(600 + int(list_points_object[index].x/ max_distance * 119))
                y=(500 + int(list_points_object[index].y/ max_distance * 119))
                if prec_label!=list_points_object[index].label:
                    if cpt_label<len(l_color)-1 :
                        cpt_label+=1
                    prec_label=list_points_object[index].label
                point=[x,y]
                
                color=l_color[cpt_label][0],l_color[cpt_label][1],l_color[cpt_label][2]
                self.lcd.set_at(point, pygame.Color(l_color[cpt_label][0],l_color[cpt_label][1],l_color[cpt_label][2]))
            pygame.display.update()
    def get_data(self,x,y,alpha) :
        data=self.current_state
        result=[]
        
        for point in data :
            New_point=Point(0,0,0)

            x=x+point.x
            y=y+point.y
            New_point.x=cos(alpha)*x+sin(alpha)*y
            New_point.y=-sin(alpha)*x+cos(alpha)*y
            New_point.label=point.label
            result.append(New_point)
        return result
            


            

