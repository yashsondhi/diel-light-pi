#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon 22 March 12:04:43 2021

@author: yashsondhi
Creates class for Log file manipulation

"""
import os
import glob
import re
import numpy as np
import pandas as pd
import datetime as dt
import timeit
import linecache


class Log:
    "Class with functions to manipulate log files"
    def __init__(self,set_input_folder):
        self.input_folder= set_input_folder #path to input folder with log files
        
    def combine(self,treatment=False,set_treatment="",filetype="txt",output_to_folder=False,output_folder_name="output"):
        """combines all log files in input folder based on a search criterion.
        
        ---
        Combines all txt files in a the working directory that fit a search criteria. Ignores previusly created combined files and overwrites them
        Inputs:
        set_treatment: type=str, set search string to filter log files by.
        filetype: type=str, sets file_type of file
        output_to_folder: type=boolean, save to a new folder, if true, file_name specifies an output folder including name
        output_folder_name: type =str, output folder name

        Output
        Returns
        filename of combined file or relative path to combined files in the specified folder
        """
        path=self.input_folder # Stores path to working directory
        os.chdir(path)   # changes path to working directory
        combined_list=[]  # creates an emty combined list for file names
        if(set_treatment!= ""): 
            set_treatment_name=set_treatment+"_" # if a treatment has been specified filters files based on treatment
        out_file="combined"+"_"+set_treatment_name+"log.txt" # name of outfile
        
        for filename in sorted(glob.glob(path+"/**/*."+filetype,recursive=True)): # Walks recursively through all the files that match filetype in the folder
            if(not "combined" in filename): # ignores previosuly combined text files
                if(treatment):
                    if(set_treatment in filename):
                        print(filename)
                        combined_list.append(filename)
                elif(not treatment):
                    if(filename!=out_file):
                        combined_list.append(filename)
        if(not output_to_folder): # Stores outputs in the same working directory
            with open(out_file,"w+") as combined:
                for names in combined_list:
                    with open(names,"r") as infile:
                        combined.write(infile.read())
        elif(output_to_folder): # Stores outputs in a specified output folder
            if not os.path.exists(output_folder_name):
                os.makedirs(output_folder_name)
                out_path=path+"/"+output_folder_name
            out_file="combined"+"_"+set_treatment_name+"log.txt" # name of outfile
            with open(out_path+"/"+out_file,"w+") as combined: #Creates a new file and overwrites old combined files
                for names in combined_list: # opens each filename that match treatment 
                    with open(names,"r") as infile: 
                        combined.write(infile.read()) # writes each file to new file
            out_file=out_path+"/"+out_file                           
        return out_file # returns outfile name or path to outfile
    def extract_motion_version(self,file_path):
        "takes a log file and extracts motion version"
        with open(file_path, 'r') as file:
            first_line = file.readline()
            version_string = first_line.strip()
            start_index = version_string.find("Motion") + len("Motion")
            end_index = version_string.find("Started", start_index)
            version = version_string[start_index:end_index].strip()
            return version    
    def extractCsv(self,infile,conf_type="first"):
        """takes a log file and extracts parameters to csv file.
        ___
        Inputs:
        infile:type str, input file name
        conf_type: str, kind of config file used, 
            first = Stores timestamp of image, pix difference and time in seconds of motion event
            all = Stores timestamp of all images and pizel difference
        
        returns
        Copy of a pandas dataframe with differnet columns, depending on conf_type

        """
        path=self.input_folder
        os.chdir(path)
        mv=self.extract_motion_version(infile) # extracts motion version
        dfObj = pd.DataFrame(columns=['timestamp', 'pix_dif'])
        with open (infile, 'rt') as myfile:
            if(conf_type=="all"):
                #takes all frames and gives pixel difference and timestamps 
                pattern = re.compile(".jpg", re.IGNORECASE)
                data_list=[] # Creates empty list to store required lines
                for linenum,line in enumerate(myfile):
                    if (pattern.search(line) != None):
                        # If a match is found 
                        #temp=linecache.getline(myfile,linenum+1).rstrip('\n')
                        data_list.append(line.rstrip('\n'))
                time_stamp_arr=np.zeros(len(data_list),dtype="O")
                pix_diff_arr=np.zeros(len(data_list),dtype=np.float64)   
                for counter,jpg in enumerate(data_list):                            # Iterate over the list of tuples
                    string = str(jpg)
                    if string.endswith('.jpg'):
                        string = string[:-4]
                    if(float(mv[:-2])>=4.5):
                        date_time_str = string[78:92]
                        pix_dif = string[96:]
                    elif(float(mv[:-2])<=4.5):
                        date_time_str = string[80:94]
                        pix_dif = string[98:]
                    date_time_obj = dt.datetime.strptime(date_time_str, '%Y%m%d%H%M%S')
                    time_stamp_arr[counter]=date_time_obj # saves time stamp
                    pix_diff_arr[counter]=float(pix_dif) # casts pixel difference as a float
                dfObj["timestamp"]=time_stamp_arr
                dfObj["pix_dif"]=pix_diff_arr
            elif(conf_type=="first"):
                #takes first frame and gives timestamp of start of event,pixel difference and time to end of event
                pattern_start= re.compile(".jpg", re.IGNORECASE)
                pattern_end =re.compile("End of event", re.IGNORECASE)
                data_list=[] # type list
                for linenum,line in enumerate(myfile):
                    if (pattern_start.search(line) != None):      # If a match is found 
                        motion_start=linecache.getline(infile,linenum).rstrip("\n") # gets motion start
                        picture_line=linecache.getline(infile,linenum+1).rstrip("\n") # gets picture
                        motion_end=linecache.getline(infile,linenum+2).rstrip("\n") # Gets motion end
                        if(pattern_end.search(motion_end) != None):
                            data_list.append((motion_start,picture_line,motion_end)) # checks if motion end has "End of event" and save
                        else:
                            print(motion_end,"Check input log format, use all instead for less stringent procesing")
                            break
                dfObj = pd.DataFrame(columns=['timestamp', 'pix_dif',"motion_int"])
                time_stamp_arr=np.zeros(len(data_list),dtype="O") # Creates an array for storing timestamp
                pix_diff_arr=np.zeros(len(data_list),dtype=np.float64)   # Creates empy array for storing pixel difference
                motion_int_arr=np.zeros(len(data_list),dtype="O") # Creates empy array for storing duration of motion
                for counter,jpg in enumerate(data_list):                            # Iterate over the list of tuples
                    string = str(jpg[1])
                    if string.endswith('.jpg'):
                        string = string[:-4]
                    motion_end=str(jpg[2])[21:36] # Saves start and end time
                    motion_start=str(jpg[0])[21:36]
                    FMT = '%b %d %H:%M:%S' # Format for motion, start and end
                    tdelta = dt.datetime.strptime(motion_end, FMT) - dt.datetime.strptime(motion_start, FMT) #calculates length of motion bout
                    date_time_str = string[80:94]
                    pix_dif = string[98:]
                    date_time_obj = dt.datetime.strptime(date_time_str, '%Y%m%d%H%M%S')
                    time_stamp_arr[counter]=date_time_obj # saves time stamp
                    pix_diff_arr[counter]=float(pix_dif) # casts pixel difference as a float
                    motion_int_arr[counter]=tdelta
                dfObj["timestamp"]=time_stamp_arr # appends numpy arrays into the dataframe
                dfObj["pix_dif"]=pix_diff_arr
                dfObj["motion_int"]=motion_int_arr
                
            elif (conf_type=="all-field"):
            #takes all frames and gives image num
                pattern = re.compile(".jpg", re.IGNORECASE)
                data_list=[] # Creates empty list to store required lines
                for linenum,line in enumerate(myfile):
                    if (pattern.search(line) != None):
                        # If a match is found 
                        #temp=linecache.getline(myfile,linenum+1).rstrip('\n')
                        data_list.append(line.rstrip('\n'))
                time_stamp_arr=np.zeros(len(data_list),dtype="O")
                pix_diff_arr=np.zeros(len(data_list),dtype="O")
                img_num_arr=np.zeros(len(data_list),dtype=np.float64)   
                for counter,jpg in enumerate(data_list):                            # Iterate over the list of tuples
                    string = str(jpg)
                    if string.endswith('.jpg'):
                        string = string[:-4]
                    date_time_str = string[80:94]
                    img_num=string[95:]
                    pix_dif = string[98:]
                    date_time_obj = dt.datetime.strptime(date_time_str, '%Y%m%d%H%M%S')
                    time_stamp_arr[counter]=date_time_obj # saves time stamp
                    if(len(pix_dif)<1): # checks for empty
                        pix_diff_arr[counter]= "n/a"
                    else:
                        pix_diff_arr[counter]= pix-dif
                    img_num_arr[counter]=int(img_num)
                dfObj["timestamp"]=time_stamp_arr
                dfObj["img_num"]=img_num_arr
                dfObj["pix_dif"]=pix_diff_arr
            elif (conf_type=="first-field"):
            #takes all frames and gives start and end of event and event num 
                pattern_start= re.compile("motion_detected: Motion detected", re.IGNORECASE)
                pattern_end =re.compile("End of event", re.IGNORECASE)
                data_list=[] # type list
                for linenum,line in enumerate(myfile):
                    if (pattern_start.search(line) != None):
                          # If a match is found 
                        motion_start=linecache.getline(infile,linenum+1).rstrip("\n") # gets motion start
                        picture_line=linecache.getline(infile,linenum+2).rstrip("\n") # gets picture
                        i=linenum+1#current line number reset counter
                        while True:
                            #current linue 
                            current_line=linecache.getline(infile,i).rstrip("\n")
                            pic_previous=   linecache.getline(infile,i-2).rstrip("\n")
                            if(pattern_end.search(current_line) != None):
                                data_list.append((motion_start,picture_line,current_line,pic_previous))
                                break # checks if motion end has "End of event" and save
                            else:
                                i=i+1
                        else:
                            print(motion_end,"Check input log format, use all instead for less stringent procesing")
                            break
                dfObj = pd.DataFrame(columns=['timestamp', 'pix_dif',"motion_int","img_name","event_num","motion_man"])
                time_stamp_arr=np.zeros(len(data_list),dtype="O") # Creates an array for storing timestamp
                pix_diff_arr=np.zeros(len(data_list),dtype="O")   # Creates empy array for storing pixel difference
                motion_int_arr=np.zeros(len(data_list),dtype="O")# Creates empy array for storing duration of motion
                image_name_arr=np.zeros(len(data_list),dtype="O") # Creates empy array for storing image name
                event_num_arr=np.zeros(len(data_list),dtype="O") # Creates empy array for storing event index
                motion_man_arr=np.zeros(len(data_list),dtype="O") # Creates empy array for storing whether motion occured
                for counter,jpg in enumerate(data_list):                            # Iterate over the list of tuples
                    
                    string = str(jpg[1])
                    if string.endswith('.jpg'):
                        string = string[:-4]
                    motion_end=str(jpg[2])[21:36] # Saves start and end time
                    motion_start=str(jpg[0])[21:36]
                    img_name=string[80:]
                    event_num=(jpg[2].split(" "))[-1]
                    #breakpoint()
                    FMT = '%b %d %H:%M:%S' # Format for motion, start and end
                    tdelta = dt.datetime.strptime(motion_end, FMT) - dt.datetime.strptime(motion_start, FMT) #calculates length of motion bout
                    motion_man="get_from_user"
                    if(tdelta.total_seconds()>2):
                        motion_man="1"
                        img_name=(jpg[3])[80:-4]
                    
                    date_time_str = string[80:94]
                    #pix_dif = string[98:]
                    date_time_obj = dt.datetime.strptime(date_time_str, '%Y%m%d%H%M%S')
                    time_stamp_arr[counter]=date_time_obj # saves time stamp
                    pix_diff_arr[counter]="get_from_image" # casts pixel difference as a float #TODO get pixel extractor script here using image_name
                    motion_int_arr[counter]=tdelta
                    image_name_arr[counter]=img_name
                    event_num_arr[counter]=event_num
                    motion_man_arr[counter]=motion_man #TODO get pixel extractor script here using image_name
                dfObj["timestamp"]=time_stamp_arr # appends numpy arrays into the dataframe
                dfObj["pix_dif"]=pix_diff_arr
                dfObj["motion_int"]=motion_int_arr
                dfObj["img_name"]=image_name_arr
                dfObj["event_num"]=event_num_arr
                dfObj["motion_man"]=motion_man_arr
                ###break
            return dfObj.copy(deep=True)
            
    def save_df(self,data_frame,output_file_name="extracted_data.csv",filetype="csv",output_to_folder=False,output_folder_name="output"):
        """ Saves dataframe as csv or spedcified filetype
        -- 
        Input:
        data_frame: type=pandas, dataframe object that needs to be saved
        output_file_name: type=str, name of file
        filetype: type=str, kind of file to save, default = csv
        output_to_folder: type=boolean, save to a new folder, if true, file_name specifies an output folder including name
        output_folder_name: type =str, output folder name
        Output
        Returns filename of combined file or relative path to combined files in the specified folder
        """
        path=self.input_folder
        if(not output_to_folder):
            data_frame.to_csv(output_file_name+".csv")
            output_file_name=output_file_name+".csv"# saves output file name
        elif(output_to_folder):
            if not os.path.exists(output_folder_name):
                os.makedirs(output_folder_name) # Creates output directory if it doe not exist
            output_folder_path=path+"/"+output_folder_name
            output_file_path=output_folder_path+"/"+output_file_name
            data_frame.to_csv(output_file_path+".csv") 
            output_file_name=output_file_path+".csv" # saves output path and filename
        return output_file_name
    



# Define a cli() function that prints what we need .
def cli():
    #UNIT CASE 1
    #log=Log("/Users/apple/Desktop/diel-light/analysis/benchmark")
    #output=log.combine(filetype="txt",set_treatment="14",treatment=True)
    #df=log.extractCsv(output,conf_type="first")
    #x=log.save_df(data_frame=df,output_file_name="14_combined",output_to_folder=True)
    
    #Analysis of folder with all data 
    log=Log("/Users/apple/Desktop/diel-light/raw_data_hdd_wd")
    output=log.combine(filetype="txt",set_treatment="cage",treatment=True)
    df=log.extractCsv(output,conf_type="first")
    x=log.save_df(data_frame=df,output_file_name="cage",output_to_folder=True)
    
    

# This is the standard boilerplate that calls the cli() function if called using the script name
if __name__ == '__main__':
  cli()
    
