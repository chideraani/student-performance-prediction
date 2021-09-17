import pandas as pd
import numpy as np
import seaborn as sns
import joblib
import matplotlib.pylab as plt
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules



df = pd.read_csv('./authenticate/model_alg/association1.csv')
df.set_index('S/N', inplace=True)

support = 0.2
confidence = 0.6

# create frequent itemsets
itemsets = apriori(df, min_support=support, use_colnames=True)

# convert into rules
rules = association_rules(itemsets, metric='confidence', min_threshold=confidence)

rules["antecedents"] = rules["antecedents"].apply(lambda x: list(x)[0]).astype("unicode")
rules["consequents"] = rules["consequents"].apply(lambda x: list(x)[0]).astype("unicode")


rules = rules[['antecedents','consequents','support','confidence','lift']]
rules = rules.sort_values(['confidence'], ascending =[False])

result_perf = rules.loc[(rules['consequents'] == 'CPerformance_Poor')| (rules['consequents'] == 'CPerformance_Fair') | (rules['consequents'] == 'CPerformance_Good')]

filename = './authenticate/model_alg/model2.sav'
joblib.dump(result_perf, filename)