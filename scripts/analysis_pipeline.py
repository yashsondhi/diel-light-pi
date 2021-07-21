import argparse
from log_pipeline import Log
from plot_pipeline import Plot
import matplotlib.pyplot as plt
import yaml
####Chaining pipeline for cleaning, data, plotting parameters etc.
# Example of usage python analysis.py --mode first --folder "/Users/apple/Desktop/diel-light/raw_data_hdd_wd/output" --out test --usecsv True --csvlist "/Users/apple/Desktop/diel-light/raw_data_hdd_wd/output/test.csv" --plot True
# Example to extract specific file python analysis.py --mode first --folder "/Users/apple/Desktop/diel-light/analysis/light_pollution/3-27-30" --treatment lp_cage --out lp --extract
# Example to plot extracted csv file or files python3 ~/Desktop/diel-light/diel-scripts/analysis.py --mode first --folder /Users/apple/Desktop/diel-light/analysis/light_pollution/4-9-30/output --treatment test_lp --out lp_cage_test --plot --usecsv --csvlist lp_cage_test.csv
# Example to extract old field data getting only first frames and event duration from log files:python3 analysis.py --mode first-field --folder "/Users/apple/Desktop/diel-light/analysis/field-data/T_clotho" --treatment log --out t_clotho_all --extract
def run_mode_first(folder,treatment,out):
    """ Saves dataframe as csv or specified filetype using treatment
        -- 
        Input:
        folder: type : str, path to folder with log files
        set_treatment: type=str, set search string to filter log files by.
        out: type =str, output file name
        Output
        Returns filename of combined file or relative path to combined files in the specified folder
        """
    log = Log(folder)
    print(folder)
    log=Log(folder)
    output=log.combine(filetype="txt",set_treatment=treatment,treatment=True)
    df=log.extractCsv(output,conf_type="first")
    output_path=log.save_df(data_frame=df,output_file_name=out,output_to_folder=True)
    return output_path
def first_plotter_pd(folder,infile,param="pix_dif",min_val=100,max_val=1000,plot_title="",outfile_descriptor=""):
    """ Plots dataframe for parameter pixel diference over all days : TODO: make other functions for different plotters
        -- 
        Input:
        folder: type : str, path to folder with csv files
        infile: input dataframe, or list of dataframes
        param: parameter to be plotted
        min_val: type : int filter pixel difference min val
        max_val : type : int filter pixel difference max value
        plot_title: type: str, Plot title string
        outfile_descriptor: type: str, Output plot inclutes descriptor in file name
        Output
        Plots required dataframes
        """
    no_of_plots=len(infile)
    fig, ax = plt.subplots(1,no_of_plots,sharey=True,figsize =(8,5))
    PP=Plot(folder)
    i=0
    for name in infile:
        print(name)
        df=PP.csv_reader(name)
        ## Specially for pix_dif all put this in a different function
        cleaned_df=PP.clean_dataframe(data_frame=df,plot_parameter=param)
        filtered_df=PP.filter_dataframe(data_frame=cleaned_df,plot_parameter=param,filter_parameter="min",min_val=100)
        filtered_df=PP.filter_dataframe(data_frame=filtered_df,plot_parameter=param,filter_parameter="max",max_val=1000)
        if(no_of_plots<=1):
            PP.plot_pixel_dif(data_frame=filtered_df,ax=ax,graph_title=plot_title)
        elif(no_of_plots>1):
            PP.plot_pixel_dif(data_frame=filtered_df,ax=ax[i],graph_title=plot_title)
            i=i+1     
    plt.savefig((param+"_"+outfile_descriptor+".pdf"))

def first_plotter_pd_hist(folder,infile,param="pix_dif",min_val=100,max_val=1000,no_of_plots=1,outfile_descriptor="",plot_title=""):
    """ Plots dataframe for parameter pixel difference with histogram and averaged by hour
        Input:
        folder: type : str, path to folder with csv files
        infile: input dataframe
        param: parameter to be plotted
        min_val: type : int filter pixel difference min val
        max_val : type : int filter pixel difference max value
        no_of_plots: type : int , 1: Only hist, 2 hist + daily counts TODO: Add more options
        plot_title: type: str, Plot title string
        outfile_descriptor: type: str, Output plot inclutes descriptor in file name
        Output
        Plots required dataframes
        """
    no_of_plots=2
    fig, ax = plt.subplots(no_of_plots,1,sharey=False,figsize =(9,6))
    PP=Plot(folder)
    i=0
    for name in infile:
        print(name)
        df=PP.csv_reader(name)
        ## Specially for pix_dif all put this in a different function
        cleaned_df=PP.clean_dataframe(data_frame=df,plot_parameter=param)
        filtered_df=PP.filter_dataframe(data_frame=cleaned_df,plot_parameter=param,filter_parameter="min",min_val=100)
        filtered_df=PP.filter_dataframe(data_frame=filtered_df,plot_parameter=param,filter_parameter="max",max_val=5000)
        filtered_hour=PP.filter_dataframe(cleaned_df,plot_parameter="pix_dif",filter_parameter="average_hour")
        #standard deviation takes over all values.
        if(no_of_plots==1):
            PP.plot_count_hist(filtered_hour,ax=ax,graph_title=plot_title)
        elif(no_of_plots==2):
            PP.plot_count_hist(filtered_hour,ax=ax[i],graph_title=plot_title,plot_param="pix_dif")
            i=i+1
            PP.plot_pixel_dif(data_frame=filtered_df,ax=ax[i],graph_title="")

    plt.savefig((param+"_hist_"+outfile_descriptor+".pdf"))
