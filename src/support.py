import pandas as pd
import numpy as np
from pyaxis import pyaxis
import src.library as bb
import os

from IPython.display import display

class INE_Experimental:
    def __init__(self, df, code):
        self.df = df
        self.code = code

    def getData(code):
        """
        Objective:
        - The 'getData' method is designed to retrieve data from a specific URL and parse its contents into a pandas dataframe.

        Inputs:
        - 'code': a string representing the code of the data to be retrieved.

        Flow:
        - Construct a URL using the input 'code'.
        - Parse the contents of the URL using the 'pyaxis' library.
        - Extract the 'DATA' section of the parsed contents and store it in a pandas dataframe.
        - Return the dataframe.

        Outputs:
        - 'df': a pandas dataframe containing the data retrieved from the URL.

        Additional aspects:
        - The 'getData' method is a part of the 'INE_Experimental' class.
        - The parsed contents of the URL are assumed to be in the 'px' format.
        - The 'pyaxis' library is used to parse the contents of the URL.
        """
        link = f'https://www.ine.es/jaxiT3/files/t/es/px/{code}.px?nocab=1'
        #set file path (or URL)
        #parse contents of *.px file
        px = pyaxis.parse(uri = link , encoding = 'ISO-8859-2')
        df = px['DATA']
        return df
    
    def cleanData(df, code):
        """
        Objective:
        - The 'cleanData' method is designed to clean and transform a pandas dataframe containing data retrieved from a specific URL.

        Inputs:
        - 'df': a pandas dataframe containing the data to be cleaned and transformed.
        - 'code': a string representing the code of the data to be cleaned and transformed.

        Flow:
        - Split the 'Unidades territoriales' column of the input dataframe into two columns 'cod' and 'nom'.
        - Depending on the input 'code', pivot the input dataframe to transform it into a more usable format.
        - Rename and modify specific values in the resulting dataframe.
        - Convert certain columns of the resulting dataframe to numeric data type.
        - Return the resulting dataframe.

        Outputs:
        - 'df_norm': a pandas dataframe containing the cleaned and transformed data.

        Additional aspects:
        - The 'cleanData' method is a part of the 'INE_Experimental' class.
        - The resulting dataframe is assumed to be in a specific format depending on the input 'code'.
        - The method modifies specific values in the resulting dataframe to ensure consistency and usability.
        """
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
        elif code == bb.ine_experimental['Índice de Gini y Distribución de la renta P80_P20']:
            df_norm = pd.pivot(df, values='DATA', index=['cod', 'nom', 'Periodo'], columns=['Indicadores de renta media']).reset_index()
        else:
            pass
        df_norm.loc[df_norm['cod'] == 'Guijarrosa,', 'nom'] = 'Guijarrosa, La distrito 01'
        df_norm.loc[df_norm['cod'] == 'Guijarrosa,', 'cod'] = '1490201'
        df_norm['nivel'] = np.where((df_norm['cod'].str.len() == 5), 'municipio', np.where((df_norm['cod'].str.len() == 7), 'distrito', np.where((df_norm['cod'].str.len() == 10), 'sección censal', 'check')))
        for column in df_norm.columns.tolist():
            if column == 'cod' or column == 'nom' or column == 'nivel':
                pass
            else:
                df_norm[column] = pd.to_numeric(df_norm[column])
        return df_norm

    def export(df, code):
        """
        Objective:
        - The 'export' method is designed to export a pandas dataframe to an Excel file with a specific filename.

        Inputs:
        - 'df': a pandas dataframe containing the data to be exported.
        - 'code': a string representing the code of the data being handled.

        Flow:
        - Construct a file path using the 'code' input.
        - Filter the input dataframe to only include the rows with the maximum value in the 'Periodo' column.
        - Export the filtered dataframe to an Excel file with the constructed file path.

        Outputs:
        - None

        Additional aspects:
        - The 'export' method is a part of the 'INE_Experimental' class.
        - The exported Excel file is stored in a specific folder.
        - The filename of the exported Excel file is constructed using the 'code' input, with certain characters replaced to ensure compatibility with file naming conventions.
        """
        folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'output', 'xlsx'))
        name = code.replace('/', '_') .replace(' ', '_') + '.xlsx'
        df[(df['Periodo'] == max(df['Periodo'])) & (df['nivel'] == 'sección censal')].to_excel(os.path.join(folder, name), index=False, engine = 'openpyxl')

