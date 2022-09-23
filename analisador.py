import pandas
import csv
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_curve, make_scorer, precision_recall_fscore_support, classification_report
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_excel('dados.xlsx')

#df = df.drop(df.loc[df['tempo'] > 87].index)
df = df.drop(df.loc[df['tempo'] < 86].index)

#df = df.loc[df['target 2 cantos'] >= 0]
#df = df.drop('Unnamed: 0',1)
#df = df.drop('Unnamed: 0.1',1)
#df = df.drop('Unnamed: 0.2',1)
#df = df.drop('Unnamed: 0.3',1)
#df = df.drop('Unnamed: 0.4',1)

df = df.drop('faltas casa',1)
df = df.drop('faltas fora',1)
df = df.drop('link',1)
#df = df.drop('tempo',1)

display(df.shape)
display(df)

df1 = df.loc[df['target 1 canto'] == 0]
df1 = df1.loc[(df1['gols casa'] - df1['gols fora']) < 2]
df1 = df1.loc[(df1['gols casa'] - df1['gols fora']) > -2]
df1 = df1.drop(df1.index[3:500])


df2 = df.loc[df['target 2 cantos'] == 1]
df2 = df2.loc[(df2['gols casa'] - df2['gols fora']) < 2]
df2 = df2.loc[(df2['gols casa'] - df2['gols fora']) > -2]
df2 = df2.loc[(df2['cantos casa'] + df2['cantos fora']) > 7]


display(df1.shape)
display(df2.shape)

frames = [df1,df2]

dfa = pd.concat(frames)

display(dfa.shape)

display(df2)

X = dfa[['odd pre casa', 'odd pre fora',
        'odd live casa', 'odd live fora', 'gols casa',
        'gols fora','posse casa','posse fora','chutes casa','chutes fora',
        'chutes no gol casa','chutes no gol fora','ataques perigosos casa',
        'ataques perigosos fora','cantos casa','cantos fora','cartao vermelho casa',
        'cartao vermelho fora','tempo ultimo gol','cantos pos ultimo gol']].values

y = dfa['target 2 cantos'].values

X_train, X_test, y_train, y_test = train_test_split(X, y)

model = LogisticRegression(solver="liblinear")
model.fit(X_train, y_train)

#y_pred = model.predict(X_test)

y_pred = model.predict_proba(X_test)[:, 1] > 0.9

print(confusion_matrix(y_test, y_pred))

print('')




#print(y_pred)



#display(f1_score(y_test, y_pred, average='weighted', labels=np.unique(y_pred)))
#print(model.score(X_test, y_test))
#print("accuracy:", accuracy_score(y_test, y_pred))
print("precision:", precision_score(y_test, y_pred))
print("recall:", recall_score(y_test, y_pred))



#def specificity_score(y_true, y_pred):
#    p, r, f, s = precision_recall_fscore_support(y_true, y_pred)
#    return r[0]

#print(precision_recall_fscore_support(y_test, y_pred))    
#print(specificity_score(y_test, y_pred))
