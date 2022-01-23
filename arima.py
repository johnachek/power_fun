import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from statsmodels.tsa.arima.model import ARIMA
from datetime import date

df = pd.read_csv('./powerball.csv')
df['draw_date'] = pd.to_datetime(df['draw_date'])
df = df.sort_values('draw_date')
df.reset_index(inplace=True)
df.drop(columns=['index', 'draw_date', 'day', 'outcome'], inplace=True)

best_all = []
train=[]
test=[]
for col in ['first', 'second', 'third', 'fourth', 'fifth', 'power']:
    best_aic = 1_000_000
    best_p = 0
    best_q = 0
    y_train=df[col].drop(df.index[-1])
    y_test = df[col][df.index[-1]]
    train.append(y_train)
    test.append(y_test)
    for p in range(df.shape[0]):
        for q in range(df.shape[0]):
            try:
                arima = ARIMA(endog=y_train, order=(p, 1, q))
                model = arima.fit()
                if model.aic < best_aic:
                    best_aic = model.aic
                    best_p = p
                    best_q = q
                    
            except:
                pass
    best_all.append((best_p, 1, best_q))

predictions = []
for i in range(len(best_all)):
    arima = ARIMA(endog=train[i], order=best_all[i])
    model = arima.fit()
    preds = model.predict(start=df.index[-1], end=df.index[-1])
    predictions.append(preds)

pred = []
for i in range(len(predictions)):
    num = predictions[i][df.index[-1]]
    pred.append(round(num))
date = date.today()
pred.to_csv(f'./predictions/arima_from_{date}.csv', index=False)
