# ------- written by Sebastian Schanz --------
# this code generates random triangles in cadquery-editor
# for further information on cadquery python CAD library see:
# https://github.com/CadQuery/CQ-editor#installation
# https://cadquery.readthedocs.io/en/latest/



import random as rn
import cadquery as cq



# random_triangle_generation
pts = [[rn.randint(0,100), rn.randint(0,100)],
       [rn.randint(0,100), rn.randint(0,100)],
       [rn.randint(0,100), rn.randint(0,100)],]
#pts =  [[98, 99], [92, 4], [1, 10]]    # for specific
wire = cq.Workplane('front')\
.polyline(pts)\
.close()\
.val()
pts = wire.Vertices()



# wire = wire.fillet(1, pts)




# sweep = wire, pts[0]

face = cq.Face.makeFromWires(wire)

show_object(face)