#plt.show()
#plt.show()
        

def first_plotter_mi(folder,infile,param="motion_int",plot_title="",outfile_descriptor=""):
    """ Plots dataframe for parameter motion_int frequency distribution over all days : 
        -- 
        Input:
        folder: type : str, path to folder with csv files
        infile: input dataframe, or list of dataframes
        param: parameter to be plotted
        min_val: type : int filter pixel difference min val
        max_val : type : int filter pixel difference max value
        graph_title: type: str, Plot title string
        outfile_descriptor: type: str, Output plot inclutes descriptor in file name
        
        Output
        Plots required dataframes
        """
    no_of_plots=len(infile)
    fig, ax = plt.subplots(1,no_of_plots,sharey=True,figsize =(8,5))
    LP=Plot(folder)
    i=0
    for name in infile:
        print(name)
        df=LP.csv_reader(name)
        ## Specially for pix_dif all put this in a different function
        cleaned_df=LP.clean_dataframe(data_frame=df,plot_parameter=param)
        if(no_of_plots<=1):
            LP.plot_interval_hist(cleaned_df,ax=ax,graph_title=plot_title)
        elif(no_of_plots>1):
            LP.plot_interval_hist(cleaned_df,ax=ax[i],graph_title=plot_title)
            i=i+1
    plt.savefig((param+"_dist_"+outfile_descriptor+".pdf"))
    
def benchmark(folder,infile,param="motion_int",graph_title="benchmark"):
    """ Plots dataframe for parameter motion_int over list of benchmark csv files : 
        -- 
        Input:
        folder: type : str, path to folder with csv files
        infile: input dataframe, or list of dataframes
        param: parameter to be plotted
        Output
        Plots required dataframes
        """
    no_of_plots=len(infile)
    if(no_of_plots<=4):
        fig, ax = plt.subplots(1,no_of_plots,sharey=True,figsize =(8,5))
    elif(no_of_plots>4):
        col=int((no_of_plots+1)/3)
        fig, ax = plt.subplots(3,col,sharex=True,sharey=True,figsize =(12,9))
    LP=Plot(folder)
    i=0
    for name in infile:
        print(name)
        df=LP.csv_reader(name)
        ## Specially for pix_dif all put this in a different function
        cleaned_df=LP.clean_dataframe(data_frame=df,plot_parameter=param)
        if(no_of_plots<=1):
            LP.plot_interval_hist(cleaned_df,ax=ax,graph_title=name[:-4])
        elif(no_of_plots>1):
            r=int(i/3)
            c=int(i%3)
            LP.plot_interval_hist(cleaned_df,ax=ax[r,c],graph_title=name[:-4],x_label=None,y_label=None)
            i=i+1

    plt.savefig((param+"_"+"benchmark_summary"+".pdf"))
def daily_plotter(folder,infile,param="pix_dif",descriptor="",use_filter=False,filter_max=2000,filter_min=100,ylm=200):
    """ Plots dataframe for daily plots with summary using JT code: 
        -- 
        Input:
        folder: type : str, path to folder with csv files
        infile: input dataframe, or list of dataframes
        param: parameter to be plotted
        filter_max: float, max_value of pixel difference
        filter_min: float, min_value of pixel difference
        Output
        Plots required dataframes
        """
    PP=Plot(folder)
    
    for name in infile:
        print(name)
        df=PP.csv_reader(name)
        if(use_filter):
            df=PP.filter_dataframe(data_frame=df,plot_parameter="pix_dif",filter_parameter="max",max_val=2000)
            df=PP.filter_dataframe(data_frame=df,plot_parameter="pix_dif",filter_parameter="max",max_val=2000)
        
        ## Specially for pix_dif all put this in a different function
        PP.daily(df=df,name=descriptor,ylm=ylm)
        plt.savefig(name.replace(".csv",("daily_"+descriptor+".pdf")))
def run_mode_extract_all_field(folder,treatment,out):
    """ Saves dataframe as csv or specified filetype using treatment for log files all
        -- 
        Input:
        folder: type : str, path to folder with log files
        set_treatment: type=str, set search string to filter log files by.
        out: type =str, output file name
        Output
        Returns filename of combined file or relative path to combined files in the specified folder
        """
    log = Log(folder)
    print(folder)
    log=Log(folder)
    output=log.combine(filetype="txt",set_treatment=treatment,treatment=True)
    df=log.extractCsv(output,conf_type="all-field")
    output_path=log.save_df(data_frame=df,output_file_name=out,output_to_folder=True)
    return output_path
