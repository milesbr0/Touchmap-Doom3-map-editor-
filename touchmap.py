#!/usr/bin/env python

import pygame, touchgui, touchguipalate, touchguiconf, math, os
from pygame.locals import *
from array2d import array2d

# display_width, display_height = 1920, 1080
display_width, display_height = 800, 600
display_width, display_height = 1920, 1080
full_screen = False
full_screen = True
toggle_delay = 250
cell_size = 100
cell_array = array2d (0, 0, " ")   #  the contents will be written to the file and is the complete 2D map
button_array = array2d (0, 0, [None])  #  contains just the 2D array of cells (buttons) visible on the tablet
xoffset = 0
yoffset = 0
xborder = 120  # pixels from the edge
yborder = 120  # pixels from the edge
black = (0,0,0)
dark_grey = (37, 56, 60)
light_grey = (182, 182, 180)
mid_grey = (132, 132, 130)
white = (255, 255, 255)
blank_t, wall_t, door_t, spawn_t, hell_t, tick_t, room_t,doom_button  = range (8)  # enumerated types
rooms_available = [] # any room number which was deleted is placed here
next_room = 1 # the next available room number to be used.
next_tile = wall_t
asset_list = [] # list of assets
asset_desc = {} # dictionary of asset descriptions
asset_count = {} # how many of each asset are we using?
last_pos = [] # the last saved position
wall_image_name = "city2_1"
door_image_name = "adoor01_2"
pointer_name = "cross" # the image name used to mark cursor position on the map
current_map_name = "test"

#button class
class button:
    def __init__ (self, x, y, size):
        self._x = x
        self._y = y
        self._size = size
        self._tile = touchgui.image_tile (blank_list ("wallv", size),
                                          x, y,
                                          size, size, cellback)

    def to_blank (self): #set tile to blank
        self._tile.set_images (blank_list ("wallv", cell_size))
    def to_wall (self): #set tile to wall image
        self._tile.set_images (wall_list ("v", cell_size))
    def to_spawn (self): #set tile to spawn ("S")
        self._tile = touchgui.text_tile (black, light_grey, white, mid_grey,
                                         's', self._size,
                                         self._x, self._y,
                                         self._size, self._size, worldspawn, "worldspawn")
    def to_door (self): #set tile to door 
        self._tile.set_images (door_list ("v", cell_size))
    def to_hell (self): #set tile to hellknight monster image
        self._tile.set_images (private_list ("hellknight"))
    def to_tick (self): #set tile to tick monster image
        self._tile.set_images (private_list ("tick"))
    def to_room (self, room): #set tile to room number
        self._tile = touchgui.text_tile (black, light_grey, white, mid_grey,
                                      str(room), self._size,
                                      self._x, self._y,
                                      self._size, self._size, delroom, "room")
    def spawn_to_blank (self): #set tile from spawn to blank
        self._tile = touchgui.image_tile (blank_list ("wallv", self._size),
                                          self._x, self._y,
                                          self._size, self._size, cellback)

    def room_to_blank(self): #set tile from room number to blank
        self._tile = touchgui.image_tile (blank_list ("wallv", self._size),
                                          self._x, self._y,
                                          self._size, self._size, cellback)
    def get_tile (self): #returns the current tile
        return self._tile



def delspawn (param, tap): #deletes spawn tile
    global clicked, cell_array, button_array, double_tapped_cell #get global variables
    clicked = True #set clicked boolean to true
    mouse = pygame.mouse.get_pos () #get current mouse position from pygame library
    x, y = get_cell (mouse) #set x, y variables to the cell mouse pointing at
    button = button_array.get (x + xoffset, y + yoffset) #get the button that the previously set x, y variables hold
    button.spawn_to_blank () #set button to blank

def delroom (param, tap): #deletes room tile
    global clicked, cell_array, button_array, double_tapped_cell, rooms_available, next_room #get global variables
    clicked = True #set clicked boolean to true
    mouse = pygame.mouse.get_pos ()#get current mouse position from pygame library
    x, y = get_cell (mouse)#set x, y variables to the cell mouse pointing at
    button = button_array.get (x + xoffset, y + yoffset)#get the button that the previously set x, y variables hold
    button.spawn_to_blank ()#set button to blank
    rooms_available += [cell_array.get (x + xoffset, y + yoffset)] #add room number to rooms available array
    cell_array.set_contents (x + xoffset, y + yoffset, " ") 
    next_room-=1 #reduce the next room number by 1 to provide an accurate room number


