import pandas as pd
import numpy as np
from pyaxis import pyaxis
import src.library as bb

class INE_Experimental:
    def __init__(self, df, code):
        self.df = df
        self.code = code

    def getData(code):
        link = f'https://www.ine.es/jaxiT3/files/t/es/px/{code}.px?nocab=1'
        #set file path (or URL)
        #parse contents of *.px file
        px = pyaxis.parse(uri = link , encoding = 'ISO-8859-2')
        df = px['DATA']
        return df
    
    def cleanData(df, code):
        df[['cod', 'nom']] = df['Unidades territoriales'].str.split(n = 1, pat = ' ', expand = True)
        if code == bb.ine_experimental['Renta Media y Mediana']:
            df_norm = pd.pivot(df, values='DATA', index=['cod', 'nom', 'Periodo'], columns=['Indicadores de renta media']).reset_index()
        elif code == bb.ine_experimental['Distribución por fuente de ingresos']:
            df_norm = pd.pivot(df, values='DATA', index=['cod', 'nom', 'Periodo'], columns=['Distribución por fuente de ingresos']).reset_index()
        elif code == bb.ine_experimental['Porcentaje de población con ingresos por unidad de consumo por debajo de determinados umbrales fijos por sexo']:
            df_norm = pd.pivot(df[df['Sexo'] == 'Total'], values='DATA', index=['cod', 'nom', 'Periodo'], columns=['Distribución de la renta por unidad de consumo']).reset_index()
        elif code == bb.ine_experimental['Porcentaje de población con ingresos por unidad de consumo por debajo de determinados umbrales fijos por sexo y tramos de edad'] or code == bb.ine_experimental['Porcentaje de población con ingresos por unidad de consumo por debajo de determinados umbrales fijos por sexo y nacionalidad'] or code == bb.ine_experimental['Porcentaje de población con ingresos por unidad de consumo por debajo/encima de determinados umbrales relativos por sexo y tramos de edad'] or code == bb.ine_experimental['Porcentaje de población con ingresos por unidad de consumo por debajo/encima de determinados umbrales relativos por sexo y nacionalidad']:
            return None
        elif code == bb.ine_experimental['Porcentaje de población con ingresos por unidad de consumo por debajo/encima de determinados umbrales relativos por sexo']:
            df_norm = pd.pivot(df[df['Sexo'] == 'Total'], values='DATA', index=['cod', 'nom', 'Periodo'], columns=['Distribución de la renta por unidad de consumo']).reset_index()
        elif code == bb.ine_experimental['Indicadores demográficos']:
            df_norm = pd.pivot(df, values='DATA', index=['cod', 'nom', 'Periodo'], columns=['Indicadores demográficos']).reset_index()
        elif code == bb.ine_experimental['Índice de Gini y Distribución de la renta P80/P20']:
            df_norm = pd.pivot(df, values='DATA', index=['cod', 'nom', 'Periodo'], columns=['Indicadores de renta media']).reset_index()
        else:
            pass
        df_norm.loc[df_norm['cod'] == 'Guijarrosa,', 'nom'] = 'Guijarrosa, La distrito 01'
        df_norm.loc[df_norm['cod'] == 'Guijarrosa,', 'cod'] = '1490201'
        return df_norm     
        