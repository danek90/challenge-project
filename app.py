import requests
import streamlit as st
import re
from bs4 import BeautifulSoup
import pandas as pd

# reqs = requests.get(c)
# soup = BeautifulSoup(reqs.text, 'html.parser')

challengers_summary = pd.read_csv(filepath_or_buffer='./input-data/ch-summary.csv', index_col=1)
# challengers_names = tuple(challengers_summary['cLink'], challengers_summary['name'])
# cLink = '/wiki/Theresa_Jones'
challenger_names = list(challengers_summary[['cLink','name']].apply(tuple, axis=1))

print(challenger_names[0][0])

def pull_image(ch):
    print(ch)
    c = 'https://thechallenge.fandom.com'
    reqs = requests.get(c + ch)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    img = soup.find("a", {"class":"image image-thumbnail"}, href=True)['href']
    img = re.sub(r'/revision.*$',"", img)
    return img

def show_stats(ch, ch_sum=challengers_summary):
    stats = ch_sum.loc[ch_sum['cLink'] == ch]
    t_stats = stats[['seasonCount', 'seasonsWon', 'finalsCount','totalDailiesCount', 'totalDailiesWon', 'totalElim']]
    t_stats = t_stats.transpose()
    return t_stats

st.set_page_config(page_title="Challenger Stats", layout="wide", initial_sidebar_state="expanded")

ch_select = st.selectbox('Select Challenger', challengers_summary['name'])

ch_wiki = [x for x, y in challenger_names if y == ch_select][0]

col1, col2 = st.columns(2)

img = pull_image(ch=ch_wiki)

col1.image(img, caption=ch_select)
t_stats = show_stats(ch=ch_wiki)
col2.dataframe(data=t_stats)
