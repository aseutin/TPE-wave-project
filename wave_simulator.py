# Wave Simulator - One force - 1.5 kg counter weight in 14 cm of water - TPE

#-------------Prompt User-------------

# print information
print "Ceci simule ceux que nous avons trouvé durant notre experience.\n\nNous avons étudié l'effet de la topographie sur la formation des vagues pour notre projet de TPE, \n\nOn a fait l'experience avec un contre poids de 1,5 kg dans une basin avec 14 cm de profondeur."
print "\nAppuyer sur la touche 'ENTRER' pour changer le niveau de l'eau. \n\nAppuyer sur la barre espace pour changer l'échelle (représenté par la barre dans le coin en haut à droite et qui représente 5 cm). \n\nCliquer pour créer un obstacle sur le sol du bassin (l'angle sera affiché ici, dans le 'Python Shell')."
print "\nAppuyer sur la touche 'SHIFT' pour imprimé la hauteur de la vague la plus proche à l'abscisse de votre souris (sa va apparaitre ici, dans le 'Python Shell')."

# wait for user input to continue 
should_I_continue = raw_input("\nCliquer sur 'ENTER' pour lancer la simulation: ")
while should_I_continue == None:
    pass

#------------House Keeping------------
import math

import pygame, sys, random
from pygame.locals import*

pygame.init()

screen_width = 1200
screen_height= 600
pygame.display.set_caption("Wave Simulator - One force - 1.5 kg counter weight in 14 cm of water - TPE")
screen=pygame.display.set_mode((screen_width, screen_height),0,32)

#------------Def Variables------------

global water_start
water_start = 150
water_height = screen_height - water_start
pointlist = []
marker_length_in_cm = 5
distance_from_edge = 30

max_wave_height_in_cm = 2.9

white = (255, 255, 255)
dark_blue = (50, 50, 150)
sand = (255, 222, 173)
black = (0, 0, 0)

global marker_length
marker_length = 200
global pixels_per_cm
pixels_per_cm = marker_length / 5
global depth
depth = pixels_per_cm * 14

fps = 10

waves = []

#-------Def Classes and Methods-------

def cm_to_px(cm):
    global pixels_per_cm
    px = cm * pixels_per_cm
    return px

def px_to_cm(px):
    global pixels_per_cm
    cm = px/pixels_per_cm
    return cm

def draw_marker():
    global marker_length
    marker_x_2 = screen_width - distance_from_edge
    marker_x_1 =  marker_x_2 - marker_length
    
    scale_marker = pygame.draw.line(screen, black, (marker_x_1, distance_from_edge), (marker_x_2, distance_from_edge), 4)

def draw_depth():
    global water_start
    global depth

    pygame.draw.rect(screen, dark_blue , (0, water_start, screen_width, depth))

class wave:
    def __init__(self):
        waves.append(self)
        self.x_pos = 0
        self.y_pos = 0
        self.height = 0
        self.width = 0
        self.color = black
        self.get_all_values()
        self.draw()
    def find_x_pos(self):
        for i in waves:
            self.x_pos = self.x_pos + i.width
    def calculate_height(self):
        self.height = cm_to_px(max_wave_height_in_cm * 2.7**(px_to_cm(self.x_pos)*(-.016)))
    def calculate_width(self): 
        # stays constant in control - normally much longer but shortened for asthethic purposes
        self.width = 1.5 * pixels_per_cm
    def find_y_pos(self):
        self.y_pos = water_start - self.height/2
    def find_color(self):
        values = []
        for i in waves:
            value = abs(self.x_pos - i.x_pos)
            values.append(value)
        if waves[waves.index(self)-1].color == dark_blue:
            self.color = white
        else:
            self.color = dark_blue           
    def get_all_values(self):
        self.find_x_pos()
        self.calculate_height()
        self.find_y_pos()
        self.calculate_width()
        self.find_color()      
    def draw(self):
        if self.width > 5 and self.height > 5:
            pygame.draw.ellipse(screen, self.color, (self.x_pos, self.y_pos, self.width, self.height), 0)
              
def total_width_of_waves():
    total_width = 0
    for i in waves:
        total_width = total_width + i.width
    return total_width

def create_wave_instances():
    while total_width_of_waves() < screen_width:
        i = wave()

def redraw_waves():
    for i in waves:
        i.draw()

