from evaluate import load


class Metric:
    def __init__(self, metric_name):
        self.metric_name = metric_name
        self.evaluation_module = load(metric_name)

    def compute(self, **kwargs):
        return self.evaluation_module.compute(**kwargs)


class Quality(Metric):
    def __init__(self):
        super().__init__("quality")


class Cost(Metric):
    def __init__(self):
        super().__init__("cost")


class Time(Metric):
    def __init__(self):
        super().__init__("time")


# Quality Metrics
class Accuracy(Quality):
    def __init__(self):
        super().__init__("accuracy")


class F1Score(Quality):
    def __init__(self):
        super().__init__("f1")


class Precision(Quality):
    def __init__(self):
        super().__init__("precision")


class Recall(Quality):
    def __init__(self):
        super().__init__("recall")


class ExactMatch(Quality):
    def __init__(self):
        super().__init__("exact_match")


class MeanIoU(Quality):
    def __init__(self):
        super().__init__("mean_iou")


class McNemar(Quality):
    def __init__(self):
        super().__init__("mcnemar")


class WordLength(Quality):
    def __init__(self):
        super().__init__("word_length")


# Cost metrics
class USD:
    def __gt__(self, value):
        # Implement the logic for USD > value
        pass


# Time metrics
class Seconds:
    def __lt__(self, value):
        # Implement the logic for Seconds < value
        pass
