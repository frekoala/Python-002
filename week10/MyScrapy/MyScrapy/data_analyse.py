import config
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import pymysql
from snownlp import SnowNLP


def data_init():
    engine = create_engine('mysql+pymysql://%(user)s:%(password)s@%(host)s:%(port)d/%(db)s?charset=%(charset)s' %
                           config.db_info,
                           encoding='utf-8')
    telephone_sql = 'select * from telephone'
    telephone_df = pd.read_sql(telephone_sql, con=engine)
    return telephone_df


def data_to_db(df, table):
    engine = create_engine('mysql+pymysql://%(user)s:%(password)s@%(host)s:%(port)d/%(db)s?charset=%(charset)s' %
                           config.db_info,
                           encoding='utf-8')
    df.to_sql(table, con=engine, if_exists='replace', index=False)


def data_clean(telephone_df):
    # 去重
    telephone_df.drop_duplicates(subset=['description'], keep='first', inplace=True)
    # 去空值
    telephone_df['description'].replace(' ', np.NaN, inplace=True)
    telephone_df['description'].replace('', np.NaN, inplace=True)
    telephone_df.dropna(subset=['description'], how='any', inplace=True)
    data_to_db(telephone_df, 'telephone')


def emotion_analyse(telephone_df):
    for i, row in telephone_df.iterrows():
        description = row['description']
        evaluation = SnowNLP(description).sentiments
        telephone_df.loc[[i], ['evaluation']] = evaluation
        # print(telephone_df.loc[i])
        # print(type(telephone_df.loc[i]))
        # print(telephone_df.loc[[i], ['evaluation']])
    data_to_db(telephone_df, 'telephone')


def data_analyse():
    telephone_df = data_init()
    data_clean(telephone_df)
    emotion_analyse(telephone_df)


if __name__ == '__main__':
    data_analyse()