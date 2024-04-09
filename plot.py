# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 17:24:41 2024

@author: Manoj
"""
import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

class PlotPlotly:
    
    def gross_total_with_granular(self, member_temp):
        ##### gross winning amount with each win amount
        fig1 = go.Figure(data=[go.Bar(x=member_temp['Member_name'], y= member_temp['Winning_amount'],
                                      text=member_temp['Winning_amount'])])
        fig1.update_layout(yaxis=dict(title='Winning_amount'))
        
        return fig1
    
    def gross_total(self, groupped_df):
        #### gross winning amount and number of match played
        fig2 = make_subplots(specs=[[{"secondary_y": True}]])
        fig2.add_trace(go.Bar(x=groupped_df['Member_name'],
                              y= groupped_df['Total_winning_amount'],
                              text=groupped_df['Total_winning_amount'],
                              name='winning_amt',showlegend=False), secondary_y=False)
        fig2.add_trace(go.Scatter(x=groupped_df['Member_name'],
                              y= groupped_df['match_count'],
                              text=groupped_df['match_count'],
                              name='match_played',showlegend=False), secondary_y=True)
                                              
        fig2.update_layout(yaxis=dict(title='Total_winning_amount'),
                          yaxis2= dict(title='number of matches played'))
        
        return fig2
    
    def net_winning(self, groupped_net):
        ##### net winning amount per participant
        fig3 = go.Figure(data=[go.Bar(x=groupped_net['Member_name'], y= groupped_net['Net_winning'], 
                                     text=groupped_net['Net_winning'])])

        fig3.update_layout(yaxis=dict(title='Winning_amount'))
        
        return fig3
    
    def generate_line_plot(self, merged_net, selected_participants):
        ##### to generate line plot for net winning per match for selected participants
        fig4 = go.Figure()
    
        for participant in selected_participants:
            filtered_df = merged_net[merged_net['Member_name'] == participant]
            filtered_df['Cum_sum'] = filtered_df['Net_winning'].cumsum()
            fig4.add_trace(go.Scatter(x=filtered_df['Match_no'], y=filtered_df['Cum_sum'],
                                     mode='lines+markers', name=participant,showlegend= True))
    
        fig4.update_layout(xaxis_title='Match no', yaxis_title='Net amount')
        fig4.update_layout(xaxis=dict(tickvals=merged_net['Match_no']))
        fig4.add_hline(y=0, line_width=0.5, line_color='red')
        return fig4
    
    def participant_rank_trend(self, merged_net, selected_participants):
        ##### to generate line plot for net winning per match for selected participants
        fig6 = make_subplots(specs=[[{"secondary_y": True}]])
        groupped_df = merged_net.groupby(by='Match_no').count()['Member_name'].reset_index()
        groupped_df.columns=['Match_no','No_of_participant']
        fig6.add_trace(go.Bar(x=groupped_df['Match_no'],
                              y= groupped_df['No_of_participant'],
                              text=groupped_df['No_of_participant'],
                              name='No_of_participant',showlegend=True), secondary_y=True)
        fig6.update_traces(marker_color='lightgreen', opacity= 0.5)
        for participant in selected_participants:
            filtered_df = merged_net[merged_net['Member_name'] == participant]
            fig6.add_trace(go.Scatter(x=filtered_df['Match_no'], y=filtered_df['Rank'],
                                     mode='lines+markers', name=participant, showlegend= True),
                           secondary_y= False)
        
        fig6.update_layout(xaxis_title='Match no', yaxis_title='Rank',yaxis2_title='Participant_count')
        fig6.update_layout(yaxis_range= [0,groupped_df['No_of_participant'].max()+1],
                           yaxis2_range= [0,groupped_df['No_of_participant'].max()+1])
        fig6.update_layout(xaxis=dict(tickvals=groupped_df['Match_no']),
                           yaxis=dict(tickvals=list(range(1,groupped_df['No_of_participant'].max()+1))),
                           yaxis2=dict(tickvals=list(range(1,groupped_df['No_of_participant'].max()+1))))
        return fig6
    
    def commission_check(self, groupped_net):
        ##### Bet amount distribution till now
        within_wallet = groupped_net[groupped_net['Net_winning']>=0]['Net_winning'].sum()
        negative_wallet = groupped_net[groupped_net['Net_winning']<0]['Net_winning'].sum()
        commission = np.abs(negative_wallet) - within_wallet
        fig5 = go.Figure(data=[go.Pie(labels=['Total Commission', 'winning amount in all wallet'],
                                 values=[commission, within_wallet], hole=.5)])
        
        fig5.update_layout(annotations=[dict(text=str(within_wallet+commission),
                                            x=0.5, y=0.5, font_size=20, showarrow=False)])
        
        return fig5
