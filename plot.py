import matplotlib.pyplot as plt
import numpy as np

categories = ['Random Forest', 'Ada Boost', 'K Neighbors', 'SVM']
acc = [0.9964, 0.9963, 0.9945, 0.9184]
auc = [0.9999, 0.9999, 0.9983, 0.9914]
recall = [0.9964, 0.9963, 0.9945, 0.9184]
precision = [0.9964, 0.9963, 0.9945, 0.9575]

bar_width = 0.15
index = np.arange(len(categories))

plt.figure(figsize=(10, 6))
plt.bar(index - bar_width, acc, width=bar_width, label='Accuracy', color='#1f77b4')
plt.bar(index, auc, width=bar_width, label='AUC', color='#ff7f0e')
plt.bar(index + bar_width, recall, width=bar_width, label='Recall', color='#2ca02c')
plt.bar(index + bar_width * 2, precision, width=bar_width, label='Precision', color='#9467bd')

plt.xlabel('ML model')
plt.ylabel('Values')
plt.xticks(index + bar_width / 2, categories)
plt.legend(loc='upper right')

plt.tight_layout()
plt.show()