#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Plotting pipelines for different kinds of csv files"""
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import numpy as np
import glob
import os
import pandas as pd
import seaborn as sns
import matplotlib.dates as mdates
#import lightplots as lp
from pandas.plotting import register_matplotlib_converters
import matplotlib
from scipy.interpolate import interp1d

register_matplotlib_converters() # converts pandas datetime from matplotlib datetime
matplotlib.rcParams['pdf.fonttype'] = 42 # ensures pdf fonts are illustratrot worthy
matplotlib.rcParams['ps.fonttype'] = 42


class Plot:
    "Plot different kinds of csv data"
    def __init__(self,set_input_folder,set_config_file="log_config.conf",set_date_string=[]):
        self.input_folder=set_input_folder
        self.config_file=set_config_file #settings about for pipeline
        self.date_string=set_date_string #dates to be analysed
    def csv_reader(self,file_name):       
        working_dir=self.input_folder
        os.chdir(working_dir)
        dfObj = pd.read_csv(file_name)
        return dfObj.copy(deep=True)
    def clean_dataframe(self,data_frame,plot_parameter="pix_dif"):
        """ Cleans data frame and adds columns based on parameter
        Input:
        plot_parameter: type =str, which paramater to clean data
        data_frame: type=pandas, dataframe object that needs to be saved
        Output 
        cleaned data frame type=pandas
        """
        dfObj=data_frame.copy()
        dfObj.rename(columns = {'Unnamed: 0':'frame'}, inplace = True)    
        if(plot_parameter=="total_count" or plot_parameter=="average_count"):
            dfObj["timestamp"] = pd.to_datetime(dfObj["timestamp"],format="%d %b %y %H:%M:%S")
        else:
            dfObj["timestamp"] = pd.to_datetime(dfObj["timestamp"],format="%Y-%m-%d %H:%M:%S")
        dfObj=dfObj.set_index("timestamp") # sets timestamp as the index
        dfObj['Year'] = dfObj.index.year
        dfObj['Month'] = dfObj.index.month
        dfObj['Day'] = dfObj.index.day
        dfObj['Hour'] = dfObj.index.hour
        dfObj['Minute'] = dfObj.index.minute
        if(plot_parameter=="motion_int"):
            dfObj[plot_parameter] = pd.to_timedelta(dfObj[plot_parameter],unit='s').dt.total_seconds()
        if(plot_parameter=="ds_moved"):
            dfObj.rename(columns = {'Unnamed: 0':'frame'}, inplace = True)    
        #resample hourly
        return dfObj.copy(deep=True)
        
    def filter_dataframe(self,data_frame,plot_parameter,filter_parameter,rwd_size=5,min_val=0,max_val=1000):
        """ Filters  data frame and adds columns based on parameter
        Input:
        plot_parameter: type = 'str', what parameter to filter by 
            [pix-dif,= pixel diferrence of succesive images
            motion_int, = motion interval between two motion events (s)
            ds_moved, = diplacement in pixels between start and end position of moth
            avg_count, average freqeuency of beam breaking events from monitor
            total_count, total frequency of beam beaking events from monitor
        filter_paramter: type = 'str' what kind of filter
            [hour, resample over an hour
            rwd averages overa a rolling window of rwd_size
                rwd_size: type = float, Size of rolling window
            min, returns filtered by some min_val
                min_val: type=float, Minimum value
            max, returns filtered by some  max_val
                max_val: type=float, Maximummum value
            average_hour
                averages over an hour
            std_hour
                returns standard deviance over an hour

        rwd_size: type = int
        min_val: type = int
        max_val: type= int
        filter_parameter= What to 
        data_frame: type=pandas, dataframe object that needs to be saved
        Output
        filtered data frame type=pandas
        """
        dfObj=data_frame.copy()
        if(filter_parameter=="hour"): #filter by hour
            df_hourly = dfObj[plot_parameter].resample('H').mean() 
            return df_hourly.copy(deep=True)
        elif(filter_parameter=="rwd"):
        # rolling window
            rolling_wd = dfObj[plot_parameter].rolling(rwd_size, center=True).mean()
            return rolling_wd
        elif(filter_parameter=="min"):
            filtered=dfObj[dfObj[plot_parameter]>=min_val] # filter by some minimum value
            return  filtered.copy(deep=True)
        elif(filter_parameter=="max"):
            filtered=dfObj[dfObj[plot_parameter]<=max_val] # filter by some minimum value
            return  filtered.copy(deep=True)

        elif(filter_parameter=="average_hour"):
            dfHour=dfObj.groupby("Hour").mean() # Standard deviation
            dfHour['Hour'] = dfHour.index
            #dfHour=dfObj.groupby(dfObj.index.hour).mean() # Average over hour
            return dfHour.copy(deep=True)
        elif(filter_parameter=="std_hour"):
            dfHour=dfObj.groupby("Hour").std() # Standard deviation
            dfHour['Hour'] = dfHour.index
            return dfHour.copy(deep=True)
   
    def plot_pixel_dif(self,data_frame,ax,graph_title="pixel difference", horiz_label="time",plot_param="pix_dif"):
        """Plots pixel_difference over entire dataset
        -- 
        Input:
        data_frame: type= pandas dataframe. Dataframe to be plotted
        ax : type=axes index, axes to plot to
        graph_title: type='str', Title of the graph
        horiz_label: type = 'str', horizontal label of graph
        plot_param: type = 'str', can change plot_param if required
        Output
        Plots a plot at the given axes
        """
        #plot_param="pix_dif"
        dfObj=data_frame.copy()
        ax.plot(dfObj.loc["2021",plot_param], marker='.', linestyle="None",color='cornflowerblue',alpha=0.5) #plot day 1
        date_form = mdates.DateFormatter("%D %H:%M") # formats date
        ax.set_title(graph_title)
        ax.set_xlabel(horiz_label)
        ax.set_ylabel(plot_param)
        #ax.xaxis.set_major_formatter(date_form)
    def plot_interval_hist(self,data_frame,ax,graph_title="Time interval", y_label="density",plot_param="motion_int",x_label="event interval (s)"):
        "Plots event interval histogram"
        plot_param="motion_int"
        dfObj=data_frame.copy()
        sns.kdeplot(data=dfObj,x=plot_param, bw_adjust=.25,ax=ax)
        ax.set_title(graph_title)
        ax.set_ylabel(y_label)
        ax.set_xlabel(x_label)

    def plot_count_hist(self,data_frame,ax,graph_title="Density by hour", horiz_label="avg_count frequency",plot_param="avg_count"):
        "Plots count data histogram averaged by hour"
        dfObj=data_frame.copy()
        sns.barplot(data=dfObj,x ='Hour',y=plot_param,ax=ax,palette="Blues")
        ax.set_title(graph_title)
        ax.set_ylabel("frequency")
        ax.set_xlabel("Hour")
    def daily(self,df,name,ylm=600):
        """Plots individual day plots traces and total count from each day
        
        Parameters
        ---- 
        df: filtered pandas dataframe that used extractCsv
        name: str, plot title, default = None
        ylm= int, ylmit for summary plots
        """
        spd = 60*60*24 #seconds per day
        tticks = np.linspace(0,spd, 5)
        tlabs = ['midnight', '6:00', 'noon', '18:00', 'midnight'] # Sets tick labels
        tlabs = ['midnight', '', 'noon', '', 'midnight']
        breakpoint()
        interp_x=[0,spd*5/24,spd*7/24,spd*17/24,spd*19/24,spd]
        interp_fx=[0.1, 0.1, 0.95, 0.95, 0.1, 0.1]
        #dinterp = interp1d([0,spd*5/24,spd*7/24,spd*17/24,spd*19/24,spd], [0.1, 0.1, 0.95, 0.95, 0.1, 0.1]) # sets up gradient for Title
        #dinterp=np.interp([0,spd*5/24,spd*7/24,spd*17/24,spd*19/24,spd], [0.1, 0.1, 0.95, 0.95, 0.1, 0.1]))
        stripres=60
        date_strings_dark = list(df["timestamp"].values)
        act_strings_dark = list(df["pix_dif"].values)
        act_hour_dark = np.zeros(24)
        dates_dark = [dt.datetime.strptime(l,"%Y-%m-%d %H:%M:%S")
                        #- dt.timedelta(hours=12) 
                        for l in date_strings_dark]
        act_dark = np.array([float(l) for l in act_strings_dark])
        #Log and normalise counts
        lact_dark = act_dark
        lact_dark -= lact_dark.min()
        lact_dark /= lact_dark.max()

        plt.figure(1, [4.5,6])
        plt.clf()
        
        days_to_plot = (dates_dark[-1] - dates_dark[0]).days + 1 # Calculates total number of days in the file to plot

        dax = plt.subplot(211)
        for i in range(len(dates_dark)):
            date = dates_dark[i]
            hour = date.hour
            if(lact_dark[i]>0):
                act_hour_dark[hour] += 1
            day = (date - dates_dark[0].replace(hour=0, minute=0,second=0)).days # days since start of trial
            x = (date - date.replace(hour=0, minute=0,second=0)).seconds # seconds since midnight
            y0 = -day*1
            y1 = y0 + lact_dark[i]
            dax.plot([x, x], [y0, y1], 'k-')
            dax.set_xticks([])
        dax.set_yticks(range(-day, 1))
        dax.set_yticklabels(range(day+1,-1,-1))
        dax.set_ylabel('day')
        dax.spines['right'].set_visible(False)
        dax.spines['top'].set_visible(False)
        dax.spines['left'].set_visible(False)
        dax.spines['bottom'].set_visible(False)

        for t in np.arange(0,spd, stripres):
            #cd = str(dinterp(t))
            #breakpoint()
            cd =str(np.interp(t,interp_x,interp_fx))
            dax.fill([t,t,t+stripres,t+stripres], [1,2,2,1], color=cd)
        dax.text(spd/2, 1.5,name, color='k', ha='center', va='center')
        ddax = plt.subplot(3,1,3)
        ddax.bar(np.arange(24), act_hour_dark, color='0.0')
        ddax.set_xticks([0, 6, 12, 18, 24])
        ddax.set_xticklabels(['midnight', '', 'noon', '', 'midnight'])
        ddax.set_ylim(0,ylm)
        ddax.set_ylabel('Activity events')
        ddax.spines['right'].set_visible(False)
        ddax.spines['top'].set_visible(False)
