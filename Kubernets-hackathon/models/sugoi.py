import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_class_weight
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import seaborn as sns
import matplotlib.pyplot as plt

# 1) LOAD DATA ────────────────────────────────────────────────────────────────
df = pd.read_csv("k8s_failure_training_data.csv", parse_dates=["timestamp"])

# 2) FEATURE / TARGET SPLIT ───────────────────────────────────────────────────
X = df.drop(columns=["timestamp",          # not predictive
                     "anomaly_label",      # binary flag, redundant
                     "anomaly_type"])      # ← target
y = df["anomaly_type"]

# 3) TRAIN‑TEST SPLIT (stratified) ────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y)

# 4) HANDLE CLASS IMBALANCE WITH COST‑SENSITIVE LEARNING ─────────────────────
classes = np.unique(y_train)
weights = compute_class_weight(class_weight="balanced",
                               classes=classes,
                               y=y_train)
class_weights = dict(zip(classes, weights))
print("Class weights used:", class_weights)

# 5) MODEL ────────────────────────────────────────────────────────────────────
rf = RandomForestClassifier(
        n_estimators=500,
        max_depth=None,
        min_samples_leaf=2,
        n_jobs=-1,
        class_weight=class_weights,
        random_state=42)

rf.fit(X_train, y_train)

# 6) EVALUATION ───────────────────────────────────────────────────────────────
y_pred = rf.predict(X_test)
print(classification_report(y_test, y_pred, digits=3))

cm = confusion_matrix(y_test, y_pred, labels=classes)
plt.figure(figsize=(8,6))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=classes, yticklabels=classes)
plt.title("Confusion Matrix – Anomaly Type")
plt.xlabel("Predicted"); plt.ylabel("Actual"); plt.tight_layout()
plt.show()

# 7) OPTIONAL – FEATURE IMPORTANCE SNAPSHOT ──────────────────────────────────
fi = (pd.Series(rf.feature_importances_, index=X.columns)
        .sort_values(ascending=False))
print("Top 10 important features:\n", fi.head(10))

# 8) SERIALISE FOR DEPLOYMENT ────────────────────────────────────────────────
joblib.dump(rf, "k8s_anomaly_classifier.joblib")
print("Model saved to k8s_anomaly_classifier.joblib")

# 9) SAMPLE INPUT‑OUTPUT ───────────────────────────────────────────────────────
print("\nSample input to the model:")
sample_input = X_test.iloc[[0]]  # Selecting one sample row
print(sample_input)

sample_prediction = rf.predict(sample_input)
print("\nPredicted anomaly type for the sample input:", sample_prediction[0])
print("Actual anomaly type:", y_test.iloc[0])