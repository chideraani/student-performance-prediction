import joblib
import pandas as pd
import numpy as np
from numpy import mean
import seaborn as sns
import matplotlib.pylab as plt


fig_size = plt.rcParams["figure.figsize"]
fig_size[0] = 10
fig_size[1] = 8
plt.rcParams["figure.figsize"] = fig_size

df = pd.read_csv('200_viz.csv')
print(df.head())

df['PRE_CGPA'] = df['PRE WTS'] / df['PRE UNIT']
df['CGPA_CHANGE'] = (df['CGPA'] - df['PRE_CGPA']) * 100
df['CHANGE'] = df['CGPA_CHANGE'].apply(lambda x: 'increase' if x > 0 else 'decrease')
cols = df.iloc[:,6:18]
print(cols)

print(df.head())

# chart1
g= sns.barplot(x='GENDER', y='GPA', data=df,estimator=mean, ci=None)
# plt.rcParams["figure.figsize"] = (10, 15)
plt.title('Average Performance by Gender', size=20)
plt.xlabel('Gender', size=15)
plt.ylabel('Average GPA', size=15)

for p in g.patches:
    g.annotate(format(p.get_height(), '.3f'), (p.get_x() + p.get_width() / 2., p.get_height()), ha = 'center',va = 'center', xytext = (0, 10), textcoords = 'offset points')
plt.show()

# chart2
g= sns.barplot(x='CLASS', y='GPA', hue='GENDER',data=df,estimator=mean, ci=None)
# plt.rcParams["figure.figsize"] = (10, 15)
plt.title('Average Performance by Gender & Class', size=20)
plt.xlabel('Gender', size=15)
plt.ylabel('Average GPA', size=15)

for p in g.patches:
    g.annotate(format(p.get_height(), '.3f'), (p.get_x() + p.get_width() / 2., p.get_height()), ha = 'center',va = 'center', xytext = (0, 10), textcoords = 'offset points')
plt.show()

# chart3
sns.boxplot(x='GENDER', y='CGPA', data=df)
plt.show()

# chart4
g = sns.countplot(x='CLASS',data=df, color='blue')
plt.title('Class Distribution of Students')
plt.xlabel('Class')
plt.ylabel('Count')

for p in g.patches:
    g.annotate(format(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()), ha = 'center',va = 'center', xytext = (0, 10), textcoords = 'offset points')
plt.show()

# chart5
dataForPlot = df.groupby('CLASS').mean().CGPA_CHANGE
fig, ax = plt.subplots()
ax.bar(dataForPlot.index, dataForPlot, color=['blue'])
# ax.set_xticks([0, 1], False)
ax.set_xlabel('Class')
ax.set_ylabel('Average CGPA Change')
ax.set_title('Percentage Change in CGPA by Class')

for p in ax.patches:
    ax.annotate(format(p.get_height(), '.2f'), (p.get_x() + p.get_width() / 2., p.get_height()), ha = 'center',va = 'center', xytext = (0, 10), textcoords = 'offset points')
plt.show()

# chart6
sns.scatterplot(x='PRE_CGPA', y='CGPA', hue='CHANGE', data=df, s=90)
plt.title('CGPA VS PREVIOUS CGPA SHOWING INCREASE/DECREASE', size=20)
plt.xlabel('PREVIOUS CGPA', size=15)
plt.ylabel('CURRENT CGPA', size=15)
plt.show()


# chart7
sns.boxplot(x="variable", y="value", data=pd.melt(cols))
plt.show()


# filename = './authenticate/model_alg/viz_model.sav'
# joblib.dump(file, filename)