def cli():
    #LP=Plot("/Users/apple/Desktop/diel-light/analysis/benchmark/output")
    #ceaned_df=LP.clean_dataframe(data_frame=df,plot_parameter="pix_dif")
    #Plots pixels in min max range 
    #filtered_df=LP.filter_dataframe(data_frame=cleaned_df,plot_parameter="pix_dif",filter_parameter="min",min_val=100)
    #filtered_df=LP.filter_dataframe(data_frame=filtered_df,plot_parameter="pix_dif",filter_parameter="max",max_val=1000)
    #LP.plot_pixel_dif(filtered_df)
    
    #All
    # fig, ax = plt.subplots(1,1,sharey=True,figsize =(8,5))
    # LP=Plot("/Users/apple/Desktop/diel-light/raw_data_hdd_wd/output")
    # df=LP.csv_reader("test.csv")
    # cleaned_df=LP.clean_dataframe(data_frame=df,plot_parameter="pix_dif")
    # filtered_df=LP.filter_dataframe(data_frame=cleaned_df,plot_parameter="pix_dif",filter_parameter="min",min_val=100)
    # filtered_df=LP.filter_dataframe(data_frame=filtered_df,plot_parameter="pix_dif",filter_parameter="max",max_val=1000)
    # LP.plot_pixel_dif(data_frame=filtered_df,ax=ax,graph_title="test")
    
    
    """
    ###Plots no_lp cage data using fft

    LP=Plot("/Users/apple/Desktop/diel-light/analysis/light_pollution")
    df_lp=LP.csv_reader("nolp_cage.csv")
    cleaned_df=LP.clean_dataframe(data_frame=df_lp,plot_parameter="pix_dif")
    filtered_df=LP.filter_dataframe(data_frame=cleaned_df,plot_parameter="pix_dif",filter_parameter="max",max_val=5000)
    #TODO convert function to resample by hour
    f_df=filtered_df["pix_dif"].resample('H').mean().replace(np.nan,0) 
    signal=f_df
    thresh=signal>200   
    signal=thresh.astype(float)
    pixdif=np.fft.fft(signal)
    pixdif_psd=np.abs(pixdif) ** 2
    size=len(f_df)
    freq=np.fft.fftfreq(n=size,d=1/24)
    i = freq>0
    fig, ax = plt.subplots(1, 1, figsize=(8, 4))
    ax.plot(freq[i], pixdif_psd[i])
    ax.set_xlabel('Frequency hourly')
    ax.set_ylabel('pix dif')
    plt.semilogx()
    plt.semilogy()
    plt.show()"""
    

    #df_nplp=LP.csv_reader("nolp_cage.csv")

    #LP.plot_pixel_dif(data_frame=cleaned_df,ax=ax[0],graph_title="test")
    #plt.show()
    #Plot histogram of motion_interval
    
    
    #Plots benchmarks
    
    ###Plots benchmarks
    LP=Plot("/Users/apple/Desktop/diel-light/analysis/benchmark/output")
    #Plot 1
    fig, ax = plt.subplots(1,2,sharey=True,figsize =(8,5))
    df=LP.csv_reader("07_length_550.csv")
    cleaned_df=LP.clean_dataframe(data_frame=df,plot_parameter="motion_int")
    LP.plot_interval_hist(cleaned_df,ax=ax[1],graph_title="7 mm")
    

    #csvlist=["07_combined.csv","10_combined.csv","14_combined.csv"]
    # df=LP.csv_reader("07_combined.csv")
    # cleaned_df=LP.clean_dataframe(data_frame=df,plot_parameter="motion_int")
    # LP.plot_interval_hist(cleaned_df,ax=ax[0],graph_title="7 mm")
    # PLOT 2
    # df2=LP.csv_reader("10_combined.csv")
    # cleaned_df2=LP.clean_dataframe(data_frame=df2,plot_parameter="motion_int")
    # LP.plot_interval_hist(cleaned_df2,ax=ax[1],graph_title="10 mm")
    #PLOT 3
    # df3=LP.csv_reader("14_combined.csv")
    # cleaned_df3=LP.clean_dataframe(data_frame=df3,plot_parameter="motion_int")
    # LP.plot_interval_hist(cleaned_df3,ax=ax[2],graph_title="14 mm")
    plt.show()


# This is the standard boilerplate that calls the cli() function if called using the script name
if __name__ == '__main__':
  cli()
    
# plots and save functions for different datasets
#filtered=LP.filter_dataframe(data_frame=cleaned_df,plot_parameter="pix_dif",filter_parameter="hour")

                    


