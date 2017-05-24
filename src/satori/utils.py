'''
Created on May 24, 2017

@author: acer
'''
import sys
import markdown


def main(args=None):
    #args = parse_args(args)
    f=open('../static/Algorithm.md')
    md = f.read()
    extensions = ['extra', 'smarty']
    html = markdown.markdown(md, extensions=extensions, output_format='html5')
    #doc = jinja2.Template(TEMPLATE).render(content=html)
    print (html)
    #args.out.write(doc)


if __name__ == '__main__':
    main()