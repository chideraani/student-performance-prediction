import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pylab as plt
import joblib
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules


df = pd.read_csv('./authenticate/model_alg/300level_MIS_assoc.csv')
# df.set_index('COURSE_CODE', inplace=True)
df = df.astype(str)

lists = df.values.tolist()

te = TransactionEncoder()
te_ary = te.fit(lists).transform(lists)

dfs = pd.DataFrame(te_ary, columns=te.columns_)
dfs.drop('nan', axis=1, inplace=True)

support = 0.05
confidence = 0.1

itemsets = apriori(dfs, min_support=support, use_colnames=True, max_len = 2 )
rules = association_rules(itemsets, metric='confidence', min_threshold=confidence)
rules["antecedents"] = rules["antecedents"].apply(lambda x: list(x)[0]).astype("unicode")
rules["consequents"] = rules["consequents"].apply(lambda x: list(x)[0]).astype("unicode")

rules = rules[['antecedents','consequents','support','confidence','lift'] ]
print(rules)


filename = './authenticate/model_alg/model.sav'
joblib.dump(rules, filename)



