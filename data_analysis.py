import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("data/All_Diets.csv")

print(df.isna().sum())
df.fillna(df.select_dtypes(include="number").mean(), inplace=True)

grouped = df.groupby("Diet_type")[["Protein(g)", "Carbs(g)", "Fat(g)"]].mean()
print(grouped)

top5 = df.sort_values('Protein(g)', ascending=False).groupby('Diet_type').head(5)
print(top5.sort_values("Diet_type", ascending=False))

df['Protein_to_Carbs_ratio'] = df['Protein(g)'] / df['Carbs(g)']
df['Carbs_to_Fat_ratio'] = df['Carbs(g)'] / df['Fat(g)']

sns.barplot(x=grouped.index, y=grouped["Protein(g)"])
plt.title("Average Protein by Diet Type")
plt.xlabel("Diet Type")
plt.ylabel("Average Protein (g)")
plt.show()

sns.barplot(x=grouped.index, y=grouped["Carbs(g)"])
plt.title("Average Carbs by Diet Type")
plt.xlabel("Diet Type")
plt.ylabel("Average Carbs (g)")
plt.show()

sns.barplot(x=grouped.index, y=grouped["Fat(g)"])
plt.title("Average Fat by Diet Type")
plt.xlabel("Diet Type")
plt.ylabel("Average Fat (g)")
plt.show()

plt.figure(figsize=(8, 5))
sns.heatmap(grouped, annot=True, cmap="coolwarm")
plt.title("Macronutrient Heatmap by Diet Type")
plt.show()

sns.scatterplot(data=top5, x="Cuisine_type", y="Protein(g)", hue="Diet_type")
plt.xticks(rotation=45)
plt.title("Top 5 Protein-Rich Recipes by Cuisine")
plt.xlabel("Cuisine Type")
plt.ylabel("Protein (g)")
plt.show()


