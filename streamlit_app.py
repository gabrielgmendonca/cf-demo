import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

MAX_NAMES = 100
PLACES = [
    'Restaurante 🍝',
    'Boate 🪩',
    'Centro espírita 🙏',
    'Shopping 🛒',
    'Academia 💪',
    'Estádio de futebol ⚽',
    'Igreja 🕇',
    'Praia 🏖️',
    'Faculdade 🎓',
    'Parque 🌳',
    'Escola 📚',
]

place = st.selectbox('De qual ambiente estamos falando?', PLACES)

st.title(place)

default = 'ouvir música\nconversar\ncomer\nbeber'
activities = st.text_area(f'O que as pessoas vão fazer em um(a) {place.lower()}?', default)
activities = activities.split('\n')

num_people = st.number_input('Número de pessoas', 8)

female_names = pd.read_csv('https://raw.githubusercontent.com/MedidaSP/nomes-brasileiros-ibge/master/ibge-fem-10000.csv', nrows=MAX_NAMES)
male_names = pd.read_csv('https://raw.githubusercontent.com/MedidaSP/nomes-brasileiros-ibge/master/ibge-mas-10000.csv', nrows=MAX_NAMES)

women = female_names.sample(num_people // 2, weights='freq')['nome']
men = male_names.sample(num_people // 2, weights='freq')['nome']
people = pd.concat((women, men)).sample(frac=1)

df = pd.DataFrame(people)
for activity in activities:
    df[activity] = np.random.randint(2, size=num_people)
df = df.sort_values(by=activities, ascending=False)
df = df.set_index('nome')

fig, ax = plt.subplots()
sns.heatmap(df, annot=True, cbar=False, cmap='RdYlGn', ax=ax);
st.pyplot(ax)
