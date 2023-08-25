from __future__ import annotations

import enum


class BaseAIOrchestrator(str, enum.Enum):
    pass


class Orchestrator(BaseAIOrchestrator):
    LOCAL_DOCKER = "LOCAL_DOCKER"
    LOCAL_DOCKER_K8S = "LOCAL_DOCKER_K8S"
    MINIKUBE = "MINIKUBE"
    AWS_EKS = "AWS_EKS"
    AWS_EKS_ASYNC = "AWS_EKS_ASYNC"


class TrainingOrchestrator(BaseAIOrchestrator):
    LOCAL_DOCKER_K8S = "LOCAL_DOCKER_K8S"
    AWS_EKS = "AWS_EKS"