def event_test (event):
    if (event.type == KEYDOWN) and (event.key == K_ESCAPE):
        myquit (None)
    if event.type == USEREVENT+1:
        reduceSignal ()

def mydoom3 (param, tap):
    pygame.display.update ()  # flush all graphic changes to screen
    pygame.time.delay (toggle_delay * 2) # pause
    try_export (os.getcwd (), "test.txt")
    pygame.quit ()            # shutdown pygame
    dmap ()                   # run chisel and dmap doom3 compile
    exec_doom_map ()          # now run doom3
    quit ()                   # quit python

def dmap ():
    os.system ("j109-d3 +dmap test.map +quit") #starts doom3 in the 109lab, loads the "test" map then quits the game


def exec_doom_map ():
    os.system ("j109-d3 +map test.map") #starts doom3 in the j109 lab and runs the "test" map

def include_asset (a, desc): #includes assets
    global asset_list, asset_desc, asset_count #get global variables
    if not (a in asset_list): #if an asset is not in the list, 
        asset_list += [a] #add it to the list
    asset_desc[a] = desc #set the asset_description array's a to sensible data
    if asset_count.has_key (a): #if asset count has key
        asset_count[a]+=1 #add asset to asset_count
    else:
        asset_count[a] = 1 #else set it to 1

def exclude_asset (a):
    global asset_list, asset_count #get global variables
    if asset_count.has_key(a): #if asset count has key 
        asset_count[a] -= 1 #reduce asset_count by 1
        if asset_count[a] ==0: #if asset_count is 0 
            del asset_count[a] #delete from asset count
            asset_list.remove (a) #and remove it from the asset_list

def write_asset (f, a): #writes assets in the following form : "asset code" define "asset description"
    s = "define %s %s\n" % (a, asset_desc[a])
    f.write (s)
    return f

def write_assets (f): #
    for a in asset_list:
        f = write_asset (f, a)
    return f

def determine_range ():
    left = -1
    x, y = cell_array.high ()
    right = x
    for j in range (y):
        for i in range (x):
            if cell_array.get (i, j) != " ":
                if (left == -1) or (i < left):
                    left = i
                if i > right:
                    right = i
    return left, right


#button definitions
def myroom (name, tap): #if clicked on, turns tile to room
    global next_tile #get global variable
    pygame.display.update () #calls update to screen
    if tap == 1:
        next_tile = room_t


def myexport (name, tap): #if clicked on 
    global current_map_name
    pygame.display.update ()#calls update to screen
    save_map (current_map_name) #calls save_map function to save map
    try_export (os.getcwd (), current_map_name) #tries to export the map with try_export method

def save_map(name):
    f = open (name, "w") 
    f = write_assets (f) #writes included assets (i.e. : hellknight )
    f.write ("\n")  # add blank line for eye candy
    f = write_map(f) #writes included walls/spaces etc.
    f.close() #close


def try_export (directory, map_name):
    os.chdir (os.path.join (os.getenv ("HOME"), "Sandpit/chisel/python")) #changes current working directory to $HOME/Sandpit/chisel/python
    r = os.system ("./developer-txt2map " + os.path.join (directory, map_name)) #exectues ./developer-txt2map command in a subshell
    os.chdir (directory)
    if r == 0:
        doom_button.set_images (private_list ("movie"))

def write_map (f): #writes the map in a form that chisel understands / reference pic attached to the assingment
    left, right = determine_range ()
    m = ""
    mdict = {"v":"#", "h":"#", "-":".", "|":".", " ":" ",
             "H":"H", "S":"S", "T":"T"}
    x, y = cell_array.high ()
    for j in range (y):
        for i in range (left, right+1):
            if mdict.has_key (cell_array.get (i, j)):
                m += mdict[cell_array.get (i, j)]
            else:
                m += cell_array.get (i, j)
        # skip blank lines
        m = m.rstrip ()
        if len (m) > 0:
            m += "\n"
    f.write (m)
    return f

