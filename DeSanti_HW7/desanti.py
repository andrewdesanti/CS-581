#By Andrew DeSanti
#I pledge my honor that I have abided by the Stevens Honor System

#Assignment 7 - Analyze Social Network Data

#to run this program in a terminal window:"python3 desanti.py"



#determine where a political candidate should show ads based on age, sex, and region
#hypothetically this candidate is running democrat, so they are looking to sway those who are not certain of their party
#the candidate has ads that target age groups, sex, and region however they can only run it on a few social media platforms
#determine where the most efficient places are to run ads based on where the most men who are not for sure D or R view social media, for women, for people 18-25, 26-40, etc.
#import libraries
import pandas as pd
import matplotlib as plt

#import data from csv and store it in pandas dataframe df
csv_name = "Pew_Survey.csv"
df = pd.read_csv(csv_name)
#print(df)

#from this dataframe, we want to remove respondants who ARE sure that they are either R or D, so those who responded 3,4,5,8,9 to party
df_temp = df.loc[df["party"]!=1]
df_not_sure = df_temp.loc[df["party"]!=2]
#print(df_not_sure)

#df_not_sure now only contains responses from people unsure of their political association, and therefore are those who are most likely to be swayed by advertisements
