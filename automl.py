import pandas as pd
from pycaret.classification import *

link = ['total_time', 'downlink_time', 'uplink_time', 'total_size', 'downlink_size', 'uplink_size']
stats = ['max', 'min', 'mean', 'mad', 'std', 'var', 'skew', 'kurtosis', '10per', '20per', '30per', '40per', '50per', '60per', '70per', '80per', '90per', 'num']

# Load your datasets
# Replace 'file1.csv' and 'file2.csv' with your actual dataset files
df1 = pd.read_csv('feature_phish.csv')
df2 = pd.read_csv('feature_benign.csv')

# Merge the datasets
# Assuming the datasets have the same columns and you want to concatenate them by rows
df = pd.concat([df1, df2], ignore_index=True)

columns = []

for i in link:
    for j in stats:
        columns.append('%s_%s'%(i, j))
columns.append('Label')
df.columns = columns

# Initialize PyCaret setup
exp_clf = setup(data=df, target=None, train_size=0.8)

# Compare models and select the best one
best_model = compare_models(sort='F1', fold=5, n_select=10)
tuned_model = [tune_model(i, fold=5, optimize='F1', n_iter=100) for i in best_model]
# Evaluate the best model
evaluate_model(tuned_model)

# ROC Curve
# plot_model(best_model, plot='auc')

# # Precision-Recall Curve
# plot_model(best_model, plot='pr')

# Feature Importance
# plot_model(tuned_model, plot='feature')
save_model(tuned_model, './model')

# # Learning Curve
# plot_model(best_model, plot='learning')

# # Validation Curve
# plot_model(best_model, plot='vc')
