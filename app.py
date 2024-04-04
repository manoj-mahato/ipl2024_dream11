# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 13:14:17 2024

@author: Manoj
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

from preprocessing import PreProcessing
from plot import PlotPlotly

def main():
    st.set_page_config(page_title='ipl24_dream11',page_icon=':tada:', layout='wide')
    st.title("IPL 2024: Dream11 group statistics")
    #st.write("Hello, world!")
    
    match_df = pd.read_excel("F:\\ipl2024\\contest.xlsx")
    member_df = pd.read_excel("F:\\ipl2024\\contestent.xlsx")
    
    pre_obj = PreProcessing()
    plot_obj = PlotPlotly()
    
    member_temp, groupped_df, merged_net, groupped_net = pre_obj.main_processing(match_df,member_df)
    
    fig1 = plot_obj.net_winning(groupped_net)
    fig2 = plot_obj.gross_total(groupped_df)
    fig3 = plot_obj.gross_total_with_granular(member_temp)
    fig5 = plot_obj.commission_check(groupped_net)
    
    def display_plot(plot_choice):
        if plot_choice == 'Net winning amount per participant':
            st.plotly_chart(fig1, use_container_width=True)
        elif plot_choice == 'Gross winning amount per participant and match count':
            st.plotly_chart(fig2, use_container_width=True)
        elif plot_choice == 'Gross winning with each win amount per participant':
            st.plotly_chart(fig3, use_container_width=True)
   
    with st.container():
        st.write("---")
        left_column, right_column = st.columns(2)
        with left_column:            
            plot_choice = st.selectbox('Select Plot', ('Net winning amount per participant',
                                                       'Gross winning amount per participant and match count',
                                                       'Gross winning with each win amount per participant'))
            display_plot(plot_choice)
        with right_column:
            st.write("### Net winning amount for all vs commission till now")
            st.plotly_chart(fig5,use_container_width=True)
            
    st.write('---')
    st.write('#### Net amount trend of participant(s)')
    # Function to generate line plot for selected participants
    def generate_line_plot(selected_participants):
        fig = go.Figure()
    
        for participant in selected_participants:
            filtered_df = merged_net[merged_net['Member_name'] == participant]
            filtered_df['Cum_sum'] = filtered_df['Net_winning'].cumsum()
            fig.add_trace(go.Scatter(x=filtered_df['Match_no'], y=filtered_df['Cum_sum'],
                                     mode='lines+markers', name=participant))
    
        fig.update_layout(xaxis_title='Match no', yaxis_title='Net amount')
        fig.update_layout(xaxis=dict(tickvals=merged_net['Match_no']))
        fig.add_hline(y=0, line_width=0.5, line_color='red')
        st.plotly_chart(fig)
        
    participants = merged_net['Member_name'].unique()

    # Dropdown menu to select participants (multiple)
    selected_participants = st.multiselect('Select Participant(s)', participants, default=participants[0])

    # Generate line plot for selected participants
    generate_line_plot(selected_participants)
    

    
if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        st.write(str(e))
    
