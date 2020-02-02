#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
pd.set_option('display.max_columns', 50)


# In[2]:


from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV
from sklearn.externals import joblib


# In[3]:


def process_qoutation(source):
    df=source.drop(['Закон основание','Ссылка на КС','Участники КС', 'Даты проведения',                      'Адрес поставки','Заказчика','ИНН заказчика', 'КПП заказчика',                     'Наименование победителя','ИНН победителя','КПП победителя',                     'Процент снижения','Ставка победителя'],axis=1)
    df['region']=source['КПП заказчика'] // 1e7
    df=df.drop(df[(df['Статус']=='Не состоялась') | (df['Статус']=='Снята с публикации')].index)
    df=df.drop('Статус',axis=1)
    df=df.drop(df[(df['Статус контракта']!="Исполнен") & (df['Статус контракта']!="Заключен")].index)
    df=df.drop(df[df.region.isna()].index)
    df['percent']=(source['Начальная стоимость']-source['Итоговоя стоимость'])/source['Начальная стоимость']*100
    df['day_of_week']=source['Дата начала'].dt.dayofweek
    df['week']=source['Дата начала'].dt.week
    df=df.drop(['Время начала','Дата окончания','Время окончания'],axis=1) #'Дата начала',
    df=df.drop(df[df['Идентификатор СТЕ'].isna()].index)
    return df


# In[11]:


#pr_quot=pd.read_excel(r'data\КС с оффертами.xlsx',index_col=0)
offer_counts=pd.read_excel('data\offers_count.xlsx',index_col=0)


# In[83]:

def analize_it():
	region=int(input('Введите регион: '))
	id_ste=int(input('Введите идентификатор СТЕ: '))
	count=input('Введите количество: ')
	cte_type=input('Введите вид (Работа, Товар, Услуга): ')

	X=pd.DataFrame({'region':region,'week':37,'Идентификатор СТЕ':id_ste,'Количество товара':count},index=range(1))

	if cte_type=='Работа':
		ntype=4
	elif cte_type=='Товар':
		ntype=2
	elif cte_type=='Услуга':
		ntype=1
	X['type']=ntype


	# In[86]:


	X=X.astype({"Идентификатор СТЕ": 'int'})


	# In[87]:


	X=X.merge(offer_counts,on='Идентификатор СТЕ',how='left').fillna(0)


	# In[88]:




	# In[80]:


	best_clf=joblib.load('randforest.model')


	# In[89]:


	res=best_clf.predict(X)

	return res[0]




