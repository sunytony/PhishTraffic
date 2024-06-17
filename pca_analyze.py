import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder

def remove_outliers_by_class(df, label_col):
    df_no_outliers = pd.DataFrame()
    classes = df[label_col].unique()
    for cls in classes:
        class_df = df[df[label_col] == cls]
        Q1 = class_df.quantile(0.25)
        Q3 = class_df.quantile(0.75)
        IQR = Q3 - Q1
        class_no_outliers = class_df[~((class_df < (Q1 - 1.5 * IQR)) | (class_df > (Q3 + 1.5 * IQR))).any(axis=1)]
        df_no_outliers = pd.concat([df_no_outliers, class_no_outliers])
    return df_no_outliers

label_mapping = {'Benign': 0, 'Phish': 1}
label_mapping_rev = {0: 'Benign', 1: 'Phish'}

# Load your dataset
df1 = pd.read_csv('feature_phish.csv')
df2 = pd.read_csv('feature_benign.csv')

df = pd.concat([df1, df2], ignore_index=True)

num_columns = df.shape[1] - 1  # 마지막 열은 레이블
columns = [f'col_{i}' for i in range(num_columns)] + ['Label']
df.columns = columns

df['Label'] = df['Label'].map(label_mapping)

# Separate features and target variable
# Replace 'target_column' with the name of your target variable column
# X = pd.concat([df.iloc[:, 36:54], df.iloc[:, 90:108], df.iloc[:, -1]], axis=1)  
X = pd.concat([df.iloc[:, 18:36], df.iloc[:, 72:90], df.iloc[:, -1]], axis=1)
X = remove_outliers_by_class(X, 'Label')
X['Label'] = X['Label'].map(label_mapping_rev)
y = X.pop('Label')
X = X.dropna(axis=1)
print(X)

# Standardize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Perform PCA
pca = PCA(n_components=2)  # You can change the number of components as needed
principal_components = pca.fit_transform(X_scaled)

# Create a DataFrame with the principal components
pca_df = pd.DataFrame(data=principal_components, columns=['PC1', 'PC2'])
pca_df = pd.concat([pca_df, y.reset_index(drop=True)], axis=1)

# Plot the explained variance ratio
# plt.figure(figsize=(8, 6))
# plt.bar(range(1, len(pca.explained_variance_ratio_) + 1), pca.explained_variance_ratio_, alpha=0.5, align='center')
# plt.ylabel('Explained variance ratio')
# plt.xlabel('Principal components')
# plt.title('Explained Variance Ratio of Principal Components')
# plt.show()

# Scatter plot of the principal components
palette = {'Benign':'blue', 'Phish':'red'}
plt.figure(figsize=(10, 8))
sns.scatterplot(data=pca_df, x='PC1', y='PC2', hue='Label', palette=palette)
# plt.title('PCA of Dataset')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.legend(title='Target')
plt.show()

# Print the explained variance ratio
print("Explained variance ratio:", pca.explained_variance_ratio_)