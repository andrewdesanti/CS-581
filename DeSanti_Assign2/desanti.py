#By Andrew DeSanti
#I pledge my honor that I have abided by the Stevens Honor System

#Assignment 02 - Using the Google APIs to access YouTube Data 

#to run this program in a terminal window:"python3 desanti.py"
#you will be prompted for a search term... enter a string to be searched for via youtube api
#you will be prompted for a search max... enter a positive integer for the number of videos to be searched for
#Note!!! this program uses the googleapi library, csv library, and pandas library. Install them via pip before running!

#import libraries...
from googleapiclient.discovery import build   #to access google api
import csv   #to create a csv
import pandas as pd     #to create clean charts in the terminal output

#api information
API_KEY = "xxx"
API_NAME = "youtube"
API_VERSION = "v3"  

if __name__ == '__main__':
    #input search terms, catch errors when bad types are used (max should be a positive integer)
    try:
        search_term = input("Search Term: ")
        search_max = int(input("Max Number of Results: "))
        assert search_max > 0 and type(search_max) == int
    except ValueError:
        print("Invalid Search Criteria. Input a String for Search Term and a Positive Integer for Search Max.")

    print("Selected Search Term: " + str(search_term))
    print("Selected Search Max: " + str(search_max))

    result_list = []    #declare list to hold dictionaries of search results

    api_call = build(API_NAME, API_VERSION, developerKey=API_KEY) #build api call
    search = api_call.search().list(q=search_term, part="id,snippet", maxResults=search_max+1).execute()
    for result in search.get("items", []):
        if result["id"]["kind"] == "youtube#video": #if search result is actually a video (not a channel or playlist)
            video_id = result["id"]["videoId"] #get video id
            video_title = result["snippet"]["title"] #get video title

            result_data = api_call.videos().list(id=video_id,part="statistics").execute() #call api again to get more indept data
            for data in result_data.get("items",[]):
                view_count = data["statistics"]["viewCount"] #get view count
                if 'likeCount' not in data["statistics"]:   #if like count is not included then it is zero, we must test for that
                    like_count = 0
                else:
                    like_count = data["statistics"]["likeCount"]
                if 'commentCount' not in data["statistics"]:    #if comment count is not included then it is zero, we must test for that
                    comment_count = 0
                else:
                    comment_count = data["statistics"]["commentCount"]

            result_data2 = api_call.videos().list(id=video_id,part="contentDetails").execute() #call api again to get video duration
            for data in result_data2.get("items",[]):
                duration = data["contentDetails"]['duration']

            result_dict = { #store all collected data in a dictionary
                "video_id": video_id,
                "video_title": video_title,
                "view_count": view_count,
                "like_count": like_count,
                "comment_count": comment_count,
                "video_duration": duration
            }
            result_list.append(result_dict) #store this dictionary in the list

    api_call.close() #close api call
    #=====CSV=====#
    keys = result_list[0].keys() #grab dictionary keys to use as csv headers
    csv_filename = str(search_term)+"_"+str(search_max)+".csv"
    csv_file = open(csv_filename, "w") #open csv
    dict_writer = csv.DictWriter(csv_file, keys) #use csv library to store list of dictionaries in the file
    dict_writer.writeheader()
    dict_writer.writerows(result_list)
    csv_file.close()    #close file
    print("A .csv file named " + csv_filename + " has been created containing the raw data collected through the search.")
    print("====================================================================================================================================================")
    #=============#

    #=====Analysis 1=====#
    print("Analysis 1:")
    chart = pd.DataFrame(result_list) #create pandas dataframe using list of dictionaries
    print(chart)
    print("====================================================================================================================================================")
    #====================#

    #=====Analysis 2=====#
    print("Analysis 2:")
    temp_list = [] #create temp list to manipulate data without losing original search data

    for video in range(len(result_list)): #for all video dictionaries that have a view count>0
        if result_list[video]["view_count"] != 0:
            result_list[video]["like_percentage"] = int(result_list[video]["like_count"])/int(result_list[video]["view_count"]) #store like to view percentage in it
            temp_list.append(result_list[video]) #add it to the temp list
        else: 
            result_list[video]["like_percentage"] = "NULL" #if not store null

    temp_list = sorted(temp_list, key = lambda i: i['like_percentage'],reverse=True) #sort temp list by like percentage highest to lowest with lambda

    while len(temp_list) > 5: #if necessary trim temp list to have at most the top 5 results
        temp_list.pop()

    for i in range(len(temp_list)): #assign a rank to each
        temp_list[i]["rank"] = i+1

    chart2 = pd.DataFrame(temp_list) #create pandas dataframe from temp list
    chart2.drop(['video_id', 'comment_count', 'video_duration'], axis=1, inplace=True) #use .drop to remove unnecessary columns
    print(chart2)
    print("====================================================================================================================================================")
    #====================#

    #=====Analysis 3=====#
    print("Analysis 3:")
    temp_list2 = result_list #create another temp list copy of search data
    temp_list2 = sorted(temp_list2, key = lambda j: int(j['comment_count']),reverse=True) #sort by comment count highest to lowest

    while len(temp_list2) > 5: #trim to at most top 5 results
        temp_list2.pop()

    for i in range(len(temp_list2)): #assign a rank
        temp_list2[i]["rank"] = i+1

    chart3 = pd.DataFrame(temp_list2)   #create pandas dataframe
    chart3.drop(['video_id', 'video_duration', 'like_count', 'like_percentage'], axis=1, inplace=True) #remove unnecessary columns
    print(chart3)
    print("====================================================================================================================================================")
    #====================#
    
    
    