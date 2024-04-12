# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 17:13:15 2024

@author: Manoj
"""
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")
import easyocr
import cv2
import time
import streamlit as st

class UploadData:
    @st.cache_data
    def member(_self, uploaded_file):
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        # Read the image from the NumPy array
        image = cv2.imdecode(file_bytes, 1)
        gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresh, binary_img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

        reader = easyocr.Reader(['en'])
        result = reader.readtext(binary_img)
        all_text = [i[1] for i in result]
        for text in all_text:
            if 'Dipak Warriors' in text:
                all_text[all_text.index(text)] = 'Dipak Warriors 1103'
                
        temp_member = pd.DataFrame(columns=['Match_no', 'Member_name', 'Rank', 'Winning_amount'])
        position = all_text.index('Rank')
        while position < len(all_text):
            if position+4 >= len(all_text):
                break
            if position+4 == len(all_text)-1:
                temp_member = temp_member._append({'Member_name':all_text[position+1]+'('+all_text[position+2]+')',
                                    'Rank':all_text[position+4],
                                    'Winning_amount':0}, ignore_index=True)
                position= position+4
            elif ('Won' in all_text[position+5]) or ('You won' in all_text[position+5]):
                p = all_text[position+5].index('on')
                temp_member = temp_member._append({'Member_name':all_text[position+1]+'('+all_text[position+2]+')',
                                    'Rank':all_text[position+4],
                                    'Winning_amount':all_text[position+5][p+4:]}, ignore_index=True)
                position= position+5
            else:
                temp_member = temp_member._append({'Member_name':all_text[position+1]+'('+all_text[position+2]+')',
                                    'Rank':all_text[position+4],
                                    'Winning_amount':0}, ignore_index=True)
                position= position+4
                
        temp_member['Rank'] = temp_member['Rank'].str.replace('#', '')
        temp_member[['Rank','Winning_amount']] = temp_member[['Rank','Winning_amount']].astype(int)
        temp_member.sort_values(by='Rank', inplace=True)
        temp_member.reset_index(drop='True', inplace=True)
        return temp_member