#
def myquit (name = None, tap = 1): #quits pygame
    pygame.display.update ()
    pygame.time.delay (toggle_delay * 2)
    pygame.quit ()
    quit ()


def myreturn (name, tap): #returns the map in terminal for debug purposes
    pygame.display.update ()
    x, y = cell_array.high ()
    print "the map"
    m = ""
    mdict = {"v":"#", "h":"#", "-":".", "|":".", " ":" ", "s":"s"}
    for j in range (y):
        for i in range (x):
            m += mdict[cell_array.get (i, j)]
        m += "\n"
    print m


def libimagedir (name):
    return os.path.join (touchguiconf.touchguidir, name)

#changes the button colors depending on the action (i.e.:spawn/delete)
def button_list (name):
    return [touchgui.image_gui (libimagedir ("images/PNG/White/2x/%s.png") % (name)).white2grey (.5),
            touchgui.image_gui (libimagedir ("images/PNG/White/2x/%s.png") % (name)).white2grey (.1),
            touchgui.image_gui (libimagedir ("images/PNG/White/2x/%s.png") % (name)),
            touchgui.image_gui (libimagedir ("images/PNG/White/2x/%s.png") % (name)).white2rgb (.1, .2, .4)]

#zooms in and out
def myzoom (is_larger, tap):
    global cell_size, clicked

    clicked = True
    if is_larger:
        cell_size += 10
    else:
        cell_size -= 10
    recreate_button_grid ()


#recreates the tiles and buttons, comes handy when zooming
def recreate_button_grid ():
    global button_array
    button_array = array2d (0, 0, [None])


#buttons
def buttons ():
    return [touchgui.image_tile (button_list ("power"),
                                 touchgui.posX (0.95), touchgui.posY (1.0),
                                 100, 100, myquit),
            touchgui.image_tile (button_list ("export"),
                                 touchgui.posX (0.0), touchgui.posY (1.0),
                                 100, 100, myexport),
            touchgui.image_tile (button_list ("mouse"),
                                 touchgui.posX (0.05), touchgui.posY (1.0),
                                 100, 100, mydoom3),
            touchgui.image_tile (button_list ("smaller"),
                                 touchgui.posX (0.0), touchgui.posY (0.10),
                                 100, 100, myzoom, True),
            touchgui.image_tile (button_list ("larger"),
                                 touchgui.posX (0.95), touchgui.posY (0.10),
                                 100, 100, myzoom, False)]

#changes the button colors depending on the action (i.e.:spawn/delete)
def private_list (name):
    return [touchgui.image_gui ("%s.png" % (name)).white2grey (.5),
            touchgui.image_gui ("%s.png" % (name)).white2grey (.1),
            touchgui.image_gui ("%s.png" % (name)),
            touchgui.image_gui ("%s.png" % (name)).white2rgb (.1, .2, .4)]

#hellknight button
def hellknight (name, tap):
    global next_tile #get global variable
    pygame.display.update () #call update to the screen
    if tap == 1: #when clicked on
        next_tile = hell_t #next tile becomes hellknight

#tick button
def tick (name, tap):
    global next_tile#get global variable
    pygame.display.update ()#call update to the screen
    if tap == 1: #when clicked on
        next_tile = tick_t #next tile becomes hellknight

#assets we use 
def assets ():
    return [touchgui.image_tile (private_list ("hellknight"),
                                 touchgui.posX (0.95), touchgui.posY (0.9),
                                 100, 100, hellknight),
            touchgui.image_tile (private_list ("tick"),
                                 touchgui.posX (0.95), touchgui.posY (0.8),
                                 100, 100, tick)]


#worldspawn button
def worldspawn (name, tap): 
    global next_tile #get global variable
    pygame.display.update () #call update to the screen
    if tap == 1: #when clicked on
        print "worldspawn called", name, tap #prints out debug line
        next_tile = spawn_t #next tile becomes tick