def distance_from_start(pointlist, x_pos):
    # calculate the distance from the start of the variation 
    a,b = pointlist[0]
    c,d = pointlist[1]
    distance_from_start = px_to_cm(x_pos - a)
    return distance_from_start

def find_angle_of_slope(pointlist):
    a,b = pointlist[0]
    c,d = pointlist[1]
    # find the length of the hypotenuse
    hypotenuse = ((a-c)**2 + (b-d)**2)**.5
    # find the length of the base (adjacent to angle)
    adjacent = abs(c - a)
    # get angle with cosine
    angle = math.degrees(math.acos(adjacent/hypotenuse))
    if value_y_one > water_start + depth:
        angle = angle * -1
    return angle

def find_value_of_a(angle):
    answer = -0.001*angle + 0.0016 # might not need the + 0.0016
    return answer

def find_percent_of_change_at_point(pointlist, x_pos):
    # answer = a * distance_from_start
    answer = find_value_of_a(find_angle_of_slope(pointlist)) * distance_from_start(pointlist, x_pos)
    return answer

def calculate_new_height(pointlist):
    for i in waves:
        i.height = i.height * (find_percent_of_change_at_point(pointlist, i.x_pos) + 1)

#------------Run Main Loop------------
        
while True:
    pygame.time.Clock().tick(fps)
    
    #refresh values
    pixels_per_cm = marker_length / 5
    water_height = screen_height - water_start
    depth = pixels_per_cm * 14
    
    a,b=pygame.mouse.get_pos()

    background = pygame.draw.rect(screen, white , (0, 0, screen_width, screen_height))

    water =  pygame.draw.rect(screen, sand, (0, water_start, screen_width, water_height))

    draw_depth()

    create_wave_instances()
    # redefine wave attributes (methods retain original values of variables and don't update without this)
    for i in waves:
        i.height = cm_to_px(max_wave_height_in_cm * 2.7**(px_to_cm(i.x_pos)*(-.016)))
        i.width = 1.5 * pixels_per_cm
        i.x_pos = 0
        for j in range(waves.index(i)):
            i.x_pos = i.x_pos + waves[j].width
        if pointlist != [] and i.x_pos > value_x_one:
            i.height = i.height * (find_percent_of_change_at_point(pointlist, i.x_pos) + 1)
        i.y_pos = water_start - i.height/2
    redraw_waves()

    # draw black line through the middle of the waves in order to have a line of reference
    line_of_reference = pygame.draw.line(screen, black, (0, water_start), (screen_width, water_start), 1)
    
    draw_marker()
    
    # repeat definition of variables in order to not have to make each one global
    marker_x_2 = screen_width - distance_from_edge
    marker_x_1 =  marker_x_2 - marker_length
    
    for event in pygame.event.get():  
        if event.type==MOUSEBUTTONDOWN:
            # create obstacle with points in array
            value_x_one, value_y_one = pygame.mouse.get_pos()
            if value_y_one < water_start:
                value_y_one = water_start
            pointlist = [(value_x_one, water_start + depth),(screen_width, value_y_one) ,(screen_width, water_start + depth)]
            print "\nL'angle de la pente est égale à: " + str(find_angle_of_slope(pointlist)) +" degrés."
            
        if event.type==KEYDOWN:
            if event.key==K_SPACE:
                # change the scale
                if abs(a - marker_x_2) > 5:
                    pointlist = []
                    marker_length = abs(a - marker_x_2)
            if event.key==K_RETURN:
                # change the height of the water
                pointlist = []
                water_start = b
            if event.key==K_RSHIFT or event.key==K_LSHIFT:
                # find the closest wave and print its height 
                values = []
                for i in waves:
                    value = abs(a - i.x_pos)
                    values.append(value)
                closest_wave = waves[values.index(min(values))]
                print "\nLa hauteur de cette vague est égale à: " + str(px_to_cm(closest_wave.height)) + " cm." 
            else:
                pass
        if event.type==QUIT:
            pygame.quit()
            sys.exit()

    # if pointlist has any values check if it is above or below the water and change the color accordingly
    if pointlist != []:
        if value_y_one > water_start + depth:
            color = dark_blue   
        else:
            color = sand
        pygame.draw.polygon(screen, color, pointlist, 0)   
        
    pygame.display.update()
