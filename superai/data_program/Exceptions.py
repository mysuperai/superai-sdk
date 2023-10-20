class DataProgramError(Exception):
    def __init__(self, message):
        self.message = message


class EmptyPerformanceError(DataProgramError):
    def __init__(self, message):
        self.message = message


class UnsatisfiedMetricsError(DataProgramError):
    def __init__(self, message):
        self.message = message


class MetricNotImplementedError(DataProgramError):
    def __init__(self, message):
        self.message = message


class MetricCalculationFailed(DataProgramError):
    def __init__(self, message):
        self.message = message


class JobTypeNotImplemented(DataProgramError):
    def __init__(self, message):
        self.message = message


class PerformanceNotSet(DataProgramError):
    def __init__(self, message):
        self.message = message


class PerformanceNotReady(DataProgramError):
    def __init__(self, message):
        self.message = message


class BotInitNotSupported(DataProgramError):
    def __init__(self, message):
        self.message = message


class UnexpectedJobStatus(DataProgramError):
    def __init__(self, message):
        self.message = message


class UnexpectedDataType(DataProgramError):
    def __init__(self, message):
        self.message = message


class UnknownTaskStatus(DataProgramError):
    def __init__(self, message):
        self.message = message


class TaskExpired(DataProgramError):
    def __init__(self, message):
        self.message = message


class TaskExpiredMaxRetries(DataProgramError):
    def __init__(self, message):
        self.message = message


class TaskResponseNull(DataProgramError):
    def __init__(self, message):
        self.message = message


class TaskValueMissing(DataProgramError):
    def __init__(self, message):
        self.message = message


class ChildJobFailed(DataProgramError):
    def __init__(self, message):
        self.message = message


class ChildJobInternalError(DataProgramError):
    def __init__(self, message):
        self.message = message


class ChildJobExpired(DataProgramError):
    def __init__(self, message):
        self.message = message


class CancelledError(DataProgramError):
    def __init__(self, message):
        self.message = message


class MeasurerBaselineMismatch(DataProgramError):
    def __init__(self, message):
        self.message = message


class TruthsPredictionsMisatch(DataProgramError):
    def __init__(self, message):
        self.message = message


class MeasurerResponseNull(DataProgramError):
    def __init__(self, message):
        self.message = message


class MeasurerConfigError(DataProgramError):
    def __init__(self, message):
        self.message = message


class MiscMeasurerError(DataProgramError):
    def __init__(self, message):
        self.message = message


class KeyMismatch(DataProgramError):
    def __init__(self, message):
        self.message = message


class InsufficientBaseline(DataProgramError):
    def __init__(self, message):
        self.message = message


class QualifierTaskExpired(DataProgramError):
    def __init__(self, message):
        self.message = message
