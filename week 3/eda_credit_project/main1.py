import pandas as pd
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import seaborn as sns

print("Generating EDA Charts according to the Table of Contents...")

try:
    df = pd.read_csv("credit_data.csv")
except FileNotFoundError:
    print("Error: credit_data.csv not found. Run main.py first!")
    exit()

plt.figure(figsize=(10, 6))
sns.histplot(df['credit_amount'], kde=True, color='blue')
plt.title('3.1 Distribution of Credit Amount')
plt.savefig('section3_1_histogram.png')
print("✅ Saved: section3_1_histogram.png")

plt.figure(figsize=(10, 6))
sns.countplot(x='class', data=df, palette='Set3')
plt.title('3.2 Frequency of Credit Classes (Good vs Bad)')
plt.savefig('section3_2_countplot.png')
print("✅ Saved: section3_2_countplot.png")

plt.figure(figsize=(12, 8))
numeric_df = df.select_dtypes(include=['number'])
sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm')
plt.title('4.1 Correlation Heatmap')
plt.savefig('section4_1_heatmap.png')
print("✅ Saved: section4_1_heatmap.png")

plt.figure(figsize=(10, 6))
sns.boxplot(x='class', y='duration', data=df, palette='Pastel1')
plt.title('4.2 Loan Duration by Credit Class')
plt.savefig('section4_2_boxplot.png')
print("✅ Saved: section4_2_boxplot.png")

print("\nAll 4 required charts have been generated!")
print("Please ensure your README.md links to these new filenames.")