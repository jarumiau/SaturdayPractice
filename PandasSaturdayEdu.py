# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 10:21:53 2019

@author: a45a
"""

import numpy as np
import pandas as pd
import datetime as dt 

def quality_report(data):
    
    if (type(data) != pd.core.frame.DataFrame):
        raise TypeError("Data must be pandas.core.frame.DataFrame")
    else:
        columns = list(data.columns.values)
        #print(data.columns.values)
        data_type = pd.DataFrame(data.dtypes, columns=['Data type'])
        missing_data = pd.DataFrame(
        data.isnull().sum(), columns=['missing values'])
        present_data = pd.DataFrame(data.count(), columns=['present values'])
        unique_values = pd.DataFrame(columns=['unique values'])
        minimum_values = pd.DataFrame(columns=['minimum values'])
        max_values = pd.DataFrame(columns=['maximun values'])
        
        for i in columns:
            unique_values.loc[i] = [data[i].nunique()]
            try:
                minimum_values.loc[i] = [data[i].min()]
                max_values.loc[i] = [data[i].max()]
            except:
                pass
        
        DQ_report = data_type.join(missing_data).join(present_data).join(
        unique_values).join(minimum_values).join(max_values)
    
    return DQ_report

csv_original = 'DataSetNike.csv'
dataset_original = pd.read_csv(csv_original, encoding='latin-1', low_memory=False)
(dataset_original)
quality_report(dataset_original)


#Para la misiòn selecciòn de columnas Material, Date, Unis
TareaEdu = dataset_original[['Material', 'Date', 'Units']]
TareaEdu = TareaEdu.dropna()
TareaEdu = TareaEdu.rename(columns = {'Material':'CÓDIGO'})
TareaEdu = TareaEdu[TareaEdu['Units'] >= 1]

#Agrupando fecha
TareaEdu['Date'] = pd.to_datetime(TareaEdu['Date']) 
TareaEdu['Month'] = TareaEdu['Date'].dt.month 
TareaEdu['AÑO'] = TareaEdu['Date'].dt.year 

#Agrupando columnas por CODIGO, Año, mes y sumando unidades para cada mes con aggfunc='sum' para int
TareaEdu = TareaEdu.pivot_table(values = 'Units', index = ['CÓDIGO', 'AÑO'], columns = 'Month', fill_value=0, aggfunc = 'sum') 
#Cambiando 1 : ENE.. 12:DIC
TareaEdu = TareaEdu.rename(columns = {1:'ENE', 2:'FEB.', 3:'MAR.', 4:'ABR.',5:'MAY.',6:'JUN.',7:'JUL.',8:'AGO.',9:'SEP',10:'OCT.',11:'NOV.',12:'DIC.'} ) 
TareaEdu = TareaEdu.sort_values(['AÑO','CÓDIGO'])
TareaEdu = TareaEdu.reset_index() 


print(TareaEdu)
print(quality_report(TareaEdu)) 
TareaEdu.to_csv('TareaEdu.csv')


















