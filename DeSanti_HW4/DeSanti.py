#Andrew DeSanti
#CS-581
#Assignment04
#This program takes in a .csv file and parses it to collect information about the triads formed by the connections detailed within

#to run this program simply type "python3 Desanti.py"
#the external libraries pandas and datetime are required

import pandas as pd     #to create clean charts in the terminal output
import datetime

def insideHelper(value , array): #same as in but for checking the oth index of a list of lists
    for sublist in array:
        if sublist[0] == value:
            return True
    return False

def countNodeAppearances(node, list): #function to count the number of times certain node appears in a subset of relations
    counter = 0
    for sublist in list:
        if sublist[0]==node or sublist[1]==node:
            counter+=1
    return counter/2

def sortOnlyFirstTwo(list): #function to sort only the first two elements of a three element list
    new_list = [list[0], list[1]]
    new_list.sort()
    new_list.append(list[2])
    return new_list

def toPercent(floating): #function to convert float to percent string
    percentage = "{:.2%}".format(floating)
    return percentage

def removeDupes(list): #function to remove duplicates and blank spaces from triad list
    for node in list:
        for triad in node:
            unwrapped = sorted([triad[0][0],triad[0][1],triad[0][2],triad[1][0],triad[1][1],triad[1][2],triad[2][0],triad[2][1],triad[2][2]]) #this is the raw data of a triad
            counter = 0
            for node1 in list:
                for triad1 in node1:
                    compared_to = sorted([triad1[0][0],triad1[0][1],triad1[0][2],triad1[1][0],triad1[1][1],triad1[1][2],triad1[2][0],triad1[2][1],triad1[2][2]])
                    if compared_to == unwrapped:
                        counter+=1
                        if counter>1:
                            node1.remove(triad1)
    for node in list:
        if node == []:
            list.remove(node)
            for triad in node:
                if triad==[]:
                    node.remove(triad)
                if sum(triad)==0:
                    node.remove(triad)
                for connection in triad ==[]:
                    if connection ==[]:
                        triad.remove(connection)
                    if sum(connection)==0:
                        triad.remove(connection)

