# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 13:14:17 2024

@author: Manoj
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")
import cv2

from preprocessing import PreProcessing
from plot import PlotPlotly
from upload_data import UploadData


def main():
    st.set_page_config(page_title='ipl24_dream11',page_icon=':tada:', layout='wide')
    selected = option_menu(menu_title=None,
                           options=["Home","Upload Data"],
                           icons=['house','box-arrow-in-up'],
                           default_index=0,
                           orientation="horizontal")
    
    pre_obj = PreProcessing()
    plot_obj = PlotPlotly()
    upload_obj = UploadData()
    
    match_df = pd.read_excel("./data/contest.xlsx")
    member_df = pd.read_excel("./data/contestent.xlsx")

    if selected == "Home":
        
        st.title("IPL 2024: Dream11 group statistics")
        
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
        participants = merged_net['Member_name'].unique()   
        # Dropdown menu to select participants (multiple)
        selected_participants = st.multiselect('Select Participant(s)', participants, default=participants[0], key='net_amount')
        fig4 = plot_obj.generate_line_plot(merged_net, selected_participants)
        st.plotly_chart(fig4)
        st.write('---')
        st.write('#### Rank trend of participant(s) with no of participant')
        selected_participants2 = st.multiselect('Select Participant(s)', participants, default=participants[0], key='rank')
        fig6 = plot_obj.participant_rank_trend(merged_net, selected_participants2)
        st.plotly_chart(fig6)

        
    if selected == "Upload Data":
        with st.container():
            left_column, right_column = st.columns(2)
            with left_column: 
                all_teams = ['Chennai', 'Punjab', 'Kolkata', 'Rajasthan', 'Gujarat',
                             'Bangalore', 'Hyderabad', 'Lucknow', 'Delhi', 'Mumbai']
                
                st.write('##### Fill Match and contest details:')
                last_updated_match = match_df['Match_no'].max()
                last_team1 = match_df[match_df['Match_no']==last_updated_match]['Team1'].item()
                last_team2 = match_df[match_df['Match_no']==last_updated_match]['Team2'].item()
                last_winner = match_df[match_df['Match_no']==last_updated_match]['Winner'].item()
                st.write(f"""Last updated match number is {last_updated_match}, played between
                         {last_team1} and {last_team2}, won by {last_winner}""")
                
                # Input fields
                match_no = st.number_input('Match No', min_value=1, max_value=99, value=last_updated_match+1, step=1)
                team1 = st.selectbox('Select Team 1', options=all_teams)
                team2 = st.selectbox('Select Team 2', options=all_teams)
                winner= st.selectbox('Select winner', options=[team1,team2])
                entry_fee = st.number_input('Entry Fee', min_value=0, value= 20, step=1)
                entered_details = pd.DataFrame({'Match_no':match_no,'Team1':team1,'Team2':team2,
                                                'Winner':winner,'Entry':entry_fee}, index=[0])
                
                
                if 'entered_details' not in st.session_state:                    
                    st.session_state['entered_details'] = pd.DataFrame()   
                def match_details():
                    st.write('### Entered details:')
                    st.dataframe(st.session_state['entered_details'], hide_index=True)
                    
                if st.button('Submit'):
                    st.session_state['entered_details'] = entered_details
                
                if not st.session_state['entered_details'].empty:
                    match_details()
        
            with right_column:
                uploaded_file = st.file_uploader("##### Upload Screenshot of Leaderboard", type=["png", "jpg", "jpeg"])
                
                if 'data_frame' not in st.session_state:                   
                    st.session_state["data_frame"]= pd.DataFrame()
                    
                
                if uploaded_file is not None:
                    temp_member = upload_obj.member(uploaded_file)
                    temp_member['Match_no'] = match_no
                    st.session_state["data_frame"] = temp_member.copy()
                    edited_df = st.data_editor(st.session_state["data_frame"],hide_index= True, num_rows= "dynamic")
                    #edited_df.on_change(lambda df: st.session_state.update({"data_frame": df}))
                    prize_pool = edited_df['Winning_amount'].sum()
                    member_count = edited_df['Member_name'].count()
                    st.write("##### Is the fetched data correct? If not then edit the above table and click Yes")
                    if st.button("Yes"):
                        entered_details['Member_count'] = member_count
                        entered_details['Prize_pool'] = prize_pool
                        match_df = match_df._append(entered_details)
                        member_df = member_df._append(edited_df, ignore_index=True)
                        match_df.to_excel("./data/contest.xlsx", index=False)
                        member_df.to_excel("./data/contestent.xlsx", index=False)
                        st.success("Data saved.")   
    

    
if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        st.write(str(e))
    
