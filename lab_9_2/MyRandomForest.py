import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier


class MyRandomForest:
    def __init__(self, trees_count: int = 5):
        self.trees: [DecisionTreeClassifier] = [DecisionTreeClassifier() for _ in range(trees_count)]

    def fit(self, features: pd.DataFrame, target: np.ndarray) -> None:
        features_by_tree = np.array(np.array_split(features, len(self.trees)))
        targets_by_tree = np.array(np.array_split(target, len(self.trees)))

        for index, tree in enumerate(self.trees):
            tree.fit(features_by_tree[index], targets_by_tree[index])

    def predict(self, features: pd.DataFrame) -> np.ndarray:
        predictions_by_tree = np.array([tree.predict(features.values) for tree in self.trees])

        def round_binary(array: np.ndarray) -> int:
            mean = array.mean()
            return 0 if mean < 0.5 else 1

        predictions = np.apply_along_axis(func1d=round_binary, axis=0, arr=predictions_by_tree)
        return predictions