if __name__ == '__main__':
    starttime = datetime.datetime.now()
    #setup, parse csv and create lists...
    list_of_connections = []
    csv_name = input("Enter the file name (xxx.csv)\n")
    col_names = ['1', '2', 'Cond']
    df = pd.read_csv(csv_name, names=col_names, header=None)
    #get max of row one and two to find minimum number of iterations...
    col_1 = df["1"]
    col_2 = df["2"]
    max_of_1 = col_1.max()
    max_of_2 = col_2.max()
    if max_of_1 >= max_of_2:
        num_of_nodes = max_of_1
    else:
        num_of_nodes = max_of_2
    #create a list of lists of all connections
    for index, row in df.iterrows(): 
        if row.values.tolist() in list_of_connections:
            pass
        else:
            list_of_connections.append(row.values.tolist())
    

    #create a sublist containing a node to check for triads
    all_triads = []
    final_list_of_triads = []
    num_triads = 0
    for node in range(num_of_nodes+1):
        temp_list_index = 0
        temp_list = [] #list to hold sublists containing node
        connected_to_node = [] #list holding nodes connected to the node
        triads_members = [] #holds sets of three that actually are part of a triad
        all_triads_for_node = []

        for sublist in list_of_connections:
            if sublist[0] == node or sublist[1] == node:
                temp_list.append(sublist)
        for sublist in temp_list: 
            if sublist[0]!=node:
                connected_to_node.append([sublist[0], temp_list_index])
            if sublist[1]!=node:
                connected_to_node.append([sublist[1], temp_list_index])
            temp_list_index+=1

        if len(connected_to_node) > 1: #needs to be connected to at least two other nodes for a triad to even be possible:
            for connection in connected_to_node: #connection is the number connected to node
                for list in list_of_connections: #list is the row from the original csv file
                    if (list[0] == connection[0] and insideHelper(list[1],connected_to_node)) or (insideHelper(list[0], connected_to_node) and list[1] == connection[0]):
                        triads_members.append(list) #add the sublist into the temp list. 
                        triads_members.append(temp_list[connection[1]])
            #from here we need to actually create the triads themselves...
            number_of_triads_with_node = countNodeAppearances(node, triads_members)
            num_triads+=number_of_triads_with_node


            if triads_members!=[]:#if not empty
                copy_of_triads_members = triads_members #create temporary version of triad list
                for connection in copy_of_triads_members:
                    temp_triad = []
                    first_flag = False
                    second_flag = False
                    if connection[0]!= node and connection[1]!=node:
                        a = connection[0]
                        b = connection[1]
                        temp_triad.append(connection)

                        
                        for i in copy_of_triads_members:
                            if ((i[0]==node and i[1]==a) or (i[0]==a and i[1]==node)) and first_flag==False: 
                                temp_triad.append(sortOnlyFirstTwo(i))
                                first_flag = True
                            if ((i[0]==node and i[1]==b) or (i[0]==b and i[1]==node)) and second_flag==False:
                                temp_triad.append(sortOnlyFirstTwo(i))
                                second_flag = True
                        if temp_triad in all_triads_for_node:
                            pass
                        else:
                            all_triads_for_node.append(temp_triad)
                        

            #sorted_all_for_node = sorted(all_triads_for_node, key=lambda x:x[0][1])
            all_triads.append(all_triads_for_node)
    removeDupes(all_triads)
    for node in all_triads:
        for triad in node:
            final_list_of_triads.append(triad)
    print("***")
    print("Final list of triads stored as a list of lists named final_list_of_triads")
    print("Parsed from: " + csv_name)

    #collect number and type of edges
    positive_edges = 0
    negative_edges = 0
    number_of_edges = len(list_of_connections)
    for connections in list_of_connections:
        if connections[2]==1:
            positive_edges+=1
        elif connections[2]==-1:
            negative_edges+=1

    #probabilities
    prob_positive_edge = (positive_edges/number_of_edges)
    prob_negative_edge = (1 - prob_positive_edge)
    prob_of_ttt = pow(prob_positive_edge,3)
    prob_of_ttd = pow(prob_positive_edge,2)*prob_negative_edge
    prob_of_tdd = pow(prob_negative_edge,2)*prob_positive_edge
    prob_of_ddd = pow(prob_negative_edge,3)

    #collect triad types
    TTT = 0
    TTD = 0
    TDD = 0
    DDD = 0
    for triad in final_list_of_triads:
        relation_type = triad[0][2]+triad[1][2]+triad[2][2]
        if relation_type == 3:
            TTT+=1
        elif relation_type == 1:
            TTD+=1
        elif relation_type == -1:
            TDD+=1
        elif relation_type == -3:
            DDD+=1
    total = len(final_list_of_triads)
    percent_ttt = TTT/total
    percent_ttd = TTD/total
    percent_tdd = TDD/total
    percent_ddd = DDD/total


    endtime = datetime.datetime.now()
    print("==============================================================================================")
    print("Number of edges used to identify triads: " + str(number_of_edges))
    print("Number of positive (trust) edges: " + str(positive_edges))
    print("Number of negative (distrust) edges: " + str(negative_edges))
    print("Probability that an edge will be positive: " + str(prob_positive_edge))
    print("Probability that an edge will be negative: " + str(prob_negative_edge))
    print("Number of TTT triads: " + str(TTT))
    print("Number of TTD triads: " + str(TTD))
    print("Number of TDD triads: " + str(TDD))
    print("Number of DDD triads: " + str(DDD))
    print("Total Number of triads: " + str(total))
    print("Expected Distribution:")
    print("TTT- Percent: " + str(toPercent(prob_of_ttt)) + " Number:  " +str(prob_of_ttt*total))
    print("TTD- Percent: " + str(toPercent(prob_of_ttd)) + " Number:  " +str(prob_of_ttd*total))
    print("TDD- Percent: " + toPercent(prob_of_tdd) + " Number:  " +str(prob_of_tdd*total))
    print("DDD- Percent: " + toPercent(prob_of_ddd) + " Number:  " +str(prob_of_ddd*total))
    print("Actual Distribution:")
    print("TTT- Percent: " + toPercent(percent_ttt) + " Number:  " +str(TTT))
    print("TTD- Percent: " + toPercent(percent_ttd) + " Number:  " +str(TTD))
    print("TDD- Percent: " + toPercent(percent_tdd) + " Number:  " +str(TDD))
    print("DDD- Percent: " + toPercent(percent_ddd) + " Number:  " +str(DDD))
    print("This program took: " + str(endtime-starttime))
    print("==============================================================================================")