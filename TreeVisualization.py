#from ete3 import Tree
from Bio import Phylo
#import os
#import pylab

#ete way
#t = Tree(file)
#print(t)

#path = "PhlyoTreeDirectory/tree_file"
#f = open(path)
#f.read()

# the name of the file
file = "tree_file"

#Phylo way -- terminal
temp = Phylo.read(file, 'newick')
Phylo.draw_ascii(temp) # prints out the tree to the terminal

#Phylo way -- jpeg
temp.ladderize() # Flip branches so deeper clades are displayed at top
Phylo.draw(temp) # prints out in seperate window, can be saved as a jpeg

#Phylo.draw_graphviz(temp, node_size=0)
#pylab.show()

