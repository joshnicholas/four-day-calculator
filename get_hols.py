# %%

import holidays
import os 
import pathlib
pathos = pathlib.Path(__file__).parent
os.chdir(pathos)

print(os.getcwd())

import pandas as pd
from sudulunu.helpers import dumper, pp 

# %%


def ensure_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return path

# %%

listo = []


for state in ["ACT", 'NSW', 'NT', "QLD", 'SA', 'TAS', 'VIC', 'WA']:

    statto = holidays.country_holidays('AUS', years=['2025', '2026', '2027', '2028'], subdiv=state)

    frame = pd.DataFrame(statto, index=['Day', 'Thing']).T.reset_index()
    frame.rename(columns={"index": "Date"}, inplace=True)
    frame.drop(columns={"Thing"}, inplace=True)

    frame['State'] = state

    frame['Weekday'] = pd.to_datetime(frame['Date']).dt.strftime('%A')

    dumper(ensure_folder('input/states'), state, frame)

    listo.append(frame)
    # print(statto)
    print(frame)

cat = pd.concat(listo)

dumper('input', 'combined', cat)


#     oz = holidays.country_holidays('AUS', years=['2025', '2026', '2027'])

# print(oz)
# us_holidays = holidays.country_holidays('US')  # this is a dict-like object

# %%

# print(statto.keys())

# test = pd.DataFrame(statto, index=['Day', 'Thing']).T.reset_index()

# test.rename()

# print(test)
# print(test.columns.tolist())


# %%
