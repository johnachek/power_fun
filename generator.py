import numpy as np
import pandas as pd
import os
import random
import secrets
import requests
from bs4 import BeautifulSoup

from datetime import date

pb = pd.read_csv('./powerball.csv')
pb['draw_date'] = pd.to_datetime(pb['draw_date'])
pb.sort_values('draw_date', inplace=True)
pb.reset_index(drop=True, inplace=True)
pb.drop(columns=['draw_date', 'day', 'outcome'], inplace=True)

first = pb['first'].value_counts()
first = first.sort_index()
second = pb['second'].value_counts()
second = second.sort_index()
third = pb['third'].value_counts()
third = third.sort_index()
fourth = pb['fourth'].value_counts()
fourth = fourth.sort_index()
fifth = pb['fifth'].value_counts()
fifth = fifth.sort_index()
power = pb['power'].value_counts()
power = power.sort_index()

non_first = []
non_second = []
non_third = []
non_fourth = []
non_fifth = []
non_power = []
for i in list(range(1, 70)):
    if not i in list(first.index):
        non_first.append((i, 0))
    if not i in list(second.index):
        non_second.append((i, 0))
    if not i in list(third.index):
        non_third.append((i, 0))
    if not i in list(fourth.index):
        non_fourth.append((i, 0))
    if not i in list(fifth.index):
        non_fifth.append((i, 0))
    if not i in list(power.index):
        non_power.append((i, 0))

first = sorted(list(zip(first.index, first.values)) + non_first)
second = sorted(list(zip(second.index, second.values)) + non_second)
third = sorted(list(zip(third.index, third.values)) + non_third)
fourth = sorted(list(zip(fourth.index, fourth.values)) + non_fourth)
fifth = sorted(list(zip(fifth.index, fifth.values)) + non_fifth)
power = sorted(list(zip(power.index, power.values)) + non_power)

date = date.today()

def randomizer():
    num1 = random.choices([i[0] for i in first], weights = [i[1] for i in first])
    num2 = random.choices([i[0] for i in second], weights = [i[1] for i in second])
    num3 = random.choices([i[0] for i in third], weights = [i[1] for i in third])
    num4 = random.choices([i[0] for i in fourth], weights = [i[1] for i in fourth])
    num5 = random.choices([i[0] for i in fifth], weights = [i[1] for i in fifth])
    nump = random.choices([i[0] for i in power], weights = [i[1] for i in power])
    return (num1, num2, num3, num4, num5, [nump])

the_list = []
roll = secrets.randbits(random.choice(range(5,9)))
iterab = []
for i in range(roll):
    iterab.append(i)
differ = secrets.choice(iterab)
for j in range(roll):
    if j == roll-differ:
        for i in range(10):
            the_list.append(randomizer())
result=False
for wins in the_list:
    for i in range(pb.shape[0]):
        if wins[0][0] == pb.iloc[i, 2] & wins[1][0] == pb.iloc[i, 3] & wins[2][0] == pb.iloc[i, 4] & wins[3][0] == pb.iloc[i, 5] & wins[4][0] == pb.iloc[i, 6] & wins[5][0] ==pb.iloc[i, 7]:
            result=True
all_wins = []
for wins in the_list:
    win = []
    for num in wins:
        win.append(num[0])
    all_wins.append(win)

df = pd.DataFrame(all_wins)
for n in df.index:
    df.loc[n, 5] = df.loc[n,5][0]
df.to_csv(f'./predictions/generated_from_{date}.csv', index=False)