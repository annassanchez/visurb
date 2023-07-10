import pandas as pd
import numpy as np
from pyaxis import pyaxis
import src.library as bb

class INE_Experimental:
    def __init__(self, df):
        self.df = df

    def getData(code):
        link = f'https://www.ine.es/jaxiT3/files/t/es/px/{code}.px?nocab=1'
        #set file path (or URL)
        #parse contents of *.px file
        px = pyaxis.parse(uri = link , encoding = 'ISO-8859-2')
        df = px['DATA']
        df[['cod', 'nom']] = df['Unidades territoriales'].str.split(n = 1, pat = ' ', expand = True)
        if code == bb.ine_experimental['Renta Media y Mediana']:
            df_norm = pd.pivot(df, values='DATA', index=['cod', 'nom', 'Periodo'], columns=['Indicadores de renta media']).reset_index()
            return df_norm
        else:
            pass
        