def run_mode_extract_first_field(folder,treatment,out):
    """ Saves dataframe as csv or specified filetype using treatment for log files first
        -- 
        Input:
        folder: type : str, path to folder with log files
        set_treatment: type=str, set search string to filter log files by.
        out: type =str, output file name
        Output
        Returns filename of combined file or relative path to combined files in the specified folder
        """
    log = Log(folder)
    print(folder)
    log=Log(folder)
    output=log.combine(filetype="txt",set_treatment=treatment,treatment=True)
    df=log.extractCsv(output,conf_type="first-field")
    output_path=log.save_df(data_frame=df,output_file_name=out,output_to_folder=True)
    return output_path

def run_mode_grid():
    pass
def get_args():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder',default=False,help="path to folder with data files to be analysed")
    parser.add_argument('--mode', type=str, default='first',
                        choices=['first', 'grid','all-field',"first-field"],help=
                        "first: gets log files which saved only first image of motion \
                        grid: Not yet defined\
                        all-field: gets all images from log files of field data w/o pixel difference \
                        first-field: gets first image and start and end duration from log files field data without pix differnce    ")
    parser.add_argument('--treatment',default=False,help='Use options like cage,inc,log-file-header etc, default= False')
    #parser.add_argument('--analyse',default=False,action='store_true', help="plots different kinds of plots")
    parser.add_argument('--usecsv',default=False, action='store_true', help="use list of csv files to be plotted")
    parser.add_argument('--extract',default=False,action='store_true', help="extracts csv")
    parser.add_argument('--outpath',default=False, help="output file path")
    parser.add_argument('--out',default=False,help="output file name")
    #parser.add_argument('--plot_test',default=False,action='store_true',help="calls plotter for respective outfile, change code of plot for various plots")
    parser.add_argument('--plot_all',default=False,action='store_true',help="calls daily_ plotter for respective outfile with plots for each day and sumarry of counts using parameters in configuration file")
    parser.add_argument('--conf', default='../diel-light-pi/configs/analysis.conf', help='Path to config file to open for analysis parameteers')
    parser.add_argument('--logfile', default='log_analysis.txt', help='Log file to write analysis logs to')
    
    args = parser.parse_args()
    return (args)
#Create config file


def main():
    """Main function of the script"""
    args=get_args()
    # Input project metadata
    with open(args.conf) as yamlfile:
        config = yaml.load(yamlfile, Loader=yaml.FullLoader)
    # Input folder name
    if args.folder:
        folder = args.folder
    else:
        folder=config["INPUT_PATH"]
    # Input analysis mode
    if args.mode:
        mode = args.mode
    else:
        mode=config["MODE"]
    #treatment for combining file types 
    if args.treatment:
        treatment = args.treatment
    else:
        treatment=config["TREATMENT"]
    #sets output path for plots 
    if args.outpath:
        out_path=args.outpath
    else:
        out_path=config["OUTPATH"]
    # sets output file name
    if args.out:
        outfile=args.out
    else:
        outfile=config["OUTFILENAME"]

    #Set csv file to use

    if args.usecsv:  
        csv_path = [config["CSVFILE"]]
    else:
        #defaults output path
        csv_path=[outfile+".csv"]
    
    if config["USE_FILTER"]:
        use_filter_val=config["USE_FILTER"]
        filter_max_val=config["FILTER_MAX"]
        filter_min_val=config["FILTER_MIN"]
    else:
        use_filter_val=False
        filter_max_val=10000
        filter_min_val=100
    
    # reads csv list in a txt file
    extract=args.extract
    analysis_log=args.logfile
    #plot_test = args.plot_test
    plot_all = args.plot_all

    #... other args ... #
    if mode == 'first':
        if extract:
            #Add logging
            csv_path=run_mode_first(folder,treatment,outfile) 
        if plot_all :
            folder=folder+"/"+out_path
            #reads plot title from config file othersiwe sets default plot title
            if config["PLOT_TITLE"]:
                plot_title_val=config["PLOT_TITLE"]
            else:
                plot_title_val=outfile #default
            #reads ylim for summary plot from config file otherwise sets default  ylim
            if config["YLIM"]:
                ylim_val=config["YLIM"]
            else:
                ylim_val=600 #default
    
            daily_plotter(folder,csv_path,use_filter=use_filter_val,descriptor=plot_title_val,filter_max=filter_max_val,filter_min=filter_min_val,ylm=ylim_val)
            #benchmark(folder,csv_path,"motion_int")

    elif mode == "all-field":
        if(extract):
            csv_path=run_mode_extract_all_field(folder,treatment,outfile)
    elif mode == "first-field":
        if(extract):
            csv_path=run_mode_extract_first_field(folder,treatment,outfile)
    else:
        run_mode_grid()

if __name__ == "__main__":
    main()