from igraph import *
import csv
import os
from collections import defaultdict
#pip install igraph
#pip install pycairo
'''
Comments about this code:

The visualization (plot) of the graph does not show all edges.
Not alle edges showing up is simply a plotting error.
The edgelist shows that the system registers them correctly.

Make sure the CSV is in the exact same directory as your python module.

'''

# Mother=source page, that recommends the corresponding index in recommendation1 list, recommendation 2 list, etc
Motherlist = []
Rec1list = []
Rec2list = []
Rec3list = []
Rec4list = []
Rec5list = []

# creates individual lists from the csv

with open('bol.csv', encoding='utf-8-sig') as file:  # encoding in right form deletes the unneccesary characters
    csv_reader = csv.reader(file, delimiter=',')
    line_count = 0
    for row in file:

        row = row.split(',')
        index = 0
        for e in row:
            if index == 0:
                Motherlist.append(e)
                index += 1
            elif index == 1:
                Rec1list.append(e)
                index += 1
            elif index == 2:
                Rec2list.append(e)
                index += 1
            elif index == 3:
                Rec3list.append(e)
                index += 1
            elif index == 4:
                Rec4list.append(e)
                index += 1
            elif index == 5:
                Rec5list.append(e)
                index += 1
            else:
                print(
                    "something went wrong. Please check the booklist and the length of the recommendations. All books should have exactly five recommendations.")

        line_count += 1
    print(f'Processed {line_count} books.')

# tests if the lists are compiled correctly
'''
print(Motherlist)
print(Rec1list)
print(Rec2list)
print(Rec3list)
print(Rec4list)
print(Rec5list)
'''

# creates a list of recommendationlists
Recommendationlist = []
Recommendationlist.append(Rec1list)
Recommendationlist.append(Rec2list)
Recommendationlist.append(Rec3list)
Recommendationlist.append(Rec4list)
Recommendationlist.append(Rec5list)

# create graph
bookgraph = Graph(directed=True)
for mother in Motherlist:  # creates all mother vertices
    bookgraph.add_vertex(mother)
bookgraph.vs["Mother"] = Motherlist  # assigns the value Mother to those

# add recommendation vertices and edges
for i in range(len(Motherlist)):
    mother = Motherlist[i]
    for r in range(5):
        rec = Recommendationlist[r][i]
        # print(mother, rec)
        bookgraph.add_vertex(rec)
        bookgraph.es["Recommendends"] = rec  # assigns meaning to edges
        bookgraph.add_edges([(mother, rec)])  # creates edges

# print(bookgraph)
bookgraph.vs["label"] = bookgraph.vs["name"]  # shows the names on the graph
layout = bookgraph.layout("random")

# visualize the graph
plot(bookgraph, layout=layout)
print(bookgraph.assortativity_degree())


###  operations that work:
'''
plot(bookgraph, layout=layout)#shows the graph
#bookgraph.get_edgelist()
#print(bookgraph.indegree())
#print(bookgraph.outdegree())
#print(bookgraph.density())
#print(bookgraph.girth())
print(bookgraph.maxdegree())

'''

###operations that i still need to figure out:

# print(bookgraph.clusters())  #what does this return mean?
# print(bookgraph.pagerank()) # what does this return mean
# print(bookgraph.assortativity_degree()) # add types  of vertices for it to work
# print(bookgraph.authority_score()) # what does this return mean
# print(bookgraph.average_path_length()) # what does this return mean
# print(bookgraph.cliques()) # what does this return mean
# print(bookgraph.coreness())# what does this return mean
# print(bookgraph.radius())