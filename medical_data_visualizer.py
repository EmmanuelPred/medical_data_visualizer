import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('medical_examination.csv')

# Add 'overweight' column
BMI=df['weight']/(np.power((df['height']/100),2))
count=0
for bmi in BMI:
    count+=1
    if bmi > 25:
        BMI[count-1]=1
    else:
        BMI[count-1]=0   
df['overweight'] = BMI


# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
cholesterol2=df['cholesterol'].copy()
gluc2=df['gluc'].copy()
df2=df.drop(columns=['cholesterol','gluc'])
count2=0
for col in cholesterol2:
    count2+=1
    if col > 1:
        cholesterol2[count2-1]=int(1)
    else:
        cholesterol2[count2-1]=int(0)  
count3=0
for glu in gluc2:
    count3+=1
    if glu > 1:
        gluc2[count3-1]=int(1)
    else:
        gluc2[count3-1]=int(0)  
df2['cholesterol'] = cholesterol2
df2['gluc'] = gluc2
df2

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat =pd.melt(df2,value_vars=['cholesterol','gluc','smoke','alco','active','overweight'],id_vars='cardio')

    df_cat['total'] = 0
    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    df_cat= df_cat.groupby(['cardio', 'variable', 'value']).count().reset_index()

    # Draw the catplot with 'sns.catplot()'

    grap=sns.catplot(x="variable", y='total', hue="value",col="cardio", data=df_cat, kind="bar")
    fig=grap.fig
    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = df
    df_heat = df_heat[df_heat["ap_lo"] <= df_heat["ap_hi"]]
    df_heat = df_heat[df_heat["height"] >= df_heat["height"].quantile(0.025)]
    df_heat = df_heat[df_heat["height"] <= df_heat["height"].quantile(0.975)]
    df_heat = df_heat[df_heat["weight"] >= df_heat["weight"].quantile(0.025)]
    df_heat = df_heat[df_heat["weight"] <= df_heat["weight"].quantile(0.975)]
    

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))



    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize = (11, 11))

    # Draw the heatmap with 'sns.heatmap()'
    ax=sns.heatmap(corr, mask=mask, linewidths=.5, vmin=-0.15, vmax=0.3,annot=True, fmt="0.1f", square=True)      


    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
