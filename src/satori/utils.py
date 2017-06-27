'''
Created on May 24, 2017

@author: acer
'''
import sys
import markdown
import inspect
from pprint import pprint
from werkzeug.security import _sys_rng

def load_class_from_name(fqcn):
    # Break apart fqcn to get module and classname
    paths = fqcn.split('.')
    modulename = '.'.join(paths[:-1])
    classname = paths[-1]
    # Import the module
    __import__(modulename, globals(), locals(), ['*'])
    # Get the class
    cls = getattr(sys.modules[modulename], classname)
    # Check cls
    if not inspect.isclass(cls):
       raise TypeError("%s is not a class" % fqcn)
    # Return class
    return cls

def main(args=None):
    #args = parse_args(args)
    f=open('../static/Algorithm.md')
    md = f.read()
    extensions = ['extra', 'smarty']
    html = markdown.markdown(md, extensions=extensions, output_format='html5')
    #doc = jinja2.Template(TEMPLATE).render(content=html)
    print (html)
    #args.out.write(doc)

def transformArrayToScale(arr1):
    #arr1 = [['0-7',.10],['8-17',0.20],['18-23',0.1]]
    #arr1=[[0,0],[1,0],[2,0],[3,0],[4,0],[5,0],[6,1],[7,5],[8,9],[9,15],[10,20],[11,25],[12,26]
    #      ,[13,25],[14,22],[15,20],[16,15],[17,10],[18,5],[19,3],[20,0],[21,0],[22,0],[23,0]]
    arr2=[]
    for i in range(24):
        for j in range(len(arr1)):
            rng = arr1[j][0]
            if isinstance(rng, str):
                nos = rng.split('-')
                frm = int(nos[0])
                to = int(frm if len(nos) ==1 else nos[1])
            else:
                frm = rng
                to=frm
            if i >= frm and i <= to:
                arr2.append([i,arr1[j][1]])
                break
    return arr2

            

if __name__ == '__main__':
    transformArrayToScale()