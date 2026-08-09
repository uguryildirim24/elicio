"""Simple classifiers and evaluation helpers.

Three small, fast models are used as the baseline:
LDA (linear discriminant analysis), a linear support-vector machine,
and a gradient-boosted tree ensemble. All three fit in minutes on a
laptop CPU for the data sizes in this project.
"""
from __future__ import annotations

from typing import Dict, Optional

import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC


def build_models(random_state: int = 0) -> Dict[str, object]:
    """Return a fresh, untrained dict of {model_name: sklearn estimator}."""
    return {
        "LDA": make_pipeline(StandardScaler(), LinearDiscriminantAnalysis()),
        "Linear_SVM": make_pipeline(
            StandardScaler(), LinearSVC(random_state=random_state, dual="auto", max_iter=5000)
        ),
        "Gradient_Boosted_Trees": HistGradientBoostingClassifier(random_state=random_state),
    }


def fit_and_score(
    model,
    X_train: np.ndarray,
    y_train: np.ndarray,
    X_test: np.ndarray,
    y_test: np.ndarray,
) -> Dict[str, float]:
    """Fit one model and return accuracy and macro-F1 on the test rows."""
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    return {
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "macro_f1": float(f1_score(y_test, y_pred, average="macro")),
        "n_train": int(len(y_train)),
        "n_test": int(len(y_test)),
    }


def select_channels_by_fscore(
    X_train: np.ndarray,
    y_train: np.ndarray,
    feature_names,
    channel_names,
    n_channels: int,
    largest: bool = True,
):
    """Rank channels by an ANOVA F-score computed on the train rows only.

    Each channel has 5 feature columns; a channel's score is the mean
    F-score of its 5 columns. Returns (chosen_channel_names,
    chosen_feature_column_indices). Ranking uses only X_train / y_train,
    so no test-set information leaks into the channel choice.
    """
    from sklearn.feature_selection import f_classif

    f_scores, _ = f_classif(X_train, y_train)
    ch_to_cols = {}
    for i, name in enumerate(feature_names):
        ch = name.split("_")[0]
        ch_to_cols.setdefault(ch, []).append(i)

    ch_scores = {ch: float(np.mean(f_scores[cols])) for ch, cols in ch_to_cols.items()}
    ordered = sorted(channel_names, key=lambda c: ch_scores[c], reverse=largest)
    chosen = ordered[:n_channels]
    cols = sorted(sum((ch_to_cols[c] for c in chosen), []))
    return chosen, cols
