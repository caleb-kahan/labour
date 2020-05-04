import mdl
from display import *
from matrix import *
from draw import *

def run(filename):
    """
    This function runs an mdl script
    """
    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print("Parsing failed.")
        return

    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [255,
              255,
              255]]

    color = [0, 0, 0]
    tmp = new_matrix()
    ident( tmp )

    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    zbuffer = new_zbuffer()
    tmp = []
    step_3d = 100
    consts = ''
    coords = []
    coords1 = []
    symbols['.white'] = ['constants',
                         {'red': [0.2, 0.5, 0.5],
                          'green': [0.2, 0.5, 0.5],
                          'blue': [0.2, 0.5, 0.5]}]
    reflect = '.white'
    #I can iterate through this list later to find the reflective values
    colors = ['red','green','blue']

    print(symbols)
    for command in commands:
        #pulling all necessary data from commands dictionary
        function = command['op']
        args = command['args']

        if function == "push":
            #just copying from old parser-should be no difference
            #renaming system to stack
            stack.append( [x[:] for x in stack[-1]] )
        elif function == "pop":
            #just copying from old parser-should be no difference
            #renaming system to stack
            stack.pop()
        elif function == "rotate":
            #float is no longer necessary
            theta = args[1] * (math.pi / 180)
            if args[0] == 'x':
                t = make_rotX(theta)
            elif args[0] == 'y':
                t = make_rotY(theta)
            else:
                t = make_rotZ(theta)
            matrix_mult( stack[-1], t )
            stack[-1] = [ x[:] for x in t]
        elif function == "move":
            t = make_translate(args[0], args[1], args[2])
            matrix_mult( stack[-1], t )
            stack[-1] = [ x[:] for x in t]
        elif function == "scale":
            t = make_scale(args[0],args[1],args[2])
            matrix_mult( stack[-1], t )
            stack[-1] = [ x[:] for x in t]
        elif function == "box":
            #replacing tmp with temp
            #constants is only a a parameter for certain functions
            consts = command['constants']
            if consts is None:
                consts = reflect
            add_box(tmp, args[0], args[1], args[2],
                    args[3], args[4], args[5])
            matrix_mult( stack[-1], tmp )
            draw_polygons(tmp, screen, zbuffer, view, ambient, light,symbols,consts)
            tmp = []
        elif function == "torus":
            consts = command['constants']
            if consts is None:
                consts = reflect
            add_torus(tmp,
                      args[0], args[1], args[2],
                      args[3], args[4], step_3d)
            matrix_mult( stack[-1], tmp )
            draw_polygons(tmp, screen, zbuffer, view, ambient, light,symbols,consts)
            tmp = []
        elif function == "sphere":
            consts = command['constants']
            if consts is None:
                consts = reflect
            add_sphere(tmp,
                       args[0], args[1], args[2],
                       args[3], step_3d)
            matrix_mult( stack[-1], tmp )
            draw_polygons(tmp, screen, zbuffer, view, ambient, light,symbols,consts)
            tmp = []
        elif function == "line":
            add_edge( tmp,
                      args[0], args[1], args[2],
                      args[3], args[4], args[5] )
            matrix_mult( stack[-1], tmp )
            draw_lines(tmp, screen, zbuffer, color)
            tmp = []
        elif function == "save":
            save_extension(screen, args[0])
        elif function == "display":
            display(screen)
