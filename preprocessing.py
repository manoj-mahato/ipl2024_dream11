# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 17:00:28 2024

@author: Manoj
"""
import pandas as pd

class PreProcessing:
        
    def main_processing(self, df1, df2):
        match_df = df1.copy()
        member_df = df2.copy()
        member_df['Member_name'] = member_df['Member_name'].replace({'ANILK6782RS(T1)':'FallenNoob(T1)','FallenNoob(T2)':'Krishna(T1)'})
        member_df['Member_name'] = member_df['Member_name'].str[0:-4]
        ##### group based on participant name
        groupped_df = member_df.groupby(by='Member_name').sum()['Winning_amount'].reset_index()
        groupped_df = member_df.groupby('Member_name').agg({'Winning_amount': 'sum',
                                                            'Member_name': 'count'})
        groupped_df = groupped_df.rename(columns={'Winning_amount': 'Total_winning_amount', 'Member_name': 'match_count'})
        groupped_df.reset_index(inplace=True)
        groupped_df.sort_values(by='Total_winning_amount', ascending= False, inplace=True)
        groupped_df.reset_index(drop= True, inplace= True)
        groupped_df = groupped_df.reset_index()
        groupped_df.rename(columns={'index':'sort_order'}, inplace= True)
        groupped_df['sort_order'] = groupped_df['sort_order'] + 1
        ##### keep each entry of all participant but in order
        member_temp = pd.merge(member_df, groupped_df, on='Member_name', how='left')
        member_temp.sort_values(by='sort_order', inplace=True)
        ##### to find net earning of each participant for each match
        merged_net = pd.merge(member_df,match_df, on='Match_no')[['Match_no', 'Member_name', 'Rank',
                                                                  'Winning_amount','Entry']]
        merged_net['Net_winning'] = merged_net['Winning_amount'] - merged_net['Entry']
        ##### participant wise net winning amount
        groupped_net = merged_net.groupby(by='Member_name').sum()['Net_winning'].reset_index()
        groupped_net.sort_values(by='Net_winning', ascending= False, inplace=True)
        
        return member_temp, groupped_df, merged_net, groupped_net