#glyphs we use
def glyphs ():
    return [touchgui.text_tile (black, mid_grey, white, light_grey,
                                'S', touchgui.unitY (0.05),
                                touchgui.posX (0.5), touchgui.posY (1.0),
                                100, 100, worldspawn, "worldspawn"),
            touchgui.text_tile (black, mid_grey, white, light_grey,
                                'room', touchgui.unitY (0.05),
                                touchgui.posX (0.45), touchgui.posY (1.0),
                                100, 100, myroom, "room")]

def mygrid (name, tap):
    print "grid callback"

#changes the button colors depending on the action (i.e.:spawn/delete)
def blank_list (name, size):
    return [touchgui.image_gui ("%s-bw.png" % (name)).resize (size, size),
            touchgui.color_tile (touchguipalate.black, size, size),
            touchgui.image_gui ("%s.png" % (name)).resize (size, size),
            touchgui.image_gui ("%s.png" % (name)).resize (size, size)]

#changes the button colors depending on the action (i.e.:spawn/delete)
def wall_list (orientation, size):
    return [touchgui.image_gui ("wall%s-bw.png" % (orientation)).resize (size, size),
            touchgui.image_gui ("wall%s.png" % (orientation)).resize (size, size),
            touchgui.image_gui ("door%s.png" % (orientation)).resize (size, size),
            touchgui.image_gui ("door%s.png" % (orientation)).resize (size, size)]

#changes the button colors depending on the action (i.e.:spawn/delete)
def door_list (orientation, size):
    return [touchgui.image_gui ("door%s-bw.png" % (orientation)).resize (size, size),
            touchgui.image_gui ("door%s.png" % (orientation)).resize (size, size),
            touchgui.color_tile (touchguipalate.black, size, size),
            touchgui.color_tile (touchguipalate.black, size, size)]


def blank (x, y, size):
    b = touchgui.image_tile (blank_list ("wallv", size),
                             x, y,
                             size, size, cellback)
    assert (b != None)
    return b

#returns current cell that mouse pointing to
def get_cell (mouse):
    x, y = mouse
    x -= xborder
    y -= yborder
    return x / cell_size, y / cell_size

double_tapped_cell = None


#create blank tile
def create_blank (button):
    button.to_blank ()

#create wall tile
def create_wall (button):
    button.to_wall ()

#create door tile
def create_door (button):
    button.to_door ()

#create hellknight tile
def create_hell (button):
    global next_tile                                        #get global variable
    mouse = pygame.mouse.get_pos ()                         #get current mouse position
    x, y = get_cell(mouse)                                  #get cell that mouse pointing at
    button.to_hell ()                                       #call hellknight button
    include_asset ('H', "monster monster_demon_hellknight") #include hellknight asset
    cell_array.set_contents (x+ xoffset, y + yoffset, "H")  #
    next_tile = wall_t                                      #next tile to wall

#create spawn tile
def create_spawn (button):
    global next_tile#get global variable
    mouse = pygame.mouse.get_pos ()#get current mouse position
    x, y =get_cell (mouse)#get cell that mouse pointing at
    button.to_spawn ()#set button to spawn
    include_asset('S', "worldspawn")
    cell_array.set_contents (x + xoffset, y + yoffset, 'S')
    next_tile = wall_t#next tile to wall

#create room tile
def create_room (button):
    global next_room#get global variable
    mouse = pygame.mouse.get_pos ()#get current mouse position
    x, y = get_cell (mouse)#get cell that mouse pointing at
    button.to_room(next_room)#set button to enxt room number
    include_asset(str(next_room), "room %s" % str(next_room)) #include room asset
    cell_array.set_contents (x + xoffset, y + yoffset, str(next_room))
    next_room = next_room+1
    next_tile = wall_t#next tile to wall

#create tick tile
def create_tick (button):
    global next_tile#get global variable
    mouse = pygame.mouse.get_pos ()#get current mouse position
    x, y = get_cell (mouse)#get cell that mouse pointing at
    button.to_tick ()#set button to tick
    include_asset ('T', "monster monster_demon_tick") #include tick asset
    cell_array.set_contents (x + xoffset, y + yoffset, "T")
    next_tile = wall_t#next tile to wall


function_create = {blank_t:create_blank,
                   wall_t:create_wall,
                   door_t:create_door,
                   spawn_t:create_spawn,
                   room_t:create_room,
                   hell_t:create_hell,
                   tick_t:create_tick}



