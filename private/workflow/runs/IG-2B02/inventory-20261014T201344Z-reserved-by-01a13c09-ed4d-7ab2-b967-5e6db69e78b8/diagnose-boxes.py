from ops import *
from math import floor,ceil
items=load(AR+'/author-specifications.json')['specifications']
for i,a in enumerate(items):
 for b in items[i+1:]:
  if a['page']!=b['page']:continue
  def box(s):
   x0,y0,x1,y1=s['observed_pixel_box'];return [floor(x0*1000000/1224),floor(y0*1000000/1584),ceil(x1*1000000/1224),ceil(y1*1000000/1584)]
  x,y=box(a),box(b)
  if max(x[0],y[0])<min(x[2],y[2]) and max(x[1],y[1])<min(x[3],y[3]):print(a['key'],b['key'],x,y)
