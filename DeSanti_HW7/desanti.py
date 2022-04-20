#By Andrew DeSanti
#I pledge my honor that I have abided by the Stevens Honor System

#Assignment 7 - Analyze Social Network Data

#to run this program in a terminal window:"python3 desanti.py"

#determine where a political candidate should show ads based on age, sex, and region
#hypothetically this candidate is looking to sway those who are not certain of their party, ie those who are strongly R or D are not likely to change their vote based on an ad
#the candidate has ads that target age groups, sex, and region however they can only run it on a few social media platforms
#determine where the most efficient places are to run ads based on where the most men who are not for sure D or R view social media, for women, for people 18-25, 26-40, etc.

#import libraries
import pandas as pd
import matplotlib.pyplot as plt

#function to count the number of rows where the value of a give collumn is 1
def one_counter(collumn, source):
    sample = source.apply(lambda x : True
            if x[collumn] == 1 else False, axis = 1)
    num_rows = len(sample[sample == True].index)
    return num_rows

#function to return a dictionary of sums of platforms from a pregrouped dataframe
def sum_by_service(source):
    sums = {
    "total_t": one_counter("web1a", source),
    "total_inst" : one_counter("web1b", source),
    "total_fb" : one_counter("web1c", source),
    "total_sc" : one_counter("web1d", source),
    "total_yt" : one_counter("web1e", source),
    "total_wa" : one_counter("web1f", source),
    "total_pt" : one_counter("web1g", source),
    "total_ln" : one_counter("web1h", source),
    "total_rdt" : one_counter("web1i", source), 
    }
    return sums

#function to add labels to bargraph
def addlabels(x,y):
    for i in range(len(x)):
        plt.text(i,y[i],y[i])

#function to create the bar graph from a dictionary
def graph_from_sums(sums, DataSet):
    DataSet = str(DataSet)
    keys = list(sums.keys())
    values = list(sums.values())
    fig = plt.figure(figsize=(7,7))
    plt.bar(keys, values, color=['cyan', 'purple', 'darkblue', 'yellow', 'red', 'green', 'maroon', 'blue', 'orange'])
    addlabels(keys, values)
    plt.xlabel("Social Media Platforms")
    plt.ylabel("Number of users from " + DataSet)
    plt.title("Number of Users from " + DataSet + " per Social Media Platform")
    plt.show()



if __name__ == "__main__":
    #import data from csv and store it in pandas dataframe df
    csv_name = "Pew_Survey.csv"
    df = pd.read_csv(csv_name)

    #from this dataframe, we want to remove respondants who ARE sure that they are either R or D, so those who do not respond 1 or 2 to party
    df_temp = df.loc[df["party"]!=1]
    df_not_sure = df_temp.loc[df_temp["party"]!=2]

    #df_not_sure now only contains responses from people unsure of their political association, and therefore are those who are most likely to be swayed by advertisements
    #first lets find the optimal social media platform for ads that target gender based issues
    df_women = df_not_sure.loc[df_not_sure["sex"]==2]
    graph_from_sums(sum_by_service(df_women), "Women")

    df_men = df_not_sure.loc[df_not_sure["sex"]==1]
    graph_from_sums(sum_by_service(df_men), "Men")


    #we can now create a similar scenario spliting by age
    df_youngest = df_not_sure.loc[df_not_sure["age"]<25]
    graph_from_sums(sum_by_service(df_youngest), "Ages 0-24")

    df_temp = df_not_sure.loc[df_not_sure["age"]>=25]
    df_young = df_temp.loc[df_temp["age"]<50]
    graph_from_sums(sum_by_service(df_young), "Ages 25-49")

    df_temp = df_not_sure.loc[df_not_sure["age"]>=50]
    df_old = df_temp.loc[df_temp["age"]<75]
    graph_from_sums(sum_by_service(df_old), "Ages 50-74")

    df_temp = df_not_sure.loc[df_not_sure["age"]>=75]
    df_older = df_temp.loc[df_temp["age"]<98]
    graph_from_sums(sum_by_service(df_older), "Ages 75 and Up")

    #and now we split by region
    df_northeast = df_not_sure.loc[df_not_sure["cregion"]==1]
    graph_from_sums(sum_by_service(df_northeast), "Northeast")

    df_midwest = df_not_sure.loc[df_not_sure["cregion"]==2]
    graph_from_sums(sum_by_service(df_midwest), "Midwest")

    df_south = df_not_sure.loc[df_not_sure["cregion"]==3]
    graph_from_sums(sum_by_service(df_south), "South")

    df_west = df_not_sure.loc[df_not_sure["cregion"]==4]
    graph_from_sums(sum_by_service(df_west), "West")

    #lets say that the most important topic for this candidate discusses women from the south between the ages 18 to 35...
    df_temp = df_not_sure.loc[df_not_sure["age"]<=35]
    df_temp1 = df_temp[df_temp["sex"]==2]
    df_important = df_temp1[df_temp1["cregion"]==3]
    graph_from_sums(sum_by_service(df_important), "Important")