#
#  save_wall_pos - saves the coordinate [x, y] to last_pos
#

def save_wall_pos (x, y):
    global last_pos
    last_pos = [x, y]

#
#  match_line - return True if [x, y] is the same as the last_pos
#


def match_line (x, y):
    return (last_pos != []) and ((last_pos[0] == x) or (last_pos[1] == y))

#
#  draw_line - draw a line from the last_pos to, [x, y] providing [x, y]
#              lies on the same axis.
#


def draw_line (x, y):
    global cell_array, button_array
    if last_pos != []:
        if last_pos[0] == x:
            for j in range (min (y, last_pos[1]), max (y, last_pos[1])+1):
                old = cell_array.get (x, j)
                button = button_array.get (x, j)
                if old == " ":
                    button.to_wall ()
                    cell_array.set_contents (x, j, "v")

        elif last_pos[1] == y:
            for i in range (min (x, last_pos[0]), max (x, last_pos[0])+1):
                old = cell_array.get (i, y)
                button = button_array.get (i, y)
                if old == " ":
                    button.to_wall ()
                    cell_array.set_contents (i, y, "v")


def cellback (param, tap):
    global clicked, cell_array, button_array, last_pos
    clicked = True
    mouse = pygame.mouse.get_pos ()
    x, y = get_cell (mouse)
    old = cell_array.get (x + xoffset, y + yoffset)
    button = button_array.get (x + xoffset, y + yoffset)

    if (old in ["v", " "]) and (tap == 2):
        save_wall_pos (x + xoffset, y + yoffset)
    elif old == " ":
        # blank -> next_tile
        if match_line (x + xoffset, y + yoffset):
            draw_line (x + xoffset, y + yoffset)
        else:
            function_create[next_tile] (button)
        last_pos = []  # forget about last_pos
    elif old == "v":
        # wall -> door
        button.to_door ()
        cell_array.set_contents (x + xoffset, y + yoffset, "|")
    elif old == "|":
        # door -> blank
        button.to_blank ()
        cell_array.set_contents (x + xoffset, y + yoffset, " ")
    elif old in ["H", "S", "T"]:
        # remove asset
        button.to_blank ()
        cell_array.set_contents (x + xoffset, y + yoffset, " ")
        exclude_asset (old)



#
#  get_button - returns an existing cell if it exists, or create a new blank button.
#

def get_button (i, j, x, y, size):
    global cell_array, button_array
    if cell_array.inRange (xoffset + i, yoffset + j):
        if button_array.inRange (xoffset + i, yoffset + j):
            b = button_array.get (xoffset + i, yoffset + j)
            if b != None:
                return b
        content = cell_array.get (xoffset + i, yoffset + j)
        b = button (x, y, size)
        if content == "v":
            b.to_wall ()
        elif content == "|":
            b.to_door ()
        button_array.set_contents (xoffset + i, yoffset + j, [b])
        return b
    b = button (x, y, size)
    b.to_blank ()
    cell_array.set_contents (xoffset + i, yoffset + j, " ")
    button_array.set_contents (xoffset + i, yoffset + j, [b])
    return b


def finished ():
    return clicked


def button_grid (size):
    global clicked

    clicked = False
    b = []
    for i, x in enumerate (range (xborder, display_width-xborder, size)):
        for j, y in enumerate (range (yborder, display_height-yborder, size)):
            c = get_button (i, j, x, y, size)
            assert (c != None)
            b += [c.get_tile ()]
    return b


def main ():
    global players, grid, cell_size

    pygame.init ()
    if full_screen:
        gameDisplay = pygame.display.set_mode ((display_width, display_height), FULLSCREEN)
    else:
        gameDisplay = pygame.display.set_mode ((display_width, display_height))

    pygame.display.set_caption ("Map editor test")
    touchgui.set_display (gameDisplay, display_width, display_height)
    controls = buttons () + glyphs () + assets ()

    gameDisplay.fill (touchguipalate.black)
    while True:
        grid = button_grid (cell_size)
        forms = controls + grid
        touchgui.select (forms, event_test, finished)


main ()
