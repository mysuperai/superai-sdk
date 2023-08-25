from typing import List

import pandas as pd
from tabulate import tabulate


class Evaluator:
    """
    A class to evaluate the performance of a model by comparing its predictions against ground truth. The evaluation is
    designed for multi-field predictions of strings. An empty string will interpret as a negative.

    Attributes:
        ground_truth (list of dicts): A list of dictionaries containing ground truth labels.
        predictions (list of dicts): A list of dictionaries containing predicted labels.
    """

    def __init__(self, ground_truth: List[dict], predictions: List[dict]):
        self.ground_truth = ground_truth
        self.predictions = predictions

    @staticmethod
    def _count_metrics(gt, pred):
        """Counts true positives, false positives, true negatives, false negatives, and incorrect positives.

        Args:
            gt (list): A list of ground truth labels.
            pred (list): A list of predicted labels.

        Returns:
            tuple: A tuple containing true positives, false positives, true negatives, false negatives, and incorrect
            positives.
        """
        tp = 0
        fp = 0
        tn = 0
        fn = 0
        ip = 0

        for i, (g, p) in enumerate(zip(gt, pred)):
            if g != "" and p != "":
                if g == p:
                    tp += 1
                else:
                    ip += 1
                    print(i, g, p)
            elif g == "" and p != "":
                fp += 1
            elif g != "" and p == "":
                print(i, g, p)
                fn += 1
            else:
                tn += 1

        return tp, fp, tn, fn, ip

    @staticmethod
    def _compute_metrics(tp, fp, tn, fn, ip):
        correct_positive = tp / (tp + fn + ip) if fn + tp + ip > 0 else 0
        false_positive_rate = fp / (fp + tn) if fp + tn > 0 else 0
        false_negative_rate = fn / (fn + tp + ip) if fn + tp + ip > 0 else 0
        true_negative_rate = tn / (tn + fp) if tn + fp > 0 else 0
        true_positive_rate = tp / (tp + fn + ip) if tp + fn + ip > 0 else 0

        return {
            "correct_positive": correct_positive,
            "accuracy": (tp + tn) / (tp + fp + tn + fn + ip),
            "false_positive_rate": false_positive_rate,
            "false_negative_rate": false_negative_rate,
            "true_negative_rate": true_negative_rate,
            "true_positive_rate": true_positive_rate,
            "num_positive": tp + fn + ip,
            "num_negative": tn + fp,
            "total": (tp + fp + tn + fn + ip),
        }

    def evaluate(self, as_formatted_string=True):
        """Evaluates the performance of a model by comparing its predictions against ground truth for each key in the
        datasets.

        Returns:
            dict: A dictionary containing the performance metrics for each key.

        """
        results = {}
        keys = set().union(*(d.keys() for d in self.ground_truth))

        for key in keys:
            gt = [d.get(key, "") for d in self.ground_truth]
            pred = [d.get(key, "") for d in self.predictions]

            tp, fp, tn, fn, ip = self._count_metrics(gt, pred)
            metrics = self._compute_metrics(tp, fp, tn, fn, ip)
            results[key] = metrics
        if as_formatted_string:
            df = pd.DataFrame(results).T.sort_index()
            results = tabulate(df, headers=df.columns)

        return results
