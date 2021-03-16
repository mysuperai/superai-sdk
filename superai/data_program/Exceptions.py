class EmptyPerformanceError(Exception):
    def __init__(self, message):
        self.message = message


class UnsatisfiedMetricsError(Exception):
    def __init__(self, message):
        self.message = message


class MetricNotImplementedError(Exception):
    def __init__(self, message):
        self.message = message


class MetricCalculationFailed(Exception):
    def __init__(self, message):
        self.message = message


class JobTypeNotImplemented(Exception):
    def __init__(self, message):
        self.message = message


class PerformanceNotSet(Exception):
    def __init__(self, message):
        self.message = message


class PerformanceNotReady(Exception):
    def __init__(self, message):
        self.message = message


class BotInitNotSupported(Exception):
    def __init__(self, message):
        self.message = message


class UnexpectedJobStatus(Exception):
    def __init__(self, message):
        self.message = message


class UnexpectedDataType(Exception):
    def __init__(self, message):
        self.message = message


class UnknownTaskStatus(Exception):
    def __init__(self, message):
        self.message = message


class TaskExpired(Exception):
    def __init__(self, message):
        self.message = message


class TaskExpiredMaxRetries(Exception):
    def __init__(self, message):
        self.message = message


class TaskResponseNull(Exception):
    def __init__(self, message):
        self.message = message


class TaskValueMissing(Exception):
    def __init__(self, message):
        self.message = message


class ChildJobFailed(Exception):
    def __init__(self, message):
        self.message = message


class ChildJobInternalError(Exception):
    def __init__(self, message):
        self.message = message


class CancelledError(Exception):
    def __init__(self, message):
        self.message = message


class MeasurerBaselineMismatch(Exception):
    def __init__(self, message):
        self.message = message


class TruthsPredictionsMisatch(Exception):
    def __init__(self, message):
        self.message = message


class MeasurerResponseNull(Exception):
    def __init__(self, message):
        self.message = message


class MeasurerConfigError(Exception):
    def __init__(self, message):
        self.message = message


class MiscMeasurerError(Exception):
    def __init__(self, message):
        self.message = message


class KeyMismatch(Exception):
    def __init__(self, message):
        self.message = message


class InsufficientBaseline(Exception):
    def __init__(self, message):
        self.message = message


class QualifierTaskExpired(Exception):
    def __init__(self, message):
        self.message = message