class Padron:
    """
    Main functionalities:
    The Padron class is designed to handle data related to population statistics in Spain. It has methods to retrieve data from a specific year and code, clean the data by filtering and pivoting, and export the cleaned data to an Excel file. The class takes in a dataframe, a code, a year, and a variable as parameters, and stores them as fields for later use in the methods.

    Methods:
    - getData(year, code): retrieves data from a specific year and code using a URL and the pyaxis library, and returns a dataframe.
    - cleanData(df, variable): cleans the data by filtering out unwanted rows and pivoting the data based on the variable parameter. Returns a cleaned dataframe.
    - export(df, code): exports the cleaned dataframe to an Excel file with the given code as the filename.

    Fields:
    - code: a string representing the code for the data being handled.
    - df: a dataframe containing the data being handled.
    - year: an integer representing the year of the data being handled.
    - variable: a string representing the variable being used to pivot the data during cleaning.
    """
    def __init__(self, df, code, year, variable) -> None:
        self.code = code
        self.df = df
        self.year = year
        self.variable = variable
    
    def getData(year, code):
        """
        Objective:
        - The 'getData' method is designed to retrieve data from a specific URL and parse its contents into a pandas dataframe.

        Inputs:
        - 'year': an integer representing the year of the data to be retrieved.
        - 'code': a string representing the code of the data to be retrieved.

        Flow:
        - Construct a URL using the input 'year' and 'code'.
        - Parse the contents of the URL using the 'pyaxis' library.
        - Extract the 'DATA' section of the parsed contents and store it in a pandas dataframe.
        - Return the dataframe.

        Outputs:
        - 'df': a pandas dataframe containing the data retrieved from the URL.

        Additional aspects:
        - The 'getData' method is a part of the 'Padron' class.
        - The parsed contents of the URL are assumed to be in the 'px' format.
        - The 'pyaxis' library is used to parse the contents of the URL.
        - The resulting dataframe is assumed to contain the 'DATA' section of the parsed contents.
        """
        link = f'https://www.ine.es/pcaxisdl/t20/e245/p07/a{year}/l0/{code}.px'
        #set file path (or URL)
        #parse contents of *.px file
        px = pyaxis.parse(uri = link , encoding = 'ISO-8859-2')
        df = px['DATA']
        return df
    
    def cleanData(df, variable):
        """
        Objective:
        - The 'cleanData' method is designed to clean and transform a pandas dataframe containing population statistics data retrieved from a specific URL. The method takes in a dataframe and a variable as inputs, and returns a cleaned dataframe.

        Inputs:
        - 'df': a pandas dataframe containing the population statistics data to be cleaned and transformed.
        - 'variable': a string representing the variable being used to pivot the data during cleaning.

        Flow:
        - Filter the input dataframe to only include rows with 'sexo' as 'Ambos Sexos' and 'sección' not equal to 'TOTAL'.
        - Depending on the input 'variable', pivot the input dataframe to transform it into a more usable format.
        - Rename and modify specific values in the resulting dataframe.
        - Display the resulting dataframe.
        - Return the resulting dataframe.

        Outputs:
        - 'df_norm': a pandas dataframe containing the cleaned and transformed population statistics data.

        Additional aspects:
        - The 'cleanData' method is a part of the 'Padron' class.
        - The resulting dataframe is assumed to be in a specific format depending on the input 'variable'.
        - The method modifies specific values in the resulting dataframe to ensure consistency and usability.
        - The resulting dataframe is displayed for visualization purposes.
        """
        df = df[(df['sexo'] == 'Ambos Sexos') & (df['sección'] != 'TOTAL')]
        if variable == 'Población por sexo, Sección y edad':
            df_norm = pd.pivot(df, values='DATA', index=['sección'], columns=['edad (grupos quinquenales)']).reset_index()
            df_norm.columns = ['edad_' + name.replace('-', '_').replace(' y más', '') for name in df_norm.columns.tolist()]
        elif variable == 'Población por sexo, Sección y nacionalidad (principales nacionalidades)':
            df_norm = pd.pivot(df, values='DATA', index=['sección'], columns=['nacionalidad']).reset_index()
        else:
            pass
        display(df_norm)
        return df_norm
    
    def export(df, code):
        """
        Objective:
        - The 'export' method is designed to export a pandas dataframe to an Excel file with a specific filename.

        Inputs:
        - 'df': a pandas dataframe containing the data to be exported.
        - 'code': a string representing the code of the data being handled.

        Flow:
        - Construct a file path using the 'code' input.
        - Export the input dataframe to an Excel file with the constructed file path.

        Outputs:
        - None

        Additional aspects:
        - The 'export' method is a part of the 'Padron' class.
        - The exported Excel file is stored in a specific folder.
        - The filename of the exported Excel file is constructed using the 'code' input.
        """
        folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'output', 'xlsx'))
        name = code + '.xlsx'
        df.to_excel(os.path.join(folder, name), index=False, engine = 'openpyxl')
