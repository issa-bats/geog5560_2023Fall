import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def subset(full_data, *col):
    """input the raw dataset and return a sub-setted dataset
    
    Parameters
    ----------
    full_data : the full dataset
    *col : variable length positional argument containing the column names          
        
    Return
    ------
            : a dataframe containing only the specified columns
    
    """
    subset_data = full_data[[*col]]
    return subset_data



def length_format(data, col, length):
    """change all the values in a specified column to a specified length
    
    Parameters
    ----------
    full_data : the full dataset
    col : a string containing the column name
    length: an integer specifying the value length
        
    Return
    ------
            : a dataframe containing the formatted column
    
    """
    rounded_data = data.copy()
    rounded_data[col] = rounded_data[col].apply(lambda x: round(x, length))
    return rounded_data



#let's run through and calculate the percent contribution from each state and
#make a dataframe using the unique values from the Trap State column and the percent_source output

def all_county(data, column):
    """calculate the percent contribution of each state to the release population across all counties
    
    Parameters
    ----------
    data : the dataset
    column: a string containing the column name
        
    Return
    ------
            : a dataframe containing the percent contributions of each state
    
    """
    trap_states = data[column].dropna().unique()
    percent_contributions = []
    
    
    
    for state in trap_states:
        state_count = len(data[data[column] == state])
        total_count = len(data[column].dropna())
        percent_source = (state_count / total_count) * 100
        percent_source = round(percent_source, 2)
        
        percent_contributions.append({"Trap State": state,
                                      "Percent Contribution":
                                      percent_source})
    
    df_contribution = pd.DataFrame(percent_contributions)
    return df_contribution





def get_each_county(data, county_col, state_col): 
    """calculate the percent contribution of each state to the release population for each county
    
    Parameters
    ----------
    data : the dataset
    county_col: a string containing the county column name
    state_col: a string containing the state column name
        
    Return
    ------
            : a dictionary containing the percent contributions of each state for every county
    
    """
    counties = data[county_col].dropna().unique()                               #list of unique values in the county col
    counties_df = {}                                                            #create empty dictionary for counties
   
    for county in counties:                                                     #for each county in the county list
        county_data = data[data[county_col]==county]                            #create a dataset for each county
        trap_states = data[state_col].dropna().unique()                         #list of unique values in the state col
        percent_contributions = []                                              #create empty list to later add percent contribution values
       
        for state in trap_states:    #for each state in the state list
            state_count = len(county_data[county_data[state_col] == state])     #count up the number of that particular state
            total_count = len(county_data[state_col].dropna())                  #count up the total number of states
            percent_source = (state_count / total_count) * 100                 #calculate the percent contribution from that state
            percent_source = round(percent_source, 2)                          #round the values to two decimal places
       
            percent_contributions.append({"Trap State": state,                  #create a dictionary that matches all the data up!
                                          "Percent Contribution":
                                          percent_source})      
       
        counties_df[county] = pd.DataFrame(percent_contributions)
   
    return counties_df                                                          #return the final list of dataframes!





def pie_county(dataframes_dict, state_col, contribution_col, county_col):
    """generate a pie graph of the demography data for each county
    
    Parameters
    ----------
    dataframes_list : a list of the county dataframes
    state_col: a string containing the state column name
    contribution_col: a string containing the percent contribution column name
    county_col: a string containing the county column name
        
    Return
    ------
            : seven pie graphs, one for each county
    
    """
    colors = ['#4D6931', '#ED7D31', '#A5A5A5', '#5B9BD5', '#9E480E',
              '#FFC000', '#02C1C6', '#264478', '#D31F4E', '#7030A0', '#70AD47']

    for county, dataframe in dataframes_dict.items():
        labels = dataframe[state_col] + " (" + dataframe[contribution_col].astype(str) + "%)"
        sizes = dataframe[contribution_col]

        fig, ax = plt.subplots(figsize=(7, 4), subplot_kw=dict(aspect="equal"))
        
        wedges, texts = ax.pie(sizes, colors=colors)

        ax.legend(wedges, labels,
                  title="States",
                  loc="center left",
                  bbox_to_anchor=(1, 0, 0.5, 1))
        

        ax.set_title(county + " County Percent Composition by State")
    
        plt.show()