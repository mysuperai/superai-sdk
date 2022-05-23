import sgqlc.types

meta_ai_graphql_schema = sgqlc.types.Schema()


########################################################################
# Scalars and Enumerations
########################################################################
Boolean = sgqlc.types.Boolean

Float = sgqlc.types.Float


class InsertMetaAiModelMutationMetaAiEnvironmentEnum(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("DEV", "LOCAL", "PROD", "SANDBOX", "STAGING")


Int = sgqlc.types.Int

String = sgqlc.types.String


class bigint(sgqlc.types.Scalar):
    __schema__ = meta_ai_graphql_schema


class date(sgqlc.types.Scalar):
    __schema__ = meta_ai_graphql_schema


class float8(sgqlc.types.Scalar):
    __schema__ = meta_ai_graphql_schema


class json(sgqlc.types.Scalar):
    __schema__ = meta_ai_graphql_schema


class jsonb(sgqlc.types.Scalar):
    __schema__ = meta_ai_graphql_schema


class meta_ai_app_constraint(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("app_modelId_id_assigned_key", "app_pkey")


class meta_ai_app_select_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("active", "assigned", "id", "modelId", "threshold")


class meta_ai_app_update_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("active", "assigned", "id", "modelId", "threshold")


class meta_ai_assignment_constraint(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("assignment_pkey",)


class meta_ai_assignment_enum(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("ACTIVE_LEARNING", "LABEL", "PRELABEL", "RAW", "TASK")


class meta_ai_assignment_select_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("type",)


class meta_ai_assignment_update_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("type",)


class meta_ai_dataset_constraint(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("dataset_pkey",)


class meta_ai_dataset_metric_constraint(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("dataset_metric_pkey",)


class meta_ai_dataset_metric_select_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("created_at", "dataset_id", "id", "metric", "model_id", "updated_at")


class meta_ai_dataset_metric_update_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("created_at", "dataset_id", "id", "metric", "model_id", "updated_at")


class meta_ai_dataset_select_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("app_id", "created_at", "id", "metadata", "reference", "task_name", "updated_at")


class meta_ai_dataset_update_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("app_id", "created_at", "id", "metadata", "reference", "task_name", "updated_at")


class meta_ai_deployment_constraint(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("deployment_id_key", "deployment_pkey")


class meta_ai_deployment_log_constraint(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("deployment_log_pkey",)


class meta_ai_deployment_log_select_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("deployment_id", "id", "started_at", "stopped_at")


class meta_ai_deployment_log_update_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("deployment_id", "id", "started_at", "stopped_at")


class meta_ai_deployment_purpose_constraint(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("deployment_purpose_pkey",)


class meta_ai_deployment_purpose_enum(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("SERVING", "TRAINING")


class meta_ai_deployment_purpose_select_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("purpose",)


class meta_ai_deployment_purpose_update_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("purpose",)


class meta_ai_deployment_select_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = (
        "created_at",
        "current_log_id",
        "endpoint",
        "id",
        "image",
        "min_instances",
        "modelId",
        "ownerId",
        "properties",
        "purpose",
        "scale_in_timeout",
        "state_timestamp",
        "status",
        "target_status",
        "training_id",
        "type",
        "updated_at",
    )


class meta_ai_deployment_status_constraint(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("model_status_pkey",)


class meta_ai_deployment_status_enum(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("FAILED", "FINISHED", "MAINTENANCE", "OFFLINE", "ONLINE", "PAUSED", "STARTING", "UNKNOWN")


class meta_ai_deployment_status_select_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("status",)


class meta_ai_deployment_status_update_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("status",)


class meta_ai_deployment_type_constraint(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("deployment_type_pkey",)


class meta_ai_deployment_type_enum(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("AWS_EKS", "AWS_LAMBDA", "AWS_SAGEMAKER", "AWS_SAGEMAKER_ASYNC", "DUMMY", "EKS_POLYAXON")


class meta_ai_deployment_type_select_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("name",)


class meta_ai_deployment_type_update_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("name",)


class meta_ai_deployment_update_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = (
        "created_at",
        "current_log_id",
        "endpoint",
        "id",
        "image",
        "min_instances",
        "modelId",
        "ownerId",
        "properties",
        "purpose",
        "scale_in_timeout",
        "state_timestamp",
        "status",
        "target_status",
        "training_id",
        "type",
        "updated_at",
    )


class meta_ai_environment_constraint(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("environment_pkey",)


class meta_ai_environment_enum(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("DEV", "LOCAL", "PROD", "SANDBOX", "STAGING")


class meta_ai_environment_select_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("name",)


class meta_ai_environment_update_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("name",)


class meta_ai_instance_constraint(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("instance_pkey",)


class meta_ai_instance_select_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("id", "output", "predictionId", "score")


class meta_ai_instance_update_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("id", "output", "predictionId", "score")


class meta_ai_model_constraint(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = (
        "model_ai_worker_id_key",
        "model_ai_worker_username_key",
        "model_name_ownerId_version_key",
        "model_pkey",
    )


class meta_ai_model_select_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = (
        "ai_worker_id",
        "ai_worker_username",
        "createdAt",
        "default_training_parameters",
        "description",
        "editorId",
        "endpoint",
        "id",
        "image",
        "inputSchema",
        "metadata",
        "modelSavePath",
        "name",
        "outputSchema",
        "ownerId",
        "root_id",
        "served_by",
        "stage",
        "trainable",
        "updatedAt",
        "version",
        "visibility",
        "weightsPath",
    )


class meta_ai_model_update_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = (
        "ai_worker_id",
        "ai_worker_username",
        "createdAt",
        "default_training_parameters",
        "description",
        "editorId",
        "endpoint",
        "id",
        "image",
        "inputSchema",
        "metadata",
        "modelSavePath",
        "name",
        "outputSchema",
        "ownerId",
        "root_id",
        "served_by",
        "stage",
        "trainable",
        "updatedAt",
        "version",
        "visibility",
        "weightsPath",
    )


class meta_ai_prediction_constraint(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("prediction_modelId_jobId_type_taskId_key", "prediction_pkey")


class meta_ai_prediction_select_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = (
        "appId",
        "completedAt",
        "createdAt",
        "deploymentId",
        "errorMessage",
        "id",
        "jobId",
        "jobUUID",
        "modelId",
        "retries",
        "startedAt",
        "state",
        "taskId",
        "type",
    )


class meta_ai_prediction_state_constraint(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("prediction_state_pkey",)


class meta_ai_prediction_state_enum(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = (
        "CANCELED",
        "COMPLETED",
        "DELETED",
        "ENQUEUED",
        "EXPIRED",
        "FAILED",
        "INTERNAL_ERROR",
        "IN_PROGRESS",
        "PENDING",
        "SCHEDULED",
        "SUSPENDED",
    )


class meta_ai_prediction_state_select_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("state",)


class meta_ai_prediction_state_update_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("state",)


class meta_ai_prediction_update_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = (
        "appId",
        "completedAt",
        "createdAt",
        "deploymentId",
        "errorMessage",
        "id",
        "jobId",
        "jobUUID",
        "modelId",
        "retries",
        "startedAt",
        "state",
        "taskId",
        "type",
    )


class meta_ai_predictions_by_day_select_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("appId", "count", "day", "modelId", "type")


class meta_ai_task_registry_constraint(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("task_registry_pkey", "task_registry_task_name_app_id_key")


class meta_ai_task_registry_select_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("app_id", "id", "model_id", "task_name")


class meta_ai_task_registry_update_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("app_id", "id", "model_id", "task_name")


class meta_ai_training_instance_constraint(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("training_instance_pkey",)


class meta_ai_training_instance_select_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = (
        "artifacts",
        "createdAt",
        "currentProperties",
        "dataset_id",
        "deployment_id",
        "id",
        "modelId",
        "state",
        "trainingTemplateId",
        "updated_at",
    )


class meta_ai_training_instance_update_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = (
        "artifacts",
        "createdAt",
        "currentProperties",
        "dataset_id",
        "deployment_id",
        "id",
        "modelId",
        "state",
        "trainingTemplateId",
        "updated_at",
    )


class meta_ai_training_state_constraint(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("training_state_pkey",)


class meta_ai_training_state_enum(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("FINISHED", "INTERNAL_ERROR", "IN_PROGRESS", "STARTING", "STOPPED")


class meta_ai_training_state_select_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("state",)


class meta_ai_training_state_update_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("state",)


class meta_ai_training_template_constraint(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("training_template_modelId_appId_key", "training_template_pkey")


class meta_ai_training_template_select_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("appId", "createdAt", "description", "id", "modelId", "properties", "updated_at")


class meta_ai_training_template_update_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("appId", "createdAt", "description", "id", "modelId", "properties", "updated_at")


class meta_ai_visibility_constraint(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("visibility_pkey",)


class meta_ai_visibility_enum(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("PRIVATE", "PUBLIC")


class meta_ai_visibility_select_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("type",)


class meta_ai_visibility_update_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("type",)


class numeric(sgqlc.types.Scalar):
    __schema__ = meta_ai_graphql_schema


class order_by(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("asc", "asc_nulls_first", "asc_nulls_last", "desc", "desc_nulls_first", "desc_nulls_last")


class timestamp(sgqlc.types.Scalar):
    __schema__ = meta_ai_graphql_schema


class timestamptz(sgqlc.types.Scalar):
    __schema__ = meta_ai_graphql_schema


class turbine_app_constraint(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("app_pkey",)


class turbine_app_select_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("id",)


class turbine_app_update_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("id",)


class turbine_job_constraint(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("job_pkey",)


class turbine_job_select_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = (
        "created",
        "data",
        "id",
        "payload",
        "root_app_uuid",
        "started",
        "state",
        "type",
        "update_count",
        "workflow",
    )


class turbine_job_update_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = (
        "created",
        "data",
        "id",
        "payload",
        "root_app_uuid",
        "started",
        "state",
        "type",
        "update_count",
        "workflow",
    )


class turbine_task_constraint(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ("task_pkey",)


class turbine_task_select_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = (
        "app_id",
        "completed",
        "created",
        "id",
        "job_id",
        "name",
        "owner_id",
        "payload",
        "state",
        "update_count",
        "worker_type",
    )


class turbine_task_update_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = (
        "app_id",
        "completed",
        "created",
        "id",
        "job_id",
        "name",
        "owner_id",
        "payload",
        "state",
        "update_count",
        "worker_type",
    )


class uuid(sgqlc.types.Scalar):
    __schema__ = meta_ai_graphql_schema


########################################################################
# Input Objects
########################################################################
class Boolean_comparison_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("_eq", "_gt", "_gte", "_in", "_is_null", "_lt", "_lte", "_neq", "_nin")
    _eq = sgqlc.types.Field(Boolean, graphql_name="_eq")
    _gt = sgqlc.types.Field(Boolean, graphql_name="_gt")
    _gte = sgqlc.types.Field(Boolean, graphql_name="_gte")
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(Boolean)), graphql_name="_in")
    _is_null = sgqlc.types.Field(Boolean, graphql_name="_is_null")
    _lt = sgqlc.types.Field(Boolean, graphql_name="_lt")
    _lte = sgqlc.types.Field(Boolean, graphql_name="_lte")
    _neq = sgqlc.types.Field(Boolean, graphql_name="_neq")
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(Boolean)), graphql_name="_nin")


class Int_comparison_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("_eq", "_gt", "_gte", "_in", "_is_null", "_lt", "_lte", "_neq", "_nin")
    _eq = sgqlc.types.Field(Int, graphql_name="_eq")
    _gt = sgqlc.types.Field(Int, graphql_name="_gt")
    _gte = sgqlc.types.Field(Int, graphql_name="_gte")
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(Int)), graphql_name="_in")
    _is_null = sgqlc.types.Field(Boolean, graphql_name="_is_null")
    _lt = sgqlc.types.Field(Int, graphql_name="_lt")
    _lte = sgqlc.types.Field(Int, graphql_name="_lte")
    _neq = sgqlc.types.Field(Int, graphql_name="_neq")
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(Int)), graphql_name="_nin")


class PredictionRequest(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("data", "deployment_id", "model_id", "parameters")
    data = sgqlc.types.Field(json, graphql_name="data")
    deployment_id = sgqlc.types.Field(uuid, graphql_name="deployment_id")
    model_id = sgqlc.types.Field(uuid, graphql_name="model_id")
    parameters = sgqlc.types.Field(json, graphql_name="parameters")


class String_comparison_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "_eq",
        "_gt",
        "_gte",
        "_ilike",
        "_in",
        "_iregex",
        "_is_null",
        "_like",
        "_lt",
        "_lte",
        "_neq",
        "_nilike",
        "_nin",
        "_niregex",
        "_nlike",
        "_nregex",
        "_nsimilar",
        "_regex",
        "_similar",
    )
    _eq = sgqlc.types.Field(String, graphql_name="_eq")
    _gt = sgqlc.types.Field(String, graphql_name="_gt")
    _gte = sgqlc.types.Field(String, graphql_name="_gte")
    _ilike = sgqlc.types.Field(String, graphql_name="_ilike")
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name="_in")
    _iregex = sgqlc.types.Field(String, graphql_name="_iregex")
    _is_null = sgqlc.types.Field(Boolean, graphql_name="_is_null")
    _like = sgqlc.types.Field(String, graphql_name="_like")
    _lt = sgqlc.types.Field(String, graphql_name="_lt")
    _lte = sgqlc.types.Field(String, graphql_name="_lte")
    _neq = sgqlc.types.Field(String, graphql_name="_neq")
    _nilike = sgqlc.types.Field(String, graphql_name="_nilike")
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name="_nin")
    _niregex = sgqlc.types.Field(String, graphql_name="_niregex")
    _nlike = sgqlc.types.Field(String, graphql_name="_nlike")
    _nregex = sgqlc.types.Field(String, graphql_name="_nregex")
    _nsimilar = sgqlc.types.Field(String, graphql_name="_nsimilar")
    _regex = sgqlc.types.Field(String, graphql_name="_regex")
    _similar = sgqlc.types.Field(String, graphql_name="_similar")


class bigint_comparison_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("_eq", "_gt", "_gte", "_in", "_is_null", "_lt", "_lte", "_neq", "_nin")
    _eq = sgqlc.types.Field(bigint, graphql_name="_eq")
    _gt = sgqlc.types.Field(bigint, graphql_name="_gt")
    _gte = sgqlc.types.Field(bigint, graphql_name="_gte")
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(bigint)), graphql_name="_in")
    _is_null = sgqlc.types.Field(Boolean, graphql_name="_is_null")
    _lt = sgqlc.types.Field(bigint, graphql_name="_lt")
    _lte = sgqlc.types.Field(bigint, graphql_name="_lte")
    _neq = sgqlc.types.Field(bigint, graphql_name="_neq")
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(bigint)), graphql_name="_nin")


class date_comparison_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("_eq", "_gt", "_gte", "_in", "_is_null", "_lt", "_lte", "_neq", "_nin")
    _eq = sgqlc.types.Field(date, graphql_name="_eq")
    _gt = sgqlc.types.Field(date, graphql_name="_gt")
    _gte = sgqlc.types.Field(date, graphql_name="_gte")
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(date)), graphql_name="_in")
    _is_null = sgqlc.types.Field(Boolean, graphql_name="_is_null")
    _lt = sgqlc.types.Field(date, graphql_name="_lt")
    _lte = sgqlc.types.Field(date, graphql_name="_lte")
    _neq = sgqlc.types.Field(date, graphql_name="_neq")
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(date)), graphql_name="_nin")


class float8_comparison_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("_eq", "_gt", "_gte", "_in", "_is_null", "_lt", "_lte", "_neq", "_nin")
    _eq = sgqlc.types.Field(float8, graphql_name="_eq")
    _gt = sgqlc.types.Field(float8, graphql_name="_gt")
    _gte = sgqlc.types.Field(float8, graphql_name="_gte")
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(float8)), graphql_name="_in")
    _is_null = sgqlc.types.Field(Boolean, graphql_name="_is_null")
    _lt = sgqlc.types.Field(float8, graphql_name="_lt")
    _lte = sgqlc.types.Field(float8, graphql_name="_lte")
    _neq = sgqlc.types.Field(float8, graphql_name="_neq")
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(float8)), graphql_name="_nin")


class jsonb_comparison_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "_contained_in",
        "_contains",
        "_eq",
        "_gt",
        "_gte",
        "_has_key",
        "_has_keys_all",
        "_has_keys_any",
        "_in",
        "_is_null",
        "_lt",
        "_lte",
        "_neq",
        "_nin",
    )
    _contained_in = sgqlc.types.Field(jsonb, graphql_name="_contained_in")
    _contains = sgqlc.types.Field(jsonb, graphql_name="_contains")
    _eq = sgqlc.types.Field(jsonb, graphql_name="_eq")
    _gt = sgqlc.types.Field(jsonb, graphql_name="_gt")
    _gte = sgqlc.types.Field(jsonb, graphql_name="_gte")
    _has_key = sgqlc.types.Field(String, graphql_name="_has_key")
    _has_keys_all = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name="_has_keys_all")
    _has_keys_any = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name="_has_keys_any")
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(jsonb)), graphql_name="_in")
    _is_null = sgqlc.types.Field(Boolean, graphql_name="_is_null")
    _lt = sgqlc.types.Field(jsonb, graphql_name="_lt")
    _lte = sgqlc.types.Field(jsonb, graphql_name="_lte")
    _neq = sgqlc.types.Field(jsonb, graphql_name="_neq")
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(jsonb)), graphql_name="_nin")


class meta_ai_app_aggregate_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "avg",
        "count",
        "max",
        "min",
        "stddev",
        "stddev_pop",
        "stddev_samp",
        "sum",
        "var_pop",
        "var_samp",
        "variance",
    )
    avg = sgqlc.types.Field("meta_ai_app_avg_order_by", graphql_name="avg")
    count = sgqlc.types.Field(order_by, graphql_name="count")
    max = sgqlc.types.Field("meta_ai_app_max_order_by", graphql_name="max")
    min = sgqlc.types.Field("meta_ai_app_min_order_by", graphql_name="min")
    stddev = sgqlc.types.Field("meta_ai_app_stddev_order_by", graphql_name="stddev")
    stddev_pop = sgqlc.types.Field("meta_ai_app_stddev_pop_order_by", graphql_name="stddev_pop")
    stddev_samp = sgqlc.types.Field("meta_ai_app_stddev_samp_order_by", graphql_name="stddev_samp")
    sum = sgqlc.types.Field("meta_ai_app_sum_order_by", graphql_name="sum")
    var_pop = sgqlc.types.Field("meta_ai_app_var_pop_order_by", graphql_name="var_pop")
    var_samp = sgqlc.types.Field("meta_ai_app_var_samp_order_by", graphql_name="var_samp")
    variance = sgqlc.types.Field("meta_ai_app_variance_order_by", graphql_name="variance")


class meta_ai_app_arr_rel_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("data", "on_conflict")
    data = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_app_insert_input"))), graphql_name="data"
    )
    on_conflict = sgqlc.types.Field("meta_ai_app_on_conflict", graphql_name="on_conflict")


class meta_ai_app_avg_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("threshold",)
    threshold = sgqlc.types.Field(order_by, graphql_name="threshold")


class meta_ai_app_bool_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "_and",
        "_not",
        "_or",
        "active",
        "assigned",
        "id",
        "jobs",
        "model",
        "model_id",
        "predictions",
        "statistics",
        "threshold",
    )
    _and = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_app_bool_exp")), graphql_name="_and")
    _not = sgqlc.types.Field("meta_ai_app_bool_exp", graphql_name="_not")
    _or = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_app_bool_exp")), graphql_name="_or")
    active = sgqlc.types.Field(Boolean_comparison_exp, graphql_name="active")
    assigned = sgqlc.types.Field("meta_ai_assignment_enum_comparison_exp", graphql_name="assigned")
    id = sgqlc.types.Field("uuid_comparison_exp", graphql_name="id")
    jobs = sgqlc.types.Field("turbine_job_bool_exp", graphql_name="jobs")
    model = sgqlc.types.Field("meta_ai_model_bool_exp", graphql_name="model")
    model_id = sgqlc.types.Field("uuid_comparison_exp", graphql_name="modelId")
    predictions = sgqlc.types.Field("meta_ai_prediction_bool_exp", graphql_name="predictions")
    statistics = sgqlc.types.Field("meta_ai_predictions_by_day_bool_exp", graphql_name="statistics")
    threshold = sgqlc.types.Field("numeric_comparison_exp", graphql_name="threshold")


class meta_ai_app_inc_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("threshold",)
    threshold = sgqlc.types.Field(numeric, graphql_name="threshold")


class meta_ai_app_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "active",
        "assigned",
        "id",
        "jobs",
        "model",
        "model_id",
        "predictions",
        "statistics",
        "threshold",
    )
    active = sgqlc.types.Field(Boolean, graphql_name="active")
    assigned = sgqlc.types.Field(meta_ai_assignment_enum, graphql_name="assigned")
    id = sgqlc.types.Field(uuid, graphql_name="id")
    jobs = sgqlc.types.Field("turbine_job_arr_rel_insert_input", graphql_name="jobs")
    model = sgqlc.types.Field("meta_ai_model_obj_rel_insert_input", graphql_name="model")
    model_id = sgqlc.types.Field(uuid, graphql_name="modelId")
    predictions = sgqlc.types.Field("meta_ai_prediction_arr_rel_insert_input", graphql_name="predictions")
    statistics = sgqlc.types.Field("meta_ai_predictions_by_day_arr_rel_insert_input", graphql_name="statistics")
    threshold = sgqlc.types.Field(numeric, graphql_name="threshold")


class meta_ai_app_max_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "model_id", "threshold")
    id = sgqlc.types.Field(order_by, graphql_name="id")
    model_id = sgqlc.types.Field(order_by, graphql_name="modelId")
    threshold = sgqlc.types.Field(order_by, graphql_name="threshold")


class meta_ai_app_min_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "model_id", "threshold")
    id = sgqlc.types.Field(order_by, graphql_name="id")
    model_id = sgqlc.types.Field(order_by, graphql_name="modelId")
    threshold = sgqlc.types.Field(order_by, graphql_name="threshold")


class meta_ai_app_obj_rel_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("data", "on_conflict")
    data = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_app_insert_input), graphql_name="data")
    on_conflict = sgqlc.types.Field("meta_ai_app_on_conflict", graphql_name="on_conflict")


class meta_ai_app_on_conflict(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("constraint", "update_columns", "where")
    constraint = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_app_constraint), graphql_name="constraint")
    update_columns = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_app_update_column))),
        graphql_name="update_columns",
    )
    where = sgqlc.types.Field(meta_ai_app_bool_exp, graphql_name="where")


class meta_ai_app_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "active",
        "assigned",
        "id",
        "jobs_aggregate",
        "model",
        "model_id",
        "predictions_aggregate",
        "statistics_aggregate",
        "threshold",
    )
    active = sgqlc.types.Field(order_by, graphql_name="active")
    assigned = sgqlc.types.Field(order_by, graphql_name="assigned")
    id = sgqlc.types.Field(order_by, graphql_name="id")
    jobs_aggregate = sgqlc.types.Field("turbine_job_aggregate_order_by", graphql_name="jobs_aggregate")
    model = sgqlc.types.Field("meta_ai_model_order_by", graphql_name="model")
    model_id = sgqlc.types.Field(order_by, graphql_name="modelId")
    predictions_aggregate = sgqlc.types.Field(
        "meta_ai_prediction_aggregate_order_by", graphql_name="predictions_aggregate"
    )
    statistics_aggregate = sgqlc.types.Field(
        "meta_ai_predictions_by_day_aggregate_order_by", graphql_name="statistics_aggregate"
    )
    threshold = sgqlc.types.Field(order_by, graphql_name="threshold")


class meta_ai_app_pk_columns_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("assigned", "id", "model_id")
    assigned = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_assignment_enum), graphql_name="assigned")
    id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name="id")
    model_id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name="modelId")


class meta_ai_app_set_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("active", "assigned", "id", "model_id", "threshold")
    active = sgqlc.types.Field(Boolean, graphql_name="active")
    assigned = sgqlc.types.Field(meta_ai_assignment_enum, graphql_name="assigned")
    id = sgqlc.types.Field(uuid, graphql_name="id")
    model_id = sgqlc.types.Field(uuid, graphql_name="modelId")
    threshold = sgqlc.types.Field(numeric, graphql_name="threshold")


class meta_ai_app_stddev_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("threshold",)
    threshold = sgqlc.types.Field(order_by, graphql_name="threshold")


class meta_ai_app_stddev_pop_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("threshold",)
    threshold = sgqlc.types.Field(order_by, graphql_name="threshold")


class meta_ai_app_stddev_samp_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("threshold",)
    threshold = sgqlc.types.Field(order_by, graphql_name="threshold")


class meta_ai_app_sum_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("threshold",)
    threshold = sgqlc.types.Field(order_by, graphql_name="threshold")


class meta_ai_app_var_pop_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("threshold",)
    threshold = sgqlc.types.Field(order_by, graphql_name="threshold")


class meta_ai_app_var_samp_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("threshold",)
    threshold = sgqlc.types.Field(order_by, graphql_name="threshold")


class meta_ai_app_variance_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("threshold",)
    threshold = sgqlc.types.Field(order_by, graphql_name="threshold")


class meta_ai_assignment_bool_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("_and", "_not", "_or", "apps", "type")
    _and = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_assignment_bool_exp")), graphql_name="_and"
    )
    _not = sgqlc.types.Field("meta_ai_assignment_bool_exp", graphql_name="_not")
    _or = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_assignment_bool_exp")), graphql_name="_or"
    )
    apps = sgqlc.types.Field(meta_ai_app_bool_exp, graphql_name="apps")
    type = sgqlc.types.Field(String_comparison_exp, graphql_name="type")


class meta_ai_assignment_enum_comparison_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("_eq", "_in", "_is_null", "_neq", "_nin")
    _eq = sgqlc.types.Field(meta_ai_assignment_enum, graphql_name="_eq")
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_assignment_enum)), graphql_name="_in")
    _is_null = sgqlc.types.Field(Boolean, graphql_name="_is_null")
    _neq = sgqlc.types.Field(meta_ai_assignment_enum, graphql_name="_neq")
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_assignment_enum)), graphql_name="_nin")


class meta_ai_assignment_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("apps", "type")
    apps = sgqlc.types.Field(meta_ai_app_arr_rel_insert_input, graphql_name="apps")
    type = sgqlc.types.Field(String, graphql_name="type")


class meta_ai_assignment_on_conflict(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("constraint", "update_columns", "where")
    constraint = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_assignment_constraint), graphql_name="constraint")
    update_columns = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_assignment_update_column))),
        graphql_name="update_columns",
    )
    where = sgqlc.types.Field(meta_ai_assignment_bool_exp, graphql_name="where")


class meta_ai_assignment_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("apps_aggregate", "type")
    apps_aggregate = sgqlc.types.Field(meta_ai_app_aggregate_order_by, graphql_name="apps_aggregate")
    type = sgqlc.types.Field(order_by, graphql_name="type")


class meta_ai_assignment_pk_columns_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("type",)
    type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="type")


class meta_ai_assignment_set_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("type",)
    type = sgqlc.types.Field(String, graphql_name="type")


class meta_ai_dataset_aggregate_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("count", "max", "min")
    count = sgqlc.types.Field(order_by, graphql_name="count")
    max = sgqlc.types.Field("meta_ai_dataset_max_order_by", graphql_name="max")
    min = sgqlc.types.Field("meta_ai_dataset_min_order_by", graphql_name="min")


class meta_ai_dataset_append_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("metadata",)
    metadata = sgqlc.types.Field(jsonb, graphql_name="metadata")


class meta_ai_dataset_arr_rel_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("data", "on_conflict")
    data = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_dataset_insert_input"))),
        graphql_name="data",
    )
    on_conflict = sgqlc.types.Field("meta_ai_dataset_on_conflict", graphql_name="on_conflict")


class meta_ai_dataset_bool_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "_and",
        "_not",
        "_or",
        "app",
        "app_id",
        "created_at",
        "id",
        "metadata",
        "metrics",
        "reference",
        "task_name",
        "updated_at",
    )
    _and = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_dataset_bool_exp")), graphql_name="_and")
    _not = sgqlc.types.Field("meta_ai_dataset_bool_exp", graphql_name="_not")
    _or = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_dataset_bool_exp")), graphql_name="_or")
    app = sgqlc.types.Field("turbine_app_bool_exp", graphql_name="app")
    app_id = sgqlc.types.Field("uuid_comparison_exp", graphql_name="app_id")
    created_at = sgqlc.types.Field("timestamptz_comparison_exp", graphql_name="created_at")
    id = sgqlc.types.Field("uuid_comparison_exp", graphql_name="id")
    metadata = sgqlc.types.Field(jsonb_comparison_exp, graphql_name="metadata")
    metrics = sgqlc.types.Field("meta_ai_dataset_metric_bool_exp", graphql_name="metrics")
    reference = sgqlc.types.Field(String_comparison_exp, graphql_name="reference")
    task_name = sgqlc.types.Field(String_comparison_exp, graphql_name="task_name")
    updated_at = sgqlc.types.Field("timestamptz_comparison_exp", graphql_name="updated_at")


class meta_ai_dataset_delete_at_path_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("metadata",)
    metadata = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name="metadata")


class meta_ai_dataset_delete_elem_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("metadata",)
    metadata = sgqlc.types.Field(Int, graphql_name="metadata")


class meta_ai_dataset_delete_key_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("metadata",)
    metadata = sgqlc.types.Field(String, graphql_name="metadata")


class meta_ai_dataset_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "app",
        "app_id",
        "created_at",
        "id",
        "metadata",
        "metrics",
        "reference",
        "task_name",
        "updated_at",
    )
    app = sgqlc.types.Field("turbine_app_obj_rel_insert_input", graphql_name="app")
    app_id = sgqlc.types.Field(uuid, graphql_name="app_id")
    created_at = sgqlc.types.Field(timestamptz, graphql_name="created_at")
    id = sgqlc.types.Field(uuid, graphql_name="id")
    metadata = sgqlc.types.Field(jsonb, graphql_name="metadata")
    metrics = sgqlc.types.Field("meta_ai_dataset_metric_arr_rel_insert_input", graphql_name="metrics")
    reference = sgqlc.types.Field(String, graphql_name="reference")
    task_name = sgqlc.types.Field(String, graphql_name="task_name")
    updated_at = sgqlc.types.Field(timestamptz, graphql_name="updated_at")


class meta_ai_dataset_max_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("app_id", "created_at", "id", "reference", "task_name", "updated_at")
    app_id = sgqlc.types.Field(order_by, graphql_name="app_id")
    created_at = sgqlc.types.Field(order_by, graphql_name="created_at")
    id = sgqlc.types.Field(order_by, graphql_name="id")
    reference = sgqlc.types.Field(order_by, graphql_name="reference")
    task_name = sgqlc.types.Field(order_by, graphql_name="task_name")
    updated_at = sgqlc.types.Field(order_by, graphql_name="updated_at")


class meta_ai_dataset_metric_aggregate_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "avg",
        "count",
        "max",
        "min",
        "stddev",
        "stddev_pop",
        "stddev_samp",
        "sum",
        "var_pop",
        "var_samp",
        "variance",
    )
    avg = sgqlc.types.Field("meta_ai_dataset_metric_avg_order_by", graphql_name="avg")
    count = sgqlc.types.Field(order_by, graphql_name="count")
    max = sgqlc.types.Field("meta_ai_dataset_metric_max_order_by", graphql_name="max")
    min = sgqlc.types.Field("meta_ai_dataset_metric_min_order_by", graphql_name="min")
    stddev = sgqlc.types.Field("meta_ai_dataset_metric_stddev_order_by", graphql_name="stddev")
    stddev_pop = sgqlc.types.Field("meta_ai_dataset_metric_stddev_pop_order_by", graphql_name="stddev_pop")
    stddev_samp = sgqlc.types.Field("meta_ai_dataset_metric_stddev_samp_order_by", graphql_name="stddev_samp")
    sum = sgqlc.types.Field("meta_ai_dataset_metric_sum_order_by", graphql_name="sum")
    var_pop = sgqlc.types.Field("meta_ai_dataset_metric_var_pop_order_by", graphql_name="var_pop")
    var_samp = sgqlc.types.Field("meta_ai_dataset_metric_var_samp_order_by", graphql_name="var_samp")
    variance = sgqlc.types.Field("meta_ai_dataset_metric_variance_order_by", graphql_name="variance")


class meta_ai_dataset_metric_append_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("metric",)
    metric = sgqlc.types.Field(jsonb, graphql_name="metric")


class meta_ai_dataset_metric_arr_rel_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("data", "on_conflict")
    data = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_dataset_metric_insert_input"))),
        graphql_name="data",
    )
    on_conflict = sgqlc.types.Field("meta_ai_dataset_metric_on_conflict", graphql_name="on_conflict")


class meta_ai_dataset_metric_avg_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(order_by, graphql_name="id")


class meta_ai_dataset_metric_bool_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("_and", "_not", "_or", "created_at", "dataset_id", "id", "metric", "model_id", "updated_at")
    _and = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_dataset_metric_bool_exp")), graphql_name="_and"
    )
    _not = sgqlc.types.Field("meta_ai_dataset_metric_bool_exp", graphql_name="_not")
    _or = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_dataset_metric_bool_exp")), graphql_name="_or"
    )
    created_at = sgqlc.types.Field("timestamptz_comparison_exp", graphql_name="created_at")
    dataset_id = sgqlc.types.Field("uuid_comparison_exp", graphql_name="dataset_id")
    id = sgqlc.types.Field(Int_comparison_exp, graphql_name="id")
    metric = sgqlc.types.Field(jsonb_comparison_exp, graphql_name="metric")
    model_id = sgqlc.types.Field("uuid_comparison_exp", graphql_name="model_id")
    updated_at = sgqlc.types.Field("timestamptz_comparison_exp", graphql_name="updated_at")


class meta_ai_dataset_metric_delete_at_path_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("metric",)
    metric = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name="metric")


class meta_ai_dataset_metric_delete_elem_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("metric",)
    metric = sgqlc.types.Field(Int, graphql_name="metric")


class meta_ai_dataset_metric_delete_key_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("metric",)
    metric = sgqlc.types.Field(String, graphql_name="metric")


class meta_ai_dataset_metric_inc_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(Int, graphql_name="id")


class meta_ai_dataset_metric_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("created_at", "dataset_id", "id", "metric", "model_id", "updated_at")
    created_at = sgqlc.types.Field(timestamptz, graphql_name="created_at")
    dataset_id = sgqlc.types.Field(uuid, graphql_name="dataset_id")
    id = sgqlc.types.Field(Int, graphql_name="id")
    metric = sgqlc.types.Field(jsonb, graphql_name="metric")
    model_id = sgqlc.types.Field(uuid, graphql_name="model_id")
    updated_at = sgqlc.types.Field(timestamptz, graphql_name="updated_at")


class meta_ai_dataset_metric_max_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("created_at", "dataset_id", "id", "model_id", "updated_at")
    created_at = sgqlc.types.Field(order_by, graphql_name="created_at")
    dataset_id = sgqlc.types.Field(order_by, graphql_name="dataset_id")
    id = sgqlc.types.Field(order_by, graphql_name="id")
    model_id = sgqlc.types.Field(order_by, graphql_name="model_id")
    updated_at = sgqlc.types.Field(order_by, graphql_name="updated_at")


class meta_ai_dataset_metric_min_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("created_at", "dataset_id", "id", "model_id", "updated_at")
    created_at = sgqlc.types.Field(order_by, graphql_name="created_at")
    dataset_id = sgqlc.types.Field(order_by, graphql_name="dataset_id")
    id = sgqlc.types.Field(order_by, graphql_name="id")
    model_id = sgqlc.types.Field(order_by, graphql_name="model_id")
    updated_at = sgqlc.types.Field(order_by, graphql_name="updated_at")


class meta_ai_dataset_metric_on_conflict(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("constraint", "update_columns", "where")
    constraint = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_dataset_metric_constraint), graphql_name="constraint")
    update_columns = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_dataset_metric_update_column))),
        graphql_name="update_columns",
    )
    where = sgqlc.types.Field(meta_ai_dataset_metric_bool_exp, graphql_name="where")


class meta_ai_dataset_metric_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("created_at", "dataset_id", "id", "metric", "model_id", "updated_at")
    created_at = sgqlc.types.Field(order_by, graphql_name="created_at")
    dataset_id = sgqlc.types.Field(order_by, graphql_name="dataset_id")
    id = sgqlc.types.Field(order_by, graphql_name="id")
    metric = sgqlc.types.Field(order_by, graphql_name="metric")
    model_id = sgqlc.types.Field(order_by, graphql_name="model_id")
    updated_at = sgqlc.types.Field(order_by, graphql_name="updated_at")


class meta_ai_dataset_metric_pk_columns_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="id")


class meta_ai_dataset_metric_prepend_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("metric",)
    metric = sgqlc.types.Field(jsonb, graphql_name="metric")


class meta_ai_dataset_metric_set_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("created_at", "dataset_id", "id", "metric", "model_id", "updated_at")
    created_at = sgqlc.types.Field(timestamptz, graphql_name="created_at")
    dataset_id = sgqlc.types.Field(uuid, graphql_name="dataset_id")
    id = sgqlc.types.Field(Int, graphql_name="id")
    metric = sgqlc.types.Field(jsonb, graphql_name="metric")
    model_id = sgqlc.types.Field(uuid, graphql_name="model_id")
    updated_at = sgqlc.types.Field(timestamptz, graphql_name="updated_at")


class meta_ai_dataset_metric_stddev_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(order_by, graphql_name="id")


class meta_ai_dataset_metric_stddev_pop_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(order_by, graphql_name="id")


class meta_ai_dataset_metric_stddev_samp_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(order_by, graphql_name="id")


class meta_ai_dataset_metric_sum_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(order_by, graphql_name="id")


class meta_ai_dataset_metric_var_pop_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(order_by, graphql_name="id")


class meta_ai_dataset_metric_var_samp_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(order_by, graphql_name="id")


class meta_ai_dataset_metric_variance_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(order_by, graphql_name="id")


class meta_ai_dataset_min_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("app_id", "created_at", "id", "reference", "task_name", "updated_at")
    app_id = sgqlc.types.Field(order_by, graphql_name="app_id")
    created_at = sgqlc.types.Field(order_by, graphql_name="created_at")
    id = sgqlc.types.Field(order_by, graphql_name="id")
    reference = sgqlc.types.Field(order_by, graphql_name="reference")
    task_name = sgqlc.types.Field(order_by, graphql_name="task_name")
    updated_at = sgqlc.types.Field(order_by, graphql_name="updated_at")


class meta_ai_dataset_obj_rel_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("data", "on_conflict")
    data = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_dataset_insert_input), graphql_name="data")
    on_conflict = sgqlc.types.Field("meta_ai_dataset_on_conflict", graphql_name="on_conflict")


class meta_ai_dataset_on_conflict(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("constraint", "update_columns", "where")
    constraint = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_dataset_constraint), graphql_name="constraint")
    update_columns = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_dataset_update_column))),
        graphql_name="update_columns",
    )
    where = sgqlc.types.Field(meta_ai_dataset_bool_exp, graphql_name="where")


class meta_ai_dataset_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "app",
        "app_id",
        "created_at",
        "id",
        "metadata",
        "metrics_aggregate",
        "reference",
        "task_name",
        "updated_at",
    )
    app = sgqlc.types.Field("turbine_app_order_by", graphql_name="app")
    app_id = sgqlc.types.Field(order_by, graphql_name="app_id")
    created_at = sgqlc.types.Field(order_by, graphql_name="created_at")
    id = sgqlc.types.Field(order_by, graphql_name="id")
    metadata = sgqlc.types.Field(order_by, graphql_name="metadata")
    metrics_aggregate = sgqlc.types.Field(meta_ai_dataset_metric_aggregate_order_by, graphql_name="metrics_aggregate")
    reference = sgqlc.types.Field(order_by, graphql_name="reference")
    task_name = sgqlc.types.Field(order_by, graphql_name="task_name")
    updated_at = sgqlc.types.Field(order_by, graphql_name="updated_at")


class meta_ai_dataset_pk_columns_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name="id")


class meta_ai_dataset_prepend_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("metadata",)
    metadata = sgqlc.types.Field(jsonb, graphql_name="metadata")


class meta_ai_dataset_set_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("app_id", "created_at", "id", "metadata", "reference", "task_name", "updated_at")
    app_id = sgqlc.types.Field(uuid, graphql_name="app_id")
    created_at = sgqlc.types.Field(timestamptz, graphql_name="created_at")
    id = sgqlc.types.Field(uuid, graphql_name="id")
    metadata = sgqlc.types.Field(jsonb, graphql_name="metadata")
    reference = sgqlc.types.Field(String, graphql_name="reference")
    task_name = sgqlc.types.Field(String, graphql_name="task_name")
    updated_at = sgqlc.types.Field(timestamptz, graphql_name="updated_at")


class meta_ai_deployment_aggregate_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "avg",
        "count",
        "max",
        "min",
        "stddev",
        "stddev_pop",
        "stddev_samp",
        "sum",
        "var_pop",
        "var_samp",
        "variance",
    )
    avg = sgqlc.types.Field("meta_ai_deployment_avg_order_by", graphql_name="avg")
    count = sgqlc.types.Field(order_by, graphql_name="count")
    max = sgqlc.types.Field("meta_ai_deployment_max_order_by", graphql_name="max")
    min = sgqlc.types.Field("meta_ai_deployment_min_order_by", graphql_name="min")
    stddev = sgqlc.types.Field("meta_ai_deployment_stddev_order_by", graphql_name="stddev")
    stddev_pop = sgqlc.types.Field("meta_ai_deployment_stddev_pop_order_by", graphql_name="stddev_pop")
    stddev_samp = sgqlc.types.Field("meta_ai_deployment_stddev_samp_order_by", graphql_name="stddev_samp")
    sum = sgqlc.types.Field("meta_ai_deployment_sum_order_by", graphql_name="sum")
    var_pop = sgqlc.types.Field("meta_ai_deployment_var_pop_order_by", graphql_name="var_pop")
    var_samp = sgqlc.types.Field("meta_ai_deployment_var_samp_order_by", graphql_name="var_samp")
    variance = sgqlc.types.Field("meta_ai_deployment_variance_order_by", graphql_name="variance")


class meta_ai_deployment_append_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("properties",)
    properties = sgqlc.types.Field(jsonb, graphql_name="properties")


class meta_ai_deployment_arr_rel_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("data", "on_conflict")
    data = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_deployment_insert_input"))),
        graphql_name="data",
    )
    on_conflict = sgqlc.types.Field("meta_ai_deployment_on_conflict", graphql_name="on_conflict")


class meta_ai_deployment_avg_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("current_log_id", "min_instances", "owner_id", "scale_in_timeout")
    current_log_id = sgqlc.types.Field(order_by, graphql_name="current_log_id")
    min_instances = sgqlc.types.Field(order_by, graphql_name="min_instances")
    owner_id = sgqlc.types.Field(order_by, graphql_name="ownerId")
    scale_in_timeout = sgqlc.types.Field(order_by, graphql_name="scale_in_timeout")


class meta_ai_deployment_bool_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "_and",
        "_not",
        "_or",
        "created_at",
        "current_log",
        "current_log_id",
        "deployment_logs",
        "endpoint",
        "id",
        "image",
        "min_instances",
        "model",
        "model_id",
        "owner_id",
        "properties",
        "purpose",
        "scale_in_timeout",
        "state_timestamp",
        "status",
        "target_status",
        "training_id",
        "type",
        "updated_at",
    )
    _and = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_deployment_bool_exp")), graphql_name="_and"
    )
    _not = sgqlc.types.Field("meta_ai_deployment_bool_exp", graphql_name="_not")
    _or = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_deployment_bool_exp")), graphql_name="_or"
    )
    created_at = sgqlc.types.Field("timestamptz_comparison_exp", graphql_name="created_at")
    current_log = sgqlc.types.Field("meta_ai_deployment_log_bool_exp", graphql_name="current_log")
    current_log_id = sgqlc.types.Field(Int_comparison_exp, graphql_name="current_log_id")
    deployment_logs = sgqlc.types.Field("meta_ai_deployment_log_bool_exp", graphql_name="deployment_logs")
    endpoint = sgqlc.types.Field(String_comparison_exp, graphql_name="endpoint")
    id = sgqlc.types.Field("uuid_comparison_exp", graphql_name="id")
    image = sgqlc.types.Field(String_comparison_exp, graphql_name="image")
    min_instances = sgqlc.types.Field(Int_comparison_exp, graphql_name="min_instances")
    model = sgqlc.types.Field("meta_ai_model_bool_exp", graphql_name="model")
    model_id = sgqlc.types.Field("uuid_comparison_exp", graphql_name="modelId")
    owner_id = sgqlc.types.Field(bigint_comparison_exp, graphql_name="ownerId")
    properties = sgqlc.types.Field(jsonb_comparison_exp, graphql_name="properties")
    purpose = sgqlc.types.Field("meta_ai_deployment_purpose_enum_comparison_exp", graphql_name="purpose")
    scale_in_timeout = sgqlc.types.Field(Int_comparison_exp, graphql_name="scale_in_timeout")
    state_timestamp = sgqlc.types.Field("timestamptz_comparison_exp", graphql_name="state_timestamp")
    status = sgqlc.types.Field("meta_ai_deployment_status_enum_comparison_exp", graphql_name="status")
    target_status = sgqlc.types.Field("meta_ai_deployment_status_enum_comparison_exp", graphql_name="target_status")
    training_id = sgqlc.types.Field("uuid_comparison_exp", graphql_name="training_id")
    type = sgqlc.types.Field("meta_ai_deployment_type_enum_comparison_exp", graphql_name="type")
    updated_at = sgqlc.types.Field("timestamptz_comparison_exp", graphql_name="updated_at")


class meta_ai_deployment_delete_at_path_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("properties",)
    properties = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name="properties")


class meta_ai_deployment_delete_elem_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("properties",)
    properties = sgqlc.types.Field(Int, graphql_name="properties")


class meta_ai_deployment_delete_key_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("properties",)
    properties = sgqlc.types.Field(String, graphql_name="properties")


class meta_ai_deployment_inc_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("current_log_id", "min_instances", "owner_id", "scale_in_timeout")
    current_log_id = sgqlc.types.Field(Int, graphql_name="current_log_id")
    min_instances = sgqlc.types.Field(Int, graphql_name="min_instances")
    owner_id = sgqlc.types.Field(bigint, graphql_name="ownerId")
    scale_in_timeout = sgqlc.types.Field(Int, graphql_name="scale_in_timeout")


class meta_ai_deployment_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "created_at",
        "current_log",
        "current_log_id",
        "deployment_logs",
        "endpoint",
        "id",
        "image",
        "min_instances",
        "model",
        "model_id",
        "owner_id",
        "properties",
        "purpose",
        "scale_in_timeout",
        "state_timestamp",
        "status",
        "target_status",
        "training_id",
        "type",
        "updated_at",
    )
    created_at = sgqlc.types.Field(timestamptz, graphql_name="created_at")
    current_log = sgqlc.types.Field("meta_ai_deployment_log_obj_rel_insert_input", graphql_name="current_log")
    current_log_id = sgqlc.types.Field(Int, graphql_name="current_log_id")
    deployment_logs = sgqlc.types.Field("meta_ai_deployment_log_arr_rel_insert_input", graphql_name="deployment_logs")
    endpoint = sgqlc.types.Field(String, graphql_name="endpoint")
    id = sgqlc.types.Field(uuid, graphql_name="id")
    image = sgqlc.types.Field(String, graphql_name="image")
    min_instances = sgqlc.types.Field(Int, graphql_name="min_instances")
    model = sgqlc.types.Field("meta_ai_model_obj_rel_insert_input", graphql_name="model")
    model_id = sgqlc.types.Field(uuid, graphql_name="modelId")
    owner_id = sgqlc.types.Field(bigint, graphql_name="ownerId")
    properties = sgqlc.types.Field(jsonb, graphql_name="properties")
    purpose = sgqlc.types.Field(meta_ai_deployment_purpose_enum, graphql_name="purpose")
    scale_in_timeout = sgqlc.types.Field(Int, graphql_name="scale_in_timeout")
    state_timestamp = sgqlc.types.Field(timestamptz, graphql_name="state_timestamp")
    status = sgqlc.types.Field(meta_ai_deployment_status_enum, graphql_name="status")
    target_status = sgqlc.types.Field(meta_ai_deployment_status_enum, graphql_name="target_status")
    training_id = sgqlc.types.Field(uuid, graphql_name="training_id")
    type = sgqlc.types.Field(meta_ai_deployment_type_enum, graphql_name="type")
    updated_at = sgqlc.types.Field(timestamptz, graphql_name="updated_at")


class meta_ai_deployment_log_aggregate_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "avg",
        "count",
        "max",
        "min",
        "stddev",
        "stddev_pop",
        "stddev_samp",
        "sum",
        "var_pop",
        "var_samp",
        "variance",
    )
    avg = sgqlc.types.Field("meta_ai_deployment_log_avg_order_by", graphql_name="avg")
    count = sgqlc.types.Field(order_by, graphql_name="count")
    max = sgqlc.types.Field("meta_ai_deployment_log_max_order_by", graphql_name="max")
    min = sgqlc.types.Field("meta_ai_deployment_log_min_order_by", graphql_name="min")
    stddev = sgqlc.types.Field("meta_ai_deployment_log_stddev_order_by", graphql_name="stddev")
    stddev_pop = sgqlc.types.Field("meta_ai_deployment_log_stddev_pop_order_by", graphql_name="stddev_pop")
    stddev_samp = sgqlc.types.Field("meta_ai_deployment_log_stddev_samp_order_by", graphql_name="stddev_samp")
    sum = sgqlc.types.Field("meta_ai_deployment_log_sum_order_by", graphql_name="sum")
    var_pop = sgqlc.types.Field("meta_ai_deployment_log_var_pop_order_by", graphql_name="var_pop")
    var_samp = sgqlc.types.Field("meta_ai_deployment_log_var_samp_order_by", graphql_name="var_samp")
    variance = sgqlc.types.Field("meta_ai_deployment_log_variance_order_by", graphql_name="variance")


class meta_ai_deployment_log_arr_rel_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("data", "on_conflict")
    data = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_deployment_log_insert_input"))),
        graphql_name="data",
    )
    on_conflict = sgqlc.types.Field("meta_ai_deployment_log_on_conflict", graphql_name="on_conflict")


class meta_ai_deployment_log_avg_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(order_by, graphql_name="id")


class meta_ai_deployment_log_bool_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("_and", "_not", "_or", "deployment", "deployment_id", "id", "started_at", "stopped_at")
    _and = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_deployment_log_bool_exp")), graphql_name="_and"
    )
    _not = sgqlc.types.Field("meta_ai_deployment_log_bool_exp", graphql_name="_not")
    _or = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_deployment_log_bool_exp")), graphql_name="_or"
    )
    deployment = sgqlc.types.Field(meta_ai_deployment_bool_exp, graphql_name="deployment")
    deployment_id = sgqlc.types.Field("uuid_comparison_exp", graphql_name="deployment_id")
    id = sgqlc.types.Field(Int_comparison_exp, graphql_name="id")
    started_at = sgqlc.types.Field("timestamptz_comparison_exp", graphql_name="started_at")
    stopped_at = sgqlc.types.Field("timestamptz_comparison_exp", graphql_name="stopped_at")


class meta_ai_deployment_log_inc_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(Int, graphql_name="id")


class meta_ai_deployment_log_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("deployment", "deployment_id", "id", "started_at", "stopped_at")
    deployment = sgqlc.types.Field("meta_ai_deployment_obj_rel_insert_input", graphql_name="deployment")
    deployment_id = sgqlc.types.Field(uuid, graphql_name="deployment_id")
    id = sgqlc.types.Field(Int, graphql_name="id")
    started_at = sgqlc.types.Field(timestamptz, graphql_name="started_at")
    stopped_at = sgqlc.types.Field(timestamptz, graphql_name="stopped_at")


class meta_ai_deployment_log_max_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("deployment_id", "id", "started_at", "stopped_at")
    deployment_id = sgqlc.types.Field(order_by, graphql_name="deployment_id")
    id = sgqlc.types.Field(order_by, graphql_name="id")
    started_at = sgqlc.types.Field(order_by, graphql_name="started_at")
    stopped_at = sgqlc.types.Field(order_by, graphql_name="stopped_at")


class meta_ai_deployment_log_min_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("deployment_id", "id", "started_at", "stopped_at")
    deployment_id = sgqlc.types.Field(order_by, graphql_name="deployment_id")
    id = sgqlc.types.Field(order_by, graphql_name="id")
    started_at = sgqlc.types.Field(order_by, graphql_name="started_at")
    stopped_at = sgqlc.types.Field(order_by, graphql_name="stopped_at")


class meta_ai_deployment_log_obj_rel_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("data", "on_conflict")
    data = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_deployment_log_insert_input), graphql_name="data")
    on_conflict = sgqlc.types.Field("meta_ai_deployment_log_on_conflict", graphql_name="on_conflict")


class meta_ai_deployment_log_on_conflict(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("constraint", "update_columns", "where")
    constraint = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_deployment_log_constraint), graphql_name="constraint")
    update_columns = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_log_update_column))),
        graphql_name="update_columns",
    )
    where = sgqlc.types.Field(meta_ai_deployment_log_bool_exp, graphql_name="where")


class meta_ai_deployment_log_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("deployment", "deployment_id", "id", "started_at", "stopped_at")
    deployment = sgqlc.types.Field("meta_ai_deployment_order_by", graphql_name="deployment")
    deployment_id = sgqlc.types.Field(order_by, graphql_name="deployment_id")
    id = sgqlc.types.Field(order_by, graphql_name="id")
    started_at = sgqlc.types.Field(order_by, graphql_name="started_at")
    stopped_at = sgqlc.types.Field(order_by, graphql_name="stopped_at")


class meta_ai_deployment_log_pk_columns_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("deployment_id", "id")
    deployment_id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name="deployment_id")
    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="id")


class meta_ai_deployment_log_set_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("deployment_id", "id", "started_at", "stopped_at")
    deployment_id = sgqlc.types.Field(uuid, graphql_name="deployment_id")
    id = sgqlc.types.Field(Int, graphql_name="id")
    started_at = sgqlc.types.Field(timestamptz, graphql_name="started_at")
    stopped_at = sgqlc.types.Field(timestamptz, graphql_name="stopped_at")


class meta_ai_deployment_log_stddev_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(order_by, graphql_name="id")


class meta_ai_deployment_log_stddev_pop_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(order_by, graphql_name="id")


class meta_ai_deployment_log_stddev_samp_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(order_by, graphql_name="id")


class meta_ai_deployment_log_sum_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(order_by, graphql_name="id")


class meta_ai_deployment_log_var_pop_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(order_by, graphql_name="id")


class meta_ai_deployment_log_var_samp_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(order_by, graphql_name="id")


class meta_ai_deployment_log_variance_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(order_by, graphql_name="id")


class meta_ai_deployment_max_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "created_at",
        "current_log_id",
        "endpoint",
        "id",
        "image",
        "min_instances",
        "model_id",
        "owner_id",
        "scale_in_timeout",
        "state_timestamp",
        "training_id",
        "updated_at",
    )
    created_at = sgqlc.types.Field(order_by, graphql_name="created_at")
    current_log_id = sgqlc.types.Field(order_by, graphql_name="current_log_id")
    endpoint = sgqlc.types.Field(order_by, graphql_name="endpoint")
    id = sgqlc.types.Field(order_by, graphql_name="id")
    image = sgqlc.types.Field(order_by, graphql_name="image")
    min_instances = sgqlc.types.Field(order_by, graphql_name="min_instances")
    model_id = sgqlc.types.Field(order_by, graphql_name="modelId")
    owner_id = sgqlc.types.Field(order_by, graphql_name="ownerId")
    scale_in_timeout = sgqlc.types.Field(order_by, graphql_name="scale_in_timeout")
    state_timestamp = sgqlc.types.Field(order_by, graphql_name="state_timestamp")
    training_id = sgqlc.types.Field(order_by, graphql_name="training_id")
    updated_at = sgqlc.types.Field(order_by, graphql_name="updated_at")


class meta_ai_deployment_min_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "created_at",
        "current_log_id",
        "endpoint",
        "id",
        "image",
        "min_instances",
        "model_id",
        "owner_id",
        "scale_in_timeout",
        "state_timestamp",
        "training_id",
        "updated_at",
    )
    created_at = sgqlc.types.Field(order_by, graphql_name="created_at")
    current_log_id = sgqlc.types.Field(order_by, graphql_name="current_log_id")
    endpoint = sgqlc.types.Field(order_by, graphql_name="endpoint")
    id = sgqlc.types.Field(order_by, graphql_name="id")
    image = sgqlc.types.Field(order_by, graphql_name="image")
    min_instances = sgqlc.types.Field(order_by, graphql_name="min_instances")
    model_id = sgqlc.types.Field(order_by, graphql_name="modelId")
    owner_id = sgqlc.types.Field(order_by, graphql_name="ownerId")
    scale_in_timeout = sgqlc.types.Field(order_by, graphql_name="scale_in_timeout")
    state_timestamp = sgqlc.types.Field(order_by, graphql_name="state_timestamp")
    training_id = sgqlc.types.Field(order_by, graphql_name="training_id")
    updated_at = sgqlc.types.Field(order_by, graphql_name="updated_at")


class meta_ai_deployment_obj_rel_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("data", "on_conflict")
    data = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_deployment_insert_input), graphql_name="data")
    on_conflict = sgqlc.types.Field("meta_ai_deployment_on_conflict", graphql_name="on_conflict")


class meta_ai_deployment_on_conflict(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("constraint", "update_columns", "where")
    constraint = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_deployment_constraint), graphql_name="constraint")
    update_columns = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_update_column))),
        graphql_name="update_columns",
    )
    where = sgqlc.types.Field(meta_ai_deployment_bool_exp, graphql_name="where")


class meta_ai_deployment_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "created_at",
        "current_log",
        "current_log_id",
        "deployment_logs_aggregate",
        "endpoint",
        "id",
        "image",
        "min_instances",
        "model",
        "model_id",
        "owner_id",
        "properties",
        "purpose",
        "scale_in_timeout",
        "state_timestamp",
        "status",
        "target_status",
        "training_id",
        "type",
        "updated_at",
    )
    created_at = sgqlc.types.Field(order_by, graphql_name="created_at")
    current_log = sgqlc.types.Field(meta_ai_deployment_log_order_by, graphql_name="current_log")
    current_log_id = sgqlc.types.Field(order_by, graphql_name="current_log_id")
    deployment_logs_aggregate = sgqlc.types.Field(
        meta_ai_deployment_log_aggregate_order_by, graphql_name="deployment_logs_aggregate"
    )
    endpoint = sgqlc.types.Field(order_by, graphql_name="endpoint")
    id = sgqlc.types.Field(order_by, graphql_name="id")
    image = sgqlc.types.Field(order_by, graphql_name="image")
    min_instances = sgqlc.types.Field(order_by, graphql_name="min_instances")
    model = sgqlc.types.Field("meta_ai_model_order_by", graphql_name="model")
    model_id = sgqlc.types.Field(order_by, graphql_name="modelId")
    owner_id = sgqlc.types.Field(order_by, graphql_name="ownerId")
    properties = sgqlc.types.Field(order_by, graphql_name="properties")
    purpose = sgqlc.types.Field(order_by, graphql_name="purpose")
    scale_in_timeout = sgqlc.types.Field(order_by, graphql_name="scale_in_timeout")
    state_timestamp = sgqlc.types.Field(order_by, graphql_name="state_timestamp")
    status = sgqlc.types.Field(order_by, graphql_name="status")
    target_status = sgqlc.types.Field(order_by, graphql_name="target_status")
    training_id = sgqlc.types.Field(order_by, graphql_name="training_id")
    type = sgqlc.types.Field(order_by, graphql_name="type")
    updated_at = sgqlc.types.Field(order_by, graphql_name="updated_at")


class meta_ai_deployment_pk_columns_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name="id")


class meta_ai_deployment_prepend_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("properties",)
    properties = sgqlc.types.Field(jsonb, graphql_name="properties")


class meta_ai_deployment_purpose_bool_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("_and", "_not", "_or", "deployments", "purpose")
    _and = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_deployment_purpose_bool_exp")), graphql_name="_and"
    )
    _not = sgqlc.types.Field("meta_ai_deployment_purpose_bool_exp", graphql_name="_not")
    _or = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_deployment_purpose_bool_exp")), graphql_name="_or"
    )
    deployments = sgqlc.types.Field(meta_ai_deployment_bool_exp, graphql_name="deployments")
    purpose = sgqlc.types.Field(String_comparison_exp, graphql_name="purpose")


class meta_ai_deployment_purpose_enum_comparison_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("_eq", "_in", "_is_null", "_neq", "_nin")
    _eq = sgqlc.types.Field(meta_ai_deployment_purpose_enum, graphql_name="_eq")
    _in = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_purpose_enum)), graphql_name="_in"
    )
    _is_null = sgqlc.types.Field(Boolean, graphql_name="_is_null")
    _neq = sgqlc.types.Field(meta_ai_deployment_purpose_enum, graphql_name="_neq")
    _nin = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_purpose_enum)), graphql_name="_nin"
    )


class meta_ai_deployment_purpose_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("deployments", "purpose")
    deployments = sgqlc.types.Field(meta_ai_deployment_arr_rel_insert_input, graphql_name="deployments")
    purpose = sgqlc.types.Field(String, graphql_name="purpose")


class meta_ai_deployment_purpose_on_conflict(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("constraint", "update_columns", "where")
    constraint = sgqlc.types.Field(
        sgqlc.types.non_null(meta_ai_deployment_purpose_constraint), graphql_name="constraint"
    )
    update_columns = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_purpose_update_column))),
        graphql_name="update_columns",
    )
    where = sgqlc.types.Field(meta_ai_deployment_purpose_bool_exp, graphql_name="where")


class meta_ai_deployment_purpose_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("deployments_aggregate", "purpose")
    deployments_aggregate = sgqlc.types.Field(
        meta_ai_deployment_aggregate_order_by, graphql_name="deployments_aggregate"
    )
    purpose = sgqlc.types.Field(order_by, graphql_name="purpose")


class meta_ai_deployment_purpose_pk_columns_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("purpose",)
    purpose = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="purpose")


class meta_ai_deployment_purpose_set_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("purpose",)
    purpose = sgqlc.types.Field(String, graphql_name="purpose")


class meta_ai_deployment_set_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "created_at",
        "current_log_id",
        "endpoint",
        "id",
        "image",
        "min_instances",
        "model_id",
        "owner_id",
        "properties",
        "purpose",
        "scale_in_timeout",
        "state_timestamp",
        "status",
        "target_status",
        "training_id",
        "type",
        "updated_at",
    )
    created_at = sgqlc.types.Field(timestamptz, graphql_name="created_at")
    current_log_id = sgqlc.types.Field(Int, graphql_name="current_log_id")
    endpoint = sgqlc.types.Field(String, graphql_name="endpoint")
    id = sgqlc.types.Field(uuid, graphql_name="id")
    image = sgqlc.types.Field(String, graphql_name="image")
    min_instances = sgqlc.types.Field(Int, graphql_name="min_instances")
    model_id = sgqlc.types.Field(uuid, graphql_name="modelId")
    owner_id = sgqlc.types.Field(bigint, graphql_name="ownerId")
    properties = sgqlc.types.Field(jsonb, graphql_name="properties")
    purpose = sgqlc.types.Field(meta_ai_deployment_purpose_enum, graphql_name="purpose")
    scale_in_timeout = sgqlc.types.Field(Int, graphql_name="scale_in_timeout")
    state_timestamp = sgqlc.types.Field(timestamptz, graphql_name="state_timestamp")
    status = sgqlc.types.Field(meta_ai_deployment_status_enum, graphql_name="status")
    target_status = sgqlc.types.Field(meta_ai_deployment_status_enum, graphql_name="target_status")
    training_id = sgqlc.types.Field(uuid, graphql_name="training_id")
    type = sgqlc.types.Field(meta_ai_deployment_type_enum, graphql_name="type")
    updated_at = sgqlc.types.Field(timestamptz, graphql_name="updated_at")


class meta_ai_deployment_status_bool_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("_and", "_not", "_or", "deployments", "deployments_by_target_status", "status")
    _and = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_deployment_status_bool_exp")), graphql_name="_and"
    )
    _not = sgqlc.types.Field("meta_ai_deployment_status_bool_exp", graphql_name="_not")
    _or = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_deployment_status_bool_exp")), graphql_name="_or"
    )
    deployments = sgqlc.types.Field(meta_ai_deployment_bool_exp, graphql_name="deployments")
    deployments_by_target_status = sgqlc.types.Field(
        meta_ai_deployment_bool_exp, graphql_name="deploymentsByTargetStatus"
    )
    status = sgqlc.types.Field(String_comparison_exp, graphql_name="status")


class meta_ai_deployment_status_enum_comparison_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("_eq", "_in", "_is_null", "_neq", "_nin")
    _eq = sgqlc.types.Field(meta_ai_deployment_status_enum, graphql_name="_eq")
    _in = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_status_enum)), graphql_name="_in"
    )
    _is_null = sgqlc.types.Field(Boolean, graphql_name="_is_null")
    _neq = sgqlc.types.Field(meta_ai_deployment_status_enum, graphql_name="_neq")
    _nin = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_status_enum)), graphql_name="_nin"
    )


class meta_ai_deployment_status_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("deployments", "deployments_by_target_status", "status")
    deployments = sgqlc.types.Field(meta_ai_deployment_arr_rel_insert_input, graphql_name="deployments")
    deployments_by_target_status = sgqlc.types.Field(
        meta_ai_deployment_arr_rel_insert_input, graphql_name="deploymentsByTargetStatus"
    )
    status = sgqlc.types.Field(String, graphql_name="status")


class meta_ai_deployment_status_on_conflict(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("constraint", "update_columns", "where")
    constraint = sgqlc.types.Field(
        sgqlc.types.non_null(meta_ai_deployment_status_constraint), graphql_name="constraint"
    )
    update_columns = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_status_update_column))),
        graphql_name="update_columns",
    )
    where = sgqlc.types.Field(meta_ai_deployment_status_bool_exp, graphql_name="where")


class meta_ai_deployment_status_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("deployments_by_target_status_aggregate", "deployments_aggregate", "status")
    deployments_by_target_status_aggregate = sgqlc.types.Field(
        meta_ai_deployment_aggregate_order_by, graphql_name="deploymentsByTargetStatus_aggregate"
    )
    deployments_aggregate = sgqlc.types.Field(
        meta_ai_deployment_aggregate_order_by, graphql_name="deployments_aggregate"
    )
    status = sgqlc.types.Field(order_by, graphql_name="status")


class meta_ai_deployment_status_pk_columns_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("status",)
    status = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="status")


class meta_ai_deployment_status_set_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("status",)
    status = sgqlc.types.Field(String, graphql_name="status")


class meta_ai_deployment_stddev_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("current_log_id", "min_instances", "owner_id", "scale_in_timeout")
    current_log_id = sgqlc.types.Field(order_by, graphql_name="current_log_id")
    min_instances = sgqlc.types.Field(order_by, graphql_name="min_instances")
    owner_id = sgqlc.types.Field(order_by, graphql_name="ownerId")
    scale_in_timeout = sgqlc.types.Field(order_by, graphql_name="scale_in_timeout")


class meta_ai_deployment_stddev_pop_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("current_log_id", "min_instances", "owner_id", "scale_in_timeout")
    current_log_id = sgqlc.types.Field(order_by, graphql_name="current_log_id")
    min_instances = sgqlc.types.Field(order_by, graphql_name="min_instances")
    owner_id = sgqlc.types.Field(order_by, graphql_name="ownerId")
    scale_in_timeout = sgqlc.types.Field(order_by, graphql_name="scale_in_timeout")


class meta_ai_deployment_stddev_samp_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("current_log_id", "min_instances", "owner_id", "scale_in_timeout")
    current_log_id = sgqlc.types.Field(order_by, graphql_name="current_log_id")
    min_instances = sgqlc.types.Field(order_by, graphql_name="min_instances")
    owner_id = sgqlc.types.Field(order_by, graphql_name="ownerId")
    scale_in_timeout = sgqlc.types.Field(order_by, graphql_name="scale_in_timeout")


class meta_ai_deployment_sum_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("current_log_id", "min_instances", "owner_id", "scale_in_timeout")
    current_log_id = sgqlc.types.Field(order_by, graphql_name="current_log_id")
    min_instances = sgqlc.types.Field(order_by, graphql_name="min_instances")
    owner_id = sgqlc.types.Field(order_by, graphql_name="ownerId")
    scale_in_timeout = sgqlc.types.Field(order_by, graphql_name="scale_in_timeout")


class meta_ai_deployment_type_bool_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("_and", "_not", "_or", "deployments", "name")
    _and = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_deployment_type_bool_exp")), graphql_name="_and"
    )
    _not = sgqlc.types.Field("meta_ai_deployment_type_bool_exp", graphql_name="_not")
    _or = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_deployment_type_bool_exp")), graphql_name="_or"
    )
    deployments = sgqlc.types.Field(meta_ai_deployment_bool_exp, graphql_name="deployments")
    name = sgqlc.types.Field(String_comparison_exp, graphql_name="name")


class meta_ai_deployment_type_enum_comparison_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("_eq", "_in", "_is_null", "_neq", "_nin")
    _eq = sgqlc.types.Field(meta_ai_deployment_type_enum, graphql_name="_eq")
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_type_enum)), graphql_name="_in")
    _is_null = sgqlc.types.Field(Boolean, graphql_name="_is_null")
    _neq = sgqlc.types.Field(meta_ai_deployment_type_enum, graphql_name="_neq")
    _nin = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_type_enum)), graphql_name="_nin"
    )


class meta_ai_deployment_type_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("deployments", "name")
    deployments = sgqlc.types.Field(meta_ai_deployment_arr_rel_insert_input, graphql_name="deployments")
    name = sgqlc.types.Field(String, graphql_name="name")


class meta_ai_deployment_type_on_conflict(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("constraint", "update_columns", "where")
    constraint = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_deployment_type_constraint), graphql_name="constraint")
    update_columns = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_type_update_column))),
        graphql_name="update_columns",
    )
    where = sgqlc.types.Field(meta_ai_deployment_type_bool_exp, graphql_name="where")


class meta_ai_deployment_type_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("deployments_aggregate", "name")
    deployments_aggregate = sgqlc.types.Field(
        meta_ai_deployment_aggregate_order_by, graphql_name="deployments_aggregate"
    )
    name = sgqlc.types.Field(order_by, graphql_name="name")


class meta_ai_deployment_type_pk_columns_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("name",)
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")


class meta_ai_deployment_type_set_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("name",)
    name = sgqlc.types.Field(String, graphql_name="name")


class meta_ai_deployment_var_pop_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("current_log_id", "min_instances", "owner_id", "scale_in_timeout")
    current_log_id = sgqlc.types.Field(order_by, graphql_name="current_log_id")
    min_instances = sgqlc.types.Field(order_by, graphql_name="min_instances")
    owner_id = sgqlc.types.Field(order_by, graphql_name="ownerId")
    scale_in_timeout = sgqlc.types.Field(order_by, graphql_name="scale_in_timeout")


class meta_ai_deployment_var_samp_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("current_log_id", "min_instances", "owner_id", "scale_in_timeout")
    current_log_id = sgqlc.types.Field(order_by, graphql_name="current_log_id")
    min_instances = sgqlc.types.Field(order_by, graphql_name="min_instances")
    owner_id = sgqlc.types.Field(order_by, graphql_name="ownerId")
    scale_in_timeout = sgqlc.types.Field(order_by, graphql_name="scale_in_timeout")


class meta_ai_deployment_variance_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("current_log_id", "min_instances", "owner_id", "scale_in_timeout")
    current_log_id = sgqlc.types.Field(order_by, graphql_name="current_log_id")
    min_instances = sgqlc.types.Field(order_by, graphql_name="min_instances")
    owner_id = sgqlc.types.Field(order_by, graphql_name="ownerId")
    scale_in_timeout = sgqlc.types.Field(order_by, graphql_name="scale_in_timeout")


class meta_ai_environment_bool_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("_and", "_not", "_or", "name")
    _and = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_environment_bool_exp")), graphql_name="_and"
    )
    _not = sgqlc.types.Field("meta_ai_environment_bool_exp", graphql_name="_not")
    _or = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_environment_bool_exp")), graphql_name="_or"
    )
    name = sgqlc.types.Field(String_comparison_exp, graphql_name="name")


class meta_ai_environment_enum_comparison_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("_eq", "_in", "_is_null", "_neq", "_nin")
    _eq = sgqlc.types.Field(meta_ai_environment_enum, graphql_name="_eq")
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_environment_enum)), graphql_name="_in")
    _is_null = sgqlc.types.Field(Boolean, graphql_name="_is_null")
    _neq = sgqlc.types.Field(meta_ai_environment_enum, graphql_name="_neq")
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_environment_enum)), graphql_name="_nin")


class meta_ai_environment_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("name",)
    name = sgqlc.types.Field(String, graphql_name="name")


class meta_ai_environment_on_conflict(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("constraint", "update_columns", "where")
    constraint = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_environment_constraint), graphql_name="constraint")
    update_columns = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_environment_update_column))),
        graphql_name="update_columns",
    )
    where = sgqlc.types.Field(meta_ai_environment_bool_exp, graphql_name="where")


class meta_ai_environment_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("name",)
    name = sgqlc.types.Field(order_by, graphql_name="name")


class meta_ai_environment_pk_columns_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("name",)
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")


class meta_ai_environment_set_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("name",)
    name = sgqlc.types.Field(String, graphql_name="name")


class meta_ai_instance_aggregate_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "avg",
        "count",
        "max",
        "min",
        "stddev",
        "stddev_pop",
        "stddev_samp",
        "sum",
        "var_pop",
        "var_samp",
        "variance",
    )
    avg = sgqlc.types.Field("meta_ai_instance_avg_order_by", graphql_name="avg")
    count = sgqlc.types.Field(order_by, graphql_name="count")
    max = sgqlc.types.Field("meta_ai_instance_max_order_by", graphql_name="max")
    min = sgqlc.types.Field("meta_ai_instance_min_order_by", graphql_name="min")
    stddev = sgqlc.types.Field("meta_ai_instance_stddev_order_by", graphql_name="stddev")
    stddev_pop = sgqlc.types.Field("meta_ai_instance_stddev_pop_order_by", graphql_name="stddev_pop")
    stddev_samp = sgqlc.types.Field("meta_ai_instance_stddev_samp_order_by", graphql_name="stddev_samp")
    sum = sgqlc.types.Field("meta_ai_instance_sum_order_by", graphql_name="sum")
    var_pop = sgqlc.types.Field("meta_ai_instance_var_pop_order_by", graphql_name="var_pop")
    var_samp = sgqlc.types.Field("meta_ai_instance_var_samp_order_by", graphql_name="var_samp")
    variance = sgqlc.types.Field("meta_ai_instance_variance_order_by", graphql_name="variance")


class meta_ai_instance_append_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("output",)
    output = sgqlc.types.Field(jsonb, graphql_name="output")


class meta_ai_instance_arr_rel_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("data", "on_conflict")
    data = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_instance_insert_input"))),
        graphql_name="data",
    )
    on_conflict = sgqlc.types.Field("meta_ai_instance_on_conflict", graphql_name="on_conflict")


class meta_ai_instance_avg_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "score")
    id = sgqlc.types.Field(order_by, graphql_name="id")
    score = sgqlc.types.Field(order_by, graphql_name="score")


class meta_ai_instance_bool_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("_and", "_not", "_or", "id", "output", "prediction", "prediction_id", "score")
    _and = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_instance_bool_exp")), graphql_name="_and"
    )
    _not = sgqlc.types.Field("meta_ai_instance_bool_exp", graphql_name="_not")
    _or = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_instance_bool_exp")), graphql_name="_or")
    id = sgqlc.types.Field(Int_comparison_exp, graphql_name="id")
    output = sgqlc.types.Field(jsonb_comparison_exp, graphql_name="output")
    prediction = sgqlc.types.Field("meta_ai_prediction_bool_exp", graphql_name="prediction")
    prediction_id = sgqlc.types.Field("uuid_comparison_exp", graphql_name="predictionId")
    score = sgqlc.types.Field(float8_comparison_exp, graphql_name="score")


class meta_ai_instance_delete_at_path_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("output",)
    output = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name="output")


class meta_ai_instance_delete_elem_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("output",)
    output = sgqlc.types.Field(Int, graphql_name="output")


class meta_ai_instance_delete_key_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("output",)
    output = sgqlc.types.Field(String, graphql_name="output")


class meta_ai_instance_inc_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "score")
    id = sgqlc.types.Field(Int, graphql_name="id")
    score = sgqlc.types.Field(float8, graphql_name="score")


class meta_ai_instance_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "output", "prediction", "prediction_id", "score")
    id = sgqlc.types.Field(Int, graphql_name="id")
    output = sgqlc.types.Field(jsonb, graphql_name="output")
    prediction = sgqlc.types.Field("meta_ai_prediction_obj_rel_insert_input", graphql_name="prediction")
    prediction_id = sgqlc.types.Field(uuid, graphql_name="predictionId")
    score = sgqlc.types.Field(float8, graphql_name="score")


class meta_ai_instance_max_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "prediction_id", "score")
    id = sgqlc.types.Field(order_by, graphql_name="id")
    prediction_id = sgqlc.types.Field(order_by, graphql_name="predictionId")
    score = sgqlc.types.Field(order_by, graphql_name="score")


class meta_ai_instance_min_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "prediction_id", "score")
    id = sgqlc.types.Field(order_by, graphql_name="id")
    prediction_id = sgqlc.types.Field(order_by, graphql_name="predictionId")
    score = sgqlc.types.Field(order_by, graphql_name="score")


class meta_ai_instance_on_conflict(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("constraint", "update_columns", "where")
    constraint = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_instance_constraint), graphql_name="constraint")
    update_columns = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_instance_update_column))),
        graphql_name="update_columns",
    )
    where = sgqlc.types.Field(meta_ai_instance_bool_exp, graphql_name="where")


class meta_ai_instance_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "output", "prediction", "prediction_id", "score")
    id = sgqlc.types.Field(order_by, graphql_name="id")
    output = sgqlc.types.Field(order_by, graphql_name="output")
    prediction = sgqlc.types.Field("meta_ai_prediction_order_by", graphql_name="prediction")
    prediction_id = sgqlc.types.Field(order_by, graphql_name="predictionId")
    score = sgqlc.types.Field(order_by, graphql_name="score")


class meta_ai_instance_pk_columns_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "prediction_id")
    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="id")
    prediction_id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name="predictionId")


class meta_ai_instance_prepend_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("output",)
    output = sgqlc.types.Field(jsonb, graphql_name="output")


class meta_ai_instance_set_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "output", "prediction_id", "score")
    id = sgqlc.types.Field(Int, graphql_name="id")
    output = sgqlc.types.Field(jsonb, graphql_name="output")
    prediction_id = sgqlc.types.Field(uuid, graphql_name="predictionId")
    score = sgqlc.types.Field(float8, graphql_name="score")


class meta_ai_instance_stddev_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "score")
    id = sgqlc.types.Field(order_by, graphql_name="id")
    score = sgqlc.types.Field(order_by, graphql_name="score")


class meta_ai_instance_stddev_pop_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "score")
    id = sgqlc.types.Field(order_by, graphql_name="id")
    score = sgqlc.types.Field(order_by, graphql_name="score")


class meta_ai_instance_stddev_samp_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "score")
    id = sgqlc.types.Field(order_by, graphql_name="id")
    score = sgqlc.types.Field(order_by, graphql_name="score")


class meta_ai_instance_sum_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "score")
    id = sgqlc.types.Field(order_by, graphql_name="id")
    score = sgqlc.types.Field(order_by, graphql_name="score")


class meta_ai_instance_var_pop_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "score")
    id = sgqlc.types.Field(order_by, graphql_name="id")
    score = sgqlc.types.Field(order_by, graphql_name="score")


class meta_ai_instance_var_samp_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "score")
    id = sgqlc.types.Field(order_by, graphql_name="id")
    score = sgqlc.types.Field(order_by, graphql_name="score")


class meta_ai_instance_variance_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "score")
    id = sgqlc.types.Field(order_by, graphql_name="id")
    score = sgqlc.types.Field(order_by, graphql_name="score")


class meta_ai_model_aggregate_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "avg",
        "count",
        "max",
        "min",
        "stddev",
        "stddev_pop",
        "stddev_samp",
        "sum",
        "var_pop",
        "var_samp",
        "variance",
    )
    avg = sgqlc.types.Field("meta_ai_model_avg_order_by", graphql_name="avg")
    count = sgqlc.types.Field(order_by, graphql_name="count")
    max = sgqlc.types.Field("meta_ai_model_max_order_by", graphql_name="max")
    min = sgqlc.types.Field("meta_ai_model_min_order_by", graphql_name="min")
    stddev = sgqlc.types.Field("meta_ai_model_stddev_order_by", graphql_name="stddev")
    stddev_pop = sgqlc.types.Field("meta_ai_model_stddev_pop_order_by", graphql_name="stddev_pop")
    stddev_samp = sgqlc.types.Field("meta_ai_model_stddev_samp_order_by", graphql_name="stddev_samp")
    sum = sgqlc.types.Field("meta_ai_model_sum_order_by", graphql_name="sum")
    var_pop = sgqlc.types.Field("meta_ai_model_var_pop_order_by", graphql_name="var_pop")
    var_samp = sgqlc.types.Field("meta_ai_model_var_samp_order_by", graphql_name="var_samp")
    variance = sgqlc.types.Field("meta_ai_model_variance_order_by", graphql_name="variance")


class meta_ai_model_append_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("default_training_parameters", "input_schema", "metadata", "output_schema")
    default_training_parameters = sgqlc.types.Field(jsonb, graphql_name="default_training_parameters")
    input_schema = sgqlc.types.Field(jsonb, graphql_name="inputSchema")
    metadata = sgqlc.types.Field(jsonb, graphql_name="metadata")
    output_schema = sgqlc.types.Field(jsonb, graphql_name="outputSchema")


class meta_ai_model_arr_rel_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("data", "on_conflict")
    data = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_model_insert_input"))),
        graphql_name="data",
    )
    on_conflict = sgqlc.types.Field("meta_ai_model_on_conflict", graphql_name="on_conflict")


class meta_ai_model_avg_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("ai_worker_id", "editor_id", "owner_id", "version")
    ai_worker_id = sgqlc.types.Field(order_by, graphql_name="ai_worker_id")
    editor_id = sgqlc.types.Field(order_by, graphql_name="editorId")
    owner_id = sgqlc.types.Field(order_by, graphql_name="ownerId")
    version = sgqlc.types.Field(order_by, graphql_name="version")


class meta_ai_model_bool_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "_and",
        "_not",
        "_or",
        "ai_worker_id",
        "ai_worker_username",
        "apps",
        "created_at",
        "default_training_parameters",
        "deployment",
        "description",
        "editor_id",
        "endpoint",
        "id",
        "image",
        "input_schema",
        "metadata",
        "model_save_path",
        "name",
        "output_schema",
        "owner_id",
        "predictions",
        "root_id",
        "root_model",
        "served_by",
        "sibling_models",
        "stage",
        "trainable",
        "updated_at",
        "version",
        "visibility",
        "weights_path",
    )
    _and = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_model_bool_exp")), graphql_name="_and")
    _not = sgqlc.types.Field("meta_ai_model_bool_exp", graphql_name="_not")
    _or = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_model_bool_exp")), graphql_name="_or")
    ai_worker_id = sgqlc.types.Field(Int_comparison_exp, graphql_name="ai_worker_id")
    ai_worker_username = sgqlc.types.Field(String_comparison_exp, graphql_name="ai_worker_username")
    apps = sgqlc.types.Field(meta_ai_app_bool_exp, graphql_name="apps")
    created_at = sgqlc.types.Field("timestamptz_comparison_exp", graphql_name="createdAt")
    default_training_parameters = sgqlc.types.Field(jsonb_comparison_exp, graphql_name="default_training_parameters")
    deployment = sgqlc.types.Field(meta_ai_deployment_bool_exp, graphql_name="deployment")
    description = sgqlc.types.Field(String_comparison_exp, graphql_name="description")
    editor_id = sgqlc.types.Field(bigint_comparison_exp, graphql_name="editorId")
    endpoint = sgqlc.types.Field(String_comparison_exp, graphql_name="endpoint")
    id = sgqlc.types.Field("uuid_comparison_exp", graphql_name="id")
    image = sgqlc.types.Field(String_comparison_exp, graphql_name="image")
    input_schema = sgqlc.types.Field(jsonb_comparison_exp, graphql_name="inputSchema")
    metadata = sgqlc.types.Field(jsonb_comparison_exp, graphql_name="metadata")
    model_save_path = sgqlc.types.Field(String_comparison_exp, graphql_name="modelSavePath")
    name = sgqlc.types.Field(String_comparison_exp, graphql_name="name")
    output_schema = sgqlc.types.Field(jsonb_comparison_exp, graphql_name="outputSchema")
    owner_id = sgqlc.types.Field(bigint_comparison_exp, graphql_name="ownerId")
    predictions = sgqlc.types.Field("meta_ai_prediction_bool_exp", graphql_name="predictions")
    root_id = sgqlc.types.Field("uuid_comparison_exp", graphql_name="root_id")
    root_model = sgqlc.types.Field("meta_ai_model_bool_exp", graphql_name="root_model")
    served_by = sgqlc.types.Field("uuid_comparison_exp", graphql_name="served_by")
    sibling_models = sgqlc.types.Field("meta_ai_model_bool_exp", graphql_name="sibling_models")
    stage = sgqlc.types.Field(meta_ai_environment_enum_comparison_exp, graphql_name="stage")
    trainable = sgqlc.types.Field(Boolean_comparison_exp, graphql_name="trainable")
    updated_at = sgqlc.types.Field("timestamptz_comparison_exp", graphql_name="updatedAt")
    version = sgqlc.types.Field(Int_comparison_exp, graphql_name="version")
    visibility = sgqlc.types.Field("meta_ai_visibility_enum_comparison_exp", graphql_name="visibility")
    weights_path = sgqlc.types.Field(String_comparison_exp, graphql_name="weightsPath")


class meta_ai_model_delete_at_path_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("default_training_parameters", "input_schema", "metadata", "output_schema")
    default_training_parameters = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name="default_training_parameters"
    )
    input_schema = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name="inputSchema")
    metadata = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name="metadata")
    output_schema = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name="outputSchema")


class meta_ai_model_delete_elem_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("default_training_parameters", "input_schema", "metadata", "output_schema")
    default_training_parameters = sgqlc.types.Field(Int, graphql_name="default_training_parameters")
    input_schema = sgqlc.types.Field(Int, graphql_name="inputSchema")
    metadata = sgqlc.types.Field(Int, graphql_name="metadata")
    output_schema = sgqlc.types.Field(Int, graphql_name="outputSchema")


class meta_ai_model_delete_key_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("default_training_parameters", "input_schema", "metadata", "output_schema")
    default_training_parameters = sgqlc.types.Field(String, graphql_name="default_training_parameters")
    input_schema = sgqlc.types.Field(String, graphql_name="inputSchema")
    metadata = sgqlc.types.Field(String, graphql_name="metadata")
    output_schema = sgqlc.types.Field(String, graphql_name="outputSchema")


class meta_ai_model_inc_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("ai_worker_id", "editor_id", "owner_id", "version")
    ai_worker_id = sgqlc.types.Field(Int, graphql_name="ai_worker_id")
    editor_id = sgqlc.types.Field(bigint, graphql_name="editorId")
    owner_id = sgqlc.types.Field(bigint, graphql_name="ownerId")
    version = sgqlc.types.Field(Int, graphql_name="version")


class meta_ai_model_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "ai_worker_id",
        "ai_worker_username",
        "apps",
        "created_at",
        "default_training_parameters",
        "deployment",
        "description",
        "editor_id",
        "endpoint",
        "id",
        "image",
        "input_schema",
        "metadata",
        "model_save_path",
        "name",
        "output_schema",
        "owner_id",
        "predictions",
        "root_id",
        "root_model",
        "served_by",
        "sibling_models",
        "stage",
        "trainable",
        "updated_at",
        "version",
        "visibility",
        "weights_path",
    )
    ai_worker_id = sgqlc.types.Field(Int, graphql_name="ai_worker_id")
    ai_worker_username = sgqlc.types.Field(String, graphql_name="ai_worker_username")
    apps = sgqlc.types.Field(meta_ai_app_arr_rel_insert_input, graphql_name="apps")
    created_at = sgqlc.types.Field(timestamptz, graphql_name="createdAt")
    default_training_parameters = sgqlc.types.Field(jsonb, graphql_name="default_training_parameters")
    deployment = sgqlc.types.Field(meta_ai_deployment_obj_rel_insert_input, graphql_name="deployment")
    description = sgqlc.types.Field(String, graphql_name="description")
    editor_id = sgqlc.types.Field(bigint, graphql_name="editorId")
    endpoint = sgqlc.types.Field(String, graphql_name="endpoint")
    id = sgqlc.types.Field(uuid, graphql_name="id")
    image = sgqlc.types.Field(String, graphql_name="image")
    input_schema = sgqlc.types.Field(jsonb, graphql_name="inputSchema")
    metadata = sgqlc.types.Field(jsonb, graphql_name="metadata")
    model_save_path = sgqlc.types.Field(String, graphql_name="modelSavePath")
    name = sgqlc.types.Field(String, graphql_name="name")
    output_schema = sgqlc.types.Field(jsonb, graphql_name="outputSchema")
    owner_id = sgqlc.types.Field(bigint, graphql_name="ownerId")
    predictions = sgqlc.types.Field("meta_ai_prediction_arr_rel_insert_input", graphql_name="predictions")
    root_id = sgqlc.types.Field(uuid, graphql_name="root_id")
    root_model = sgqlc.types.Field("meta_ai_model_obj_rel_insert_input", graphql_name="root_model")
    served_by = sgqlc.types.Field(uuid, graphql_name="served_by")
    sibling_models = sgqlc.types.Field(meta_ai_model_arr_rel_insert_input, graphql_name="sibling_models")
    stage = sgqlc.types.Field(meta_ai_environment_enum, graphql_name="stage")
    trainable = sgqlc.types.Field(Boolean, graphql_name="trainable")
    updated_at = sgqlc.types.Field(timestamptz, graphql_name="updatedAt")
    version = sgqlc.types.Field(Int, graphql_name="version")
    visibility = sgqlc.types.Field(meta_ai_visibility_enum, graphql_name="visibility")
    weights_path = sgqlc.types.Field(String, graphql_name="weightsPath")


class meta_ai_model_max_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "ai_worker_id",
        "ai_worker_username",
        "created_at",
        "description",
        "editor_id",
        "endpoint",
        "id",
        "image",
        "model_save_path",
        "name",
        "owner_id",
        "root_id",
        "served_by",
        "updated_at",
        "version",
        "weights_path",
    )
    ai_worker_id = sgqlc.types.Field(order_by, graphql_name="ai_worker_id")
    ai_worker_username = sgqlc.types.Field(order_by, graphql_name="ai_worker_username")
    created_at = sgqlc.types.Field(order_by, graphql_name="createdAt")
    description = sgqlc.types.Field(order_by, graphql_name="description")
    editor_id = sgqlc.types.Field(order_by, graphql_name="editorId")
    endpoint = sgqlc.types.Field(order_by, graphql_name="endpoint")
    id = sgqlc.types.Field(order_by, graphql_name="id")
    image = sgqlc.types.Field(order_by, graphql_name="image")
    model_save_path = sgqlc.types.Field(order_by, graphql_name="modelSavePath")
    name = sgqlc.types.Field(order_by, graphql_name="name")
    owner_id = sgqlc.types.Field(order_by, graphql_name="ownerId")
    root_id = sgqlc.types.Field(order_by, graphql_name="root_id")
    served_by = sgqlc.types.Field(order_by, graphql_name="served_by")
    updated_at = sgqlc.types.Field(order_by, graphql_name="updatedAt")
    version = sgqlc.types.Field(order_by, graphql_name="version")
    weights_path = sgqlc.types.Field(order_by, graphql_name="weightsPath")


class meta_ai_model_min_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "ai_worker_id",
        "ai_worker_username",
        "created_at",
        "description",
        "editor_id",
        "endpoint",
        "id",
        "image",
        "model_save_path",
        "name",
        "owner_id",
        "root_id",
        "served_by",
        "updated_at",
        "version",
        "weights_path",
    )
    ai_worker_id = sgqlc.types.Field(order_by, graphql_name="ai_worker_id")
    ai_worker_username = sgqlc.types.Field(order_by, graphql_name="ai_worker_username")
    created_at = sgqlc.types.Field(order_by, graphql_name="createdAt")
    description = sgqlc.types.Field(order_by, graphql_name="description")
    editor_id = sgqlc.types.Field(order_by, graphql_name="editorId")
    endpoint = sgqlc.types.Field(order_by, graphql_name="endpoint")
    id = sgqlc.types.Field(order_by, graphql_name="id")
    image = sgqlc.types.Field(order_by, graphql_name="image")
    model_save_path = sgqlc.types.Field(order_by, graphql_name="modelSavePath")
    name = sgqlc.types.Field(order_by, graphql_name="name")
    owner_id = sgqlc.types.Field(order_by, graphql_name="ownerId")
    root_id = sgqlc.types.Field(order_by, graphql_name="root_id")
    served_by = sgqlc.types.Field(order_by, graphql_name="served_by")
    updated_at = sgqlc.types.Field(order_by, graphql_name="updatedAt")
    version = sgqlc.types.Field(order_by, graphql_name="version")
    weights_path = sgqlc.types.Field(order_by, graphql_name="weightsPath")


class meta_ai_model_obj_rel_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("data", "on_conflict")
    data = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_model_insert_input), graphql_name="data")
    on_conflict = sgqlc.types.Field("meta_ai_model_on_conflict", graphql_name="on_conflict")


class meta_ai_model_on_conflict(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("constraint", "update_columns", "where")
    constraint = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_model_constraint), graphql_name="constraint")
    update_columns = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_model_update_column))),
        graphql_name="update_columns",
    )
    where = sgqlc.types.Field(meta_ai_model_bool_exp, graphql_name="where")


class meta_ai_model_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "ai_worker_id",
        "ai_worker_username",
        "apps_aggregate",
        "created_at",
        "default_training_parameters",
        "deployment",
        "description",
        "editor_id",
        "endpoint",
        "id",
        "image",
        "input_schema",
        "metadata",
        "model_save_path",
        "name",
        "output_schema",
        "owner_id",
        "predictions_aggregate",
        "root_id",
        "root_model",
        "served_by",
        "sibling_models_aggregate",
        "stage",
        "trainable",
        "updated_at",
        "version",
        "visibility",
        "weights_path",
    )
    ai_worker_id = sgqlc.types.Field(order_by, graphql_name="ai_worker_id")
    ai_worker_username = sgqlc.types.Field(order_by, graphql_name="ai_worker_username")
    apps_aggregate = sgqlc.types.Field(meta_ai_app_aggregate_order_by, graphql_name="apps_aggregate")
    created_at = sgqlc.types.Field(order_by, graphql_name="createdAt")
    default_training_parameters = sgqlc.types.Field(order_by, graphql_name="default_training_parameters")
    deployment = sgqlc.types.Field(meta_ai_deployment_order_by, graphql_name="deployment")
    description = sgqlc.types.Field(order_by, graphql_name="description")
    editor_id = sgqlc.types.Field(order_by, graphql_name="editorId")
    endpoint = sgqlc.types.Field(order_by, graphql_name="endpoint")
    id = sgqlc.types.Field(order_by, graphql_name="id")
    image = sgqlc.types.Field(order_by, graphql_name="image")
    input_schema = sgqlc.types.Field(order_by, graphql_name="inputSchema")
    metadata = sgqlc.types.Field(order_by, graphql_name="metadata")
    model_save_path = sgqlc.types.Field(order_by, graphql_name="modelSavePath")
    name = sgqlc.types.Field(order_by, graphql_name="name")
    output_schema = sgqlc.types.Field(order_by, graphql_name="outputSchema")
    owner_id = sgqlc.types.Field(order_by, graphql_name="ownerId")
    predictions_aggregate = sgqlc.types.Field(
        "meta_ai_prediction_aggregate_order_by", graphql_name="predictions_aggregate"
    )
    root_id = sgqlc.types.Field(order_by, graphql_name="root_id")
    root_model = sgqlc.types.Field("meta_ai_model_order_by", graphql_name="root_model")
    served_by = sgqlc.types.Field(order_by, graphql_name="served_by")
    sibling_models_aggregate = sgqlc.types.Field(
        meta_ai_model_aggregate_order_by, graphql_name="sibling_models_aggregate"
    )
    stage = sgqlc.types.Field(order_by, graphql_name="stage")
    trainable = sgqlc.types.Field(order_by, graphql_name="trainable")
    updated_at = sgqlc.types.Field(order_by, graphql_name="updatedAt")
    version = sgqlc.types.Field(order_by, graphql_name="version")
    visibility = sgqlc.types.Field(order_by, graphql_name="visibility")
    weights_path = sgqlc.types.Field(order_by, graphql_name="weightsPath")


class meta_ai_model_pk_columns_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name="id")


class meta_ai_model_prepend_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("default_training_parameters", "input_schema", "metadata", "output_schema")
    default_training_parameters = sgqlc.types.Field(jsonb, graphql_name="default_training_parameters")
    input_schema = sgqlc.types.Field(jsonb, graphql_name="inputSchema")
    metadata = sgqlc.types.Field(jsonb, graphql_name="metadata")
    output_schema = sgqlc.types.Field(jsonb, graphql_name="outputSchema")


class meta_ai_model_set_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "ai_worker_id",
        "ai_worker_username",
        "created_at",
        "default_training_parameters",
        "description",
        "editor_id",
        "endpoint",
        "id",
        "image",
        "input_schema",
        "metadata",
        "model_save_path",
        "name",
        "output_schema",
        "owner_id",
        "root_id",
        "served_by",
        "stage",
        "trainable",
        "updated_at",
        "version",
        "visibility",
        "weights_path",
    )
    ai_worker_id = sgqlc.types.Field(Int, graphql_name="ai_worker_id")
    ai_worker_username = sgqlc.types.Field(String, graphql_name="ai_worker_username")
    created_at = sgqlc.types.Field(timestamptz, graphql_name="createdAt")
    default_training_parameters = sgqlc.types.Field(jsonb, graphql_name="default_training_parameters")
    description = sgqlc.types.Field(String, graphql_name="description")
    editor_id = sgqlc.types.Field(bigint, graphql_name="editorId")
    endpoint = sgqlc.types.Field(String, graphql_name="endpoint")
    id = sgqlc.types.Field(uuid, graphql_name="id")
    image = sgqlc.types.Field(String, graphql_name="image")
    input_schema = sgqlc.types.Field(jsonb, graphql_name="inputSchema")
    metadata = sgqlc.types.Field(jsonb, graphql_name="metadata")
    model_save_path = sgqlc.types.Field(String, graphql_name="modelSavePath")
    name = sgqlc.types.Field(String, graphql_name="name")
    output_schema = sgqlc.types.Field(jsonb, graphql_name="outputSchema")
    owner_id = sgqlc.types.Field(bigint, graphql_name="ownerId")
    root_id = sgqlc.types.Field(uuid, graphql_name="root_id")
    served_by = sgqlc.types.Field(uuid, graphql_name="served_by")
    stage = sgqlc.types.Field(meta_ai_environment_enum, graphql_name="stage")
    trainable = sgqlc.types.Field(Boolean, graphql_name="trainable")
    updated_at = sgqlc.types.Field(timestamptz, graphql_name="updatedAt")
    version = sgqlc.types.Field(Int, graphql_name="version")
    visibility = sgqlc.types.Field(meta_ai_visibility_enum, graphql_name="visibility")
    weights_path = sgqlc.types.Field(String, graphql_name="weightsPath")


class meta_ai_model_stddev_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("ai_worker_id", "editor_id", "owner_id", "version")
    ai_worker_id = sgqlc.types.Field(order_by, graphql_name="ai_worker_id")
    editor_id = sgqlc.types.Field(order_by, graphql_name="editorId")
    owner_id = sgqlc.types.Field(order_by, graphql_name="ownerId")
    version = sgqlc.types.Field(order_by, graphql_name="version")


class meta_ai_model_stddev_pop_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("ai_worker_id", "editor_id", "owner_id", "version")
    ai_worker_id = sgqlc.types.Field(order_by, graphql_name="ai_worker_id")
    editor_id = sgqlc.types.Field(order_by, graphql_name="editorId")
    owner_id = sgqlc.types.Field(order_by, graphql_name="ownerId")
    version = sgqlc.types.Field(order_by, graphql_name="version")


class meta_ai_model_stddev_samp_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("ai_worker_id", "editor_id", "owner_id", "version")
    ai_worker_id = sgqlc.types.Field(order_by, graphql_name="ai_worker_id")
    editor_id = sgqlc.types.Field(order_by, graphql_name="editorId")
    owner_id = sgqlc.types.Field(order_by, graphql_name="ownerId")
    version = sgqlc.types.Field(order_by, graphql_name="version")


class meta_ai_model_sum_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("ai_worker_id", "editor_id", "owner_id", "version")
    ai_worker_id = sgqlc.types.Field(order_by, graphql_name="ai_worker_id")
    editor_id = sgqlc.types.Field(order_by, graphql_name="editorId")
    owner_id = sgqlc.types.Field(order_by, graphql_name="ownerId")
    version = sgqlc.types.Field(order_by, graphql_name="version")


class meta_ai_model_var_pop_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("ai_worker_id", "editor_id", "owner_id", "version")
    ai_worker_id = sgqlc.types.Field(order_by, graphql_name="ai_worker_id")
    editor_id = sgqlc.types.Field(order_by, graphql_name="editorId")
    owner_id = sgqlc.types.Field(order_by, graphql_name="ownerId")
    version = sgqlc.types.Field(order_by, graphql_name="version")


class meta_ai_model_var_samp_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("ai_worker_id", "editor_id", "owner_id", "version")
    ai_worker_id = sgqlc.types.Field(order_by, graphql_name="ai_worker_id")
    editor_id = sgqlc.types.Field(order_by, graphql_name="editorId")
    owner_id = sgqlc.types.Field(order_by, graphql_name="ownerId")
    version = sgqlc.types.Field(order_by, graphql_name="version")


class meta_ai_model_variance_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("ai_worker_id", "editor_id", "owner_id", "version")
    ai_worker_id = sgqlc.types.Field(order_by, graphql_name="ai_worker_id")
    editor_id = sgqlc.types.Field(order_by, graphql_name="editorId")
    owner_id = sgqlc.types.Field(order_by, graphql_name="ownerId")
    version = sgqlc.types.Field(order_by, graphql_name="version")


class meta_ai_prediction_aggregate_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "avg",
        "count",
        "max",
        "min",
        "stddev",
        "stddev_pop",
        "stddev_samp",
        "sum",
        "var_pop",
        "var_samp",
        "variance",
    )
    avg = sgqlc.types.Field("meta_ai_prediction_avg_order_by", graphql_name="avg")
    count = sgqlc.types.Field(order_by, graphql_name="count")
    max = sgqlc.types.Field("meta_ai_prediction_max_order_by", graphql_name="max")
    min = sgqlc.types.Field("meta_ai_prediction_min_order_by", graphql_name="min")
    stddev = sgqlc.types.Field("meta_ai_prediction_stddev_order_by", graphql_name="stddev")
    stddev_pop = sgqlc.types.Field("meta_ai_prediction_stddev_pop_order_by", graphql_name="stddev_pop")
    stddev_samp = sgqlc.types.Field("meta_ai_prediction_stddev_samp_order_by", graphql_name="stddev_samp")
    sum = sgqlc.types.Field("meta_ai_prediction_sum_order_by", graphql_name="sum")
    var_pop = sgqlc.types.Field("meta_ai_prediction_var_pop_order_by", graphql_name="var_pop")
    var_samp = sgqlc.types.Field("meta_ai_prediction_var_samp_order_by", graphql_name="var_samp")
    variance = sgqlc.types.Field("meta_ai_prediction_variance_order_by", graphql_name="variance")


class meta_ai_prediction_arr_rel_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("data", "on_conflict")
    data = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_prediction_insert_input"))),
        graphql_name="data",
    )
    on_conflict = sgqlc.types.Field("meta_ai_prediction_on_conflict", graphql_name="on_conflict")


class meta_ai_prediction_avg_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("job_id", "retries", "task_id")
    job_id = sgqlc.types.Field(order_by, graphql_name="jobId")
    retries = sgqlc.types.Field(order_by, graphql_name="retries")
    task_id = sgqlc.types.Field(order_by, graphql_name="taskId")


class meta_ai_prediction_bool_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "_and",
        "_not",
        "_or",
        "app",
        "app_id",
        "completed_at",
        "created_at",
        "deployment",
        "deployment_id",
        "error_message",
        "id",
        "instances",
        "job",
        "job_id",
        "job_uuid",
        "model",
        "model_id",
        "retries",
        "started_at",
        "state",
        "task",
        "task_id",
        "type",
    )
    _and = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_prediction_bool_exp")), graphql_name="_and"
    )
    _not = sgqlc.types.Field("meta_ai_prediction_bool_exp", graphql_name="_not")
    _or = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_prediction_bool_exp")), graphql_name="_or"
    )
    app = sgqlc.types.Field(meta_ai_app_bool_exp, graphql_name="app")
    app_id = sgqlc.types.Field("uuid_comparison_exp", graphql_name="appId")
    completed_at = sgqlc.types.Field("timestamptz_comparison_exp", graphql_name="completedAt")
    created_at = sgqlc.types.Field("timestamptz_comparison_exp", graphql_name="createdAt")
    deployment = sgqlc.types.Field(meta_ai_deployment_bool_exp, graphql_name="deployment")
    deployment_id = sgqlc.types.Field("uuid_comparison_exp", graphql_name="deploymentId")
    error_message = sgqlc.types.Field(String_comparison_exp, graphql_name="errorMessage")
    id = sgqlc.types.Field("uuid_comparison_exp", graphql_name="id")
    instances = sgqlc.types.Field(meta_ai_instance_bool_exp, graphql_name="instances")
    job = sgqlc.types.Field("turbine_job_bool_exp", graphql_name="job")
    job_id = sgqlc.types.Field(bigint_comparison_exp, graphql_name="jobId")
    job_uuid = sgqlc.types.Field("uuid_comparison_exp", graphql_name="jobUUID")
    model = sgqlc.types.Field(meta_ai_model_bool_exp, graphql_name="model")
    model_id = sgqlc.types.Field("uuid_comparison_exp", graphql_name="modelId")
    retries = sgqlc.types.Field(Int_comparison_exp, graphql_name="retries")
    started_at = sgqlc.types.Field("timestamptz_comparison_exp", graphql_name="startedAt")
    state = sgqlc.types.Field("meta_ai_prediction_state_enum_comparison_exp", graphql_name="state")
    task = sgqlc.types.Field("turbine_task_bool_exp", graphql_name="task")
    task_id = sgqlc.types.Field(bigint_comparison_exp, graphql_name="taskId")
    type = sgqlc.types.Field(meta_ai_assignment_enum_comparison_exp, graphql_name="type")


class meta_ai_prediction_inc_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("job_id", "retries", "task_id")
    job_id = sgqlc.types.Field(bigint, graphql_name="jobId")
    retries = sgqlc.types.Field(Int, graphql_name="retries")
    task_id = sgqlc.types.Field(bigint, graphql_name="taskId")


class meta_ai_prediction_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "app",
        "app_id",
        "completed_at",
        "created_at",
        "deployment",
        "deployment_id",
        "error_message",
        "id",
        "instances",
        "job",
        "job_id",
        "job_uuid",
        "model",
        "model_id",
        "retries",
        "started_at",
        "state",
        "task",
        "task_id",
        "type",
    )
    app = sgqlc.types.Field(meta_ai_app_obj_rel_insert_input, graphql_name="app")
    app_id = sgqlc.types.Field(uuid, graphql_name="appId")
    completed_at = sgqlc.types.Field(timestamptz, graphql_name="completedAt")
    created_at = sgqlc.types.Field(timestamptz, graphql_name="createdAt")
    deployment = sgqlc.types.Field(meta_ai_deployment_obj_rel_insert_input, graphql_name="deployment")
    deployment_id = sgqlc.types.Field(uuid, graphql_name="deploymentId")
    error_message = sgqlc.types.Field(String, graphql_name="errorMessage")
    id = sgqlc.types.Field(uuid, graphql_name="id")
    instances = sgqlc.types.Field(meta_ai_instance_arr_rel_insert_input, graphql_name="instances")
    job = sgqlc.types.Field("turbine_job_obj_rel_insert_input", graphql_name="job")
    job_id = sgqlc.types.Field(bigint, graphql_name="jobId")
    job_uuid = sgqlc.types.Field(uuid, graphql_name="jobUUID")
    model = sgqlc.types.Field(meta_ai_model_obj_rel_insert_input, graphql_name="model")
    model_id = sgqlc.types.Field(uuid, graphql_name="modelId")
    retries = sgqlc.types.Field(Int, graphql_name="retries")
    started_at = sgqlc.types.Field(timestamptz, graphql_name="startedAt")
    state = sgqlc.types.Field(meta_ai_prediction_state_enum, graphql_name="state")
    task = sgqlc.types.Field("turbine_task_obj_rel_insert_input", graphql_name="task")
    task_id = sgqlc.types.Field(bigint, graphql_name="taskId")
    type = sgqlc.types.Field(meta_ai_assignment_enum, graphql_name="type")


class meta_ai_prediction_max_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "app_id",
        "completed_at",
        "created_at",
        "deployment_id",
        "error_message",
        "id",
        "job_id",
        "job_uuid",
        "model_id",
        "retries",
        "started_at",
        "task_id",
    )
    app_id = sgqlc.types.Field(order_by, graphql_name="appId")
    completed_at = sgqlc.types.Field(order_by, graphql_name="completedAt")
    created_at = sgqlc.types.Field(order_by, graphql_name="createdAt")
    deployment_id = sgqlc.types.Field(order_by, graphql_name="deploymentId")
    error_message = sgqlc.types.Field(order_by, graphql_name="errorMessage")
    id = sgqlc.types.Field(order_by, graphql_name="id")
    job_id = sgqlc.types.Field(order_by, graphql_name="jobId")
    job_uuid = sgqlc.types.Field(order_by, graphql_name="jobUUID")
    model_id = sgqlc.types.Field(order_by, graphql_name="modelId")
    retries = sgqlc.types.Field(order_by, graphql_name="retries")
    started_at = sgqlc.types.Field(order_by, graphql_name="startedAt")
    task_id = sgqlc.types.Field(order_by, graphql_name="taskId")


class meta_ai_prediction_min_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "app_id",
        "completed_at",
        "created_at",
        "deployment_id",
        "error_message",
        "id",
        "job_id",
        "job_uuid",
        "model_id",
        "retries",
        "started_at",
        "task_id",
    )
    app_id = sgqlc.types.Field(order_by, graphql_name="appId")
    completed_at = sgqlc.types.Field(order_by, graphql_name="completedAt")
    created_at = sgqlc.types.Field(order_by, graphql_name="createdAt")
    deployment_id = sgqlc.types.Field(order_by, graphql_name="deploymentId")
    error_message = sgqlc.types.Field(order_by, graphql_name="errorMessage")
    id = sgqlc.types.Field(order_by, graphql_name="id")
    job_id = sgqlc.types.Field(order_by, graphql_name="jobId")
    job_uuid = sgqlc.types.Field(order_by, graphql_name="jobUUID")
    model_id = sgqlc.types.Field(order_by, graphql_name="modelId")
    retries = sgqlc.types.Field(order_by, graphql_name="retries")
    started_at = sgqlc.types.Field(order_by, graphql_name="startedAt")
    task_id = sgqlc.types.Field(order_by, graphql_name="taskId")


class meta_ai_prediction_obj_rel_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("data", "on_conflict")
    data = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_prediction_insert_input), graphql_name="data")
    on_conflict = sgqlc.types.Field("meta_ai_prediction_on_conflict", graphql_name="on_conflict")


class meta_ai_prediction_on_conflict(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("constraint", "update_columns", "where")
    constraint = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_prediction_constraint), graphql_name="constraint")
    update_columns = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_update_column))),
        graphql_name="update_columns",
    )
    where = sgqlc.types.Field(meta_ai_prediction_bool_exp, graphql_name="where")


class meta_ai_prediction_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "app",
        "app_id",
        "completed_at",
        "created_at",
        "deployment",
        "deployment_id",
        "error_message",
        "id",
        "instances_aggregate",
        "job",
        "job_id",
        "job_uuid",
        "model",
        "model_id",
        "retries",
        "started_at",
        "state",
        "task",
        "task_id",
        "type",
    )
    app = sgqlc.types.Field(meta_ai_app_order_by, graphql_name="app")
    app_id = sgqlc.types.Field(order_by, graphql_name="appId")
    completed_at = sgqlc.types.Field(order_by, graphql_name="completedAt")
    created_at = sgqlc.types.Field(order_by, graphql_name="createdAt")
    deployment = sgqlc.types.Field(meta_ai_deployment_order_by, graphql_name="deployment")
    deployment_id = sgqlc.types.Field(order_by, graphql_name="deploymentId")
    error_message = sgqlc.types.Field(order_by, graphql_name="errorMessage")
    id = sgqlc.types.Field(order_by, graphql_name="id")
    instances_aggregate = sgqlc.types.Field(meta_ai_instance_aggregate_order_by, graphql_name="instances_aggregate")
    job = sgqlc.types.Field("turbine_job_order_by", graphql_name="job")
    job_id = sgqlc.types.Field(order_by, graphql_name="jobId")
    job_uuid = sgqlc.types.Field(order_by, graphql_name="jobUUID")
    model = sgqlc.types.Field(meta_ai_model_order_by, graphql_name="model")
    model_id = sgqlc.types.Field(order_by, graphql_name="modelId")
    retries = sgqlc.types.Field(order_by, graphql_name="retries")
    started_at = sgqlc.types.Field(order_by, graphql_name="startedAt")
    state = sgqlc.types.Field(order_by, graphql_name="state")
    task = sgqlc.types.Field("turbine_task_order_by", graphql_name="task")
    task_id = sgqlc.types.Field(order_by, graphql_name="taskId")
    type = sgqlc.types.Field(order_by, graphql_name="type")


class meta_ai_prediction_pk_columns_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name="id")


class meta_ai_prediction_set_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "app_id",
        "completed_at",
        "created_at",
        "deployment_id",
        "error_message",
        "id",
        "job_id",
        "job_uuid",
        "model_id",
        "retries",
        "started_at",
        "state",
        "task_id",
        "type",
    )
    app_id = sgqlc.types.Field(uuid, graphql_name="appId")
    completed_at = sgqlc.types.Field(timestamptz, graphql_name="completedAt")
    created_at = sgqlc.types.Field(timestamptz, graphql_name="createdAt")
    deployment_id = sgqlc.types.Field(uuid, graphql_name="deploymentId")
    error_message = sgqlc.types.Field(String, graphql_name="errorMessage")
    id = sgqlc.types.Field(uuid, graphql_name="id")
    job_id = sgqlc.types.Field(bigint, graphql_name="jobId")
    job_uuid = sgqlc.types.Field(uuid, graphql_name="jobUUID")
    model_id = sgqlc.types.Field(uuid, graphql_name="modelId")
    retries = sgqlc.types.Field(Int, graphql_name="retries")
    started_at = sgqlc.types.Field(timestamptz, graphql_name="startedAt")
    state = sgqlc.types.Field(meta_ai_prediction_state_enum, graphql_name="state")
    task_id = sgqlc.types.Field(bigint, graphql_name="taskId")
    type = sgqlc.types.Field(meta_ai_assignment_enum, graphql_name="type")


class meta_ai_prediction_state_bool_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("_and", "_not", "_or", "predictions", "state")
    _and = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_prediction_state_bool_exp")), graphql_name="_and"
    )
    _not = sgqlc.types.Field("meta_ai_prediction_state_bool_exp", graphql_name="_not")
    _or = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_prediction_state_bool_exp")), graphql_name="_or"
    )
    predictions = sgqlc.types.Field(meta_ai_prediction_bool_exp, graphql_name="predictions")
    state = sgqlc.types.Field(String_comparison_exp, graphql_name="state")


class meta_ai_prediction_state_enum_comparison_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("_eq", "_in", "_is_null", "_neq", "_nin")
    _eq = sgqlc.types.Field(meta_ai_prediction_state_enum, graphql_name="_eq")
    _in = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_state_enum)), graphql_name="_in"
    )
    _is_null = sgqlc.types.Field(Boolean, graphql_name="_is_null")
    _neq = sgqlc.types.Field(meta_ai_prediction_state_enum, graphql_name="_neq")
    _nin = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_state_enum)), graphql_name="_nin"
    )


class meta_ai_prediction_state_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("predictions", "state")
    predictions = sgqlc.types.Field(meta_ai_prediction_arr_rel_insert_input, graphql_name="predictions")
    state = sgqlc.types.Field(String, graphql_name="state")


class meta_ai_prediction_state_on_conflict(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("constraint", "update_columns", "where")
    constraint = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_prediction_state_constraint), graphql_name="constraint")
    update_columns = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_state_update_column))),
        graphql_name="update_columns",
    )
    where = sgqlc.types.Field(meta_ai_prediction_state_bool_exp, graphql_name="where")


class meta_ai_prediction_state_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("predictions_aggregate", "state")
    predictions_aggregate = sgqlc.types.Field(
        meta_ai_prediction_aggregate_order_by, graphql_name="predictions_aggregate"
    )
    state = sgqlc.types.Field(order_by, graphql_name="state")


class meta_ai_prediction_state_pk_columns_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("state",)
    state = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="state")


class meta_ai_prediction_state_set_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("state",)
    state = sgqlc.types.Field(String, graphql_name="state")


class meta_ai_prediction_stddev_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("job_id", "retries", "task_id")
    job_id = sgqlc.types.Field(order_by, graphql_name="jobId")
    retries = sgqlc.types.Field(order_by, graphql_name="retries")
    task_id = sgqlc.types.Field(order_by, graphql_name="taskId")


class meta_ai_prediction_stddev_pop_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("job_id", "retries", "task_id")
    job_id = sgqlc.types.Field(order_by, graphql_name="jobId")
    retries = sgqlc.types.Field(order_by, graphql_name="retries")
    task_id = sgqlc.types.Field(order_by, graphql_name="taskId")


class meta_ai_prediction_stddev_samp_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("job_id", "retries", "task_id")
    job_id = sgqlc.types.Field(order_by, graphql_name="jobId")
    retries = sgqlc.types.Field(order_by, graphql_name="retries")
    task_id = sgqlc.types.Field(order_by, graphql_name="taskId")


class meta_ai_prediction_sum_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("job_id", "retries", "task_id")
    job_id = sgqlc.types.Field(order_by, graphql_name="jobId")
    retries = sgqlc.types.Field(order_by, graphql_name="retries")
    task_id = sgqlc.types.Field(order_by, graphql_name="taskId")


class meta_ai_prediction_var_pop_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("job_id", "retries", "task_id")
    job_id = sgqlc.types.Field(order_by, graphql_name="jobId")
    retries = sgqlc.types.Field(order_by, graphql_name="retries")
    task_id = sgqlc.types.Field(order_by, graphql_name="taskId")


class meta_ai_prediction_var_samp_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("job_id", "retries", "task_id")
    job_id = sgqlc.types.Field(order_by, graphql_name="jobId")
    retries = sgqlc.types.Field(order_by, graphql_name="retries")
    task_id = sgqlc.types.Field(order_by, graphql_name="taskId")


class meta_ai_prediction_variance_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("job_id", "retries", "task_id")
    job_id = sgqlc.types.Field(order_by, graphql_name="jobId")
    retries = sgqlc.types.Field(order_by, graphql_name="retries")
    task_id = sgqlc.types.Field(order_by, graphql_name="taskId")


class meta_ai_predictions_by_day_aggregate_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "avg",
        "count",
        "max",
        "min",
        "stddev",
        "stddev_pop",
        "stddev_samp",
        "sum",
        "var_pop",
        "var_samp",
        "variance",
    )
    avg = sgqlc.types.Field("meta_ai_predictions_by_day_avg_order_by", graphql_name="avg")
    count = sgqlc.types.Field(order_by, graphql_name="count")
    max = sgqlc.types.Field("meta_ai_predictions_by_day_max_order_by", graphql_name="max")
    min = sgqlc.types.Field("meta_ai_predictions_by_day_min_order_by", graphql_name="min")
    stddev = sgqlc.types.Field("meta_ai_predictions_by_day_stddev_order_by", graphql_name="stddev")
    stddev_pop = sgqlc.types.Field("meta_ai_predictions_by_day_stddev_pop_order_by", graphql_name="stddev_pop")
    stddev_samp = sgqlc.types.Field("meta_ai_predictions_by_day_stddev_samp_order_by", graphql_name="stddev_samp")
    sum = sgqlc.types.Field("meta_ai_predictions_by_day_sum_order_by", graphql_name="sum")
    var_pop = sgqlc.types.Field("meta_ai_predictions_by_day_var_pop_order_by", graphql_name="var_pop")
    var_samp = sgqlc.types.Field("meta_ai_predictions_by_day_var_samp_order_by", graphql_name="var_samp")
    variance = sgqlc.types.Field("meta_ai_predictions_by_day_variance_order_by", graphql_name="variance")


class meta_ai_predictions_by_day_arr_rel_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("data",)
    data = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_predictions_by_day_insert_input"))),
        graphql_name="data",
    )


class meta_ai_predictions_by_day_avg_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("count",)
    count = sgqlc.types.Field(order_by, graphql_name="count")


class meta_ai_predictions_by_day_bool_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("_and", "_not", "_or", "app_id", "count", "day", "model_id", "type")
    _and = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_predictions_by_day_bool_exp")), graphql_name="_and"
    )
    _not = sgqlc.types.Field("meta_ai_predictions_by_day_bool_exp", graphql_name="_not")
    _or = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_predictions_by_day_bool_exp")), graphql_name="_or"
    )
    app_id = sgqlc.types.Field("uuid_comparison_exp", graphql_name="appId")
    count = sgqlc.types.Field(bigint_comparison_exp, graphql_name="count")
    day = sgqlc.types.Field(date_comparison_exp, graphql_name="day")
    model_id = sgqlc.types.Field("uuid_comparison_exp", graphql_name="modelId")
    type = sgqlc.types.Field(String_comparison_exp, graphql_name="type")


class meta_ai_predictions_by_day_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("app_id", "count", "day", "model_id", "type")
    app_id = sgqlc.types.Field(uuid, graphql_name="appId")
    count = sgqlc.types.Field(bigint, graphql_name="count")
    day = sgqlc.types.Field(date, graphql_name="day")
    model_id = sgqlc.types.Field(uuid, graphql_name="modelId")
    type = sgqlc.types.Field(String, graphql_name="type")


class meta_ai_predictions_by_day_max_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("app_id", "count", "day", "model_id", "type")
    app_id = sgqlc.types.Field(order_by, graphql_name="appId")
    count = sgqlc.types.Field(order_by, graphql_name="count")
    day = sgqlc.types.Field(order_by, graphql_name="day")
    model_id = sgqlc.types.Field(order_by, graphql_name="modelId")
    type = sgqlc.types.Field(order_by, graphql_name="type")


class meta_ai_predictions_by_day_min_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("app_id", "count", "day", "model_id", "type")
    app_id = sgqlc.types.Field(order_by, graphql_name="appId")
    count = sgqlc.types.Field(order_by, graphql_name="count")
    day = sgqlc.types.Field(order_by, graphql_name="day")
    model_id = sgqlc.types.Field(order_by, graphql_name="modelId")
    type = sgqlc.types.Field(order_by, graphql_name="type")


class meta_ai_predictions_by_day_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("app_id", "count", "day", "model_id", "type")
    app_id = sgqlc.types.Field(order_by, graphql_name="appId")
    count = sgqlc.types.Field(order_by, graphql_name="count")
    day = sgqlc.types.Field(order_by, graphql_name="day")
    model_id = sgqlc.types.Field(order_by, graphql_name="modelId")
    type = sgqlc.types.Field(order_by, graphql_name="type")


class meta_ai_predictions_by_day_stddev_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("count",)
    count = sgqlc.types.Field(order_by, graphql_name="count")


class meta_ai_predictions_by_day_stddev_pop_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("count",)
    count = sgqlc.types.Field(order_by, graphql_name="count")


class meta_ai_predictions_by_day_stddev_samp_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("count",)
    count = sgqlc.types.Field(order_by, graphql_name="count")


class meta_ai_predictions_by_day_sum_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("count",)
    count = sgqlc.types.Field(order_by, graphql_name="count")


class meta_ai_predictions_by_day_var_pop_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("count",)
    count = sgqlc.types.Field(order_by, graphql_name="count")


class meta_ai_predictions_by_day_var_samp_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("count",)
    count = sgqlc.types.Field(order_by, graphql_name="count")


class meta_ai_predictions_by_day_variance_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("count",)
    count = sgqlc.types.Field(order_by, graphql_name="count")


class meta_ai_task_registry_bool_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("_and", "_not", "_or", "app_id", "id", "model", "model_id", "task_name", "tasks")
    _and = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_task_registry_bool_exp")), graphql_name="_and"
    )
    _not = sgqlc.types.Field("meta_ai_task_registry_bool_exp", graphql_name="_not")
    _or = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_task_registry_bool_exp")), graphql_name="_or"
    )
    app_id = sgqlc.types.Field("uuid_comparison_exp", graphql_name="app_id")
    id = sgqlc.types.Field(bigint_comparison_exp, graphql_name="id")
    model = sgqlc.types.Field(meta_ai_model_bool_exp, graphql_name="model")
    model_id = sgqlc.types.Field("uuid_comparison_exp", graphql_name="model_id")
    task_name = sgqlc.types.Field(String_comparison_exp, graphql_name="task_name")
    tasks = sgqlc.types.Field("turbine_task_bool_exp", graphql_name="tasks")


class meta_ai_task_registry_inc_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(bigint, graphql_name="id")


class meta_ai_task_registry_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("app_id", "id", "model", "model_id", "task_name", "tasks")
    app_id = sgqlc.types.Field(uuid, graphql_name="app_id")
    id = sgqlc.types.Field(bigint, graphql_name="id")
    model = sgqlc.types.Field(meta_ai_model_obj_rel_insert_input, graphql_name="model")
    model_id = sgqlc.types.Field(uuid, graphql_name="model_id")
    task_name = sgqlc.types.Field(String, graphql_name="task_name")
    tasks = sgqlc.types.Field("turbine_task_arr_rel_insert_input", graphql_name="tasks")


class meta_ai_task_registry_on_conflict(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("constraint", "update_columns", "where")
    constraint = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_task_registry_constraint), graphql_name="constraint")
    update_columns = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_task_registry_update_column))),
        graphql_name="update_columns",
    )
    where = sgqlc.types.Field(meta_ai_task_registry_bool_exp, graphql_name="where")


class meta_ai_task_registry_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("app_id", "id", "model", "model_id", "task_name", "tasks_aggregate")
    app_id = sgqlc.types.Field(order_by, graphql_name="app_id")
    id = sgqlc.types.Field(order_by, graphql_name="id")
    model = sgqlc.types.Field(meta_ai_model_order_by, graphql_name="model")
    model_id = sgqlc.types.Field(order_by, graphql_name="model_id")
    task_name = sgqlc.types.Field(order_by, graphql_name="task_name")
    tasks_aggregate = sgqlc.types.Field("turbine_task_aggregate_order_by", graphql_name="tasks_aggregate")


class meta_ai_task_registry_pk_columns_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(sgqlc.types.non_null(bigint), graphql_name="id")


class meta_ai_task_registry_set_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("app_id", "id", "model_id", "task_name")
    app_id = sgqlc.types.Field(uuid, graphql_name="app_id")
    id = sgqlc.types.Field(bigint, graphql_name="id")
    model_id = sgqlc.types.Field(uuid, graphql_name="model_id")
    task_name = sgqlc.types.Field(String, graphql_name="task_name")


class meta_ai_training_instance_aggregate_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("count", "max", "min")
    count = sgqlc.types.Field(order_by, graphql_name="count")
    max = sgqlc.types.Field("meta_ai_training_instance_max_order_by", graphql_name="max")
    min = sgqlc.types.Field("meta_ai_training_instance_min_order_by", graphql_name="min")


class meta_ai_training_instance_append_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("current_properties",)
    current_properties = sgqlc.types.Field(jsonb, graphql_name="currentProperties")


class meta_ai_training_instance_arr_rel_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("data", "on_conflict")
    data = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_training_instance_insert_input"))),
        graphql_name="data",
    )
    on_conflict = sgqlc.types.Field("meta_ai_training_instance_on_conflict", graphql_name="on_conflict")


class meta_ai_training_instance_bool_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "_and",
        "_not",
        "_or",
        "artifacts",
        "created_at",
        "current_properties",
        "dataset",
        "dataset_id",
        "deployment",
        "deployment_id",
        "id",
        "model",
        "model_id",
        "state",
        "training_template_id",
        "training_state",
        "training_template",
        "updated_at",
    )
    _and = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_training_instance_bool_exp")), graphql_name="_and"
    )
    _not = sgqlc.types.Field("meta_ai_training_instance_bool_exp", graphql_name="_not")
    _or = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_training_instance_bool_exp")), graphql_name="_or"
    )
    artifacts = sgqlc.types.Field(String_comparison_exp, graphql_name="artifacts")
    created_at = sgqlc.types.Field("timestamptz_comparison_exp", graphql_name="createdAt")
    current_properties = sgqlc.types.Field(jsonb_comparison_exp, graphql_name="currentProperties")
    dataset = sgqlc.types.Field(meta_ai_dataset_bool_exp, graphql_name="dataset")
    dataset_id = sgqlc.types.Field("uuid_comparison_exp", graphql_name="dataset_id")
    deployment = sgqlc.types.Field(meta_ai_deployment_bool_exp, graphql_name="deployment")
    deployment_id = sgqlc.types.Field("uuid_comparison_exp", graphql_name="deployment_id")
    id = sgqlc.types.Field("uuid_comparison_exp", graphql_name="id")
    model = sgqlc.types.Field(meta_ai_model_bool_exp, graphql_name="model")
    model_id = sgqlc.types.Field("uuid_comparison_exp", graphql_name="modelId")
    state = sgqlc.types.Field("meta_ai_training_state_enum_comparison_exp", graphql_name="state")
    training_template_id = sgqlc.types.Field("uuid_comparison_exp", graphql_name="trainingTemplateId")
    training_state = sgqlc.types.Field("meta_ai_training_state_bool_exp", graphql_name="training_state")
    training_template = sgqlc.types.Field("meta_ai_training_template_bool_exp", graphql_name="training_template")
    updated_at = sgqlc.types.Field("timestamptz_comparison_exp", graphql_name="updated_at")


class meta_ai_training_instance_delete_at_path_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("current_properties",)
    current_properties = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name="currentProperties"
    )


class meta_ai_training_instance_delete_elem_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("current_properties",)
    current_properties = sgqlc.types.Field(Int, graphql_name="currentProperties")


class meta_ai_training_instance_delete_key_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("current_properties",)
    current_properties = sgqlc.types.Field(String, graphql_name="currentProperties")


class meta_ai_training_instance_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "artifacts",
        "created_at",
        "current_properties",
        "dataset",
        "dataset_id",
        "deployment",
        "deployment_id",
        "id",
        "model",
        "model_id",
        "state",
        "training_template_id",
        "training_state",
        "training_template",
        "updated_at",
    )
    artifacts = sgqlc.types.Field(String, graphql_name="artifacts")
    created_at = sgqlc.types.Field(timestamptz, graphql_name="createdAt")
    current_properties = sgqlc.types.Field(jsonb, graphql_name="currentProperties")
    dataset = sgqlc.types.Field(meta_ai_dataset_obj_rel_insert_input, graphql_name="dataset")
    dataset_id = sgqlc.types.Field(uuid, graphql_name="dataset_id")
    deployment = sgqlc.types.Field(meta_ai_deployment_obj_rel_insert_input, graphql_name="deployment")
    deployment_id = sgqlc.types.Field(uuid, graphql_name="deployment_id")
    id = sgqlc.types.Field(uuid, graphql_name="id")
    model = sgqlc.types.Field(meta_ai_model_obj_rel_insert_input, graphql_name="model")
    model_id = sgqlc.types.Field(uuid, graphql_name="modelId")
    state = sgqlc.types.Field(meta_ai_training_state_enum, graphql_name="state")
    training_template_id = sgqlc.types.Field(uuid, graphql_name="trainingTemplateId")
    training_state = sgqlc.types.Field("meta_ai_training_state_obj_rel_insert_input", graphql_name="training_state")
    training_template = sgqlc.types.Field(
        "meta_ai_training_template_obj_rel_insert_input", graphql_name="training_template"
    )
    updated_at = sgqlc.types.Field(timestamptz, graphql_name="updated_at")


class meta_ai_training_instance_max_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "artifacts",
        "created_at",
        "dataset_id",
        "deployment_id",
        "id",
        "model_id",
        "training_template_id",
        "updated_at",
    )
    artifacts = sgqlc.types.Field(order_by, graphql_name="artifacts")
    created_at = sgqlc.types.Field(order_by, graphql_name="createdAt")
    dataset_id = sgqlc.types.Field(order_by, graphql_name="dataset_id")
    deployment_id = sgqlc.types.Field(order_by, graphql_name="deployment_id")
    id = sgqlc.types.Field(order_by, graphql_name="id")
    model_id = sgqlc.types.Field(order_by, graphql_name="modelId")
    training_template_id = sgqlc.types.Field(order_by, graphql_name="trainingTemplateId")
    updated_at = sgqlc.types.Field(order_by, graphql_name="updated_at")


class meta_ai_training_instance_min_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "artifacts",
        "created_at",
        "dataset_id",
        "deployment_id",
        "id",
        "model_id",
        "training_template_id",
        "updated_at",
    )
    artifacts = sgqlc.types.Field(order_by, graphql_name="artifacts")
    created_at = sgqlc.types.Field(order_by, graphql_name="createdAt")
    dataset_id = sgqlc.types.Field(order_by, graphql_name="dataset_id")
    deployment_id = sgqlc.types.Field(order_by, graphql_name="deployment_id")
    id = sgqlc.types.Field(order_by, graphql_name="id")
    model_id = sgqlc.types.Field(order_by, graphql_name="modelId")
    training_template_id = sgqlc.types.Field(order_by, graphql_name="trainingTemplateId")
    updated_at = sgqlc.types.Field(order_by, graphql_name="updated_at")


class meta_ai_training_instance_on_conflict(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("constraint", "update_columns", "where")
    constraint = sgqlc.types.Field(
        sgqlc.types.non_null(meta_ai_training_instance_constraint), graphql_name="constraint"
    )
    update_columns = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_training_instance_update_column))),
        graphql_name="update_columns",
    )
    where = sgqlc.types.Field(meta_ai_training_instance_bool_exp, graphql_name="where")


class meta_ai_training_instance_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "artifacts",
        "created_at",
        "current_properties",
        "dataset",
        "dataset_id",
        "deployment",
        "deployment_id",
        "id",
        "model",
        "model_id",
        "state",
        "training_template_id",
        "training_state",
        "training_template",
        "updated_at",
    )
    artifacts = sgqlc.types.Field(order_by, graphql_name="artifacts")
    created_at = sgqlc.types.Field(order_by, graphql_name="createdAt")
    current_properties = sgqlc.types.Field(order_by, graphql_name="currentProperties")
    dataset = sgqlc.types.Field(meta_ai_dataset_order_by, graphql_name="dataset")
    dataset_id = sgqlc.types.Field(order_by, graphql_name="dataset_id")
    deployment = sgqlc.types.Field(meta_ai_deployment_order_by, graphql_name="deployment")
    deployment_id = sgqlc.types.Field(order_by, graphql_name="deployment_id")
    id = sgqlc.types.Field(order_by, graphql_name="id")
    model = sgqlc.types.Field(meta_ai_model_order_by, graphql_name="model")
    model_id = sgqlc.types.Field(order_by, graphql_name="modelId")
    state = sgqlc.types.Field(order_by, graphql_name="state")
    training_template_id = sgqlc.types.Field(order_by, graphql_name="trainingTemplateId")
    training_state = sgqlc.types.Field("meta_ai_training_state_order_by", graphql_name="training_state")
    training_template = sgqlc.types.Field("meta_ai_training_template_order_by", graphql_name="training_template")
    updated_at = sgqlc.types.Field(order_by, graphql_name="updated_at")


class meta_ai_training_instance_pk_columns_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name="id")


class meta_ai_training_instance_prepend_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("current_properties",)
    current_properties = sgqlc.types.Field(jsonb, graphql_name="currentProperties")


class meta_ai_training_instance_set_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "artifacts",
        "created_at",
        "current_properties",
        "dataset_id",
        "deployment_id",
        "id",
        "model_id",
        "state",
        "training_template_id",
        "updated_at",
    )
    artifacts = sgqlc.types.Field(String, graphql_name="artifacts")
    created_at = sgqlc.types.Field(timestamptz, graphql_name="createdAt")
    current_properties = sgqlc.types.Field(jsonb, graphql_name="currentProperties")
    dataset_id = sgqlc.types.Field(uuid, graphql_name="dataset_id")
    deployment_id = sgqlc.types.Field(uuid, graphql_name="deployment_id")
    id = sgqlc.types.Field(uuid, graphql_name="id")
    model_id = sgqlc.types.Field(uuid, graphql_name="modelId")
    state = sgqlc.types.Field(meta_ai_training_state_enum, graphql_name="state")
    training_template_id = sgqlc.types.Field(uuid, graphql_name="trainingTemplateId")
    updated_at = sgqlc.types.Field(timestamptz, graphql_name="updated_at")


class meta_ai_training_state_bool_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("_and", "_not", "_or", "state", "training_instances")
    _and = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_training_state_bool_exp")), graphql_name="_and"
    )
    _not = sgqlc.types.Field("meta_ai_training_state_bool_exp", graphql_name="_not")
    _or = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_training_state_bool_exp")), graphql_name="_or"
    )
    state = sgqlc.types.Field(String_comparison_exp, graphql_name="state")
    training_instances = sgqlc.types.Field(meta_ai_training_instance_bool_exp, graphql_name="training_instances")


class meta_ai_training_state_enum_comparison_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("_eq", "_in", "_is_null", "_neq", "_nin")
    _eq = sgqlc.types.Field(meta_ai_training_state_enum, graphql_name="_eq")
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_training_state_enum)), graphql_name="_in")
    _is_null = sgqlc.types.Field(Boolean, graphql_name="_is_null")
    _neq = sgqlc.types.Field(meta_ai_training_state_enum, graphql_name="_neq")
    _nin = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_training_state_enum)), graphql_name="_nin"
    )


class meta_ai_training_state_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("state", "training_instances")
    state = sgqlc.types.Field(String, graphql_name="state")
    training_instances = sgqlc.types.Field(
        meta_ai_training_instance_arr_rel_insert_input, graphql_name="training_instances"
    )


class meta_ai_training_state_obj_rel_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("data", "on_conflict")
    data = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_training_state_insert_input), graphql_name="data")
    on_conflict = sgqlc.types.Field("meta_ai_training_state_on_conflict", graphql_name="on_conflict")


class meta_ai_training_state_on_conflict(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("constraint", "update_columns", "where")
    constraint = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_training_state_constraint), graphql_name="constraint")
    update_columns = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_training_state_update_column))),
        graphql_name="update_columns",
    )
    where = sgqlc.types.Field(meta_ai_training_state_bool_exp, graphql_name="where")


class meta_ai_training_state_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("state", "training_instances_aggregate")
    state = sgqlc.types.Field(order_by, graphql_name="state")
    training_instances_aggregate = sgqlc.types.Field(
        meta_ai_training_instance_aggregate_order_by, graphql_name="training_instances_aggregate"
    )


class meta_ai_training_state_pk_columns_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("state",)
    state = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="state")


class meta_ai_training_state_set_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("state",)
    state = sgqlc.types.Field(String, graphql_name="state")


class meta_ai_training_template_append_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("properties",)
    properties = sgqlc.types.Field(jsonb, graphql_name="properties")


class meta_ai_training_template_bool_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "_and",
        "_not",
        "_or",
        "app_id",
        "created_at",
        "description",
        "id",
        "model",
        "model_id",
        "properties",
        "training_instances",
        "updated_at",
    )
    _and = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_training_template_bool_exp")), graphql_name="_and"
    )
    _not = sgqlc.types.Field("meta_ai_training_template_bool_exp", graphql_name="_not")
    _or = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_training_template_bool_exp")), graphql_name="_or"
    )
    app_id = sgqlc.types.Field("uuid_comparison_exp", graphql_name="appId")
    created_at = sgqlc.types.Field("timestamptz_comparison_exp", graphql_name="createdAt")
    description = sgqlc.types.Field(String_comparison_exp, graphql_name="description")
    id = sgqlc.types.Field("uuid_comparison_exp", graphql_name="id")
    model = sgqlc.types.Field(meta_ai_model_bool_exp, graphql_name="model")
    model_id = sgqlc.types.Field("uuid_comparison_exp", graphql_name="modelId")
    properties = sgqlc.types.Field(jsonb_comparison_exp, graphql_name="properties")
    training_instances = sgqlc.types.Field(meta_ai_training_instance_bool_exp, graphql_name="training_instances")
    updated_at = sgqlc.types.Field("timestamptz_comparison_exp", graphql_name="updated_at")


class meta_ai_training_template_delete_at_path_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("properties",)
    properties = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name="properties")


class meta_ai_training_template_delete_elem_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("properties",)
    properties = sgqlc.types.Field(Int, graphql_name="properties")


class meta_ai_training_template_delete_key_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("properties",)
    properties = sgqlc.types.Field(String, graphql_name="properties")


class meta_ai_training_template_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "app_id",
        "created_at",
        "description",
        "id",
        "model",
        "model_id",
        "properties",
        "training_instances",
        "updated_at",
    )
    app_id = sgqlc.types.Field(uuid, graphql_name="appId")
    created_at = sgqlc.types.Field(timestamptz, graphql_name="createdAt")
    description = sgqlc.types.Field(String, graphql_name="description")
    id = sgqlc.types.Field(uuid, graphql_name="id")
    model = sgqlc.types.Field(meta_ai_model_obj_rel_insert_input, graphql_name="model")
    model_id = sgqlc.types.Field(uuid, graphql_name="modelId")
    properties = sgqlc.types.Field(jsonb, graphql_name="properties")
    training_instances = sgqlc.types.Field(
        meta_ai_training_instance_arr_rel_insert_input, graphql_name="training_instances"
    )
    updated_at = sgqlc.types.Field(timestamptz, graphql_name="updated_at")


class meta_ai_training_template_obj_rel_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("data", "on_conflict")
    data = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_training_template_insert_input), graphql_name="data")
    on_conflict = sgqlc.types.Field("meta_ai_training_template_on_conflict", graphql_name="on_conflict")


class meta_ai_training_template_on_conflict(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("constraint", "update_columns", "where")
    constraint = sgqlc.types.Field(
        sgqlc.types.non_null(meta_ai_training_template_constraint), graphql_name="constraint"
    )
    update_columns = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_training_template_update_column))),
        graphql_name="update_columns",
    )
    where = sgqlc.types.Field(meta_ai_training_template_bool_exp, graphql_name="where")


class meta_ai_training_template_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "app_id",
        "created_at",
        "description",
        "id",
        "model",
        "model_id",
        "properties",
        "training_instances_aggregate",
        "updated_at",
    )
    app_id = sgqlc.types.Field(order_by, graphql_name="appId")
    created_at = sgqlc.types.Field(order_by, graphql_name="createdAt")
    description = sgqlc.types.Field(order_by, graphql_name="description")
    id = sgqlc.types.Field(order_by, graphql_name="id")
    model = sgqlc.types.Field(meta_ai_model_order_by, graphql_name="model")
    model_id = sgqlc.types.Field(order_by, graphql_name="modelId")
    properties = sgqlc.types.Field(order_by, graphql_name="properties")
    training_instances_aggregate = sgqlc.types.Field(
        meta_ai_training_instance_aggregate_order_by, graphql_name="training_instances_aggregate"
    )
    updated_at = sgqlc.types.Field(order_by, graphql_name="updated_at")


class meta_ai_training_template_pk_columns_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name="id")


class meta_ai_training_template_prepend_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("properties",)
    properties = sgqlc.types.Field(jsonb, graphql_name="properties")


class meta_ai_training_template_set_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("app_id", "created_at", "description", "id", "model_id", "properties", "updated_at")
    app_id = sgqlc.types.Field(uuid, graphql_name="appId")
    created_at = sgqlc.types.Field(timestamptz, graphql_name="createdAt")
    description = sgqlc.types.Field(String, graphql_name="description")
    id = sgqlc.types.Field(uuid, graphql_name="id")
    model_id = sgqlc.types.Field(uuid, graphql_name="modelId")
    properties = sgqlc.types.Field(jsonb, graphql_name="properties")
    updated_at = sgqlc.types.Field(timestamptz, graphql_name="updated_at")


class meta_ai_visibility_bool_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("_and", "_not", "_or", "models", "type")
    _and = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_visibility_bool_exp")), graphql_name="_and"
    )
    _not = sgqlc.types.Field("meta_ai_visibility_bool_exp", graphql_name="_not")
    _or = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_visibility_bool_exp")), graphql_name="_or"
    )
    models = sgqlc.types.Field(meta_ai_model_bool_exp, graphql_name="models")
    type = sgqlc.types.Field(String_comparison_exp, graphql_name="type")


class meta_ai_visibility_enum_comparison_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("_eq", "_in", "_is_null", "_neq", "_nin")
    _eq = sgqlc.types.Field(meta_ai_visibility_enum, graphql_name="_eq")
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_visibility_enum)), graphql_name="_in")
    _is_null = sgqlc.types.Field(Boolean, graphql_name="_is_null")
    _neq = sgqlc.types.Field(meta_ai_visibility_enum, graphql_name="_neq")
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_visibility_enum)), graphql_name="_nin")


class meta_ai_visibility_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("models", "type")
    models = sgqlc.types.Field(meta_ai_model_arr_rel_insert_input, graphql_name="models")
    type = sgqlc.types.Field(String, graphql_name="type")


class meta_ai_visibility_on_conflict(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("constraint", "update_columns", "where")
    constraint = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_visibility_constraint), graphql_name="constraint")
    update_columns = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_visibility_update_column))),
        graphql_name="update_columns",
    )
    where = sgqlc.types.Field(meta_ai_visibility_bool_exp, graphql_name="where")


class meta_ai_visibility_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("models_aggregate", "type")
    models_aggregate = sgqlc.types.Field(meta_ai_model_aggregate_order_by, graphql_name="models_aggregate")
    type = sgqlc.types.Field(order_by, graphql_name="type")


class meta_ai_visibility_pk_columns_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("type",)
    type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="type")


class meta_ai_visibility_set_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("type",)
    type = sgqlc.types.Field(String, graphql_name="type")


class numeric_comparison_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("_eq", "_gt", "_gte", "_in", "_is_null", "_lt", "_lte", "_neq", "_nin")
    _eq = sgqlc.types.Field(numeric, graphql_name="_eq")
    _gt = sgqlc.types.Field(numeric, graphql_name="_gt")
    _gte = sgqlc.types.Field(numeric, graphql_name="_gte")
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(numeric)), graphql_name="_in")
    _is_null = sgqlc.types.Field(Boolean, graphql_name="_is_null")
    _lt = sgqlc.types.Field(numeric, graphql_name="_lt")
    _lte = sgqlc.types.Field(numeric, graphql_name="_lte")
    _neq = sgqlc.types.Field(numeric, graphql_name="_neq")
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(numeric)), graphql_name="_nin")


class timestamp_comparison_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("_eq", "_gt", "_gte", "_in", "_is_null", "_lt", "_lte", "_neq", "_nin")
    _eq = sgqlc.types.Field(timestamp, graphql_name="_eq")
    _gt = sgqlc.types.Field(timestamp, graphql_name="_gt")
    _gte = sgqlc.types.Field(timestamp, graphql_name="_gte")
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(timestamp)), graphql_name="_in")
    _is_null = sgqlc.types.Field(Boolean, graphql_name="_is_null")
    _lt = sgqlc.types.Field(timestamp, graphql_name="_lt")
    _lte = sgqlc.types.Field(timestamp, graphql_name="_lte")
    _neq = sgqlc.types.Field(timestamp, graphql_name="_neq")
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(timestamp)), graphql_name="_nin")


class timestamptz_comparison_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("_eq", "_gt", "_gte", "_in", "_is_null", "_lt", "_lte", "_neq", "_nin")
    _eq = sgqlc.types.Field(timestamptz, graphql_name="_eq")
    _gt = sgqlc.types.Field(timestamptz, graphql_name="_gt")
    _gte = sgqlc.types.Field(timestamptz, graphql_name="_gte")
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(timestamptz)), graphql_name="_in")
    _is_null = sgqlc.types.Field(Boolean, graphql_name="_is_null")
    _lt = sgqlc.types.Field(timestamptz, graphql_name="_lt")
    _lte = sgqlc.types.Field(timestamptz, graphql_name="_lte")
    _neq = sgqlc.types.Field(timestamptz, graphql_name="_neq")
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(timestamptz)), graphql_name="_nin")


class turbine_app_bool_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("_and", "_not", "_or", "datasets", "id", "jobs", "tasks")
    _and = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null("turbine_app_bool_exp")), graphql_name="_and")
    _not = sgqlc.types.Field("turbine_app_bool_exp", graphql_name="_not")
    _or = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null("turbine_app_bool_exp")), graphql_name="_or")
    datasets = sgqlc.types.Field(meta_ai_dataset_bool_exp, graphql_name="datasets")
    id = sgqlc.types.Field("uuid_comparison_exp", graphql_name="id")
    jobs = sgqlc.types.Field("turbine_job_bool_exp", graphql_name="jobs")
    tasks = sgqlc.types.Field("turbine_task_bool_exp", graphql_name="tasks")


class turbine_app_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("datasets", "id", "jobs", "tasks")
    datasets = sgqlc.types.Field(meta_ai_dataset_arr_rel_insert_input, graphql_name="datasets")
    id = sgqlc.types.Field(uuid, graphql_name="id")
    jobs = sgqlc.types.Field("turbine_job_arr_rel_insert_input", graphql_name="jobs")
    tasks = sgqlc.types.Field("turbine_task_arr_rel_insert_input", graphql_name="tasks")


class turbine_app_obj_rel_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("data", "on_conflict")
    data = sgqlc.types.Field(sgqlc.types.non_null(turbine_app_insert_input), graphql_name="data")
    on_conflict = sgqlc.types.Field("turbine_app_on_conflict", graphql_name="on_conflict")


class turbine_app_on_conflict(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("constraint", "update_columns", "where")
    constraint = sgqlc.types.Field(sgqlc.types.non_null(turbine_app_constraint), graphql_name="constraint")
    update_columns = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(turbine_app_update_column))),
        graphql_name="update_columns",
    )
    where = sgqlc.types.Field(turbine_app_bool_exp, graphql_name="where")


class turbine_app_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("datasets_aggregate", "id", "jobs_aggregate", "tasks_aggregate")
    datasets_aggregate = sgqlc.types.Field(meta_ai_dataset_aggregate_order_by, graphql_name="datasets_aggregate")
    id = sgqlc.types.Field(order_by, graphql_name="id")
    jobs_aggregate = sgqlc.types.Field("turbine_job_aggregate_order_by", graphql_name="jobs_aggregate")
    tasks_aggregate = sgqlc.types.Field("turbine_task_aggregate_order_by", graphql_name="tasks_aggregate")


class turbine_app_pk_columns_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name="id")


class turbine_app_set_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(uuid, graphql_name="id")


class turbine_job_aggregate_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "avg",
        "count",
        "max",
        "min",
        "stddev",
        "stddev_pop",
        "stddev_samp",
        "sum",
        "var_pop",
        "var_samp",
        "variance",
    )
    avg = sgqlc.types.Field("turbine_job_avg_order_by", graphql_name="avg")
    count = sgqlc.types.Field(order_by, graphql_name="count")
    max = sgqlc.types.Field("turbine_job_max_order_by", graphql_name="max")
    min = sgqlc.types.Field("turbine_job_min_order_by", graphql_name="min")
    stddev = sgqlc.types.Field("turbine_job_stddev_order_by", graphql_name="stddev")
    stddev_pop = sgqlc.types.Field("turbine_job_stddev_pop_order_by", graphql_name="stddev_pop")
    stddev_samp = sgqlc.types.Field("turbine_job_stddev_samp_order_by", graphql_name="stddev_samp")
    sum = sgqlc.types.Field("turbine_job_sum_order_by", graphql_name="sum")
    var_pop = sgqlc.types.Field("turbine_job_var_pop_order_by", graphql_name="var_pop")
    var_samp = sgqlc.types.Field("turbine_job_var_samp_order_by", graphql_name="var_samp")
    variance = sgqlc.types.Field("turbine_job_variance_order_by", graphql_name="variance")


class turbine_job_append_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("data", "payload")
    data = sgqlc.types.Field(jsonb, graphql_name="data")
    payload = sgqlc.types.Field(jsonb, graphql_name="payload")


class turbine_job_arr_rel_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("data", "on_conflict")
    data = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("turbine_job_insert_input"))), graphql_name="data"
    )
    on_conflict = sgqlc.types.Field("turbine_job_on_conflict", graphql_name="on_conflict")


class turbine_job_avg_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "update_count")
    id = sgqlc.types.Field(order_by, graphql_name="id")
    update_count = sgqlc.types.Field(order_by, graphql_name="update_count")


class turbine_job_bool_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "_and",
        "_not",
        "_or",
        "app",
        "created",
        "data",
        "id",
        "payload",
        "predictions",
        "root_app_uuid",
        "started",
        "state",
        "type",
        "update_count",
        "workflow",
    )
    _and = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null("turbine_job_bool_exp")), graphql_name="_and")
    _not = sgqlc.types.Field("turbine_job_bool_exp", graphql_name="_not")
    _or = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null("turbine_job_bool_exp")), graphql_name="_or")
    app = sgqlc.types.Field(turbine_app_bool_exp, graphql_name="app")
    created = sgqlc.types.Field(timestamp_comparison_exp, graphql_name="created")
    data = sgqlc.types.Field(jsonb_comparison_exp, graphql_name="data")
    id = sgqlc.types.Field(bigint_comparison_exp, graphql_name="id")
    payload = sgqlc.types.Field(jsonb_comparison_exp, graphql_name="payload")
    predictions = sgqlc.types.Field(meta_ai_prediction_bool_exp, graphql_name="predictions")
    root_app_uuid = sgqlc.types.Field("uuid_comparison_exp", graphql_name="root_app_uuid")
    started = sgqlc.types.Field(timestamp_comparison_exp, graphql_name="started")
    state = sgqlc.types.Field(String_comparison_exp, graphql_name="state")
    type = sgqlc.types.Field(String_comparison_exp, graphql_name="type")
    update_count = sgqlc.types.Field(Int_comparison_exp, graphql_name="update_count")
    workflow = sgqlc.types.Field(String_comparison_exp, graphql_name="workflow")


class turbine_job_delete_at_path_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("data", "payload")
    data = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name="data")
    payload = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name="payload")


class turbine_job_delete_elem_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("data", "payload")
    data = sgqlc.types.Field(Int, graphql_name="data")
    payload = sgqlc.types.Field(Int, graphql_name="payload")


class turbine_job_delete_key_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("data", "payload")
    data = sgqlc.types.Field(String, graphql_name="data")
    payload = sgqlc.types.Field(String, graphql_name="payload")


class turbine_job_inc_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "update_count")
    id = sgqlc.types.Field(bigint, graphql_name="id")
    update_count = sgqlc.types.Field(Int, graphql_name="update_count")


class turbine_job_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "app",
        "created",
        "data",
        "id",
        "payload",
        "predictions",
        "root_app_uuid",
        "started",
        "state",
        "type",
        "update_count",
        "workflow",
    )
    app = sgqlc.types.Field(turbine_app_obj_rel_insert_input, graphql_name="app")
    created = sgqlc.types.Field(timestamp, graphql_name="created")
    data = sgqlc.types.Field(jsonb, graphql_name="data")
    id = sgqlc.types.Field(bigint, graphql_name="id")
    payload = sgqlc.types.Field(jsonb, graphql_name="payload")
    predictions = sgqlc.types.Field(meta_ai_prediction_arr_rel_insert_input, graphql_name="predictions")
    root_app_uuid = sgqlc.types.Field(uuid, graphql_name="root_app_uuid")
    started = sgqlc.types.Field(timestamp, graphql_name="started")
    state = sgqlc.types.Field(String, graphql_name="state")
    type = sgqlc.types.Field(String, graphql_name="type")
    update_count = sgqlc.types.Field(Int, graphql_name="update_count")
    workflow = sgqlc.types.Field(String, graphql_name="workflow")


class turbine_job_max_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("created", "id", "root_app_uuid", "started", "state", "type", "update_count", "workflow")
    created = sgqlc.types.Field(order_by, graphql_name="created")
    id = sgqlc.types.Field(order_by, graphql_name="id")
    root_app_uuid = sgqlc.types.Field(order_by, graphql_name="root_app_uuid")
    started = sgqlc.types.Field(order_by, graphql_name="started")
    state = sgqlc.types.Field(order_by, graphql_name="state")
    type = sgqlc.types.Field(order_by, graphql_name="type")
    update_count = sgqlc.types.Field(order_by, graphql_name="update_count")
    workflow = sgqlc.types.Field(order_by, graphql_name="workflow")


class turbine_job_min_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("created", "id", "root_app_uuid", "started", "state", "type", "update_count", "workflow")
    created = sgqlc.types.Field(order_by, graphql_name="created")
    id = sgqlc.types.Field(order_by, graphql_name="id")
    root_app_uuid = sgqlc.types.Field(order_by, graphql_name="root_app_uuid")
    started = sgqlc.types.Field(order_by, graphql_name="started")
    state = sgqlc.types.Field(order_by, graphql_name="state")
    type = sgqlc.types.Field(order_by, graphql_name="type")
    update_count = sgqlc.types.Field(order_by, graphql_name="update_count")
    workflow = sgqlc.types.Field(order_by, graphql_name="workflow")


class turbine_job_obj_rel_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("data", "on_conflict")
    data = sgqlc.types.Field(sgqlc.types.non_null(turbine_job_insert_input), graphql_name="data")
    on_conflict = sgqlc.types.Field("turbine_job_on_conflict", graphql_name="on_conflict")


class turbine_job_on_conflict(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("constraint", "update_columns", "where")
    constraint = sgqlc.types.Field(sgqlc.types.non_null(turbine_job_constraint), graphql_name="constraint")
    update_columns = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(turbine_job_update_column))),
        graphql_name="update_columns",
    )
    where = sgqlc.types.Field(turbine_job_bool_exp, graphql_name="where")


class turbine_job_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "app",
        "created",
        "data",
        "id",
        "payload",
        "predictions_aggregate",
        "root_app_uuid",
        "started",
        "state",
        "type",
        "update_count",
        "workflow",
    )
    app = sgqlc.types.Field(turbine_app_order_by, graphql_name="app")
    created = sgqlc.types.Field(order_by, graphql_name="created")
    data = sgqlc.types.Field(order_by, graphql_name="data")
    id = sgqlc.types.Field(order_by, graphql_name="id")
    payload = sgqlc.types.Field(order_by, graphql_name="payload")
    predictions_aggregate = sgqlc.types.Field(
        meta_ai_prediction_aggregate_order_by, graphql_name="predictions_aggregate"
    )
    root_app_uuid = sgqlc.types.Field(order_by, graphql_name="root_app_uuid")
    started = sgqlc.types.Field(order_by, graphql_name="started")
    state = sgqlc.types.Field(order_by, graphql_name="state")
    type = sgqlc.types.Field(order_by, graphql_name="type")
    update_count = sgqlc.types.Field(order_by, graphql_name="update_count")
    workflow = sgqlc.types.Field(order_by, graphql_name="workflow")


class turbine_job_pk_columns_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(sgqlc.types.non_null(bigint), graphql_name="id")


class turbine_job_prepend_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("data", "payload")
    data = sgqlc.types.Field(jsonb, graphql_name="data")
    payload = sgqlc.types.Field(jsonb, graphql_name="payload")


class turbine_job_set_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "created",
        "data",
        "id",
        "payload",
        "root_app_uuid",
        "started",
        "state",
        "type",
        "update_count",
        "workflow",
    )
    created = sgqlc.types.Field(timestamp, graphql_name="created")
    data = sgqlc.types.Field(jsonb, graphql_name="data")
    id = sgqlc.types.Field(bigint, graphql_name="id")
    payload = sgqlc.types.Field(jsonb, graphql_name="payload")
    root_app_uuid = sgqlc.types.Field(uuid, graphql_name="root_app_uuid")
    started = sgqlc.types.Field(timestamp, graphql_name="started")
    state = sgqlc.types.Field(String, graphql_name="state")
    type = sgqlc.types.Field(String, graphql_name="type")
    update_count = sgqlc.types.Field(Int, graphql_name="update_count")
    workflow = sgqlc.types.Field(String, graphql_name="workflow")


class turbine_job_stddev_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "update_count")
    id = sgqlc.types.Field(order_by, graphql_name="id")
    update_count = sgqlc.types.Field(order_by, graphql_name="update_count")


class turbine_job_stddev_pop_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "update_count")
    id = sgqlc.types.Field(order_by, graphql_name="id")
    update_count = sgqlc.types.Field(order_by, graphql_name="update_count")


class turbine_job_stddev_samp_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "update_count")
    id = sgqlc.types.Field(order_by, graphql_name="id")
    update_count = sgqlc.types.Field(order_by, graphql_name="update_count")


class turbine_job_sum_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "update_count")
    id = sgqlc.types.Field(order_by, graphql_name="id")
    update_count = sgqlc.types.Field(order_by, graphql_name="update_count")


class turbine_job_var_pop_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "update_count")
    id = sgqlc.types.Field(order_by, graphql_name="id")
    update_count = sgqlc.types.Field(order_by, graphql_name="update_count")


class turbine_job_var_samp_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "update_count")
    id = sgqlc.types.Field(order_by, graphql_name="id")
    update_count = sgqlc.types.Field(order_by, graphql_name="update_count")


class turbine_job_variance_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "update_count")
    id = sgqlc.types.Field(order_by, graphql_name="id")
    update_count = sgqlc.types.Field(order_by, graphql_name="update_count")


class turbine_task_aggregate_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "avg",
        "count",
        "max",
        "min",
        "stddev",
        "stddev_pop",
        "stddev_samp",
        "sum",
        "var_pop",
        "var_samp",
        "variance",
    )
    avg = sgqlc.types.Field("turbine_task_avg_order_by", graphql_name="avg")
    count = sgqlc.types.Field(order_by, graphql_name="count")
    max = sgqlc.types.Field("turbine_task_max_order_by", graphql_name="max")
    min = sgqlc.types.Field("turbine_task_min_order_by", graphql_name="min")
    stddev = sgqlc.types.Field("turbine_task_stddev_order_by", graphql_name="stddev")
    stddev_pop = sgqlc.types.Field("turbine_task_stddev_pop_order_by", graphql_name="stddev_pop")
    stddev_samp = sgqlc.types.Field("turbine_task_stddev_samp_order_by", graphql_name="stddev_samp")
    sum = sgqlc.types.Field("turbine_task_sum_order_by", graphql_name="sum")
    var_pop = sgqlc.types.Field("turbine_task_var_pop_order_by", graphql_name="var_pop")
    var_samp = sgqlc.types.Field("turbine_task_var_samp_order_by", graphql_name="var_samp")
    variance = sgqlc.types.Field("turbine_task_variance_order_by", graphql_name="variance")


class turbine_task_append_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("payload",)
    payload = sgqlc.types.Field(jsonb, graphql_name="payload")


class turbine_task_arr_rel_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("data", "on_conflict")
    data = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("turbine_task_insert_input"))),
        graphql_name="data",
    )
    on_conflict = sgqlc.types.Field("turbine_task_on_conflict", graphql_name="on_conflict")


class turbine_task_avg_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "job_id", "owner_id", "update_count")
    id = sgqlc.types.Field(order_by, graphql_name="id")
    job_id = sgqlc.types.Field(order_by, graphql_name="job_id")
    owner_id = sgqlc.types.Field(order_by, graphql_name="owner_id")
    update_count = sgqlc.types.Field(order_by, graphql_name="update_count")


class turbine_task_bool_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "_and",
        "_not",
        "_or",
        "app",
        "app_id",
        "completed",
        "created",
        "id",
        "job",
        "job_id",
        "name",
        "owner_id",
        "payload",
        "prediction",
        "state",
        "update_count",
        "worker_type",
    )
    _and = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null("turbine_task_bool_exp")), graphql_name="_and")
    _not = sgqlc.types.Field("turbine_task_bool_exp", graphql_name="_not")
    _or = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null("turbine_task_bool_exp")), graphql_name="_or")
    app = sgqlc.types.Field(turbine_app_bool_exp, graphql_name="app")
    app_id = sgqlc.types.Field("uuid_comparison_exp", graphql_name="app_id")
    completed = sgqlc.types.Field(timestamptz_comparison_exp, graphql_name="completed")
    created = sgqlc.types.Field(timestamptz_comparison_exp, graphql_name="created")
    id = sgqlc.types.Field(bigint_comparison_exp, graphql_name="id")
    job = sgqlc.types.Field(turbine_job_bool_exp, graphql_name="job")
    job_id = sgqlc.types.Field(bigint_comparison_exp, graphql_name="job_id")
    name = sgqlc.types.Field(String_comparison_exp, graphql_name="name")
    owner_id = sgqlc.types.Field(bigint_comparison_exp, graphql_name="owner_id")
    payload = sgqlc.types.Field(jsonb_comparison_exp, graphql_name="payload")
    prediction = sgqlc.types.Field(meta_ai_prediction_bool_exp, graphql_name="prediction")
    state = sgqlc.types.Field(String_comparison_exp, graphql_name="state")
    update_count = sgqlc.types.Field(Int_comparison_exp, graphql_name="update_count")
    worker_type = sgqlc.types.Field(String_comparison_exp, graphql_name="worker_type")


class turbine_task_delete_at_path_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("payload",)
    payload = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name="payload")


class turbine_task_delete_elem_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("payload",)
    payload = sgqlc.types.Field(Int, graphql_name="payload")


class turbine_task_delete_key_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("payload",)
    payload = sgqlc.types.Field(String, graphql_name="payload")


class turbine_task_inc_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "job_id", "owner_id", "update_count")
    id = sgqlc.types.Field(bigint, graphql_name="id")
    job_id = sgqlc.types.Field(bigint, graphql_name="job_id")
    owner_id = sgqlc.types.Field(bigint, graphql_name="owner_id")
    update_count = sgqlc.types.Field(Int, graphql_name="update_count")


class turbine_task_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "app",
        "app_id",
        "completed",
        "created",
        "id",
        "job",
        "job_id",
        "name",
        "owner_id",
        "payload",
        "prediction",
        "state",
        "update_count",
        "worker_type",
    )
    app = sgqlc.types.Field(turbine_app_obj_rel_insert_input, graphql_name="app")
    app_id = sgqlc.types.Field(uuid, graphql_name="app_id")
    completed = sgqlc.types.Field(timestamptz, graphql_name="completed")
    created = sgqlc.types.Field(timestamptz, graphql_name="created")
    id = sgqlc.types.Field(bigint, graphql_name="id")
    job = sgqlc.types.Field(turbine_job_obj_rel_insert_input, graphql_name="job")
    job_id = sgqlc.types.Field(bigint, graphql_name="job_id")
    name = sgqlc.types.Field(String, graphql_name="name")
    owner_id = sgqlc.types.Field(bigint, graphql_name="owner_id")
    payload = sgqlc.types.Field(jsonb, graphql_name="payload")
    prediction = sgqlc.types.Field(meta_ai_prediction_obj_rel_insert_input, graphql_name="prediction")
    state = sgqlc.types.Field(String, graphql_name="state")
    update_count = sgqlc.types.Field(Int, graphql_name="update_count")
    worker_type = sgqlc.types.Field(String, graphql_name="worker_type")


class turbine_task_max_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "app_id",
        "completed",
        "created",
        "id",
        "job_id",
        "name",
        "owner_id",
        "state",
        "update_count",
        "worker_type",
    )
    app_id = sgqlc.types.Field(order_by, graphql_name="app_id")
    completed = sgqlc.types.Field(order_by, graphql_name="completed")
    created = sgqlc.types.Field(order_by, graphql_name="created")
    id = sgqlc.types.Field(order_by, graphql_name="id")
    job_id = sgqlc.types.Field(order_by, graphql_name="job_id")
    name = sgqlc.types.Field(order_by, graphql_name="name")
    owner_id = sgqlc.types.Field(order_by, graphql_name="owner_id")
    state = sgqlc.types.Field(order_by, graphql_name="state")
    update_count = sgqlc.types.Field(order_by, graphql_name="update_count")
    worker_type = sgqlc.types.Field(order_by, graphql_name="worker_type")


class turbine_task_min_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "app_id",
        "completed",
        "created",
        "id",
        "job_id",
        "name",
        "owner_id",
        "state",
        "update_count",
        "worker_type",
    )
    app_id = sgqlc.types.Field(order_by, graphql_name="app_id")
    completed = sgqlc.types.Field(order_by, graphql_name="completed")
    created = sgqlc.types.Field(order_by, graphql_name="created")
    id = sgqlc.types.Field(order_by, graphql_name="id")
    job_id = sgqlc.types.Field(order_by, graphql_name="job_id")
    name = sgqlc.types.Field(order_by, graphql_name="name")
    owner_id = sgqlc.types.Field(order_by, graphql_name="owner_id")
    state = sgqlc.types.Field(order_by, graphql_name="state")
    update_count = sgqlc.types.Field(order_by, graphql_name="update_count")
    worker_type = sgqlc.types.Field(order_by, graphql_name="worker_type")


class turbine_task_obj_rel_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("data", "on_conflict")
    data = sgqlc.types.Field(sgqlc.types.non_null(turbine_task_insert_input), graphql_name="data")
    on_conflict = sgqlc.types.Field("turbine_task_on_conflict", graphql_name="on_conflict")


class turbine_task_on_conflict(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("constraint", "update_columns", "where")
    constraint = sgqlc.types.Field(sgqlc.types.non_null(turbine_task_constraint), graphql_name="constraint")
    update_columns = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(turbine_task_update_column))),
        graphql_name="update_columns",
    )
    where = sgqlc.types.Field(turbine_task_bool_exp, graphql_name="where")


class turbine_task_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "app",
        "app_id",
        "completed",
        "created",
        "id",
        "job",
        "job_id",
        "name",
        "owner_id",
        "payload",
        "prediction",
        "state",
        "update_count",
        "worker_type",
    )
    app = sgqlc.types.Field(turbine_app_order_by, graphql_name="app")
    app_id = sgqlc.types.Field(order_by, graphql_name="app_id")
    completed = sgqlc.types.Field(order_by, graphql_name="completed")
    created = sgqlc.types.Field(order_by, graphql_name="created")
    id = sgqlc.types.Field(order_by, graphql_name="id")
    job = sgqlc.types.Field(turbine_job_order_by, graphql_name="job")
    job_id = sgqlc.types.Field(order_by, graphql_name="job_id")
    name = sgqlc.types.Field(order_by, graphql_name="name")
    owner_id = sgqlc.types.Field(order_by, graphql_name="owner_id")
    payload = sgqlc.types.Field(order_by, graphql_name="payload")
    prediction = sgqlc.types.Field(meta_ai_prediction_order_by, graphql_name="prediction")
    state = sgqlc.types.Field(order_by, graphql_name="state")
    update_count = sgqlc.types.Field(order_by, graphql_name="update_count")
    worker_type = sgqlc.types.Field(order_by, graphql_name="worker_type")


class turbine_task_pk_columns_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(sgqlc.types.non_null(bigint), graphql_name="id")


class turbine_task_prepend_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("payload",)
    payload = sgqlc.types.Field(jsonb, graphql_name="payload")


class turbine_task_set_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "app_id",
        "completed",
        "created",
        "id",
        "job_id",
        "name",
        "owner_id",
        "payload",
        "state",
        "update_count",
        "worker_type",
    )
    app_id = sgqlc.types.Field(uuid, graphql_name="app_id")
    completed = sgqlc.types.Field(timestamptz, graphql_name="completed")
    created = sgqlc.types.Field(timestamptz, graphql_name="created")
    id = sgqlc.types.Field(bigint, graphql_name="id")
    job_id = sgqlc.types.Field(bigint, graphql_name="job_id")
    name = sgqlc.types.Field(String, graphql_name="name")
    owner_id = sgqlc.types.Field(bigint, graphql_name="owner_id")
    payload = sgqlc.types.Field(jsonb, graphql_name="payload")
    state = sgqlc.types.Field(String, graphql_name="state")
    update_count = sgqlc.types.Field(Int, graphql_name="update_count")
    worker_type = sgqlc.types.Field(String, graphql_name="worker_type")


class turbine_task_stddev_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "job_id", "owner_id", "update_count")
    id = sgqlc.types.Field(order_by, graphql_name="id")
    job_id = sgqlc.types.Field(order_by, graphql_name="job_id")
    owner_id = sgqlc.types.Field(order_by, graphql_name="owner_id")
    update_count = sgqlc.types.Field(order_by, graphql_name="update_count")


class turbine_task_stddev_pop_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "job_id", "owner_id", "update_count")
    id = sgqlc.types.Field(order_by, graphql_name="id")
    job_id = sgqlc.types.Field(order_by, graphql_name="job_id")
    owner_id = sgqlc.types.Field(order_by, graphql_name="owner_id")
    update_count = sgqlc.types.Field(order_by, graphql_name="update_count")


class turbine_task_stddev_samp_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "job_id", "owner_id", "update_count")
    id = sgqlc.types.Field(order_by, graphql_name="id")
    job_id = sgqlc.types.Field(order_by, graphql_name="job_id")
    owner_id = sgqlc.types.Field(order_by, graphql_name="owner_id")
    update_count = sgqlc.types.Field(order_by, graphql_name="update_count")


class turbine_task_sum_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "job_id", "owner_id", "update_count")
    id = sgqlc.types.Field(order_by, graphql_name="id")
    job_id = sgqlc.types.Field(order_by, graphql_name="job_id")
    owner_id = sgqlc.types.Field(order_by, graphql_name="owner_id")
    update_count = sgqlc.types.Field(order_by, graphql_name="update_count")


class turbine_task_var_pop_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "job_id", "owner_id", "update_count")
    id = sgqlc.types.Field(order_by, graphql_name="id")
    job_id = sgqlc.types.Field(order_by, graphql_name="job_id")
    owner_id = sgqlc.types.Field(order_by, graphql_name="owner_id")
    update_count = sgqlc.types.Field(order_by, graphql_name="update_count")


class turbine_task_var_samp_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "job_id", "owner_id", "update_count")
    id = sgqlc.types.Field(order_by, graphql_name="id")
    job_id = sgqlc.types.Field(order_by, graphql_name="job_id")
    owner_id = sgqlc.types.Field(order_by, graphql_name="owner_id")
    update_count = sgqlc.types.Field(order_by, graphql_name="update_count")


class turbine_task_variance_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "job_id", "owner_id", "update_count")
    id = sgqlc.types.Field(order_by, graphql_name="id")
    job_id = sgqlc.types.Field(order_by, graphql_name="job_id")
    owner_id = sgqlc.types.Field(order_by, graphql_name="owner_id")
    update_count = sgqlc.types.Field(order_by, graphql_name="update_count")


class uuid_comparison_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("_eq", "_gt", "_gte", "_in", "_is_null", "_lt", "_lte", "_neq", "_nin")
    _eq = sgqlc.types.Field(uuid, graphql_name="_eq")
    _gt = sgqlc.types.Field(uuid, graphql_name="_gt")
    _gte = sgqlc.types.Field(uuid, graphql_name="_gte")
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(uuid)), graphql_name="_in")
    _is_null = sgqlc.types.Field(Boolean, graphql_name="_is_null")
    _lt = sgqlc.types.Field(uuid, graphql_name="_lt")
    _lte = sgqlc.types.Field(uuid, graphql_name="_lte")
    _neq = sgqlc.types.Field(uuid, graphql_name="_neq")
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(uuid)), graphql_name="_nin")


########################################################################
# Output Objects and Interfaces
########################################################################
class AppPredictions(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("n_predictions",)
    n_predictions = sgqlc.types.Field(Int, graphql_name="n_predictions")


class DeploymentStatus(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("status",)
    status = sgqlc.types.Field(String, graphql_name="status")


class InsertMetaAiModelMutationOutput(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name="id")


class Prediction(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("prediction_id", "predictions", "predictions_aggregate")
    prediction_id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name="predictionId")
    predictions = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_prediction"))),
        graphql_name="predictions",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_prediction_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    predictions_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("meta_ai_prediction_aggregate"),
        graphql_name="predictions_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_prediction_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )


class Prelabel(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("prediction", "prediction_id")
    prediction = sgqlc.types.Field(sgqlc.types.non_null("meta_ai_prediction"), graphql_name="prediction")
    prediction_id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name="predictionId")


class RawPrediction(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("output", "score")
    output = sgqlc.types.Field(json, graphql_name="output")
    score = sgqlc.types.Field(numeric, graphql_name="score")


class URL(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("url",)
    url = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="url")


class meta_ai_app(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "active",
        "assigned",
        "id",
        "jobs",
        "jobs_aggregate",
        "model",
        "model_id",
        "predictions",
        "predictions_aggregate",
        "statistics",
        "statistics_aggregate",
        "threshold",
    )
    active = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="active")
    assigned = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_assignment_enum), graphql_name="assigned")
    id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name="id")
    jobs = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("turbine_job"))),
        graphql_name="jobs",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(turbine_job_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(turbine_job_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(turbine_job_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    jobs_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("turbine_job_aggregate"),
        graphql_name="jobs_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(turbine_job_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(turbine_job_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(turbine_job_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    model = sgqlc.types.Field(sgqlc.types.non_null("meta_ai_model"), graphql_name="model")
    model_id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name="modelId")
    predictions = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_prediction"))),
        graphql_name="predictions",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_prediction_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    predictions_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("meta_ai_prediction_aggregate"),
        graphql_name="predictions_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_prediction_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    statistics = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_predictions_by_day"))),
        graphql_name="statistics",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_predictions_by_day_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_predictions_by_day_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_predictions_by_day_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    statistics_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("meta_ai_predictions_by_day_aggregate"),
        graphql_name="statistics_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_predictions_by_day_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_predictions_by_day_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_predictions_by_day_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    threshold = sgqlc.types.Field(numeric, graphql_name="threshold")


class meta_ai_app_aggregate(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("aggregate", "nodes")
    aggregate = sgqlc.types.Field("meta_ai_app_aggregate_fields", graphql_name="aggregate")
    nodes = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_app))), graphql_name="nodes"
    )


class meta_ai_app_aggregate_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "avg",
        "count",
        "max",
        "min",
        "stddev",
        "stddev_pop",
        "stddev_samp",
        "sum",
        "var_pop",
        "var_samp",
        "variance",
    )
    avg = sgqlc.types.Field("meta_ai_app_avg_fields", graphql_name="avg")
    count = sgqlc.types.Field(
        sgqlc.types.non_null(Int),
        graphql_name="count",
        args=sgqlc.types.ArgDict(
            (
                (
                    "columns",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_app_select_column)),
                        graphql_name="columns",
                        default=None,
                    ),
                ),
                ("distinct", sgqlc.types.Arg(Boolean, graphql_name="distinct", default=None)),
            )
        ),
    )
    max = sgqlc.types.Field("meta_ai_app_max_fields", graphql_name="max")
    min = sgqlc.types.Field("meta_ai_app_min_fields", graphql_name="min")
    stddev = sgqlc.types.Field("meta_ai_app_stddev_fields", graphql_name="stddev")
    stddev_pop = sgqlc.types.Field("meta_ai_app_stddev_pop_fields", graphql_name="stddev_pop")
    stddev_samp = sgqlc.types.Field("meta_ai_app_stddev_samp_fields", graphql_name="stddev_samp")
    sum = sgqlc.types.Field("meta_ai_app_sum_fields", graphql_name="sum")
    var_pop = sgqlc.types.Field("meta_ai_app_var_pop_fields", graphql_name="var_pop")
    var_samp = sgqlc.types.Field("meta_ai_app_var_samp_fields", graphql_name="var_samp")
    variance = sgqlc.types.Field("meta_ai_app_variance_fields", graphql_name="variance")


class meta_ai_app_avg_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("threshold",)
    threshold = sgqlc.types.Field(Float, graphql_name="threshold")


class meta_ai_app_max_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "model_id", "threshold")
    id = sgqlc.types.Field(uuid, graphql_name="id")
    model_id = sgqlc.types.Field(uuid, graphql_name="modelId")
    threshold = sgqlc.types.Field(numeric, graphql_name="threshold")


class meta_ai_app_min_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "model_id", "threshold")
    id = sgqlc.types.Field(uuid, graphql_name="id")
    model_id = sgqlc.types.Field(uuid, graphql_name="modelId")
    threshold = sgqlc.types.Field(numeric, graphql_name="threshold")


class meta_ai_app_mutation_response(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("affected_rows", "returning")
    affected_rows = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="affected_rows")
    returning = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_app))), graphql_name="returning"
    )


class meta_ai_app_stddev_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("threshold",)
    threshold = sgqlc.types.Field(Float, graphql_name="threshold")


class meta_ai_app_stddev_pop_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("threshold",)
    threshold = sgqlc.types.Field(Float, graphql_name="threshold")


class meta_ai_app_stddev_samp_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("threshold",)
    threshold = sgqlc.types.Field(Float, graphql_name="threshold")


class meta_ai_app_sum_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("threshold",)
    threshold = sgqlc.types.Field(numeric, graphql_name="threshold")


class meta_ai_app_var_pop_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("threshold",)
    threshold = sgqlc.types.Field(Float, graphql_name="threshold")


class meta_ai_app_var_samp_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("threshold",)
    threshold = sgqlc.types.Field(Float, graphql_name="threshold")


class meta_ai_app_variance_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("threshold",)
    threshold = sgqlc.types.Field(Float, graphql_name="threshold")


class meta_ai_assignment(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("apps", "apps_aggregate", "type")
    apps = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_app))),
        graphql_name="apps",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_app_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_app_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_app_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    apps_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null(meta_ai_app_aggregate),
        graphql_name="apps_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_app_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_app_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_app_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="type")


class meta_ai_assignment_aggregate(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("aggregate", "nodes")
    aggregate = sgqlc.types.Field("meta_ai_assignment_aggregate_fields", graphql_name="aggregate")
    nodes = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_assignment))), graphql_name="nodes"
    )


class meta_ai_assignment_aggregate_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("count", "max", "min")
    count = sgqlc.types.Field(
        sgqlc.types.non_null(Int),
        graphql_name="count",
        args=sgqlc.types.ArgDict(
            (
                (
                    "columns",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_assignment_select_column)),
                        graphql_name="columns",
                        default=None,
                    ),
                ),
                ("distinct", sgqlc.types.Arg(Boolean, graphql_name="distinct", default=None)),
            )
        ),
    )
    max = sgqlc.types.Field("meta_ai_assignment_max_fields", graphql_name="max")
    min = sgqlc.types.Field("meta_ai_assignment_min_fields", graphql_name="min")


class meta_ai_assignment_max_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("type",)
    type = sgqlc.types.Field(String, graphql_name="type")


class meta_ai_assignment_min_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("type",)
    type = sgqlc.types.Field(String, graphql_name="type")


class meta_ai_assignment_mutation_response(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("affected_rows", "returning")
    affected_rows = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="affected_rows")
    returning = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_assignment))), graphql_name="returning"
    )


class meta_ai_dataset(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "app",
        "app_id",
        "created_at",
        "id",
        "metadata",
        "metrics",
        "metrics_aggregate",
        "reference",
        "task_name",
        "updated_at",
    )
    app = sgqlc.types.Field("turbine_app", graphql_name="app")
    app_id = sgqlc.types.Field(uuid, graphql_name="app_id")
    created_at = sgqlc.types.Field(sgqlc.types.non_null(timestamptz), graphql_name="created_at")
    id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name="id")
    metadata = sgqlc.types.Field(
        jsonb,
        graphql_name="metadata",
        args=sgqlc.types.ArgDict((("path", sgqlc.types.Arg(String, graphql_name="path", default=None)),)),
    )
    metrics = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_dataset_metric"))),
        graphql_name="metrics",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_dataset_metric_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_dataset_metric_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_dataset_metric_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    metrics_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("meta_ai_dataset_metric_aggregate"),
        graphql_name="metrics_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_dataset_metric_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_dataset_metric_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_dataset_metric_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    reference = sgqlc.types.Field(String, graphql_name="reference")
    task_name = sgqlc.types.Field(String, graphql_name="task_name")
    updated_at = sgqlc.types.Field(timestamptz, graphql_name="updated_at")


class meta_ai_dataset_aggregate(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("aggregate", "nodes")
    aggregate = sgqlc.types.Field("meta_ai_dataset_aggregate_fields", graphql_name="aggregate")
    nodes = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_dataset))), graphql_name="nodes"
    )


class meta_ai_dataset_aggregate_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("count", "max", "min")
    count = sgqlc.types.Field(
        sgqlc.types.non_null(Int),
        graphql_name="count",
        args=sgqlc.types.ArgDict(
            (
                (
                    "columns",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_dataset_select_column)),
                        graphql_name="columns",
                        default=None,
                    ),
                ),
                ("distinct", sgqlc.types.Arg(Boolean, graphql_name="distinct", default=None)),
            )
        ),
    )
    max = sgqlc.types.Field("meta_ai_dataset_max_fields", graphql_name="max")
    min = sgqlc.types.Field("meta_ai_dataset_min_fields", graphql_name="min")


class meta_ai_dataset_max_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("app_id", "created_at", "id", "reference", "task_name", "updated_at")
    app_id = sgqlc.types.Field(uuid, graphql_name="app_id")
    created_at = sgqlc.types.Field(timestamptz, graphql_name="created_at")
    id = sgqlc.types.Field(uuid, graphql_name="id")
    reference = sgqlc.types.Field(String, graphql_name="reference")
    task_name = sgqlc.types.Field(String, graphql_name="task_name")
    updated_at = sgqlc.types.Field(timestamptz, graphql_name="updated_at")


class meta_ai_dataset_metric(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("created_at", "dataset_id", "id", "metric", "model_id", "updated_at")
    created_at = sgqlc.types.Field(sgqlc.types.non_null(timestamptz), graphql_name="created_at")
    dataset_id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name="dataset_id")
    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="id")
    metric = sgqlc.types.Field(
        sgqlc.types.non_null(jsonb),
        graphql_name="metric",
        args=sgqlc.types.ArgDict((("path", sgqlc.types.Arg(String, graphql_name="path", default=None)),)),
    )
    model_id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name="model_id")
    updated_at = sgqlc.types.Field(timestamptz, graphql_name="updated_at")


class meta_ai_dataset_metric_aggregate(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("aggregate", "nodes")
    aggregate = sgqlc.types.Field("meta_ai_dataset_metric_aggregate_fields", graphql_name="aggregate")
    nodes = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_dataset_metric))), graphql_name="nodes"
    )


class meta_ai_dataset_metric_aggregate_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "avg",
        "count",
        "max",
        "min",
        "stddev",
        "stddev_pop",
        "stddev_samp",
        "sum",
        "var_pop",
        "var_samp",
        "variance",
    )
    avg = sgqlc.types.Field("meta_ai_dataset_metric_avg_fields", graphql_name="avg")
    count = sgqlc.types.Field(
        sgqlc.types.non_null(Int),
        graphql_name="count",
        args=sgqlc.types.ArgDict(
            (
                (
                    "columns",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_dataset_metric_select_column)),
                        graphql_name="columns",
                        default=None,
                    ),
                ),
                ("distinct", sgqlc.types.Arg(Boolean, graphql_name="distinct", default=None)),
            )
        ),
    )
    max = sgqlc.types.Field("meta_ai_dataset_metric_max_fields", graphql_name="max")
    min = sgqlc.types.Field("meta_ai_dataset_metric_min_fields", graphql_name="min")
    stddev = sgqlc.types.Field("meta_ai_dataset_metric_stddev_fields", graphql_name="stddev")
    stddev_pop = sgqlc.types.Field("meta_ai_dataset_metric_stddev_pop_fields", graphql_name="stddev_pop")
    stddev_samp = sgqlc.types.Field("meta_ai_dataset_metric_stddev_samp_fields", graphql_name="stddev_samp")
    sum = sgqlc.types.Field("meta_ai_dataset_metric_sum_fields", graphql_name="sum")
    var_pop = sgqlc.types.Field("meta_ai_dataset_metric_var_pop_fields", graphql_name="var_pop")
    var_samp = sgqlc.types.Field("meta_ai_dataset_metric_var_samp_fields", graphql_name="var_samp")
    variance = sgqlc.types.Field("meta_ai_dataset_metric_variance_fields", graphql_name="variance")


class meta_ai_dataset_metric_avg_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(Float, graphql_name="id")


class meta_ai_dataset_metric_max_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("created_at", "dataset_id", "id", "model_id", "updated_at")
    created_at = sgqlc.types.Field(timestamptz, graphql_name="created_at")
    dataset_id = sgqlc.types.Field(uuid, graphql_name="dataset_id")
    id = sgqlc.types.Field(Int, graphql_name="id")
    model_id = sgqlc.types.Field(uuid, graphql_name="model_id")
    updated_at = sgqlc.types.Field(timestamptz, graphql_name="updated_at")


class meta_ai_dataset_metric_min_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("created_at", "dataset_id", "id", "model_id", "updated_at")
    created_at = sgqlc.types.Field(timestamptz, graphql_name="created_at")
    dataset_id = sgqlc.types.Field(uuid, graphql_name="dataset_id")
    id = sgqlc.types.Field(Int, graphql_name="id")
    model_id = sgqlc.types.Field(uuid, graphql_name="model_id")
    updated_at = sgqlc.types.Field(timestamptz, graphql_name="updated_at")


class meta_ai_dataset_metric_mutation_response(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("affected_rows", "returning")
    affected_rows = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="affected_rows")
    returning = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_dataset_metric))),
        graphql_name="returning",
    )


class meta_ai_dataset_metric_stddev_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(Float, graphql_name="id")


class meta_ai_dataset_metric_stddev_pop_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(Float, graphql_name="id")


class meta_ai_dataset_metric_stddev_samp_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(Float, graphql_name="id")


class meta_ai_dataset_metric_sum_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(Int, graphql_name="id")


class meta_ai_dataset_metric_var_pop_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(Float, graphql_name="id")


class meta_ai_dataset_metric_var_samp_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(Float, graphql_name="id")


class meta_ai_dataset_metric_variance_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(Float, graphql_name="id")


class meta_ai_dataset_min_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("app_id", "created_at", "id", "reference", "task_name", "updated_at")
    app_id = sgqlc.types.Field(uuid, graphql_name="app_id")
    created_at = sgqlc.types.Field(timestamptz, graphql_name="created_at")
    id = sgqlc.types.Field(uuid, graphql_name="id")
    reference = sgqlc.types.Field(String, graphql_name="reference")
    task_name = sgqlc.types.Field(String, graphql_name="task_name")
    updated_at = sgqlc.types.Field(timestamptz, graphql_name="updated_at")


class meta_ai_dataset_mutation_response(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("affected_rows", "returning")
    affected_rows = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="affected_rows")
    returning = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_dataset))), graphql_name="returning"
    )


class meta_ai_deployment(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "created_at",
        "current_log",
        "current_log_id",
        "deployment_logs",
        "deployment_logs_aggregate",
        "endpoint",
        "id",
        "image",
        "min_instances",
        "model",
        "model_id",
        "owner_id",
        "properties",
        "purpose",
        "scale_in_timeout",
        "state_timestamp",
        "status",
        "target_status",
        "training_id",
        "type",
        "updated_at",
    )
    created_at = sgqlc.types.Field(sgqlc.types.non_null(timestamptz), graphql_name="created_at")
    current_log = sgqlc.types.Field("meta_ai_deployment_log", graphql_name="current_log")
    current_log_id = sgqlc.types.Field(Int, graphql_name="current_log_id")
    deployment_logs = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_deployment_log"))),
        graphql_name="deployment_logs",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_log_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_log_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_deployment_log_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    deployment_logs_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("meta_ai_deployment_log_aggregate"),
        graphql_name="deployment_logs_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_log_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_log_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_deployment_log_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    endpoint = sgqlc.types.Field(String, graphql_name="endpoint")
    id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name="id")
    image = sgqlc.types.Field(String, graphql_name="image")
    min_instances = sgqlc.types.Field(Int, graphql_name="min_instances")
    model = sgqlc.types.Field(sgqlc.types.non_null("meta_ai_model"), graphql_name="model")
    model_id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name="modelId")
    owner_id = sgqlc.types.Field(bigint, graphql_name="ownerId")
    properties = sgqlc.types.Field(
        jsonb,
        graphql_name="properties",
        args=sgqlc.types.ArgDict((("path", sgqlc.types.Arg(String, graphql_name="path", default=None)),)),
    )
    purpose = sgqlc.types.Field(meta_ai_deployment_purpose_enum, graphql_name="purpose")
    scale_in_timeout = sgqlc.types.Field(Int, graphql_name="scale_in_timeout")
    state_timestamp = sgqlc.types.Field(timestamptz, graphql_name="state_timestamp")
    status = sgqlc.types.Field(meta_ai_deployment_status_enum, graphql_name="status")
    target_status = sgqlc.types.Field(meta_ai_deployment_status_enum, graphql_name="target_status")
    training_id = sgqlc.types.Field(uuid, graphql_name="training_id")
    type = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_deployment_type_enum), graphql_name="type")
    updated_at = sgqlc.types.Field(sgqlc.types.non_null(timestamptz), graphql_name="updated_at")


class meta_ai_deployment_aggregate(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("aggregate", "nodes")
    aggregate = sgqlc.types.Field("meta_ai_deployment_aggregate_fields", graphql_name="aggregate")
    nodes = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment))), graphql_name="nodes"
    )


class meta_ai_deployment_aggregate_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "avg",
        "count",
        "max",
        "min",
        "stddev",
        "stddev_pop",
        "stddev_samp",
        "sum",
        "var_pop",
        "var_samp",
        "variance",
    )
    avg = sgqlc.types.Field("meta_ai_deployment_avg_fields", graphql_name="avg")
    count = sgqlc.types.Field(
        sgqlc.types.non_null(Int),
        graphql_name="count",
        args=sgqlc.types.ArgDict(
            (
                (
                    "columns",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_select_column)),
                        graphql_name="columns",
                        default=None,
                    ),
                ),
                ("distinct", sgqlc.types.Arg(Boolean, graphql_name="distinct", default=None)),
            )
        ),
    )
    max = sgqlc.types.Field("meta_ai_deployment_max_fields", graphql_name="max")
    min = sgqlc.types.Field("meta_ai_deployment_min_fields", graphql_name="min")
    stddev = sgqlc.types.Field("meta_ai_deployment_stddev_fields", graphql_name="stddev")
    stddev_pop = sgqlc.types.Field("meta_ai_deployment_stddev_pop_fields", graphql_name="stddev_pop")
    stddev_samp = sgqlc.types.Field("meta_ai_deployment_stddev_samp_fields", graphql_name="stddev_samp")
    sum = sgqlc.types.Field("meta_ai_deployment_sum_fields", graphql_name="sum")
    var_pop = sgqlc.types.Field("meta_ai_deployment_var_pop_fields", graphql_name="var_pop")
    var_samp = sgqlc.types.Field("meta_ai_deployment_var_samp_fields", graphql_name="var_samp")
    variance = sgqlc.types.Field("meta_ai_deployment_variance_fields", graphql_name="variance")


class meta_ai_deployment_avg_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("current_log_id", "min_instances", "owner_id", "scale_in_timeout")
    current_log_id = sgqlc.types.Field(Float, graphql_name="current_log_id")
    min_instances = sgqlc.types.Field(Float, graphql_name="min_instances")
    owner_id = sgqlc.types.Field(Float, graphql_name="ownerId")
    scale_in_timeout = sgqlc.types.Field(Float, graphql_name="scale_in_timeout")


class meta_ai_deployment_log(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("deployment", "deployment_id", "id", "started_at", "stopped_at")
    deployment = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_deployment), graphql_name="deployment")
    deployment_id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name="deployment_id")
    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="id")
    started_at = sgqlc.types.Field(sgqlc.types.non_null(timestamptz), graphql_name="started_at")
    stopped_at = sgqlc.types.Field(timestamptz, graphql_name="stopped_at")


class meta_ai_deployment_log_aggregate(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("aggregate", "nodes")
    aggregate = sgqlc.types.Field("meta_ai_deployment_log_aggregate_fields", graphql_name="aggregate")
    nodes = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_log))), graphql_name="nodes"
    )


class meta_ai_deployment_log_aggregate_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "avg",
        "count",
        "max",
        "min",
        "stddev",
        "stddev_pop",
        "stddev_samp",
        "sum",
        "var_pop",
        "var_samp",
        "variance",
    )
    avg = sgqlc.types.Field("meta_ai_deployment_log_avg_fields", graphql_name="avg")
    count = sgqlc.types.Field(
        sgqlc.types.non_null(Int),
        graphql_name="count",
        args=sgqlc.types.ArgDict(
            (
                (
                    "columns",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_log_select_column)),
                        graphql_name="columns",
                        default=None,
                    ),
                ),
                ("distinct", sgqlc.types.Arg(Boolean, graphql_name="distinct", default=None)),
            )
        ),
    )
    max = sgqlc.types.Field("meta_ai_deployment_log_max_fields", graphql_name="max")
    min = sgqlc.types.Field("meta_ai_deployment_log_min_fields", graphql_name="min")
    stddev = sgqlc.types.Field("meta_ai_deployment_log_stddev_fields", graphql_name="stddev")
    stddev_pop = sgqlc.types.Field("meta_ai_deployment_log_stddev_pop_fields", graphql_name="stddev_pop")
    stddev_samp = sgqlc.types.Field("meta_ai_deployment_log_stddev_samp_fields", graphql_name="stddev_samp")
    sum = sgqlc.types.Field("meta_ai_deployment_log_sum_fields", graphql_name="sum")
    var_pop = sgqlc.types.Field("meta_ai_deployment_log_var_pop_fields", graphql_name="var_pop")
    var_samp = sgqlc.types.Field("meta_ai_deployment_log_var_samp_fields", graphql_name="var_samp")
    variance = sgqlc.types.Field("meta_ai_deployment_log_variance_fields", graphql_name="variance")


class meta_ai_deployment_log_avg_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(Float, graphql_name="id")


class meta_ai_deployment_log_max_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("deployment_id", "id", "started_at", "stopped_at")
    deployment_id = sgqlc.types.Field(uuid, graphql_name="deployment_id")
    id = sgqlc.types.Field(Int, graphql_name="id")
    started_at = sgqlc.types.Field(timestamptz, graphql_name="started_at")
    stopped_at = sgqlc.types.Field(timestamptz, graphql_name="stopped_at")


class meta_ai_deployment_log_min_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("deployment_id", "id", "started_at", "stopped_at")
    deployment_id = sgqlc.types.Field(uuid, graphql_name="deployment_id")
    id = sgqlc.types.Field(Int, graphql_name="id")
    started_at = sgqlc.types.Field(timestamptz, graphql_name="started_at")
    stopped_at = sgqlc.types.Field(timestamptz, graphql_name="stopped_at")


class meta_ai_deployment_log_mutation_response(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("affected_rows", "returning")
    affected_rows = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="affected_rows")
    returning = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_log))),
        graphql_name="returning",
    )


class meta_ai_deployment_log_stddev_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(Float, graphql_name="id")


class meta_ai_deployment_log_stddev_pop_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(Float, graphql_name="id")


class meta_ai_deployment_log_stddev_samp_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(Float, graphql_name="id")


class meta_ai_deployment_log_sum_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(Int, graphql_name="id")


class meta_ai_deployment_log_var_pop_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(Float, graphql_name="id")


class meta_ai_deployment_log_var_samp_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(Float, graphql_name="id")


class meta_ai_deployment_log_variance_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(Float, graphql_name="id")


class meta_ai_deployment_max_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "created_at",
        "current_log_id",
        "endpoint",
        "id",
        "image",
        "min_instances",
        "model_id",
        "owner_id",
        "scale_in_timeout",
        "state_timestamp",
        "training_id",
        "updated_at",
    )
    created_at = sgqlc.types.Field(timestamptz, graphql_name="created_at")
    current_log_id = sgqlc.types.Field(Int, graphql_name="current_log_id")
    endpoint = sgqlc.types.Field(String, graphql_name="endpoint")
    id = sgqlc.types.Field(uuid, graphql_name="id")
    image = sgqlc.types.Field(String, graphql_name="image")
    min_instances = sgqlc.types.Field(Int, graphql_name="min_instances")
    model_id = sgqlc.types.Field(uuid, graphql_name="modelId")
    owner_id = sgqlc.types.Field(bigint, graphql_name="ownerId")
    scale_in_timeout = sgqlc.types.Field(Int, graphql_name="scale_in_timeout")
    state_timestamp = sgqlc.types.Field(timestamptz, graphql_name="state_timestamp")
    training_id = sgqlc.types.Field(uuid, graphql_name="training_id")
    updated_at = sgqlc.types.Field(timestamptz, graphql_name="updated_at")


class meta_ai_deployment_min_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "created_at",
        "current_log_id",
        "endpoint",
        "id",
        "image",
        "min_instances",
        "model_id",
        "owner_id",
        "scale_in_timeout",
        "state_timestamp",
        "training_id",
        "updated_at",
    )
    created_at = sgqlc.types.Field(timestamptz, graphql_name="created_at")
    current_log_id = sgqlc.types.Field(Int, graphql_name="current_log_id")
    endpoint = sgqlc.types.Field(String, graphql_name="endpoint")
    id = sgqlc.types.Field(uuid, graphql_name="id")
    image = sgqlc.types.Field(String, graphql_name="image")
    min_instances = sgqlc.types.Field(Int, graphql_name="min_instances")
    model_id = sgqlc.types.Field(uuid, graphql_name="modelId")
    owner_id = sgqlc.types.Field(bigint, graphql_name="ownerId")
    scale_in_timeout = sgqlc.types.Field(Int, graphql_name="scale_in_timeout")
    state_timestamp = sgqlc.types.Field(timestamptz, graphql_name="state_timestamp")
    training_id = sgqlc.types.Field(uuid, graphql_name="training_id")
    updated_at = sgqlc.types.Field(timestamptz, graphql_name="updated_at")


class meta_ai_deployment_mutation_response(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("affected_rows", "returning")
    affected_rows = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="affected_rows")
    returning = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment))), graphql_name="returning"
    )


class meta_ai_deployment_purpose(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("deployments", "deployments_aggregate", "purpose")
    deployments = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment))),
        graphql_name="deployments",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_deployment_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    deployments_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null(meta_ai_deployment_aggregate),
        graphql_name="deployments_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_deployment_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    purpose = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="purpose")


class meta_ai_deployment_purpose_aggregate(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("aggregate", "nodes")
    aggregate = sgqlc.types.Field("meta_ai_deployment_purpose_aggregate_fields", graphql_name="aggregate")
    nodes = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_purpose))),
        graphql_name="nodes",
    )


class meta_ai_deployment_purpose_aggregate_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("count", "max", "min")
    count = sgqlc.types.Field(
        sgqlc.types.non_null(Int),
        graphql_name="count",
        args=sgqlc.types.ArgDict(
            (
                (
                    "columns",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_purpose_select_column)),
                        graphql_name="columns",
                        default=None,
                    ),
                ),
                ("distinct", sgqlc.types.Arg(Boolean, graphql_name="distinct", default=None)),
            )
        ),
    )
    max = sgqlc.types.Field("meta_ai_deployment_purpose_max_fields", graphql_name="max")
    min = sgqlc.types.Field("meta_ai_deployment_purpose_min_fields", graphql_name="min")


class meta_ai_deployment_purpose_max_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("purpose",)
    purpose = sgqlc.types.Field(String, graphql_name="purpose")


class meta_ai_deployment_purpose_min_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("purpose",)
    purpose = sgqlc.types.Field(String, graphql_name="purpose")


class meta_ai_deployment_purpose_mutation_response(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("affected_rows", "returning")
    affected_rows = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="affected_rows")
    returning = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_purpose))),
        graphql_name="returning",
    )


class meta_ai_deployment_status(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "deployments",
        "deployments_by_target_status",
        "deployments_by_target_status_aggregate",
        "deployments_aggregate",
        "status",
    )
    deployments = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment))),
        graphql_name="deployments",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_deployment_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    deployments_by_target_status = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment))),
        graphql_name="deploymentsByTargetStatus",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_deployment_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    deployments_by_target_status_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null(meta_ai_deployment_aggregate),
        graphql_name="deploymentsByTargetStatus_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_deployment_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    deployments_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null(meta_ai_deployment_aggregate),
        graphql_name="deployments_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_deployment_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    status = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="status")


class meta_ai_deployment_status_aggregate(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("aggregate", "nodes")
    aggregate = sgqlc.types.Field("meta_ai_deployment_status_aggregate_fields", graphql_name="aggregate")
    nodes = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_status))), graphql_name="nodes"
    )


class meta_ai_deployment_status_aggregate_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("count", "max", "min")
    count = sgqlc.types.Field(
        sgqlc.types.non_null(Int),
        graphql_name="count",
        args=sgqlc.types.ArgDict(
            (
                (
                    "columns",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_status_select_column)),
                        graphql_name="columns",
                        default=None,
                    ),
                ),
                ("distinct", sgqlc.types.Arg(Boolean, graphql_name="distinct", default=None)),
            )
        ),
    )
    max = sgqlc.types.Field("meta_ai_deployment_status_max_fields", graphql_name="max")
    min = sgqlc.types.Field("meta_ai_deployment_status_min_fields", graphql_name="min")


class meta_ai_deployment_status_max_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("status",)
    status = sgqlc.types.Field(String, graphql_name="status")


class meta_ai_deployment_status_min_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("status",)
    status = sgqlc.types.Field(String, graphql_name="status")


class meta_ai_deployment_status_mutation_response(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("affected_rows", "returning")
    affected_rows = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="affected_rows")
    returning = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_status))),
        graphql_name="returning",
    )


class meta_ai_deployment_stddev_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("current_log_id", "min_instances", "owner_id", "scale_in_timeout")
    current_log_id = sgqlc.types.Field(Float, graphql_name="current_log_id")
    min_instances = sgqlc.types.Field(Float, graphql_name="min_instances")
    owner_id = sgqlc.types.Field(Float, graphql_name="ownerId")
    scale_in_timeout = sgqlc.types.Field(Float, graphql_name="scale_in_timeout")


class meta_ai_deployment_stddev_pop_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("current_log_id", "min_instances", "owner_id", "scale_in_timeout")
    current_log_id = sgqlc.types.Field(Float, graphql_name="current_log_id")
    min_instances = sgqlc.types.Field(Float, graphql_name="min_instances")
    owner_id = sgqlc.types.Field(Float, graphql_name="ownerId")
    scale_in_timeout = sgqlc.types.Field(Float, graphql_name="scale_in_timeout")


class meta_ai_deployment_stddev_samp_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("current_log_id", "min_instances", "owner_id", "scale_in_timeout")
    current_log_id = sgqlc.types.Field(Float, graphql_name="current_log_id")
    min_instances = sgqlc.types.Field(Float, graphql_name="min_instances")
    owner_id = sgqlc.types.Field(Float, graphql_name="ownerId")
    scale_in_timeout = sgqlc.types.Field(Float, graphql_name="scale_in_timeout")


class meta_ai_deployment_sum_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("current_log_id", "min_instances", "owner_id", "scale_in_timeout")
    current_log_id = sgqlc.types.Field(Int, graphql_name="current_log_id")
    min_instances = sgqlc.types.Field(Int, graphql_name="min_instances")
    owner_id = sgqlc.types.Field(bigint, graphql_name="ownerId")
    scale_in_timeout = sgqlc.types.Field(Int, graphql_name="scale_in_timeout")


class meta_ai_deployment_type(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("deployments", "deployments_aggregate", "name")
    deployments = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment))),
        graphql_name="deployments",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_deployment_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    deployments_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null(meta_ai_deployment_aggregate),
        graphql_name="deployments_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_deployment_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")


class meta_ai_deployment_type_aggregate(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("aggregate", "nodes")
    aggregate = sgqlc.types.Field("meta_ai_deployment_type_aggregate_fields", graphql_name="aggregate")
    nodes = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_type))), graphql_name="nodes"
    )


class meta_ai_deployment_type_aggregate_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("count", "max", "min")
    count = sgqlc.types.Field(
        sgqlc.types.non_null(Int),
        graphql_name="count",
        args=sgqlc.types.ArgDict(
            (
                (
                    "columns",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_type_select_column)),
                        graphql_name="columns",
                        default=None,
                    ),
                ),
                ("distinct", sgqlc.types.Arg(Boolean, graphql_name="distinct", default=None)),
            )
        ),
    )
    max = sgqlc.types.Field("meta_ai_deployment_type_max_fields", graphql_name="max")
    min = sgqlc.types.Field("meta_ai_deployment_type_min_fields", graphql_name="min")


class meta_ai_deployment_type_max_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("name",)
    name = sgqlc.types.Field(String, graphql_name="name")


class meta_ai_deployment_type_min_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("name",)
    name = sgqlc.types.Field(String, graphql_name="name")


class meta_ai_deployment_type_mutation_response(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("affected_rows", "returning")
    affected_rows = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="affected_rows")
    returning = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_type))),
        graphql_name="returning",
    )


class meta_ai_deployment_var_pop_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("current_log_id", "min_instances", "owner_id", "scale_in_timeout")
    current_log_id = sgqlc.types.Field(Float, graphql_name="current_log_id")
    min_instances = sgqlc.types.Field(Float, graphql_name="min_instances")
    owner_id = sgqlc.types.Field(Float, graphql_name="ownerId")
    scale_in_timeout = sgqlc.types.Field(Float, graphql_name="scale_in_timeout")


class meta_ai_deployment_var_samp_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("current_log_id", "min_instances", "owner_id", "scale_in_timeout")
    current_log_id = sgqlc.types.Field(Float, graphql_name="current_log_id")
    min_instances = sgqlc.types.Field(Float, graphql_name="min_instances")
    owner_id = sgqlc.types.Field(Float, graphql_name="ownerId")
    scale_in_timeout = sgqlc.types.Field(Float, graphql_name="scale_in_timeout")


class meta_ai_deployment_variance_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("current_log_id", "min_instances", "owner_id", "scale_in_timeout")
    current_log_id = sgqlc.types.Field(Float, graphql_name="current_log_id")
    min_instances = sgqlc.types.Field(Float, graphql_name="min_instances")
    owner_id = sgqlc.types.Field(Float, graphql_name="ownerId")
    scale_in_timeout = sgqlc.types.Field(Float, graphql_name="scale_in_timeout")


class meta_ai_environment(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("name",)
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")


class meta_ai_environment_aggregate(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("aggregate", "nodes")
    aggregate = sgqlc.types.Field("meta_ai_environment_aggregate_fields", graphql_name="aggregate")
    nodes = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_environment))), graphql_name="nodes"
    )


class meta_ai_environment_aggregate_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("count", "max", "min")
    count = sgqlc.types.Field(
        sgqlc.types.non_null(Int),
        graphql_name="count",
        args=sgqlc.types.ArgDict(
            (
                (
                    "columns",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_environment_select_column)),
                        graphql_name="columns",
                        default=None,
                    ),
                ),
                ("distinct", sgqlc.types.Arg(Boolean, graphql_name="distinct", default=None)),
            )
        ),
    )
    max = sgqlc.types.Field("meta_ai_environment_max_fields", graphql_name="max")
    min = sgqlc.types.Field("meta_ai_environment_min_fields", graphql_name="min")


class meta_ai_environment_max_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("name",)
    name = sgqlc.types.Field(String, graphql_name="name")


class meta_ai_environment_min_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("name",)
    name = sgqlc.types.Field(String, graphql_name="name")


class meta_ai_environment_mutation_response(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("affected_rows", "returning")
    affected_rows = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="affected_rows")
    returning = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_environment))), graphql_name="returning"
    )


class meta_ai_instance(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "output", "prediction", "prediction_id", "score")
    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="id")
    output = sgqlc.types.Field(
        jsonb,
        graphql_name="output",
        args=sgqlc.types.ArgDict((("path", sgqlc.types.Arg(String, graphql_name="path", default=None)),)),
    )
    prediction = sgqlc.types.Field(sgqlc.types.non_null("meta_ai_prediction"), graphql_name="prediction")
    prediction_id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name="predictionId")
    score = sgqlc.types.Field(float8, graphql_name="score")


class meta_ai_instance_aggregate(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("aggregate", "nodes")
    aggregate = sgqlc.types.Field("meta_ai_instance_aggregate_fields", graphql_name="aggregate")
    nodes = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_instance))), graphql_name="nodes"
    )


class meta_ai_instance_aggregate_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "avg",
        "count",
        "max",
        "min",
        "stddev",
        "stddev_pop",
        "stddev_samp",
        "sum",
        "var_pop",
        "var_samp",
        "variance",
    )
    avg = sgqlc.types.Field("meta_ai_instance_avg_fields", graphql_name="avg")
    count = sgqlc.types.Field(
        sgqlc.types.non_null(Int),
        graphql_name="count",
        args=sgqlc.types.ArgDict(
            (
                (
                    "columns",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_instance_select_column)),
                        graphql_name="columns",
                        default=None,
                    ),
                ),
                ("distinct", sgqlc.types.Arg(Boolean, graphql_name="distinct", default=None)),
            )
        ),
    )
    max = sgqlc.types.Field("meta_ai_instance_max_fields", graphql_name="max")
    min = sgqlc.types.Field("meta_ai_instance_min_fields", graphql_name="min")
    stddev = sgqlc.types.Field("meta_ai_instance_stddev_fields", graphql_name="stddev")
    stddev_pop = sgqlc.types.Field("meta_ai_instance_stddev_pop_fields", graphql_name="stddev_pop")
    stddev_samp = sgqlc.types.Field("meta_ai_instance_stddev_samp_fields", graphql_name="stddev_samp")
    sum = sgqlc.types.Field("meta_ai_instance_sum_fields", graphql_name="sum")
    var_pop = sgqlc.types.Field("meta_ai_instance_var_pop_fields", graphql_name="var_pop")
    var_samp = sgqlc.types.Field("meta_ai_instance_var_samp_fields", graphql_name="var_samp")
    variance = sgqlc.types.Field("meta_ai_instance_variance_fields", graphql_name="variance")


class meta_ai_instance_avg_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "score")
    id = sgqlc.types.Field(Float, graphql_name="id")
    score = sgqlc.types.Field(Float, graphql_name="score")


class meta_ai_instance_max_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "prediction_id", "score")
    id = sgqlc.types.Field(Int, graphql_name="id")
    prediction_id = sgqlc.types.Field(uuid, graphql_name="predictionId")
    score = sgqlc.types.Field(float8, graphql_name="score")


class meta_ai_instance_min_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "prediction_id", "score")
    id = sgqlc.types.Field(Int, graphql_name="id")
    prediction_id = sgqlc.types.Field(uuid, graphql_name="predictionId")
    score = sgqlc.types.Field(float8, graphql_name="score")


class meta_ai_instance_mutation_response(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("affected_rows", "returning")
    affected_rows = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="affected_rows")
    returning = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_instance))), graphql_name="returning"
    )


class meta_ai_instance_stddev_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "score")
    id = sgqlc.types.Field(Float, graphql_name="id")
    score = sgqlc.types.Field(Float, graphql_name="score")


class meta_ai_instance_stddev_pop_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "score")
    id = sgqlc.types.Field(Float, graphql_name="id")
    score = sgqlc.types.Field(Float, graphql_name="score")


class meta_ai_instance_stddev_samp_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "score")
    id = sgqlc.types.Field(Float, graphql_name="id")
    score = sgqlc.types.Field(Float, graphql_name="score")


class meta_ai_instance_sum_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "score")
    id = sgqlc.types.Field(Int, graphql_name="id")
    score = sgqlc.types.Field(float8, graphql_name="score")


class meta_ai_instance_var_pop_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "score")
    id = sgqlc.types.Field(Float, graphql_name="id")
    score = sgqlc.types.Field(Float, graphql_name="score")


class meta_ai_instance_var_samp_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "score")
    id = sgqlc.types.Field(Float, graphql_name="id")
    score = sgqlc.types.Field(Float, graphql_name="score")


class meta_ai_instance_variance_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "score")
    id = sgqlc.types.Field(Float, graphql_name="id")
    score = sgqlc.types.Field(Float, graphql_name="score")


class meta_ai_model(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "ai_worker_id",
        "ai_worker_username",
        "apps",
        "apps_aggregate",
        "created_at",
        "default_training_parameters",
        "deployment",
        "description",
        "editor_id",
        "endpoint",
        "id",
        "image",
        "input_schema",
        "metadata",
        "model_save_path",
        "name",
        "output_schema",
        "owner_id",
        "predictions",
        "predictions_aggregate",
        "root_id",
        "root_model",
        "served_by",
        "sibling_models",
        "sibling_models_aggregate",
        "stage",
        "trainable",
        "updated_at",
        "version",
        "visibility",
        "weights_path",
    )
    ai_worker_id = sgqlc.types.Field(Int, graphql_name="ai_worker_id")
    ai_worker_username = sgqlc.types.Field(String, graphql_name="ai_worker_username")
    apps = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_app))),
        graphql_name="apps",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_app_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_app_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_app_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    apps_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null(meta_ai_app_aggregate),
        graphql_name="apps_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_app_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_app_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_app_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    created_at = sgqlc.types.Field(sgqlc.types.non_null(timestamptz), graphql_name="createdAt")
    default_training_parameters = sgqlc.types.Field(
        jsonb,
        graphql_name="default_training_parameters",
        args=sgqlc.types.ArgDict((("path", sgqlc.types.Arg(String, graphql_name="path", default=None)),)),
    )
    deployment = sgqlc.types.Field(meta_ai_deployment, graphql_name="deployment")
    description = sgqlc.types.Field(String, graphql_name="description")
    editor_id = sgqlc.types.Field(bigint, graphql_name="editorId")
    endpoint = sgqlc.types.Field(String, graphql_name="endpoint")
    id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name="id")
    image = sgqlc.types.Field(String, graphql_name="image")
    input_schema = sgqlc.types.Field(
        jsonb,
        graphql_name="inputSchema",
        args=sgqlc.types.ArgDict((("path", sgqlc.types.Arg(String, graphql_name="path", default=None)),)),
    )
    metadata = sgqlc.types.Field(
        jsonb,
        graphql_name="metadata",
        args=sgqlc.types.ArgDict((("path", sgqlc.types.Arg(String, graphql_name="path", default=None)),)),
    )
    model_save_path = sgqlc.types.Field(String, graphql_name="modelSavePath")
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")
    output_schema = sgqlc.types.Field(
        jsonb,
        graphql_name="outputSchema",
        args=sgqlc.types.ArgDict((("path", sgqlc.types.Arg(String, graphql_name="path", default=None)),)),
    )
    owner_id = sgqlc.types.Field(sgqlc.types.non_null(bigint), graphql_name="ownerId")
    predictions = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_prediction"))),
        graphql_name="predictions",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_prediction_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    predictions_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("meta_ai_prediction_aggregate"),
        graphql_name="predictions_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_prediction_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    root_id = sgqlc.types.Field(uuid, graphql_name="root_id")
    root_model = sgqlc.types.Field("meta_ai_model", graphql_name="root_model")
    served_by = sgqlc.types.Field(uuid, graphql_name="served_by")
    sibling_models = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_model"))),
        graphql_name="sibling_models",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_model_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_model_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_model_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    sibling_models_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("meta_ai_model_aggregate"),
        graphql_name="sibling_models_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_model_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_model_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_model_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    stage = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_environment_enum), graphql_name="stage")
    trainable = sgqlc.types.Field(Boolean, graphql_name="trainable")
    updated_at = sgqlc.types.Field(timestamptz, graphql_name="updatedAt")
    version = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="version")
    visibility = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_visibility_enum), graphql_name="visibility")
    weights_path = sgqlc.types.Field(String, graphql_name="weightsPath")


class meta_ai_model_aggregate(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("aggregate", "nodes")
    aggregate = sgqlc.types.Field("meta_ai_model_aggregate_fields", graphql_name="aggregate")
    nodes = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_model))), graphql_name="nodes"
    )


class meta_ai_model_aggregate_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "avg",
        "count",
        "max",
        "min",
        "stddev",
        "stddev_pop",
        "stddev_samp",
        "sum",
        "var_pop",
        "var_samp",
        "variance",
    )
    avg = sgqlc.types.Field("meta_ai_model_avg_fields", graphql_name="avg")
    count = sgqlc.types.Field(
        sgqlc.types.non_null(Int),
        graphql_name="count",
        args=sgqlc.types.ArgDict(
            (
                (
                    "columns",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_model_select_column)),
                        graphql_name="columns",
                        default=None,
                    ),
                ),
                ("distinct", sgqlc.types.Arg(Boolean, graphql_name="distinct", default=None)),
            )
        ),
    )
    max = sgqlc.types.Field("meta_ai_model_max_fields", graphql_name="max")
    min = sgqlc.types.Field("meta_ai_model_min_fields", graphql_name="min")
    stddev = sgqlc.types.Field("meta_ai_model_stddev_fields", graphql_name="stddev")
    stddev_pop = sgqlc.types.Field("meta_ai_model_stddev_pop_fields", graphql_name="stddev_pop")
    stddev_samp = sgqlc.types.Field("meta_ai_model_stddev_samp_fields", graphql_name="stddev_samp")
    sum = sgqlc.types.Field("meta_ai_model_sum_fields", graphql_name="sum")
    var_pop = sgqlc.types.Field("meta_ai_model_var_pop_fields", graphql_name="var_pop")
    var_samp = sgqlc.types.Field("meta_ai_model_var_samp_fields", graphql_name="var_samp")
    variance = sgqlc.types.Field("meta_ai_model_variance_fields", graphql_name="variance")


class meta_ai_model_avg_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("ai_worker_id", "editor_id", "owner_id", "version")
    ai_worker_id = sgqlc.types.Field(Float, graphql_name="ai_worker_id")
    editor_id = sgqlc.types.Field(Float, graphql_name="editorId")
    owner_id = sgqlc.types.Field(Float, graphql_name="ownerId")
    version = sgqlc.types.Field(Float, graphql_name="version")


class meta_ai_model_max_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "ai_worker_id",
        "ai_worker_username",
        "created_at",
        "description",
        "editor_id",
        "endpoint",
        "id",
        "image",
        "model_save_path",
        "name",
        "owner_id",
        "root_id",
        "served_by",
        "updated_at",
        "version",
        "weights_path",
    )
    ai_worker_id = sgqlc.types.Field(Int, graphql_name="ai_worker_id")
    ai_worker_username = sgqlc.types.Field(String, graphql_name="ai_worker_username")
    created_at = sgqlc.types.Field(timestamptz, graphql_name="createdAt")
    description = sgqlc.types.Field(String, graphql_name="description")
    editor_id = sgqlc.types.Field(bigint, graphql_name="editorId")
    endpoint = sgqlc.types.Field(String, graphql_name="endpoint")
    id = sgqlc.types.Field(uuid, graphql_name="id")
    image = sgqlc.types.Field(String, graphql_name="image")
    model_save_path = sgqlc.types.Field(String, graphql_name="modelSavePath")
    name = sgqlc.types.Field(String, graphql_name="name")
    owner_id = sgqlc.types.Field(bigint, graphql_name="ownerId")
    root_id = sgqlc.types.Field(uuid, graphql_name="root_id")
    served_by = sgqlc.types.Field(uuid, graphql_name="served_by")
    updated_at = sgqlc.types.Field(timestamptz, graphql_name="updatedAt")
    version = sgqlc.types.Field(Int, graphql_name="version")
    weights_path = sgqlc.types.Field(String, graphql_name="weightsPath")


class meta_ai_model_min_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "ai_worker_id",
        "ai_worker_username",
        "created_at",
        "description",
        "editor_id",
        "endpoint",
        "id",
        "image",
        "model_save_path",
        "name",
        "owner_id",
        "root_id",
        "served_by",
        "updated_at",
        "version",
        "weights_path",
    )
    ai_worker_id = sgqlc.types.Field(Int, graphql_name="ai_worker_id")
    ai_worker_username = sgqlc.types.Field(String, graphql_name="ai_worker_username")
    created_at = sgqlc.types.Field(timestamptz, graphql_name="createdAt")
    description = sgqlc.types.Field(String, graphql_name="description")
    editor_id = sgqlc.types.Field(bigint, graphql_name="editorId")
    endpoint = sgqlc.types.Field(String, graphql_name="endpoint")
    id = sgqlc.types.Field(uuid, graphql_name="id")
    image = sgqlc.types.Field(String, graphql_name="image")
    model_save_path = sgqlc.types.Field(String, graphql_name="modelSavePath")
    name = sgqlc.types.Field(String, graphql_name="name")
    owner_id = sgqlc.types.Field(bigint, graphql_name="ownerId")
    root_id = sgqlc.types.Field(uuid, graphql_name="root_id")
    served_by = sgqlc.types.Field(uuid, graphql_name="served_by")
    updated_at = sgqlc.types.Field(timestamptz, graphql_name="updatedAt")
    version = sgqlc.types.Field(Int, graphql_name="version")
    weights_path = sgqlc.types.Field(String, graphql_name="weightsPath")


class meta_ai_model_mutation_response(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("affected_rows", "returning")
    affected_rows = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="affected_rows")
    returning = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_model))), graphql_name="returning"
    )


class meta_ai_model_stddev_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("ai_worker_id", "editor_id", "owner_id", "version")
    ai_worker_id = sgqlc.types.Field(Float, graphql_name="ai_worker_id")
    editor_id = sgqlc.types.Field(Float, graphql_name="editorId")
    owner_id = sgqlc.types.Field(Float, graphql_name="ownerId")
    version = sgqlc.types.Field(Float, graphql_name="version")


class meta_ai_model_stddev_pop_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("ai_worker_id", "editor_id", "owner_id", "version")
    ai_worker_id = sgqlc.types.Field(Float, graphql_name="ai_worker_id")
    editor_id = sgqlc.types.Field(Float, graphql_name="editorId")
    owner_id = sgqlc.types.Field(Float, graphql_name="ownerId")
    version = sgqlc.types.Field(Float, graphql_name="version")


class meta_ai_model_stddev_samp_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("ai_worker_id", "editor_id", "owner_id", "version")
    ai_worker_id = sgqlc.types.Field(Float, graphql_name="ai_worker_id")
    editor_id = sgqlc.types.Field(Float, graphql_name="editorId")
    owner_id = sgqlc.types.Field(Float, graphql_name="ownerId")
    version = sgqlc.types.Field(Float, graphql_name="version")


class meta_ai_model_sum_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("ai_worker_id", "editor_id", "owner_id", "version")
    ai_worker_id = sgqlc.types.Field(Int, graphql_name="ai_worker_id")
    editor_id = sgqlc.types.Field(bigint, graphql_name="editorId")
    owner_id = sgqlc.types.Field(bigint, graphql_name="ownerId")
    version = sgqlc.types.Field(Int, graphql_name="version")


class meta_ai_model_var_pop_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("ai_worker_id", "editor_id", "owner_id", "version")
    ai_worker_id = sgqlc.types.Field(Float, graphql_name="ai_worker_id")
    editor_id = sgqlc.types.Field(Float, graphql_name="editorId")
    owner_id = sgqlc.types.Field(Float, graphql_name="ownerId")
    version = sgqlc.types.Field(Float, graphql_name="version")


class meta_ai_model_var_samp_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("ai_worker_id", "editor_id", "owner_id", "version")
    ai_worker_id = sgqlc.types.Field(Float, graphql_name="ai_worker_id")
    editor_id = sgqlc.types.Field(Float, graphql_name="editorId")
    owner_id = sgqlc.types.Field(Float, graphql_name="ownerId")
    version = sgqlc.types.Field(Float, graphql_name="version")


class meta_ai_model_variance_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("ai_worker_id", "editor_id", "owner_id", "version")
    ai_worker_id = sgqlc.types.Field(Float, graphql_name="ai_worker_id")
    editor_id = sgqlc.types.Field(Float, graphql_name="editorId")
    owner_id = sgqlc.types.Field(Float, graphql_name="ownerId")
    version = sgqlc.types.Field(Float, graphql_name="version")


class meta_ai_prediction(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "app",
        "app_id",
        "completed_at",
        "created_at",
        "deployment",
        "deployment_id",
        "error_message",
        "id",
        "instances",
        "instances_aggregate",
        "job",
        "job_id",
        "job_uuid",
        "model",
        "model_id",
        "retries",
        "started_at",
        "state",
        "task",
        "task_id",
        "type",
    )
    app = sgqlc.types.Field(meta_ai_app, graphql_name="app")
    app_id = sgqlc.types.Field(uuid, graphql_name="appId")
    completed_at = sgqlc.types.Field(timestamptz, graphql_name="completedAt")
    created_at = sgqlc.types.Field(sgqlc.types.non_null(timestamptz), graphql_name="createdAt")
    deployment = sgqlc.types.Field(meta_ai_deployment, graphql_name="deployment")
    deployment_id = sgqlc.types.Field(uuid, graphql_name="deploymentId")
    error_message = sgqlc.types.Field(String, graphql_name="errorMessage")
    id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name="id")
    instances = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_instance))),
        graphql_name="instances",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_instance_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_instance_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_instance_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    instances_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null(meta_ai_instance_aggregate),
        graphql_name="instances_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_instance_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_instance_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_instance_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    job = sgqlc.types.Field("turbine_job", graphql_name="job")
    job_id = sgqlc.types.Field(bigint, graphql_name="jobId")
    job_uuid = sgqlc.types.Field(uuid, graphql_name="jobUUID")
    model = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_model), graphql_name="model")
    model_id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name="modelId")
    retries = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="retries")
    started_at = sgqlc.types.Field(timestamptz, graphql_name="startedAt")
    state = sgqlc.types.Field(meta_ai_prediction_state_enum, graphql_name="state")
    task = sgqlc.types.Field("turbine_task", graphql_name="task")
    task_id = sgqlc.types.Field(bigint, graphql_name="taskId")
    type = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_assignment_enum), graphql_name="type")


class meta_ai_prediction_aggregate(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("aggregate", "nodes")
    aggregate = sgqlc.types.Field("meta_ai_prediction_aggregate_fields", graphql_name="aggregate")
    nodes = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction))), graphql_name="nodes"
    )


class meta_ai_prediction_aggregate_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "avg",
        "count",
        "max",
        "min",
        "stddev",
        "stddev_pop",
        "stddev_samp",
        "sum",
        "var_pop",
        "var_samp",
        "variance",
    )
    avg = sgqlc.types.Field("meta_ai_prediction_avg_fields", graphql_name="avg")
    count = sgqlc.types.Field(
        sgqlc.types.non_null(Int),
        graphql_name="count",
        args=sgqlc.types.ArgDict(
            (
                (
                    "columns",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_select_column)),
                        graphql_name="columns",
                        default=None,
                    ),
                ),
                ("distinct", sgqlc.types.Arg(Boolean, graphql_name="distinct", default=None)),
            )
        ),
    )
    max = sgqlc.types.Field("meta_ai_prediction_max_fields", graphql_name="max")
    min = sgqlc.types.Field("meta_ai_prediction_min_fields", graphql_name="min")
    stddev = sgqlc.types.Field("meta_ai_prediction_stddev_fields", graphql_name="stddev")
    stddev_pop = sgqlc.types.Field("meta_ai_prediction_stddev_pop_fields", graphql_name="stddev_pop")
    stddev_samp = sgqlc.types.Field("meta_ai_prediction_stddev_samp_fields", graphql_name="stddev_samp")
    sum = sgqlc.types.Field("meta_ai_prediction_sum_fields", graphql_name="sum")
    var_pop = sgqlc.types.Field("meta_ai_prediction_var_pop_fields", graphql_name="var_pop")
    var_samp = sgqlc.types.Field("meta_ai_prediction_var_samp_fields", graphql_name="var_samp")
    variance = sgqlc.types.Field("meta_ai_prediction_variance_fields", graphql_name="variance")


class meta_ai_prediction_avg_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("job_id", "retries", "task_id")
    job_id = sgqlc.types.Field(Float, graphql_name="jobId")
    retries = sgqlc.types.Field(Float, graphql_name="retries")
    task_id = sgqlc.types.Field(Float, graphql_name="taskId")


class meta_ai_prediction_max_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "app_id",
        "completed_at",
        "created_at",
        "deployment_id",
        "error_message",
        "id",
        "job_id",
        "job_uuid",
        "model_id",
        "retries",
        "started_at",
        "task_id",
    )
    app_id = sgqlc.types.Field(uuid, graphql_name="appId")
    completed_at = sgqlc.types.Field(timestamptz, graphql_name="completedAt")
    created_at = sgqlc.types.Field(timestamptz, graphql_name="createdAt")
    deployment_id = sgqlc.types.Field(uuid, graphql_name="deploymentId")
    error_message = sgqlc.types.Field(String, graphql_name="errorMessage")
    id = sgqlc.types.Field(uuid, graphql_name="id")
    job_id = sgqlc.types.Field(bigint, graphql_name="jobId")
    job_uuid = sgqlc.types.Field(uuid, graphql_name="jobUUID")
    model_id = sgqlc.types.Field(uuid, graphql_name="modelId")
    retries = sgqlc.types.Field(Int, graphql_name="retries")
    started_at = sgqlc.types.Field(timestamptz, graphql_name="startedAt")
    task_id = sgqlc.types.Field(bigint, graphql_name="taskId")


class meta_ai_prediction_min_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "app_id",
        "completed_at",
        "created_at",
        "deployment_id",
        "error_message",
        "id",
        "job_id",
        "job_uuid",
        "model_id",
        "retries",
        "started_at",
        "task_id",
    )
    app_id = sgqlc.types.Field(uuid, graphql_name="appId")
    completed_at = sgqlc.types.Field(timestamptz, graphql_name="completedAt")
    created_at = sgqlc.types.Field(timestamptz, graphql_name="createdAt")
    deployment_id = sgqlc.types.Field(uuid, graphql_name="deploymentId")
    error_message = sgqlc.types.Field(String, graphql_name="errorMessage")
    id = sgqlc.types.Field(uuid, graphql_name="id")
    job_id = sgqlc.types.Field(bigint, graphql_name="jobId")
    job_uuid = sgqlc.types.Field(uuid, graphql_name="jobUUID")
    model_id = sgqlc.types.Field(uuid, graphql_name="modelId")
    retries = sgqlc.types.Field(Int, graphql_name="retries")
    started_at = sgqlc.types.Field(timestamptz, graphql_name="startedAt")
    task_id = sgqlc.types.Field(bigint, graphql_name="taskId")


class meta_ai_prediction_mutation_response(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("affected_rows", "returning")
    affected_rows = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="affected_rows")
    returning = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction))), graphql_name="returning"
    )


class meta_ai_prediction_state(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("predictions", "predictions_aggregate", "state")
    predictions = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction))),
        graphql_name="predictions",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_prediction_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    predictions_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null(meta_ai_prediction_aggregate),
        graphql_name="predictions_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_prediction_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    state = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="state")


class meta_ai_prediction_state_aggregate(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("aggregate", "nodes")
    aggregate = sgqlc.types.Field("meta_ai_prediction_state_aggregate_fields", graphql_name="aggregate")
    nodes = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_state))), graphql_name="nodes"
    )


class meta_ai_prediction_state_aggregate_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("count", "max", "min")
    count = sgqlc.types.Field(
        sgqlc.types.non_null(Int),
        graphql_name="count",
        args=sgqlc.types.ArgDict(
            (
                (
                    "columns",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_state_select_column)),
                        graphql_name="columns",
                        default=None,
                    ),
                ),
                ("distinct", sgqlc.types.Arg(Boolean, graphql_name="distinct", default=None)),
            )
        ),
    )
    max = sgqlc.types.Field("meta_ai_prediction_state_max_fields", graphql_name="max")
    min = sgqlc.types.Field("meta_ai_prediction_state_min_fields", graphql_name="min")


class meta_ai_prediction_state_max_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("state",)
    state = sgqlc.types.Field(String, graphql_name="state")


class meta_ai_prediction_state_min_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("state",)
    state = sgqlc.types.Field(String, graphql_name="state")


class meta_ai_prediction_state_mutation_response(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("affected_rows", "returning")
    affected_rows = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="affected_rows")
    returning = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_state))),
        graphql_name="returning",
    )


class meta_ai_prediction_stddev_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("job_id", "retries", "task_id")
    job_id = sgqlc.types.Field(Float, graphql_name="jobId")
    retries = sgqlc.types.Field(Float, graphql_name="retries")
    task_id = sgqlc.types.Field(Float, graphql_name="taskId")


class meta_ai_prediction_stddev_pop_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("job_id", "retries", "task_id")
    job_id = sgqlc.types.Field(Float, graphql_name="jobId")
    retries = sgqlc.types.Field(Float, graphql_name="retries")
    task_id = sgqlc.types.Field(Float, graphql_name="taskId")


class meta_ai_prediction_stddev_samp_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("job_id", "retries", "task_id")
    job_id = sgqlc.types.Field(Float, graphql_name="jobId")
    retries = sgqlc.types.Field(Float, graphql_name="retries")
    task_id = sgqlc.types.Field(Float, graphql_name="taskId")


class meta_ai_prediction_sum_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("job_id", "retries", "task_id")
    job_id = sgqlc.types.Field(bigint, graphql_name="jobId")
    retries = sgqlc.types.Field(Int, graphql_name="retries")
    task_id = sgqlc.types.Field(bigint, graphql_name="taskId")


class meta_ai_prediction_var_pop_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("job_id", "retries", "task_id")
    job_id = sgqlc.types.Field(Float, graphql_name="jobId")
    retries = sgqlc.types.Field(Float, graphql_name="retries")
    task_id = sgqlc.types.Field(Float, graphql_name="taskId")


class meta_ai_prediction_var_samp_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("job_id", "retries", "task_id")
    job_id = sgqlc.types.Field(Float, graphql_name="jobId")
    retries = sgqlc.types.Field(Float, graphql_name="retries")
    task_id = sgqlc.types.Field(Float, graphql_name="taskId")


class meta_ai_prediction_variance_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("job_id", "retries", "task_id")
    job_id = sgqlc.types.Field(Float, graphql_name="jobId")
    retries = sgqlc.types.Field(Float, graphql_name="retries")
    task_id = sgqlc.types.Field(Float, graphql_name="taskId")


class meta_ai_predictions_by_day(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("app_id", "count", "day", "model_id", "type")
    app_id = sgqlc.types.Field(uuid, graphql_name="appId")
    count = sgqlc.types.Field(bigint, graphql_name="count")
    day = sgqlc.types.Field(date, graphql_name="day")
    model_id = sgqlc.types.Field(uuid, graphql_name="modelId")
    type = sgqlc.types.Field(String, graphql_name="type")


class meta_ai_predictions_by_day_aggregate(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("aggregate", "nodes")
    aggregate = sgqlc.types.Field("meta_ai_predictions_by_day_aggregate_fields", graphql_name="aggregate")
    nodes = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_predictions_by_day))),
        graphql_name="nodes",
    )


class meta_ai_predictions_by_day_aggregate_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "avg",
        "count",
        "max",
        "min",
        "stddev",
        "stddev_pop",
        "stddev_samp",
        "sum",
        "var_pop",
        "var_samp",
        "variance",
    )
    avg = sgqlc.types.Field("meta_ai_predictions_by_day_avg_fields", graphql_name="avg")
    count = sgqlc.types.Field(
        sgqlc.types.non_null(Int),
        graphql_name="count",
        args=sgqlc.types.ArgDict(
            (
                (
                    "columns",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_predictions_by_day_select_column)),
                        graphql_name="columns",
                        default=None,
                    ),
                ),
                ("distinct", sgqlc.types.Arg(Boolean, graphql_name="distinct", default=None)),
            )
        ),
    )
    max = sgqlc.types.Field("meta_ai_predictions_by_day_max_fields", graphql_name="max")
    min = sgqlc.types.Field("meta_ai_predictions_by_day_min_fields", graphql_name="min")
    stddev = sgqlc.types.Field("meta_ai_predictions_by_day_stddev_fields", graphql_name="stddev")
    stddev_pop = sgqlc.types.Field("meta_ai_predictions_by_day_stddev_pop_fields", graphql_name="stddev_pop")
    stddev_samp = sgqlc.types.Field("meta_ai_predictions_by_day_stddev_samp_fields", graphql_name="stddev_samp")
    sum = sgqlc.types.Field("meta_ai_predictions_by_day_sum_fields", graphql_name="sum")
    var_pop = sgqlc.types.Field("meta_ai_predictions_by_day_var_pop_fields", graphql_name="var_pop")
    var_samp = sgqlc.types.Field("meta_ai_predictions_by_day_var_samp_fields", graphql_name="var_samp")
    variance = sgqlc.types.Field("meta_ai_predictions_by_day_variance_fields", graphql_name="variance")


class meta_ai_predictions_by_day_avg_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("count",)
    count = sgqlc.types.Field(Float, graphql_name="count")


class meta_ai_predictions_by_day_max_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("app_id", "count", "day", "model_id", "type")
    app_id = sgqlc.types.Field(uuid, graphql_name="appId")
    count = sgqlc.types.Field(bigint, graphql_name="count")
    day = sgqlc.types.Field(date, graphql_name="day")
    model_id = sgqlc.types.Field(uuid, graphql_name="modelId")
    type = sgqlc.types.Field(String, graphql_name="type")


class meta_ai_predictions_by_day_min_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("app_id", "count", "day", "model_id", "type")
    app_id = sgqlc.types.Field(uuid, graphql_name="appId")
    count = sgqlc.types.Field(bigint, graphql_name="count")
    day = sgqlc.types.Field(date, graphql_name="day")
    model_id = sgqlc.types.Field(uuid, graphql_name="modelId")
    type = sgqlc.types.Field(String, graphql_name="type")


class meta_ai_predictions_by_day_stddev_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("count",)
    count = sgqlc.types.Field(Float, graphql_name="count")


class meta_ai_predictions_by_day_stddev_pop_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("count",)
    count = sgqlc.types.Field(Float, graphql_name="count")


class meta_ai_predictions_by_day_stddev_samp_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("count",)
    count = sgqlc.types.Field(Float, graphql_name="count")


class meta_ai_predictions_by_day_sum_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("count",)
    count = sgqlc.types.Field(bigint, graphql_name="count")


class meta_ai_predictions_by_day_var_pop_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("count",)
    count = sgqlc.types.Field(Float, graphql_name="count")


class meta_ai_predictions_by_day_var_samp_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("count",)
    count = sgqlc.types.Field(Float, graphql_name="count")


class meta_ai_predictions_by_day_variance_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("count",)
    count = sgqlc.types.Field(Float, graphql_name="count")


class meta_ai_task_registry(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("app_id", "id", "model", "model_id", "task_name", "tasks", "tasks_aggregate")
    app_id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name="app_id")
    id = sgqlc.types.Field(sgqlc.types.non_null(bigint), graphql_name="id")
    model = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_model), graphql_name="model")
    model_id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name="model_id")
    task_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="task_name")
    tasks = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("turbine_task"))),
        graphql_name="tasks",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(turbine_task_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(turbine_task_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(turbine_task_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    tasks_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("turbine_task_aggregate"),
        graphql_name="tasks_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(turbine_task_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(turbine_task_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(turbine_task_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )


class meta_ai_task_registry_aggregate(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("aggregate", "nodes")
    aggregate = sgqlc.types.Field("meta_ai_task_registry_aggregate_fields", graphql_name="aggregate")
    nodes = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_task_registry))), graphql_name="nodes"
    )


class meta_ai_task_registry_aggregate_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "avg",
        "count",
        "max",
        "min",
        "stddev",
        "stddev_pop",
        "stddev_samp",
        "sum",
        "var_pop",
        "var_samp",
        "variance",
    )
    avg = sgqlc.types.Field("meta_ai_task_registry_avg_fields", graphql_name="avg")
    count = sgqlc.types.Field(
        sgqlc.types.non_null(Int),
        graphql_name="count",
        args=sgqlc.types.ArgDict(
            (
                (
                    "columns",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_task_registry_select_column)),
                        graphql_name="columns",
                        default=None,
                    ),
                ),
                ("distinct", sgqlc.types.Arg(Boolean, graphql_name="distinct", default=None)),
            )
        ),
    )
    max = sgqlc.types.Field("meta_ai_task_registry_max_fields", graphql_name="max")
    min = sgqlc.types.Field("meta_ai_task_registry_min_fields", graphql_name="min")
    stddev = sgqlc.types.Field("meta_ai_task_registry_stddev_fields", graphql_name="stddev")
    stddev_pop = sgqlc.types.Field("meta_ai_task_registry_stddev_pop_fields", graphql_name="stddev_pop")
    stddev_samp = sgqlc.types.Field("meta_ai_task_registry_stddev_samp_fields", graphql_name="stddev_samp")
    sum = sgqlc.types.Field("meta_ai_task_registry_sum_fields", graphql_name="sum")
    var_pop = sgqlc.types.Field("meta_ai_task_registry_var_pop_fields", graphql_name="var_pop")
    var_samp = sgqlc.types.Field("meta_ai_task_registry_var_samp_fields", graphql_name="var_samp")
    variance = sgqlc.types.Field("meta_ai_task_registry_variance_fields", graphql_name="variance")


class meta_ai_task_registry_avg_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(Float, graphql_name="id")


class meta_ai_task_registry_max_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("app_id", "id", "model_id", "task_name")
    app_id = sgqlc.types.Field(uuid, graphql_name="app_id")
    id = sgqlc.types.Field(bigint, graphql_name="id")
    model_id = sgqlc.types.Field(uuid, graphql_name="model_id")
    task_name = sgqlc.types.Field(String, graphql_name="task_name")


class meta_ai_task_registry_min_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("app_id", "id", "model_id", "task_name")
    app_id = sgqlc.types.Field(uuid, graphql_name="app_id")
    id = sgqlc.types.Field(bigint, graphql_name="id")
    model_id = sgqlc.types.Field(uuid, graphql_name="model_id")
    task_name = sgqlc.types.Field(String, graphql_name="task_name")


class meta_ai_task_registry_mutation_response(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("affected_rows", "returning")
    affected_rows = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="affected_rows")
    returning = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_task_registry))), graphql_name="returning"
    )


class meta_ai_task_registry_stddev_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(Float, graphql_name="id")


class meta_ai_task_registry_stddev_pop_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(Float, graphql_name="id")


class meta_ai_task_registry_stddev_samp_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(Float, graphql_name="id")


class meta_ai_task_registry_sum_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(bigint, graphql_name="id")


class meta_ai_task_registry_var_pop_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(Float, graphql_name="id")


class meta_ai_task_registry_var_samp_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(Float, graphql_name="id")


class meta_ai_task_registry_variance_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(Float, graphql_name="id")


class meta_ai_training_instance(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "artifacts",
        "created_at",
        "current_properties",
        "dataset",
        "dataset_id",
        "deployment",
        "deployment_id",
        "id",
        "model",
        "model_id",
        "state",
        "training_template_id",
        "training_state",
        "training_template",
        "updated_at",
    )
    artifacts = sgqlc.types.Field(String, graphql_name="artifacts")
    created_at = sgqlc.types.Field(sgqlc.types.non_null(timestamptz), graphql_name="createdAt")
    current_properties = sgqlc.types.Field(
        sgqlc.types.non_null(jsonb),
        graphql_name="currentProperties",
        args=sgqlc.types.ArgDict((("path", sgqlc.types.Arg(String, graphql_name="path", default=None)),)),
    )
    dataset = sgqlc.types.Field(meta_ai_dataset, graphql_name="dataset")
    dataset_id = sgqlc.types.Field(uuid, graphql_name="dataset_id")
    deployment = sgqlc.types.Field(meta_ai_deployment, graphql_name="deployment")
    deployment_id = sgqlc.types.Field(uuid, graphql_name="deployment_id")
    id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name="id")
    model = sgqlc.types.Field(meta_ai_model, graphql_name="model")
    model_id = sgqlc.types.Field(uuid, graphql_name="modelId")
    state = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_training_state_enum), graphql_name="state")
    training_template_id = sgqlc.types.Field(uuid, graphql_name="trainingTemplateId")
    training_state = sgqlc.types.Field(sgqlc.types.non_null("meta_ai_training_state"), graphql_name="training_state")
    training_template = sgqlc.types.Field("meta_ai_training_template", graphql_name="training_template")
    updated_at = sgqlc.types.Field(timestamptz, graphql_name="updated_at")


class meta_ai_training_instance_aggregate(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("aggregate", "nodes")
    aggregate = sgqlc.types.Field("meta_ai_training_instance_aggregate_fields", graphql_name="aggregate")
    nodes = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_training_instance))), graphql_name="nodes"
    )


class meta_ai_training_instance_aggregate_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("count", "max", "min")
    count = sgqlc.types.Field(
        sgqlc.types.non_null(Int),
        graphql_name="count",
        args=sgqlc.types.ArgDict(
            (
                (
                    "columns",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_training_instance_select_column)),
                        graphql_name="columns",
                        default=None,
                    ),
                ),
                ("distinct", sgqlc.types.Arg(Boolean, graphql_name="distinct", default=None)),
            )
        ),
    )
    max = sgqlc.types.Field("meta_ai_training_instance_max_fields", graphql_name="max")
    min = sgqlc.types.Field("meta_ai_training_instance_min_fields", graphql_name="min")


class meta_ai_training_instance_max_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "artifacts",
        "created_at",
        "dataset_id",
        "deployment_id",
        "id",
        "model_id",
        "training_template_id",
        "updated_at",
    )
    artifacts = sgqlc.types.Field(String, graphql_name="artifacts")
    created_at = sgqlc.types.Field(timestamptz, graphql_name="createdAt")
    dataset_id = sgqlc.types.Field(uuid, graphql_name="dataset_id")
    deployment_id = sgqlc.types.Field(uuid, graphql_name="deployment_id")
    id = sgqlc.types.Field(uuid, graphql_name="id")
    model_id = sgqlc.types.Field(uuid, graphql_name="modelId")
    training_template_id = sgqlc.types.Field(uuid, graphql_name="trainingTemplateId")
    updated_at = sgqlc.types.Field(timestamptz, graphql_name="updated_at")


class meta_ai_training_instance_min_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "artifacts",
        "created_at",
        "dataset_id",
        "deployment_id",
        "id",
        "model_id",
        "training_template_id",
        "updated_at",
    )
    artifacts = sgqlc.types.Field(String, graphql_name="artifacts")
    created_at = sgqlc.types.Field(timestamptz, graphql_name="createdAt")
    dataset_id = sgqlc.types.Field(uuid, graphql_name="dataset_id")
    deployment_id = sgqlc.types.Field(uuid, graphql_name="deployment_id")
    id = sgqlc.types.Field(uuid, graphql_name="id")
    model_id = sgqlc.types.Field(uuid, graphql_name="modelId")
    training_template_id = sgqlc.types.Field(uuid, graphql_name="trainingTemplateId")
    updated_at = sgqlc.types.Field(timestamptz, graphql_name="updated_at")


class meta_ai_training_instance_mutation_response(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("affected_rows", "returning")
    affected_rows = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="affected_rows")
    returning = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_training_instance))),
        graphql_name="returning",
    )


class meta_ai_training_state(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("state", "training_instances", "training_instances_aggregate")
    state = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="state")
    training_instances = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_training_instance))),
        graphql_name="training_instances",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_training_instance_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_training_instance_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_training_instance_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    training_instances_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null(meta_ai_training_instance_aggregate),
        graphql_name="training_instances_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_training_instance_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_training_instance_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_training_instance_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )


class meta_ai_training_state_aggregate(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("aggregate", "nodes")
    aggregate = sgqlc.types.Field("meta_ai_training_state_aggregate_fields", graphql_name="aggregate")
    nodes = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_training_state))), graphql_name="nodes"
    )


class meta_ai_training_state_aggregate_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("count", "max", "min")
    count = sgqlc.types.Field(
        sgqlc.types.non_null(Int),
        graphql_name="count",
        args=sgqlc.types.ArgDict(
            (
                (
                    "columns",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_training_state_select_column)),
                        graphql_name="columns",
                        default=None,
                    ),
                ),
                ("distinct", sgqlc.types.Arg(Boolean, graphql_name="distinct", default=None)),
            )
        ),
    )
    max = sgqlc.types.Field("meta_ai_training_state_max_fields", graphql_name="max")
    min = sgqlc.types.Field("meta_ai_training_state_min_fields", graphql_name="min")


class meta_ai_training_state_max_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("state",)
    state = sgqlc.types.Field(String, graphql_name="state")


class meta_ai_training_state_min_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("state",)
    state = sgqlc.types.Field(String, graphql_name="state")


class meta_ai_training_state_mutation_response(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("affected_rows", "returning")
    affected_rows = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="affected_rows")
    returning = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_training_state))),
        graphql_name="returning",
    )


class meta_ai_training_template(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "app_id",
        "created_at",
        "description",
        "id",
        "model",
        "model_id",
        "properties",
        "training_instances",
        "training_instances_aggregate",
        "updated_at",
    )
    app_id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name="appId")
    created_at = sgqlc.types.Field(sgqlc.types.non_null(timestamptz), graphql_name="createdAt")
    description = sgqlc.types.Field(String, graphql_name="description")
    id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name="id")
    model = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_model), graphql_name="model")
    model_id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name="modelId")
    properties = sgqlc.types.Field(
        sgqlc.types.non_null(jsonb),
        graphql_name="properties",
        args=sgqlc.types.ArgDict((("path", sgqlc.types.Arg(String, graphql_name="path", default=None)),)),
    )
    training_instances = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_training_instance))),
        graphql_name="training_instances",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_training_instance_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_training_instance_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_training_instance_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    training_instances_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null(meta_ai_training_instance_aggregate),
        graphql_name="training_instances_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_training_instance_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_training_instance_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_training_instance_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    updated_at = sgqlc.types.Field(timestamptz, graphql_name="updated_at")


class meta_ai_training_template_aggregate(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("aggregate", "nodes")
    aggregate = sgqlc.types.Field("meta_ai_training_template_aggregate_fields", graphql_name="aggregate")
    nodes = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_training_template))), graphql_name="nodes"
    )


class meta_ai_training_template_aggregate_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("count", "max", "min")
    count = sgqlc.types.Field(
        sgqlc.types.non_null(Int),
        graphql_name="count",
        args=sgqlc.types.ArgDict(
            (
                (
                    "columns",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_training_template_select_column)),
                        graphql_name="columns",
                        default=None,
                    ),
                ),
                ("distinct", sgqlc.types.Arg(Boolean, graphql_name="distinct", default=None)),
            )
        ),
    )
    max = sgqlc.types.Field("meta_ai_training_template_max_fields", graphql_name="max")
    min = sgqlc.types.Field("meta_ai_training_template_min_fields", graphql_name="min")


class meta_ai_training_template_max_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("app_id", "created_at", "description", "id", "model_id", "updated_at")
    app_id = sgqlc.types.Field(uuid, graphql_name="appId")
    created_at = sgqlc.types.Field(timestamptz, graphql_name="createdAt")
    description = sgqlc.types.Field(String, graphql_name="description")
    id = sgqlc.types.Field(uuid, graphql_name="id")
    model_id = sgqlc.types.Field(uuid, graphql_name="modelId")
    updated_at = sgqlc.types.Field(timestamptz, graphql_name="updated_at")


class meta_ai_training_template_min_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("app_id", "created_at", "description", "id", "model_id", "updated_at")
    app_id = sgqlc.types.Field(uuid, graphql_name="appId")
    created_at = sgqlc.types.Field(timestamptz, graphql_name="createdAt")
    description = sgqlc.types.Field(String, graphql_name="description")
    id = sgqlc.types.Field(uuid, graphql_name="id")
    model_id = sgqlc.types.Field(uuid, graphql_name="modelId")
    updated_at = sgqlc.types.Field(timestamptz, graphql_name="updated_at")


class meta_ai_training_template_mutation_response(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("affected_rows", "returning")
    affected_rows = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="affected_rows")
    returning = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_training_template))),
        graphql_name="returning",
    )


class meta_ai_visibility(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("models", "models_aggregate", "type")
    models = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_model))),
        graphql_name="models",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_model_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_model_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_model_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    models_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null(meta_ai_model_aggregate),
        graphql_name="models_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_model_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_model_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_model_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="type")


class meta_ai_visibility_aggregate(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("aggregate", "nodes")
    aggregate = sgqlc.types.Field("meta_ai_visibility_aggregate_fields", graphql_name="aggregate")
    nodes = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_visibility))), graphql_name="nodes"
    )


class meta_ai_visibility_aggregate_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("count", "max", "min")
    count = sgqlc.types.Field(
        sgqlc.types.non_null(Int),
        graphql_name="count",
        args=sgqlc.types.ArgDict(
            (
                (
                    "columns",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_visibility_select_column)),
                        graphql_name="columns",
                        default=None,
                    ),
                ),
                ("distinct", sgqlc.types.Arg(Boolean, graphql_name="distinct", default=None)),
            )
        ),
    )
    max = sgqlc.types.Field("meta_ai_visibility_max_fields", graphql_name="max")
    min = sgqlc.types.Field("meta_ai_visibility_min_fields", graphql_name="min")


class meta_ai_visibility_max_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("type",)
    type = sgqlc.types.Field(String, graphql_name="type")


class meta_ai_visibility_min_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("type",)
    type = sgqlc.types.Field(String, graphql_name="type")


class meta_ai_visibility_mutation_response(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("affected_rows", "returning")
    affected_rows = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="affected_rows")
    returning = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_visibility))), graphql_name="returning"
    )


class mutation_root(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "add_model",
        "delete_meta_ai_app",
        "delete_meta_ai_app_by_pk",
        "delete_meta_ai_assignment",
        "delete_meta_ai_assignment_by_pk",
        "delete_meta_ai_dataset",
        "delete_meta_ai_dataset_by_pk",
        "delete_meta_ai_dataset_metric",
        "delete_meta_ai_dataset_metric_by_pk",
        "delete_meta_ai_deployment",
        "delete_meta_ai_deployment_by_pk",
        "delete_meta_ai_deployment_log",
        "delete_meta_ai_deployment_log_by_pk",
        "delete_meta_ai_deployment_purpose",
        "delete_meta_ai_deployment_purpose_by_pk",
        "delete_meta_ai_deployment_status",
        "delete_meta_ai_deployment_status_by_pk",
        "delete_meta_ai_deployment_type",
        "delete_meta_ai_deployment_type_by_pk",
        "delete_meta_ai_environment",
        "delete_meta_ai_environment_by_pk",
        "delete_meta_ai_instance",
        "delete_meta_ai_instance_by_pk",
        "delete_meta_ai_model",
        "delete_meta_ai_model_by_pk",
        "delete_meta_ai_prediction",
        "delete_meta_ai_prediction_by_pk",
        "delete_meta_ai_prediction_state",
        "delete_meta_ai_prediction_state_by_pk",
        "delete_meta_ai_task_registry",
        "delete_meta_ai_task_registry_by_pk",
        "delete_meta_ai_training_instance",
        "delete_meta_ai_training_instance_by_pk",
        "delete_meta_ai_training_state",
        "delete_meta_ai_training_state_by_pk",
        "delete_meta_ai_training_template",
        "delete_meta_ai_training_template_by_pk",
        "delete_meta_ai_visibility",
        "delete_meta_ai_visibility_by_pk",
        "delete_turbine_app",
        "delete_turbine_app_by_pk",
        "delete_turbine_job",
        "delete_turbine_job_by_pk",
        "delete_turbine_task",
        "delete_turbine_task_by_pk",
        "insert_meta_ai_app",
        "insert_meta_ai_app_one",
        "insert_meta_ai_assignment",
        "insert_meta_ai_assignment_one",
        "insert_meta_ai_dataset",
        "insert_meta_ai_dataset_metric",
        "insert_meta_ai_dataset_metric_one",
        "insert_meta_ai_dataset_one",
        "insert_meta_ai_deployment",
        "insert_meta_ai_deployment_log",
        "insert_meta_ai_deployment_log_one",
        "insert_meta_ai_deployment_one",
        "insert_meta_ai_deployment_purpose",
        "insert_meta_ai_deployment_purpose_one",
        "insert_meta_ai_deployment_status",
        "insert_meta_ai_deployment_status_one",
        "insert_meta_ai_deployment_type",
        "insert_meta_ai_deployment_type_one",
        "insert_meta_ai_environment",
        "insert_meta_ai_environment_one",
        "insert_meta_ai_instance",
        "insert_meta_ai_instance_one",
        "insert_meta_ai_model",
        "insert_meta_ai_model_one",
        "insert_meta_ai_prediction",
        "insert_meta_ai_prediction_one",
        "insert_meta_ai_prediction_state",
        "insert_meta_ai_prediction_state_one",
        "insert_meta_ai_task_registry",
        "insert_meta_ai_task_registry_one",
        "insert_meta_ai_training_instance",
        "insert_meta_ai_training_instance_one",
        "insert_meta_ai_training_state",
        "insert_meta_ai_training_state_one",
        "insert_meta_ai_training_template",
        "insert_meta_ai_training_template_one",
        "insert_meta_ai_visibility",
        "insert_meta_ai_visibility_one",
        "insert_turbine_app",
        "insert_turbine_app_one",
        "insert_turbine_job",
        "insert_turbine_job_one",
        "insert_turbine_task",
        "insert_turbine_task_one",
        "request_prediction_of_app",
        "start_deployment",
        "update_meta_ai_app",
        "update_meta_ai_app_by_pk",
        "update_meta_ai_assignment",
        "update_meta_ai_assignment_by_pk",
        "update_meta_ai_dataset",
        "update_meta_ai_dataset_by_pk",
        "update_meta_ai_dataset_metric",
        "update_meta_ai_dataset_metric_by_pk",
        "update_meta_ai_deployment",
        "update_meta_ai_deployment_by_pk",
        "update_meta_ai_deployment_log",
        "update_meta_ai_deployment_log_by_pk",
        "update_meta_ai_deployment_purpose",
        "update_meta_ai_deployment_purpose_by_pk",
        "update_meta_ai_deployment_status",
        "update_meta_ai_deployment_status_by_pk",
        "update_meta_ai_deployment_type",
        "update_meta_ai_deployment_type_by_pk",
        "update_meta_ai_environment",
        "update_meta_ai_environment_by_pk",
        "update_meta_ai_instance",
        "update_meta_ai_instance_by_pk",
        "update_meta_ai_model",
        "update_meta_ai_model_by_pk",
        "update_meta_ai_prediction",
        "update_meta_ai_prediction_by_pk",
        "update_meta_ai_prediction_state",
        "update_meta_ai_prediction_state_by_pk",
        "update_meta_ai_task_registry",
        "update_meta_ai_task_registry_by_pk",
        "update_meta_ai_training_instance",
        "update_meta_ai_training_instance_by_pk",
        "update_meta_ai_training_state",
        "update_meta_ai_training_state_by_pk",
        "update_meta_ai_training_template",
        "update_meta_ai_training_template_by_pk",
        "update_meta_ai_visibility",
        "update_meta_ai_visibility_by_pk",
        "update_turbine_app",
        "update_turbine_app_by_pk",
        "update_turbine_job",
        "update_turbine_job_by_pk",
        "update_turbine_task",
        "update_turbine_task_by_pk",
    )
    add_model = sgqlc.types.Field(
        InsertMetaAiModelMutationOutput,
        graphql_name="add_model",
        args=sgqlc.types.ArgDict(
            (
                ("description", sgqlc.types.Arg(String, graphql_name="description", default=None)),
                ("input_schema", sgqlc.types.Arg(jsonb, graphql_name="inputSchema", default=None)),
                ("model_save_path", sgqlc.types.Arg(String, graphql_name="modelSavePath", default=None)),
                ("name", sgqlc.types.Arg(String, graphql_name="name", default=None)),
                ("output_schema", sgqlc.types.Arg(jsonb, graphql_name="outputSchema", default=None)),
                ("owner_id", sgqlc.types.Arg(bigint, graphql_name="ownerId", default=None)),
                (
                    "stage",
                    sgqlc.types.Arg(InsertMetaAiModelMutationMetaAiEnvironmentEnum, graphql_name="stage", default=None),
                ),
                ("version", sgqlc.types.Arg(Int, graphql_name="version", default=None)),
                ("weights_path", sgqlc.types.Arg(String, graphql_name="weightsPath", default=None)),
            )
        ),
    )
    delete_meta_ai_app = sgqlc.types.Field(
        meta_ai_app_mutation_response,
        graphql_name="delete_meta_ai_app",
        args=sgqlc.types.ArgDict(
            (
                (
                    "where",
                    sgqlc.types.Arg(sgqlc.types.non_null(meta_ai_app_bool_exp), graphql_name="where", default=None),
                ),
            )
        ),
    )
    delete_meta_ai_app_by_pk = sgqlc.types.Field(
        meta_ai_app,
        graphql_name="delete_meta_ai_app_by_pk",
        args=sgqlc.types.ArgDict(
            (
                (
                    "assigned",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_assignment_enum), graphql_name="assigned", default=None
                    ),
                ),
                ("id", sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name="id", default=None)),
                ("model_id", sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name="modelId", default=None)),
            )
        ),
    )
    delete_meta_ai_assignment = sgqlc.types.Field(
        meta_ai_assignment_mutation_response,
        graphql_name="delete_meta_ai_assignment",
        args=sgqlc.types.ArgDict(
            (
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_assignment_bool_exp), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    delete_meta_ai_assignment_by_pk = sgqlc.types.Field(
        meta_ai_assignment,
        graphql_name="delete_meta_ai_assignment_by_pk",
        args=sgqlc.types.ArgDict(
            (("type", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="type", default=None)),)
        ),
    )
    delete_meta_ai_dataset = sgqlc.types.Field(
        meta_ai_dataset_mutation_response,
        graphql_name="delete_meta_ai_dataset",
        args=sgqlc.types.ArgDict(
            (
                (
                    "where",
                    sgqlc.types.Arg(sgqlc.types.non_null(meta_ai_dataset_bool_exp), graphql_name="where", default=None),
                ),
            )
        ),
    )
    delete_meta_ai_dataset_by_pk = sgqlc.types.Field(
        meta_ai_dataset,
        graphql_name="delete_meta_ai_dataset_by_pk",
        args=sgqlc.types.ArgDict(
            (("id", sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name="id", default=None)),)
        ),
    )
    delete_meta_ai_dataset_metric = sgqlc.types.Field(
        meta_ai_dataset_metric_mutation_response,
        graphql_name="delete_meta_ai_dataset_metric",
        args=sgqlc.types.ArgDict(
            (
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_dataset_metric_bool_exp), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    delete_meta_ai_dataset_metric_by_pk = sgqlc.types.Field(
        meta_ai_dataset_metric,
        graphql_name="delete_meta_ai_dataset_metric_by_pk",
        args=sgqlc.types.ArgDict(
            (("id", sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name="id", default=None)),)
        ),
    )
    delete_meta_ai_deployment = sgqlc.types.Field(
        meta_ai_deployment_mutation_response,
        graphql_name="delete_meta_ai_deployment",
        args=sgqlc.types.ArgDict(
            (
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_deployment_bool_exp), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    delete_meta_ai_deployment_by_pk = sgqlc.types.Field(
        meta_ai_deployment,
        graphql_name="delete_meta_ai_deployment_by_pk",
        args=sgqlc.types.ArgDict(
            (("id", sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name="id", default=None)),)
        ),
    )
    delete_meta_ai_deployment_log = sgqlc.types.Field(
        meta_ai_deployment_log_mutation_response,
        graphql_name="delete_meta_ai_deployment_log",
        args=sgqlc.types.ArgDict(
            (
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_deployment_log_bool_exp), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    delete_meta_ai_deployment_log_by_pk = sgqlc.types.Field(
        meta_ai_deployment_log,
        graphql_name="delete_meta_ai_deployment_log_by_pk",
        args=sgqlc.types.ArgDict(
            (
                (
                    "deployment_id",
                    sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name="deployment_id", default=None),
                ),
                ("id", sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name="id", default=None)),
            )
        ),
    )
    delete_meta_ai_deployment_purpose = sgqlc.types.Field(
        meta_ai_deployment_purpose_mutation_response,
        graphql_name="delete_meta_ai_deployment_purpose",
        args=sgqlc.types.ArgDict(
            (
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_deployment_purpose_bool_exp), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    delete_meta_ai_deployment_purpose_by_pk = sgqlc.types.Field(
        meta_ai_deployment_purpose,
        graphql_name="delete_meta_ai_deployment_purpose_by_pk",
        args=sgqlc.types.ArgDict(
            (("purpose", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="purpose", default=None)),)
        ),
    )
    delete_meta_ai_deployment_status = sgqlc.types.Field(
        meta_ai_deployment_status_mutation_response,
        graphql_name="delete_meta_ai_deployment_status",
        args=sgqlc.types.ArgDict(
            (
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_deployment_status_bool_exp), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    delete_meta_ai_deployment_status_by_pk = sgqlc.types.Field(
        meta_ai_deployment_status,
        graphql_name="delete_meta_ai_deployment_status_by_pk",
        args=sgqlc.types.ArgDict(
            (("status", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="status", default=None)),)
        ),
    )
    delete_meta_ai_deployment_type = sgqlc.types.Field(
        meta_ai_deployment_type_mutation_response,
        graphql_name="delete_meta_ai_deployment_type",
        args=sgqlc.types.ArgDict(
            (
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_deployment_type_bool_exp), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    delete_meta_ai_deployment_type_by_pk = sgqlc.types.Field(
        meta_ai_deployment_type,
        graphql_name="delete_meta_ai_deployment_type_by_pk",
        args=sgqlc.types.ArgDict(
            (("name", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="name", default=None)),)
        ),
    )
    delete_meta_ai_environment = sgqlc.types.Field(
        meta_ai_environment_mutation_response,
        graphql_name="delete_meta_ai_environment",
        args=sgqlc.types.ArgDict(
            (
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_environment_bool_exp), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    delete_meta_ai_environment_by_pk = sgqlc.types.Field(
        meta_ai_environment,
        graphql_name="delete_meta_ai_environment_by_pk",
        args=sgqlc.types.ArgDict(
            (("name", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="name", default=None)),)
        ),
    )
    delete_meta_ai_instance = sgqlc.types.Field(
        meta_ai_instance_mutation_response,
        graphql_name="delete_meta_ai_instance",
        args=sgqlc.types.ArgDict(
            (
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_instance_bool_exp), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    delete_meta_ai_instance_by_pk = sgqlc.types.Field(
        meta_ai_instance,
        graphql_name="delete_meta_ai_instance_by_pk",
        args=sgqlc.types.ArgDict(
            (
                ("id", sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name="id", default=None)),
                (
                    "prediction_id",
                    sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name="predictionId", default=None),
                ),
            )
        ),
    )
    delete_meta_ai_model = sgqlc.types.Field(
        meta_ai_model_mutation_response,
        graphql_name="delete_meta_ai_model",
        args=sgqlc.types.ArgDict(
            (
                (
                    "where",
                    sgqlc.types.Arg(sgqlc.types.non_null(meta_ai_model_bool_exp), graphql_name="where", default=None),
                ),
            )
        ),
    )
    delete_meta_ai_model_by_pk = sgqlc.types.Field(
        meta_ai_model,
        graphql_name="delete_meta_ai_model_by_pk",
        args=sgqlc.types.ArgDict(
            (("id", sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name="id", default=None)),)
        ),
    )
    delete_meta_ai_prediction = sgqlc.types.Field(
        meta_ai_prediction_mutation_response,
        graphql_name="delete_meta_ai_prediction",
        args=sgqlc.types.ArgDict(
            (
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_prediction_bool_exp), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    delete_meta_ai_prediction_by_pk = sgqlc.types.Field(
        meta_ai_prediction,
        graphql_name="delete_meta_ai_prediction_by_pk",
        args=sgqlc.types.ArgDict(
            (("id", sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name="id", default=None)),)
        ),
    )
    delete_meta_ai_prediction_state = sgqlc.types.Field(
        meta_ai_prediction_state_mutation_response,
        graphql_name="delete_meta_ai_prediction_state",
        args=sgqlc.types.ArgDict(
            (
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_prediction_state_bool_exp), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    delete_meta_ai_prediction_state_by_pk = sgqlc.types.Field(
        meta_ai_prediction_state,
        graphql_name="delete_meta_ai_prediction_state_by_pk",
        args=sgqlc.types.ArgDict(
            (("state", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="state", default=None)),)
        ),
    )
    delete_meta_ai_task_registry = sgqlc.types.Field(
        meta_ai_task_registry_mutation_response,
        graphql_name="delete_meta_ai_task_registry",
        args=sgqlc.types.ArgDict(
            (
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_task_registry_bool_exp), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    delete_meta_ai_task_registry_by_pk = sgqlc.types.Field(
        meta_ai_task_registry,
        graphql_name="delete_meta_ai_task_registry_by_pk",
        args=sgqlc.types.ArgDict(
            (("id", sgqlc.types.Arg(sgqlc.types.non_null(bigint), graphql_name="id", default=None)),)
        ),
    )
    delete_meta_ai_training_instance = sgqlc.types.Field(
        meta_ai_training_instance_mutation_response,
        graphql_name="delete_meta_ai_training_instance",
        args=sgqlc.types.ArgDict(
            (
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_training_instance_bool_exp), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    delete_meta_ai_training_instance_by_pk = sgqlc.types.Field(
        meta_ai_training_instance,
        graphql_name="delete_meta_ai_training_instance_by_pk",
        args=sgqlc.types.ArgDict(
            (("id", sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name="id", default=None)),)
        ),
    )
    delete_meta_ai_training_state = sgqlc.types.Field(
        meta_ai_training_state_mutation_response,
        graphql_name="delete_meta_ai_training_state",
        args=sgqlc.types.ArgDict(
            (
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_training_state_bool_exp), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    delete_meta_ai_training_state_by_pk = sgqlc.types.Field(
        meta_ai_training_state,
        graphql_name="delete_meta_ai_training_state_by_pk",
        args=sgqlc.types.ArgDict(
            (("state", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="state", default=None)),)
        ),
    )
    delete_meta_ai_training_template = sgqlc.types.Field(
        meta_ai_training_template_mutation_response,
        graphql_name="delete_meta_ai_training_template",
        args=sgqlc.types.ArgDict(
            (
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_training_template_bool_exp), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    delete_meta_ai_training_template_by_pk = sgqlc.types.Field(
        meta_ai_training_template,
        graphql_name="delete_meta_ai_training_template_by_pk",
        args=sgqlc.types.ArgDict(
            (("id", sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name="id", default=None)),)
        ),
    )
    delete_meta_ai_visibility = sgqlc.types.Field(
        meta_ai_visibility_mutation_response,
        graphql_name="delete_meta_ai_visibility",
        args=sgqlc.types.ArgDict(
            (
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_visibility_bool_exp), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    delete_meta_ai_visibility_by_pk = sgqlc.types.Field(
        meta_ai_visibility,
        graphql_name="delete_meta_ai_visibility_by_pk",
        args=sgqlc.types.ArgDict(
            (("type", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="type", default=None)),)
        ),
    )
    delete_turbine_app = sgqlc.types.Field(
        "turbine_app_mutation_response",
        graphql_name="delete_turbine_app",
        args=sgqlc.types.ArgDict(
            (
                (
                    "where",
                    sgqlc.types.Arg(sgqlc.types.non_null(turbine_app_bool_exp), graphql_name="where", default=None),
                ),
            )
        ),
    )
    delete_turbine_app_by_pk = sgqlc.types.Field(
        "turbine_app",
        graphql_name="delete_turbine_app_by_pk",
        args=sgqlc.types.ArgDict(
            (("id", sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name="id", default=None)),)
        ),
    )
    delete_turbine_job = sgqlc.types.Field(
        "turbine_job_mutation_response",
        graphql_name="delete_turbine_job",
        args=sgqlc.types.ArgDict(
            (
                (
                    "where",
                    sgqlc.types.Arg(sgqlc.types.non_null(turbine_job_bool_exp), graphql_name="where", default=None),
                ),
            )
        ),
    )
    delete_turbine_job_by_pk = sgqlc.types.Field(
        "turbine_job",
        graphql_name="delete_turbine_job_by_pk",
        args=sgqlc.types.ArgDict(
            (("id", sgqlc.types.Arg(sgqlc.types.non_null(bigint), graphql_name="id", default=None)),)
        ),
    )
    delete_turbine_task = sgqlc.types.Field(
        "turbine_task_mutation_response",
        graphql_name="delete_turbine_task",
        args=sgqlc.types.ArgDict(
            (
                (
                    "where",
                    sgqlc.types.Arg(sgqlc.types.non_null(turbine_task_bool_exp), graphql_name="where", default=None),
                ),
            )
        ),
    )
    delete_turbine_task_by_pk = sgqlc.types.Field(
        "turbine_task",
        graphql_name="delete_turbine_task_by_pk",
        args=sgqlc.types.ArgDict(
            (("id", sgqlc.types.Arg(sgqlc.types.non_null(bigint), graphql_name="id", default=None)),)
        ),
    )
    insert_meta_ai_app = sgqlc.types.Field(
        meta_ai_app_mutation_response,
        graphql_name="insert_meta_ai_app",
        args=sgqlc.types.ArgDict(
            (
                (
                    "objects",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_app_insert_input))),
                        graphql_name="objects",
                        default=None,
                    ),
                ),
                ("on_conflict", sgqlc.types.Arg(meta_ai_app_on_conflict, graphql_name="on_conflict", default=None)),
            )
        ),
    )
    insert_meta_ai_app_one = sgqlc.types.Field(
        meta_ai_app,
        graphql_name="insert_meta_ai_app_one",
        args=sgqlc.types.ArgDict(
            (
                (
                    "object",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_app_insert_input), graphql_name="object", default=None
                    ),
                ),
                ("on_conflict", sgqlc.types.Arg(meta_ai_app_on_conflict, graphql_name="on_conflict", default=None)),
            )
        ),
    )
    insert_meta_ai_assignment = sgqlc.types.Field(
        meta_ai_assignment_mutation_response,
        graphql_name="insert_meta_ai_assignment",
        args=sgqlc.types.ArgDict(
            (
                (
                    "objects",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(
                            sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_assignment_insert_input))
                        ),
                        graphql_name="objects",
                        default=None,
                    ),
                ),
                (
                    "on_conflict",
                    sgqlc.types.Arg(meta_ai_assignment_on_conflict, graphql_name="on_conflict", default=None),
                ),
            )
        ),
    )
    insert_meta_ai_assignment_one = sgqlc.types.Field(
        meta_ai_assignment,
        graphql_name="insert_meta_ai_assignment_one",
        args=sgqlc.types.ArgDict(
            (
                (
                    "object",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_assignment_insert_input), graphql_name="object", default=None
                    ),
                ),
                (
                    "on_conflict",
                    sgqlc.types.Arg(meta_ai_assignment_on_conflict, graphql_name="on_conflict", default=None),
                ),
            )
        ),
    )
    insert_meta_ai_dataset = sgqlc.types.Field(
        meta_ai_dataset_mutation_response,
        graphql_name="insert_meta_ai_dataset",
        args=sgqlc.types.ArgDict(
            (
                (
                    "objects",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_dataset_insert_input))),
                        graphql_name="objects",
                        default=None,
                    ),
                ),
                ("on_conflict", sgqlc.types.Arg(meta_ai_dataset_on_conflict, graphql_name="on_conflict", default=None)),
            )
        ),
    )
    insert_meta_ai_dataset_metric = sgqlc.types.Field(
        meta_ai_dataset_metric_mutation_response,
        graphql_name="insert_meta_ai_dataset_metric",
        args=sgqlc.types.ArgDict(
            (
                (
                    "objects",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(
                            sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_dataset_metric_insert_input))
                        ),
                        graphql_name="objects",
                        default=None,
                    ),
                ),
                (
                    "on_conflict",
                    sgqlc.types.Arg(meta_ai_dataset_metric_on_conflict, graphql_name="on_conflict", default=None),
                ),
            )
        ),
    )
    insert_meta_ai_dataset_metric_one = sgqlc.types.Field(
        meta_ai_dataset_metric,
        graphql_name="insert_meta_ai_dataset_metric_one",
        args=sgqlc.types.ArgDict(
            (
                (
                    "object",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_dataset_metric_insert_input), graphql_name="object", default=None
                    ),
                ),
                (
                    "on_conflict",
                    sgqlc.types.Arg(meta_ai_dataset_metric_on_conflict, graphql_name="on_conflict", default=None),
                ),
            )
        ),
    )
    insert_meta_ai_dataset_one = sgqlc.types.Field(
        meta_ai_dataset,
        graphql_name="insert_meta_ai_dataset_one",
        args=sgqlc.types.ArgDict(
            (
                (
                    "object",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_dataset_insert_input), graphql_name="object", default=None
                    ),
                ),
                ("on_conflict", sgqlc.types.Arg(meta_ai_dataset_on_conflict, graphql_name="on_conflict", default=None)),
            )
        ),
    )
    insert_meta_ai_deployment = sgqlc.types.Field(
        meta_ai_deployment_mutation_response,
        graphql_name="insert_meta_ai_deployment",
        args=sgqlc.types.ArgDict(
            (
                (
                    "objects",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(
                            sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_insert_input))
                        ),
                        graphql_name="objects",
                        default=None,
                    ),
                ),
                (
                    "on_conflict",
                    sgqlc.types.Arg(meta_ai_deployment_on_conflict, graphql_name="on_conflict", default=None),
                ),
            )
        ),
    )
    insert_meta_ai_deployment_log = sgqlc.types.Field(
        meta_ai_deployment_log_mutation_response,
        graphql_name="insert_meta_ai_deployment_log",
        args=sgqlc.types.ArgDict(
            (
                (
                    "objects",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(
                            sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_log_insert_input))
                        ),
                        graphql_name="objects",
                        default=None,
                    ),
                ),
                (
                    "on_conflict",
                    sgqlc.types.Arg(meta_ai_deployment_log_on_conflict, graphql_name="on_conflict", default=None),
                ),
            )
        ),
    )
    insert_meta_ai_deployment_log_one = sgqlc.types.Field(
        meta_ai_deployment_log,
        graphql_name="insert_meta_ai_deployment_log_one",
        args=sgqlc.types.ArgDict(
            (
                (
                    "object",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_deployment_log_insert_input), graphql_name="object", default=None
                    ),
                ),
                (
                    "on_conflict",
                    sgqlc.types.Arg(meta_ai_deployment_log_on_conflict, graphql_name="on_conflict", default=None),
                ),
            )
        ),
    )
    insert_meta_ai_deployment_one = sgqlc.types.Field(
        meta_ai_deployment,
        graphql_name="insert_meta_ai_deployment_one",
        args=sgqlc.types.ArgDict(
            (
                (
                    "object",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_deployment_insert_input), graphql_name="object", default=None
                    ),
                ),
                (
                    "on_conflict",
                    sgqlc.types.Arg(meta_ai_deployment_on_conflict, graphql_name="on_conflict", default=None),
                ),
            )
        ),
    )
    insert_meta_ai_deployment_purpose = sgqlc.types.Field(
        meta_ai_deployment_purpose_mutation_response,
        graphql_name="insert_meta_ai_deployment_purpose",
        args=sgqlc.types.ArgDict(
            (
                (
                    "objects",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(
                            sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_purpose_insert_input))
                        ),
                        graphql_name="objects",
                        default=None,
                    ),
                ),
                (
                    "on_conflict",
                    sgqlc.types.Arg(meta_ai_deployment_purpose_on_conflict, graphql_name="on_conflict", default=None),
                ),
            )
        ),
    )
    insert_meta_ai_deployment_purpose_one = sgqlc.types.Field(
        meta_ai_deployment_purpose,
        graphql_name="insert_meta_ai_deployment_purpose_one",
        args=sgqlc.types.ArgDict(
            (
                (
                    "object",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_deployment_purpose_insert_input),
                        graphql_name="object",
                        default=None,
                    ),
                ),
                (
                    "on_conflict",
                    sgqlc.types.Arg(meta_ai_deployment_purpose_on_conflict, graphql_name="on_conflict", default=None),
                ),
            )
        ),
    )
    insert_meta_ai_deployment_status = sgqlc.types.Field(
        meta_ai_deployment_status_mutation_response,
        graphql_name="insert_meta_ai_deployment_status",
        args=sgqlc.types.ArgDict(
            (
                (
                    "objects",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(
                            sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_status_insert_input))
                        ),
                        graphql_name="objects",
                        default=None,
                    ),
                ),
                (
                    "on_conflict",
                    sgqlc.types.Arg(meta_ai_deployment_status_on_conflict, graphql_name="on_conflict", default=None),
                ),
            )
        ),
    )
    insert_meta_ai_deployment_status_one = sgqlc.types.Field(
        meta_ai_deployment_status,
        graphql_name="insert_meta_ai_deployment_status_one",
        args=sgqlc.types.ArgDict(
            (
                (
                    "object",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_deployment_status_insert_input),
                        graphql_name="object",
                        default=None,
                    ),
                ),
                (
                    "on_conflict",
                    sgqlc.types.Arg(meta_ai_deployment_status_on_conflict, graphql_name="on_conflict", default=None),
                ),
            )
        ),
    )
    insert_meta_ai_deployment_type = sgqlc.types.Field(
        meta_ai_deployment_type_mutation_response,
        graphql_name="insert_meta_ai_deployment_type",
        args=sgqlc.types.ArgDict(
            (
                (
                    "objects",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(
                            sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_type_insert_input))
                        ),
                        graphql_name="objects",
                        default=None,
                    ),
                ),
                (
                    "on_conflict",
                    sgqlc.types.Arg(meta_ai_deployment_type_on_conflict, graphql_name="on_conflict", default=None),
                ),
            )
        ),
    )
    insert_meta_ai_deployment_type_one = sgqlc.types.Field(
        meta_ai_deployment_type,
        graphql_name="insert_meta_ai_deployment_type_one",
        args=sgqlc.types.ArgDict(
            (
                (
                    "object",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_deployment_type_insert_input), graphql_name="object", default=None
                    ),
                ),
                (
                    "on_conflict",
                    sgqlc.types.Arg(meta_ai_deployment_type_on_conflict, graphql_name="on_conflict", default=None),
                ),
            )
        ),
    )
    insert_meta_ai_environment = sgqlc.types.Field(
        meta_ai_environment_mutation_response,
        graphql_name="insert_meta_ai_environment",
        args=sgqlc.types.ArgDict(
            (
                (
                    "objects",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(
                            sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_environment_insert_input))
                        ),
                        graphql_name="objects",
                        default=None,
                    ),
                ),
                (
                    "on_conflict",
                    sgqlc.types.Arg(meta_ai_environment_on_conflict, graphql_name="on_conflict", default=None),
                ),
            )
        ),
    )
    insert_meta_ai_environment_one = sgqlc.types.Field(
        meta_ai_environment,
        graphql_name="insert_meta_ai_environment_one",
        args=sgqlc.types.ArgDict(
            (
                (
                    "object",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_environment_insert_input), graphql_name="object", default=None
                    ),
                ),
                (
                    "on_conflict",
                    sgqlc.types.Arg(meta_ai_environment_on_conflict, graphql_name="on_conflict", default=None),
                ),
            )
        ),
    )
    insert_meta_ai_instance = sgqlc.types.Field(
        meta_ai_instance_mutation_response,
        graphql_name="insert_meta_ai_instance",
        args=sgqlc.types.ArgDict(
            (
                (
                    "objects",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_instance_insert_input))),
                        graphql_name="objects",
                        default=None,
                    ),
                ),
                (
                    "on_conflict",
                    sgqlc.types.Arg(meta_ai_instance_on_conflict, graphql_name="on_conflict", default=None),
                ),
            )
        ),
    )
    insert_meta_ai_instance_one = sgqlc.types.Field(
        meta_ai_instance,
        graphql_name="insert_meta_ai_instance_one",
        args=sgqlc.types.ArgDict(
            (
                (
                    "object",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_instance_insert_input), graphql_name="object", default=None
                    ),
                ),
                (
                    "on_conflict",
                    sgqlc.types.Arg(meta_ai_instance_on_conflict, graphql_name="on_conflict", default=None),
                ),
            )
        ),
    )
    insert_meta_ai_model = sgqlc.types.Field(
        meta_ai_model_mutation_response,
        graphql_name="insert_meta_ai_model",
        args=sgqlc.types.ArgDict(
            (
                (
                    "objects",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_model_insert_input))),
                        graphql_name="objects",
                        default=None,
                    ),
                ),
                ("on_conflict", sgqlc.types.Arg(meta_ai_model_on_conflict, graphql_name="on_conflict", default=None)),
            )
        ),
    )
    insert_meta_ai_model_one = sgqlc.types.Field(
        meta_ai_model,
        graphql_name="insert_meta_ai_model_one",
        args=sgqlc.types.ArgDict(
            (
                (
                    "object",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_model_insert_input), graphql_name="object", default=None
                    ),
                ),
                ("on_conflict", sgqlc.types.Arg(meta_ai_model_on_conflict, graphql_name="on_conflict", default=None)),
            )
        ),
    )
    insert_meta_ai_prediction = sgqlc.types.Field(
        meta_ai_prediction_mutation_response,
        graphql_name="insert_meta_ai_prediction",
        args=sgqlc.types.ArgDict(
            (
                (
                    "objects",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(
                            sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_insert_input))
                        ),
                        graphql_name="objects",
                        default=None,
                    ),
                ),
                (
                    "on_conflict",
                    sgqlc.types.Arg(meta_ai_prediction_on_conflict, graphql_name="on_conflict", default=None),
                ),
            )
        ),
    )
    insert_meta_ai_prediction_one = sgqlc.types.Field(
        meta_ai_prediction,
        graphql_name="insert_meta_ai_prediction_one",
        args=sgqlc.types.ArgDict(
            (
                (
                    "object",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_prediction_insert_input), graphql_name="object", default=None
                    ),
                ),
                (
                    "on_conflict",
                    sgqlc.types.Arg(meta_ai_prediction_on_conflict, graphql_name="on_conflict", default=None),
                ),
            )
        ),
    )
    insert_meta_ai_prediction_state = sgqlc.types.Field(
        meta_ai_prediction_state_mutation_response,
        graphql_name="insert_meta_ai_prediction_state",
        args=sgqlc.types.ArgDict(
            (
                (
                    "objects",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(
                            sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_state_insert_input))
                        ),
                        graphql_name="objects",
                        default=None,
                    ),
                ),
                (
                    "on_conflict",
                    sgqlc.types.Arg(meta_ai_prediction_state_on_conflict, graphql_name="on_conflict", default=None),
                ),
            )
        ),
    )
    insert_meta_ai_prediction_state_one = sgqlc.types.Field(
        meta_ai_prediction_state,
        graphql_name="insert_meta_ai_prediction_state_one",
        args=sgqlc.types.ArgDict(
            (
                (
                    "object",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_prediction_state_insert_input), graphql_name="object", default=None
                    ),
                ),
                (
                    "on_conflict",
                    sgqlc.types.Arg(meta_ai_prediction_state_on_conflict, graphql_name="on_conflict", default=None),
                ),
            )
        ),
    )
    insert_meta_ai_task_registry = sgqlc.types.Field(
        meta_ai_task_registry_mutation_response,
        graphql_name="insert_meta_ai_task_registry",
        args=sgqlc.types.ArgDict(
            (
                (
                    "objects",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(
                            sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_task_registry_insert_input))
                        ),
                        graphql_name="objects",
                        default=None,
                    ),
                ),
                (
                    "on_conflict",
                    sgqlc.types.Arg(meta_ai_task_registry_on_conflict, graphql_name="on_conflict", default=None),
                ),
            )
        ),
    )
    insert_meta_ai_task_registry_one = sgqlc.types.Field(
        meta_ai_task_registry,
        graphql_name="insert_meta_ai_task_registry_one",
        args=sgqlc.types.ArgDict(
            (
                (
                    "object",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_task_registry_insert_input), graphql_name="object", default=None
                    ),
                ),
                (
                    "on_conflict",
                    sgqlc.types.Arg(meta_ai_task_registry_on_conflict, graphql_name="on_conflict", default=None),
                ),
            )
        ),
    )
    insert_meta_ai_training_instance = sgqlc.types.Field(
        meta_ai_training_instance_mutation_response,
        graphql_name="insert_meta_ai_training_instance",
        args=sgqlc.types.ArgDict(
            (
                (
                    "objects",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(
                            sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_training_instance_insert_input))
                        ),
                        graphql_name="objects",
                        default=None,
                    ),
                ),
                (
                    "on_conflict",
                    sgqlc.types.Arg(meta_ai_training_instance_on_conflict, graphql_name="on_conflict", default=None),
                ),
            )
        ),
    )
    insert_meta_ai_training_instance_one = sgqlc.types.Field(
        meta_ai_training_instance,
        graphql_name="insert_meta_ai_training_instance_one",
        args=sgqlc.types.ArgDict(
            (
                (
                    "object",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_training_instance_insert_input),
                        graphql_name="object",
                        default=None,
                    ),
                ),
                (
                    "on_conflict",
                    sgqlc.types.Arg(meta_ai_training_instance_on_conflict, graphql_name="on_conflict", default=None),
                ),
            )
        ),
    )
    insert_meta_ai_training_state = sgqlc.types.Field(
        meta_ai_training_state_mutation_response,
        graphql_name="insert_meta_ai_training_state",
        args=sgqlc.types.ArgDict(
            (
                (
                    "objects",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(
                            sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_training_state_insert_input))
                        ),
                        graphql_name="objects",
                        default=None,
                    ),
                ),
                (
                    "on_conflict",
                    sgqlc.types.Arg(meta_ai_training_state_on_conflict, graphql_name="on_conflict", default=None),
                ),
            )
        ),
    )
    insert_meta_ai_training_state_one = sgqlc.types.Field(
        meta_ai_training_state,
        graphql_name="insert_meta_ai_training_state_one",
        args=sgqlc.types.ArgDict(
            (
                (
                    "object",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_training_state_insert_input), graphql_name="object", default=None
                    ),
                ),
                (
                    "on_conflict",
                    sgqlc.types.Arg(meta_ai_training_state_on_conflict, graphql_name="on_conflict", default=None),
                ),
            )
        ),
    )
    insert_meta_ai_training_template = sgqlc.types.Field(
        meta_ai_training_template_mutation_response,
        graphql_name="insert_meta_ai_training_template",
        args=sgqlc.types.ArgDict(
            (
                (
                    "objects",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(
                            sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_training_template_insert_input))
                        ),
                        graphql_name="objects",
                        default=None,
                    ),
                ),
                (
                    "on_conflict",
                    sgqlc.types.Arg(meta_ai_training_template_on_conflict, graphql_name="on_conflict", default=None),
                ),
            )
        ),
    )
    insert_meta_ai_training_template_one = sgqlc.types.Field(
        meta_ai_training_template,
        graphql_name="insert_meta_ai_training_template_one",
        args=sgqlc.types.ArgDict(
            (
                (
                    "object",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_training_template_insert_input),
                        graphql_name="object",
                        default=None,
                    ),
                ),
                (
                    "on_conflict",
                    sgqlc.types.Arg(meta_ai_training_template_on_conflict, graphql_name="on_conflict", default=None),
                ),
            )
        ),
    )
    insert_meta_ai_visibility = sgqlc.types.Field(
        meta_ai_visibility_mutation_response,
        graphql_name="insert_meta_ai_visibility",
        args=sgqlc.types.ArgDict(
            (
                (
                    "objects",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(
                            sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_visibility_insert_input))
                        ),
                        graphql_name="objects",
                        default=None,
                    ),
                ),
                (
                    "on_conflict",
                    sgqlc.types.Arg(meta_ai_visibility_on_conflict, graphql_name="on_conflict", default=None),
                ),
            )
        ),
    )
    insert_meta_ai_visibility_one = sgqlc.types.Field(
        meta_ai_visibility,
        graphql_name="insert_meta_ai_visibility_one",
        args=sgqlc.types.ArgDict(
            (
                (
                    "object",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_visibility_insert_input), graphql_name="object", default=None
                    ),
                ),
                (
                    "on_conflict",
                    sgqlc.types.Arg(meta_ai_visibility_on_conflict, graphql_name="on_conflict", default=None),
                ),
            )
        ),
    )
    insert_turbine_app = sgqlc.types.Field(
        "turbine_app_mutation_response",
        graphql_name="insert_turbine_app",
        args=sgqlc.types.ArgDict(
            (
                (
                    "objects",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(turbine_app_insert_input))),
                        graphql_name="objects",
                        default=None,
                    ),
                ),
                ("on_conflict", sgqlc.types.Arg(turbine_app_on_conflict, graphql_name="on_conflict", default=None)),
            )
        ),
    )
    insert_turbine_app_one = sgqlc.types.Field(
        "turbine_app",
        graphql_name="insert_turbine_app_one",
        args=sgqlc.types.ArgDict(
            (
                (
                    "object",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(turbine_app_insert_input), graphql_name="object", default=None
                    ),
                ),
                ("on_conflict", sgqlc.types.Arg(turbine_app_on_conflict, graphql_name="on_conflict", default=None)),
            )
        ),
    )
    insert_turbine_job = sgqlc.types.Field(
        "turbine_job_mutation_response",
        graphql_name="insert_turbine_job",
        args=sgqlc.types.ArgDict(
            (
                (
                    "objects",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(turbine_job_insert_input))),
                        graphql_name="objects",
                        default=None,
                    ),
                ),
                ("on_conflict", sgqlc.types.Arg(turbine_job_on_conflict, graphql_name="on_conflict", default=None)),
            )
        ),
    )
    insert_turbine_job_one = sgqlc.types.Field(
        "turbine_job",
        graphql_name="insert_turbine_job_one",
        args=sgqlc.types.ArgDict(
            (
                (
                    "object",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(turbine_job_insert_input), graphql_name="object", default=None
                    ),
                ),
                ("on_conflict", sgqlc.types.Arg(turbine_job_on_conflict, graphql_name="on_conflict", default=None)),
            )
        ),
    )
    insert_turbine_task = sgqlc.types.Field(
        "turbine_task_mutation_response",
        graphql_name="insert_turbine_task",
        args=sgqlc.types.ArgDict(
            (
                (
                    "objects",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(turbine_task_insert_input))),
                        graphql_name="objects",
                        default=None,
                    ),
                ),
                ("on_conflict", sgqlc.types.Arg(turbine_task_on_conflict, graphql_name="on_conflict", default=None)),
            )
        ),
    )
    insert_turbine_task_one = sgqlc.types.Field(
        "turbine_task",
        graphql_name="insert_turbine_task_one",
        args=sgqlc.types.ArgDict(
            (
                (
                    "object",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(turbine_task_insert_input), graphql_name="object", default=None
                    ),
                ),
                ("on_conflict", sgqlc.types.Arg(turbine_task_on_conflict, graphql_name="on_conflict", default=None)),
            )
        ),
    )
    request_prediction_of_app = sgqlc.types.Field(
        sgqlc.types.non_null(uuid),
        graphql_name="request_prediction_of_app",
        args=sgqlc.types.ArgDict(
            (("app_id", sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name="app_id", default=None)),)
        ),
    )
    start_deployment = sgqlc.types.Field(
        sgqlc.types.non_null(uuid),
        graphql_name="start_deployment",
        args=sgqlc.types.ArgDict(
            (("model_id", sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name="model_id", default=None)),)
        ),
    )
    update_meta_ai_app = sgqlc.types.Field(
        meta_ai_app_mutation_response,
        graphql_name="update_meta_ai_app",
        args=sgqlc.types.ArgDict(
            (
                ("_inc", sgqlc.types.Arg(meta_ai_app_inc_input, graphql_name="_inc", default=None)),
                ("_set", sgqlc.types.Arg(meta_ai_app_set_input, graphql_name="_set", default=None)),
                (
                    "where",
                    sgqlc.types.Arg(sgqlc.types.non_null(meta_ai_app_bool_exp), graphql_name="where", default=None),
                ),
            )
        ),
    )
    update_meta_ai_app_by_pk = sgqlc.types.Field(
        meta_ai_app,
        graphql_name="update_meta_ai_app_by_pk",
        args=sgqlc.types.ArgDict(
            (
                ("_inc", sgqlc.types.Arg(meta_ai_app_inc_input, graphql_name="_inc", default=None)),
                ("_set", sgqlc.types.Arg(meta_ai_app_set_input, graphql_name="_set", default=None)),
                (
                    "pk_columns",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_app_pk_columns_input), graphql_name="pk_columns", default=None
                    ),
                ),
            )
        ),
    )
    update_meta_ai_assignment = sgqlc.types.Field(
        meta_ai_assignment_mutation_response,
        graphql_name="update_meta_ai_assignment",
        args=sgqlc.types.ArgDict(
            (
                ("_set", sgqlc.types.Arg(meta_ai_assignment_set_input, graphql_name="_set", default=None)),
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_assignment_bool_exp), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    update_meta_ai_assignment_by_pk = sgqlc.types.Field(
        meta_ai_assignment,
        graphql_name="update_meta_ai_assignment_by_pk",
        args=sgqlc.types.ArgDict(
            (
                ("_set", sgqlc.types.Arg(meta_ai_assignment_set_input, graphql_name="_set", default=None)),
                (
                    "pk_columns",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_assignment_pk_columns_input),
                        graphql_name="pk_columns",
                        default=None,
                    ),
                ),
            )
        ),
    )
    update_meta_ai_dataset = sgqlc.types.Field(
        meta_ai_dataset_mutation_response,
        graphql_name="update_meta_ai_dataset",
        args=sgqlc.types.ArgDict(
            (
                ("_append", sgqlc.types.Arg(meta_ai_dataset_append_input, graphql_name="_append", default=None)),
                (
                    "_delete_at_path",
                    sgqlc.types.Arg(meta_ai_dataset_delete_at_path_input, graphql_name="_delete_at_path", default=None),
                ),
                (
                    "_delete_elem",
                    sgqlc.types.Arg(meta_ai_dataset_delete_elem_input, graphql_name="_delete_elem", default=None),
                ),
                (
                    "_delete_key",
                    sgqlc.types.Arg(meta_ai_dataset_delete_key_input, graphql_name="_delete_key", default=None),
                ),
                ("_prepend", sgqlc.types.Arg(meta_ai_dataset_prepend_input, graphql_name="_prepend", default=None)),
                ("_set", sgqlc.types.Arg(meta_ai_dataset_set_input, graphql_name="_set", default=None)),
                (
                    "where",
                    sgqlc.types.Arg(sgqlc.types.non_null(meta_ai_dataset_bool_exp), graphql_name="where", default=None),
                ),
            )
        ),
    )
    update_meta_ai_dataset_by_pk = sgqlc.types.Field(
        meta_ai_dataset,
        graphql_name="update_meta_ai_dataset_by_pk",
        args=sgqlc.types.ArgDict(
            (
                ("_append", sgqlc.types.Arg(meta_ai_dataset_append_input, graphql_name="_append", default=None)),
                (
                    "_delete_at_path",
                    sgqlc.types.Arg(meta_ai_dataset_delete_at_path_input, graphql_name="_delete_at_path", default=None),
                ),
                (
                    "_delete_elem",
                    sgqlc.types.Arg(meta_ai_dataset_delete_elem_input, graphql_name="_delete_elem", default=None),
                ),
                (
                    "_delete_key",
                    sgqlc.types.Arg(meta_ai_dataset_delete_key_input, graphql_name="_delete_key", default=None),
                ),
                ("_prepend", sgqlc.types.Arg(meta_ai_dataset_prepend_input, graphql_name="_prepend", default=None)),
                ("_set", sgqlc.types.Arg(meta_ai_dataset_set_input, graphql_name="_set", default=None)),
                (
                    "pk_columns",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_dataset_pk_columns_input), graphql_name="pk_columns", default=None
                    ),
                ),
            )
        ),
    )
    update_meta_ai_dataset_metric = sgqlc.types.Field(
        meta_ai_dataset_metric_mutation_response,
        graphql_name="update_meta_ai_dataset_metric",
        args=sgqlc.types.ArgDict(
            (
                ("_append", sgqlc.types.Arg(meta_ai_dataset_metric_append_input, graphql_name="_append", default=None)),
                (
                    "_delete_at_path",
                    sgqlc.types.Arg(
                        meta_ai_dataset_metric_delete_at_path_input, graphql_name="_delete_at_path", default=None
                    ),
                ),
                (
                    "_delete_elem",
                    sgqlc.types.Arg(
                        meta_ai_dataset_metric_delete_elem_input, graphql_name="_delete_elem", default=None
                    ),
                ),
                (
                    "_delete_key",
                    sgqlc.types.Arg(meta_ai_dataset_metric_delete_key_input, graphql_name="_delete_key", default=None),
                ),
                ("_inc", sgqlc.types.Arg(meta_ai_dataset_metric_inc_input, graphql_name="_inc", default=None)),
                (
                    "_prepend",
                    sgqlc.types.Arg(meta_ai_dataset_metric_prepend_input, graphql_name="_prepend", default=None),
                ),
                ("_set", sgqlc.types.Arg(meta_ai_dataset_metric_set_input, graphql_name="_set", default=None)),
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_dataset_metric_bool_exp), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    update_meta_ai_dataset_metric_by_pk = sgqlc.types.Field(
        meta_ai_dataset_metric,
        graphql_name="update_meta_ai_dataset_metric_by_pk",
        args=sgqlc.types.ArgDict(
            (
                ("_append", sgqlc.types.Arg(meta_ai_dataset_metric_append_input, graphql_name="_append", default=None)),
                (
                    "_delete_at_path",
                    sgqlc.types.Arg(
                        meta_ai_dataset_metric_delete_at_path_input, graphql_name="_delete_at_path", default=None
                    ),
                ),
                (
                    "_delete_elem",
                    sgqlc.types.Arg(
                        meta_ai_dataset_metric_delete_elem_input, graphql_name="_delete_elem", default=None
                    ),
                ),
                (
                    "_delete_key",
                    sgqlc.types.Arg(meta_ai_dataset_metric_delete_key_input, graphql_name="_delete_key", default=None),
                ),
                ("_inc", sgqlc.types.Arg(meta_ai_dataset_metric_inc_input, graphql_name="_inc", default=None)),
                (
                    "_prepend",
                    sgqlc.types.Arg(meta_ai_dataset_metric_prepend_input, graphql_name="_prepend", default=None),
                ),
                ("_set", sgqlc.types.Arg(meta_ai_dataset_metric_set_input, graphql_name="_set", default=None)),
                (
                    "pk_columns",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_dataset_metric_pk_columns_input),
                        graphql_name="pk_columns",
                        default=None,
                    ),
                ),
            )
        ),
    )
    update_meta_ai_deployment = sgqlc.types.Field(
        meta_ai_deployment_mutation_response,
        graphql_name="update_meta_ai_deployment",
        args=sgqlc.types.ArgDict(
            (
                ("_append", sgqlc.types.Arg(meta_ai_deployment_append_input, graphql_name="_append", default=None)),
                (
                    "_delete_at_path",
                    sgqlc.types.Arg(
                        meta_ai_deployment_delete_at_path_input, graphql_name="_delete_at_path", default=None
                    ),
                ),
                (
                    "_delete_elem",
                    sgqlc.types.Arg(meta_ai_deployment_delete_elem_input, graphql_name="_delete_elem", default=None),
                ),
                (
                    "_delete_key",
                    sgqlc.types.Arg(meta_ai_deployment_delete_key_input, graphql_name="_delete_key", default=None),
                ),
                ("_inc", sgqlc.types.Arg(meta_ai_deployment_inc_input, graphql_name="_inc", default=None)),
                ("_prepend", sgqlc.types.Arg(meta_ai_deployment_prepend_input, graphql_name="_prepend", default=None)),
                ("_set", sgqlc.types.Arg(meta_ai_deployment_set_input, graphql_name="_set", default=None)),
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_deployment_bool_exp), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    update_meta_ai_deployment_by_pk = sgqlc.types.Field(
        meta_ai_deployment,
        graphql_name="update_meta_ai_deployment_by_pk",
        args=sgqlc.types.ArgDict(
            (
                ("_append", sgqlc.types.Arg(meta_ai_deployment_append_input, graphql_name="_append", default=None)),
                (
                    "_delete_at_path",
                    sgqlc.types.Arg(
                        meta_ai_deployment_delete_at_path_input, graphql_name="_delete_at_path", default=None
                    ),
                ),
                (
                    "_delete_elem",
                    sgqlc.types.Arg(meta_ai_deployment_delete_elem_input, graphql_name="_delete_elem", default=None),
                ),
                (
                    "_delete_key",
                    sgqlc.types.Arg(meta_ai_deployment_delete_key_input, graphql_name="_delete_key", default=None),
                ),
                ("_inc", sgqlc.types.Arg(meta_ai_deployment_inc_input, graphql_name="_inc", default=None)),
                ("_prepend", sgqlc.types.Arg(meta_ai_deployment_prepend_input, graphql_name="_prepend", default=None)),
                ("_set", sgqlc.types.Arg(meta_ai_deployment_set_input, graphql_name="_set", default=None)),
                (
                    "pk_columns",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_deployment_pk_columns_input),
                        graphql_name="pk_columns",
                        default=None,
                    ),
                ),
            )
        ),
    )
    update_meta_ai_deployment_log = sgqlc.types.Field(
        meta_ai_deployment_log_mutation_response,
        graphql_name="update_meta_ai_deployment_log",
        args=sgqlc.types.ArgDict(
            (
                ("_inc", sgqlc.types.Arg(meta_ai_deployment_log_inc_input, graphql_name="_inc", default=None)),
                ("_set", sgqlc.types.Arg(meta_ai_deployment_log_set_input, graphql_name="_set", default=None)),
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_deployment_log_bool_exp), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    update_meta_ai_deployment_log_by_pk = sgqlc.types.Field(
        meta_ai_deployment_log,
        graphql_name="update_meta_ai_deployment_log_by_pk",
        args=sgqlc.types.ArgDict(
            (
                ("_inc", sgqlc.types.Arg(meta_ai_deployment_log_inc_input, graphql_name="_inc", default=None)),
                ("_set", sgqlc.types.Arg(meta_ai_deployment_log_set_input, graphql_name="_set", default=None)),
                (
                    "pk_columns",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_deployment_log_pk_columns_input),
                        graphql_name="pk_columns",
                        default=None,
                    ),
                ),
            )
        ),
    )
    update_meta_ai_deployment_purpose = sgqlc.types.Field(
        meta_ai_deployment_purpose_mutation_response,
        graphql_name="update_meta_ai_deployment_purpose",
        args=sgqlc.types.ArgDict(
            (
                ("_set", sgqlc.types.Arg(meta_ai_deployment_purpose_set_input, graphql_name="_set", default=None)),
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_deployment_purpose_bool_exp), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    update_meta_ai_deployment_purpose_by_pk = sgqlc.types.Field(
        meta_ai_deployment_purpose,
        graphql_name="update_meta_ai_deployment_purpose_by_pk",
        args=sgqlc.types.ArgDict(
            (
                ("_set", sgqlc.types.Arg(meta_ai_deployment_purpose_set_input, graphql_name="_set", default=None)),
                (
                    "pk_columns",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_deployment_purpose_pk_columns_input),
                        graphql_name="pk_columns",
                        default=None,
                    ),
                ),
            )
        ),
    )
    update_meta_ai_deployment_status = sgqlc.types.Field(
        meta_ai_deployment_status_mutation_response,
        graphql_name="update_meta_ai_deployment_status",
        args=sgqlc.types.ArgDict(
            (
                ("_set", sgqlc.types.Arg(meta_ai_deployment_status_set_input, graphql_name="_set", default=None)),
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_deployment_status_bool_exp), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    update_meta_ai_deployment_status_by_pk = sgqlc.types.Field(
        meta_ai_deployment_status,
        graphql_name="update_meta_ai_deployment_status_by_pk",
        args=sgqlc.types.ArgDict(
            (
                ("_set", sgqlc.types.Arg(meta_ai_deployment_status_set_input, graphql_name="_set", default=None)),
                (
                    "pk_columns",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_deployment_status_pk_columns_input),
                        graphql_name="pk_columns",
                        default=None,
                    ),
                ),
            )
        ),
    )
    update_meta_ai_deployment_type = sgqlc.types.Field(
        meta_ai_deployment_type_mutation_response,
        graphql_name="update_meta_ai_deployment_type",
        args=sgqlc.types.ArgDict(
            (
                ("_set", sgqlc.types.Arg(meta_ai_deployment_type_set_input, graphql_name="_set", default=None)),
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_deployment_type_bool_exp), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    update_meta_ai_deployment_type_by_pk = sgqlc.types.Field(
        meta_ai_deployment_type,
        graphql_name="update_meta_ai_deployment_type_by_pk",
        args=sgqlc.types.ArgDict(
            (
                ("_set", sgqlc.types.Arg(meta_ai_deployment_type_set_input, graphql_name="_set", default=None)),
                (
                    "pk_columns",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_deployment_type_pk_columns_input),
                        graphql_name="pk_columns",
                        default=None,
                    ),
                ),
            )
        ),
    )
    update_meta_ai_environment = sgqlc.types.Field(
        meta_ai_environment_mutation_response,
        graphql_name="update_meta_ai_environment",
        args=sgqlc.types.ArgDict(
            (
                ("_set", sgqlc.types.Arg(meta_ai_environment_set_input, graphql_name="_set", default=None)),
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_environment_bool_exp), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    update_meta_ai_environment_by_pk = sgqlc.types.Field(
        meta_ai_environment,
        graphql_name="update_meta_ai_environment_by_pk",
        args=sgqlc.types.ArgDict(
            (
                ("_set", sgqlc.types.Arg(meta_ai_environment_set_input, graphql_name="_set", default=None)),
                (
                    "pk_columns",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_environment_pk_columns_input),
                        graphql_name="pk_columns",
                        default=None,
                    ),
                ),
            )
        ),
    )
    update_meta_ai_instance = sgqlc.types.Field(
        meta_ai_instance_mutation_response,
        graphql_name="update_meta_ai_instance",
        args=sgqlc.types.ArgDict(
            (
                ("_append", sgqlc.types.Arg(meta_ai_instance_append_input, graphql_name="_append", default=None)),
                (
                    "_delete_at_path",
                    sgqlc.types.Arg(
                        meta_ai_instance_delete_at_path_input, graphql_name="_delete_at_path", default=None
                    ),
                ),
                (
                    "_delete_elem",
                    sgqlc.types.Arg(meta_ai_instance_delete_elem_input, graphql_name="_delete_elem", default=None),
                ),
                (
                    "_delete_key",
                    sgqlc.types.Arg(meta_ai_instance_delete_key_input, graphql_name="_delete_key", default=None),
                ),
                ("_inc", sgqlc.types.Arg(meta_ai_instance_inc_input, graphql_name="_inc", default=None)),
                ("_prepend", sgqlc.types.Arg(meta_ai_instance_prepend_input, graphql_name="_prepend", default=None)),
                ("_set", sgqlc.types.Arg(meta_ai_instance_set_input, graphql_name="_set", default=None)),
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_instance_bool_exp), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    update_meta_ai_instance_by_pk = sgqlc.types.Field(
        meta_ai_instance,
        graphql_name="update_meta_ai_instance_by_pk",
        args=sgqlc.types.ArgDict(
            (
                ("_append", sgqlc.types.Arg(meta_ai_instance_append_input, graphql_name="_append", default=None)),
                (
                    "_delete_at_path",
                    sgqlc.types.Arg(
                        meta_ai_instance_delete_at_path_input, graphql_name="_delete_at_path", default=None
                    ),
                ),
                (
                    "_delete_elem",
                    sgqlc.types.Arg(meta_ai_instance_delete_elem_input, graphql_name="_delete_elem", default=None),
                ),
                (
                    "_delete_key",
                    sgqlc.types.Arg(meta_ai_instance_delete_key_input, graphql_name="_delete_key", default=None),
                ),
                ("_inc", sgqlc.types.Arg(meta_ai_instance_inc_input, graphql_name="_inc", default=None)),
                ("_prepend", sgqlc.types.Arg(meta_ai_instance_prepend_input, graphql_name="_prepend", default=None)),
                ("_set", sgqlc.types.Arg(meta_ai_instance_set_input, graphql_name="_set", default=None)),
                (
                    "pk_columns",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_instance_pk_columns_input), graphql_name="pk_columns", default=None
                    ),
                ),
            )
        ),
    )
    update_meta_ai_model = sgqlc.types.Field(
        meta_ai_model_mutation_response,
        graphql_name="update_meta_ai_model",
        args=sgqlc.types.ArgDict(
            (
                ("_append", sgqlc.types.Arg(meta_ai_model_append_input, graphql_name="_append", default=None)),
                (
                    "_delete_at_path",
                    sgqlc.types.Arg(meta_ai_model_delete_at_path_input, graphql_name="_delete_at_path", default=None),
                ),
                (
                    "_delete_elem",
                    sgqlc.types.Arg(meta_ai_model_delete_elem_input, graphql_name="_delete_elem", default=None),
                ),
                (
                    "_delete_key",
                    sgqlc.types.Arg(meta_ai_model_delete_key_input, graphql_name="_delete_key", default=None),
                ),
                ("_inc", sgqlc.types.Arg(meta_ai_model_inc_input, graphql_name="_inc", default=None)),
                ("_prepend", sgqlc.types.Arg(meta_ai_model_prepend_input, graphql_name="_prepend", default=None)),
                ("_set", sgqlc.types.Arg(meta_ai_model_set_input, graphql_name="_set", default=None)),
                (
                    "where",
                    sgqlc.types.Arg(sgqlc.types.non_null(meta_ai_model_bool_exp), graphql_name="where", default=None),
                ),
            )
        ),
    )
    update_meta_ai_model_by_pk = sgqlc.types.Field(
        meta_ai_model,
        graphql_name="update_meta_ai_model_by_pk",
        args=sgqlc.types.ArgDict(
            (
                ("_append", sgqlc.types.Arg(meta_ai_model_append_input, graphql_name="_append", default=None)),
                (
                    "_delete_at_path",
                    sgqlc.types.Arg(meta_ai_model_delete_at_path_input, graphql_name="_delete_at_path", default=None),
                ),
                (
                    "_delete_elem",
                    sgqlc.types.Arg(meta_ai_model_delete_elem_input, graphql_name="_delete_elem", default=None),
                ),
                (
                    "_delete_key",
                    sgqlc.types.Arg(meta_ai_model_delete_key_input, graphql_name="_delete_key", default=None),
                ),
                ("_inc", sgqlc.types.Arg(meta_ai_model_inc_input, graphql_name="_inc", default=None)),
                ("_prepend", sgqlc.types.Arg(meta_ai_model_prepend_input, graphql_name="_prepend", default=None)),
                ("_set", sgqlc.types.Arg(meta_ai_model_set_input, graphql_name="_set", default=None)),
                (
                    "pk_columns",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_model_pk_columns_input), graphql_name="pk_columns", default=None
                    ),
                ),
            )
        ),
    )
    update_meta_ai_prediction = sgqlc.types.Field(
        meta_ai_prediction_mutation_response,
        graphql_name="update_meta_ai_prediction",
        args=sgqlc.types.ArgDict(
            (
                ("_inc", sgqlc.types.Arg(meta_ai_prediction_inc_input, graphql_name="_inc", default=None)),
                ("_set", sgqlc.types.Arg(meta_ai_prediction_set_input, graphql_name="_set", default=None)),
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_prediction_bool_exp), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    update_meta_ai_prediction_by_pk = sgqlc.types.Field(
        meta_ai_prediction,
        graphql_name="update_meta_ai_prediction_by_pk",
        args=sgqlc.types.ArgDict(
            (
                ("_inc", sgqlc.types.Arg(meta_ai_prediction_inc_input, graphql_name="_inc", default=None)),
                ("_set", sgqlc.types.Arg(meta_ai_prediction_set_input, graphql_name="_set", default=None)),
                (
                    "pk_columns",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_prediction_pk_columns_input),
                        graphql_name="pk_columns",
                        default=None,
                    ),
                ),
            )
        ),
    )
    update_meta_ai_prediction_state = sgqlc.types.Field(
        meta_ai_prediction_state_mutation_response,
        graphql_name="update_meta_ai_prediction_state",
        args=sgqlc.types.ArgDict(
            (
                ("_set", sgqlc.types.Arg(meta_ai_prediction_state_set_input, graphql_name="_set", default=None)),
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_prediction_state_bool_exp), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    update_meta_ai_prediction_state_by_pk = sgqlc.types.Field(
        meta_ai_prediction_state,
        graphql_name="update_meta_ai_prediction_state_by_pk",
        args=sgqlc.types.ArgDict(
            (
                ("_set", sgqlc.types.Arg(meta_ai_prediction_state_set_input, graphql_name="_set", default=None)),
                (
                    "pk_columns",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_prediction_state_pk_columns_input),
                        graphql_name="pk_columns",
                        default=None,
                    ),
                ),
            )
        ),
    )
    update_meta_ai_task_registry = sgqlc.types.Field(
        meta_ai_task_registry_mutation_response,
        graphql_name="update_meta_ai_task_registry",
        args=sgqlc.types.ArgDict(
            (
                ("_inc", sgqlc.types.Arg(meta_ai_task_registry_inc_input, graphql_name="_inc", default=None)),
                ("_set", sgqlc.types.Arg(meta_ai_task_registry_set_input, graphql_name="_set", default=None)),
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_task_registry_bool_exp), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    update_meta_ai_task_registry_by_pk = sgqlc.types.Field(
        meta_ai_task_registry,
        graphql_name="update_meta_ai_task_registry_by_pk",
        args=sgqlc.types.ArgDict(
            (
                ("_inc", sgqlc.types.Arg(meta_ai_task_registry_inc_input, graphql_name="_inc", default=None)),
                ("_set", sgqlc.types.Arg(meta_ai_task_registry_set_input, graphql_name="_set", default=None)),
                (
                    "pk_columns",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_task_registry_pk_columns_input),
                        graphql_name="pk_columns",
                        default=None,
                    ),
                ),
            )
        ),
    )
    update_meta_ai_training_instance = sgqlc.types.Field(
        meta_ai_training_instance_mutation_response,
        graphql_name="update_meta_ai_training_instance",
        args=sgqlc.types.ArgDict(
            (
                (
                    "_append",
                    sgqlc.types.Arg(meta_ai_training_instance_append_input, graphql_name="_append", default=None),
                ),
                (
                    "_delete_at_path",
                    sgqlc.types.Arg(
                        meta_ai_training_instance_delete_at_path_input, graphql_name="_delete_at_path", default=None
                    ),
                ),
                (
                    "_delete_elem",
                    sgqlc.types.Arg(
                        meta_ai_training_instance_delete_elem_input, graphql_name="_delete_elem", default=None
                    ),
                ),
                (
                    "_delete_key",
                    sgqlc.types.Arg(
                        meta_ai_training_instance_delete_key_input, graphql_name="_delete_key", default=None
                    ),
                ),
                (
                    "_prepend",
                    sgqlc.types.Arg(meta_ai_training_instance_prepend_input, graphql_name="_prepend", default=None),
                ),
                ("_set", sgqlc.types.Arg(meta_ai_training_instance_set_input, graphql_name="_set", default=None)),
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_training_instance_bool_exp), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    update_meta_ai_training_instance_by_pk = sgqlc.types.Field(
        meta_ai_training_instance,
        graphql_name="update_meta_ai_training_instance_by_pk",
        args=sgqlc.types.ArgDict(
            (
                (
                    "_append",
                    sgqlc.types.Arg(meta_ai_training_instance_append_input, graphql_name="_append", default=None),
                ),
                (
                    "_delete_at_path",
                    sgqlc.types.Arg(
                        meta_ai_training_instance_delete_at_path_input, graphql_name="_delete_at_path", default=None
                    ),
                ),
                (
                    "_delete_elem",
                    sgqlc.types.Arg(
                        meta_ai_training_instance_delete_elem_input, graphql_name="_delete_elem", default=None
                    ),
                ),
                (
                    "_delete_key",
                    sgqlc.types.Arg(
                        meta_ai_training_instance_delete_key_input, graphql_name="_delete_key", default=None
                    ),
                ),
                (
                    "_prepend",
                    sgqlc.types.Arg(meta_ai_training_instance_prepend_input, graphql_name="_prepend", default=None),
                ),
                ("_set", sgqlc.types.Arg(meta_ai_training_instance_set_input, graphql_name="_set", default=None)),
                (
                    "pk_columns",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_training_instance_pk_columns_input),
                        graphql_name="pk_columns",
                        default=None,
                    ),
                ),
            )
        ),
    )
    update_meta_ai_training_state = sgqlc.types.Field(
        meta_ai_training_state_mutation_response,
        graphql_name="update_meta_ai_training_state",
        args=sgqlc.types.ArgDict(
            (
                ("_set", sgqlc.types.Arg(meta_ai_training_state_set_input, graphql_name="_set", default=None)),
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_training_state_bool_exp), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    update_meta_ai_training_state_by_pk = sgqlc.types.Field(
        meta_ai_training_state,
        graphql_name="update_meta_ai_training_state_by_pk",
        args=sgqlc.types.ArgDict(
            (
                ("_set", sgqlc.types.Arg(meta_ai_training_state_set_input, graphql_name="_set", default=None)),
                (
                    "pk_columns",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_training_state_pk_columns_input),
                        graphql_name="pk_columns",
                        default=None,
                    ),
                ),
            )
        ),
    )
    update_meta_ai_training_template = sgqlc.types.Field(
        meta_ai_training_template_mutation_response,
        graphql_name="update_meta_ai_training_template",
        args=sgqlc.types.ArgDict(
            (
                (
                    "_append",
                    sgqlc.types.Arg(meta_ai_training_template_append_input, graphql_name="_append", default=None),
                ),
                (
                    "_delete_at_path",
                    sgqlc.types.Arg(
                        meta_ai_training_template_delete_at_path_input, graphql_name="_delete_at_path", default=None
                    ),
                ),
                (
                    "_delete_elem",
                    sgqlc.types.Arg(
                        meta_ai_training_template_delete_elem_input, graphql_name="_delete_elem", default=None
                    ),
                ),
                (
                    "_delete_key",
                    sgqlc.types.Arg(
                        meta_ai_training_template_delete_key_input, graphql_name="_delete_key", default=None
                    ),
                ),
                (
                    "_prepend",
                    sgqlc.types.Arg(meta_ai_training_template_prepend_input, graphql_name="_prepend", default=None),
                ),
                ("_set", sgqlc.types.Arg(meta_ai_training_template_set_input, graphql_name="_set", default=None)),
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_training_template_bool_exp), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    update_meta_ai_training_template_by_pk = sgqlc.types.Field(
        meta_ai_training_template,
        graphql_name="update_meta_ai_training_template_by_pk",
        args=sgqlc.types.ArgDict(
            (
                (
                    "_append",
                    sgqlc.types.Arg(meta_ai_training_template_append_input, graphql_name="_append", default=None),
                ),
                (
                    "_delete_at_path",
                    sgqlc.types.Arg(
                        meta_ai_training_template_delete_at_path_input, graphql_name="_delete_at_path", default=None
                    ),
                ),
                (
                    "_delete_elem",
                    sgqlc.types.Arg(
                        meta_ai_training_template_delete_elem_input, graphql_name="_delete_elem", default=None
                    ),
                ),
                (
                    "_delete_key",
                    sgqlc.types.Arg(
                        meta_ai_training_template_delete_key_input, graphql_name="_delete_key", default=None
                    ),
                ),
                (
                    "_prepend",
                    sgqlc.types.Arg(meta_ai_training_template_prepend_input, graphql_name="_prepend", default=None),
                ),
                ("_set", sgqlc.types.Arg(meta_ai_training_template_set_input, graphql_name="_set", default=None)),
                (
                    "pk_columns",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_training_template_pk_columns_input),
                        graphql_name="pk_columns",
                        default=None,
                    ),
                ),
            )
        ),
    )
    update_meta_ai_visibility = sgqlc.types.Field(
        meta_ai_visibility_mutation_response,
        graphql_name="update_meta_ai_visibility",
        args=sgqlc.types.ArgDict(
            (
                ("_set", sgqlc.types.Arg(meta_ai_visibility_set_input, graphql_name="_set", default=None)),
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_visibility_bool_exp), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    update_meta_ai_visibility_by_pk = sgqlc.types.Field(
        meta_ai_visibility,
        graphql_name="update_meta_ai_visibility_by_pk",
        args=sgqlc.types.ArgDict(
            (
                ("_set", sgqlc.types.Arg(meta_ai_visibility_set_input, graphql_name="_set", default=None)),
                (
                    "pk_columns",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_visibility_pk_columns_input),
                        graphql_name="pk_columns",
                        default=None,
                    ),
                ),
            )
        ),
    )
    update_turbine_app = sgqlc.types.Field(
        "turbine_app_mutation_response",
        graphql_name="update_turbine_app",
        args=sgqlc.types.ArgDict(
            (
                ("_set", sgqlc.types.Arg(turbine_app_set_input, graphql_name="_set", default=None)),
                (
                    "where",
                    sgqlc.types.Arg(sgqlc.types.non_null(turbine_app_bool_exp), graphql_name="where", default=None),
                ),
            )
        ),
    )
    update_turbine_app_by_pk = sgqlc.types.Field(
        "turbine_app",
        graphql_name="update_turbine_app_by_pk",
        args=sgqlc.types.ArgDict(
            (
                ("_set", sgqlc.types.Arg(turbine_app_set_input, graphql_name="_set", default=None)),
                (
                    "pk_columns",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(turbine_app_pk_columns_input), graphql_name="pk_columns", default=None
                    ),
                ),
            )
        ),
    )
    update_turbine_job = sgqlc.types.Field(
        "turbine_job_mutation_response",
        graphql_name="update_turbine_job",
        args=sgqlc.types.ArgDict(
            (
                ("_append", sgqlc.types.Arg(turbine_job_append_input, graphql_name="_append", default=None)),
                (
                    "_delete_at_path",
                    sgqlc.types.Arg(turbine_job_delete_at_path_input, graphql_name="_delete_at_path", default=None),
                ),
                (
                    "_delete_elem",
                    sgqlc.types.Arg(turbine_job_delete_elem_input, graphql_name="_delete_elem", default=None),
                ),
                (
                    "_delete_key",
                    sgqlc.types.Arg(turbine_job_delete_key_input, graphql_name="_delete_key", default=None),
                ),
                ("_inc", sgqlc.types.Arg(turbine_job_inc_input, graphql_name="_inc", default=None)),
                ("_prepend", sgqlc.types.Arg(turbine_job_prepend_input, graphql_name="_prepend", default=None)),
                ("_set", sgqlc.types.Arg(turbine_job_set_input, graphql_name="_set", default=None)),
                (
                    "where",
                    sgqlc.types.Arg(sgqlc.types.non_null(turbine_job_bool_exp), graphql_name="where", default=None),
                ),
            )
        ),
    )
    update_turbine_job_by_pk = sgqlc.types.Field(
        "turbine_job",
        graphql_name="update_turbine_job_by_pk",
        args=sgqlc.types.ArgDict(
            (
                ("_append", sgqlc.types.Arg(turbine_job_append_input, graphql_name="_append", default=None)),
                (
                    "_delete_at_path",
                    sgqlc.types.Arg(turbine_job_delete_at_path_input, graphql_name="_delete_at_path", default=None),
                ),
                (
                    "_delete_elem",
                    sgqlc.types.Arg(turbine_job_delete_elem_input, graphql_name="_delete_elem", default=None),
                ),
                (
                    "_delete_key",
                    sgqlc.types.Arg(turbine_job_delete_key_input, graphql_name="_delete_key", default=None),
                ),
                ("_inc", sgqlc.types.Arg(turbine_job_inc_input, graphql_name="_inc", default=None)),
                ("_prepend", sgqlc.types.Arg(turbine_job_prepend_input, graphql_name="_prepend", default=None)),
                ("_set", sgqlc.types.Arg(turbine_job_set_input, graphql_name="_set", default=None)),
                (
                    "pk_columns",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(turbine_job_pk_columns_input), graphql_name="pk_columns", default=None
                    ),
                ),
            )
        ),
    )
    update_turbine_task = sgqlc.types.Field(
        "turbine_task_mutation_response",
        graphql_name="update_turbine_task",
        args=sgqlc.types.ArgDict(
            (
                ("_append", sgqlc.types.Arg(turbine_task_append_input, graphql_name="_append", default=None)),
                (
                    "_delete_at_path",
                    sgqlc.types.Arg(turbine_task_delete_at_path_input, graphql_name="_delete_at_path", default=None),
                ),
                (
                    "_delete_elem",
                    sgqlc.types.Arg(turbine_task_delete_elem_input, graphql_name="_delete_elem", default=None),
                ),
                (
                    "_delete_key",
                    sgqlc.types.Arg(turbine_task_delete_key_input, graphql_name="_delete_key", default=None),
                ),
                ("_inc", sgqlc.types.Arg(turbine_task_inc_input, graphql_name="_inc", default=None)),
                ("_prepend", sgqlc.types.Arg(turbine_task_prepend_input, graphql_name="_prepend", default=None)),
                ("_set", sgqlc.types.Arg(turbine_task_set_input, graphql_name="_set", default=None)),
                (
                    "where",
                    sgqlc.types.Arg(sgqlc.types.non_null(turbine_task_bool_exp), graphql_name="where", default=None),
                ),
            )
        ),
    )
    update_turbine_task_by_pk = sgqlc.types.Field(
        "turbine_task",
        graphql_name="update_turbine_task_by_pk",
        args=sgqlc.types.ArgDict(
            (
                ("_append", sgqlc.types.Arg(turbine_task_append_input, graphql_name="_append", default=None)),
                (
                    "_delete_at_path",
                    sgqlc.types.Arg(turbine_task_delete_at_path_input, graphql_name="_delete_at_path", default=None),
                ),
                (
                    "_delete_elem",
                    sgqlc.types.Arg(turbine_task_delete_elem_input, graphql_name="_delete_elem", default=None),
                ),
                (
                    "_delete_key",
                    sgqlc.types.Arg(turbine_task_delete_key_input, graphql_name="_delete_key", default=None),
                ),
                ("_inc", sgqlc.types.Arg(turbine_task_inc_input, graphql_name="_inc", default=None)),
                ("_prepend", sgqlc.types.Arg(turbine_task_prepend_input, graphql_name="_prepend", default=None)),
                ("_set", sgqlc.types.Arg(turbine_task_set_input, graphql_name="_set", default=None)),
                (
                    "pk_columns",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(turbine_task_pk_columns_input), graphql_name="pk_columns", default=None
                    ),
                ),
            )
        ),
    )


class query_root(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "get_prelabel",
        "meta_ai_app",
        "meta_ai_app_aggregate",
        "meta_ai_app_by_pk",
        "meta_ai_assignment",
        "meta_ai_assignment_aggregate",
        "meta_ai_assignment_by_pk",
        "meta_ai_dataset",
        "meta_ai_dataset_aggregate",
        "meta_ai_dataset_by_pk",
        "meta_ai_dataset_metric",
        "meta_ai_dataset_metric_aggregate",
        "meta_ai_dataset_metric_by_pk",
        "meta_ai_deployment",
        "meta_ai_deployment_aggregate",
        "meta_ai_deployment_by_pk",
        "meta_ai_deployment_log",
        "meta_ai_deployment_log_aggregate",
        "meta_ai_deployment_log_by_pk",
        "meta_ai_deployment_purpose",
        "meta_ai_deployment_purpose_aggregate",
        "meta_ai_deployment_purpose_by_pk",
        "meta_ai_deployment_status",
        "meta_ai_deployment_status_aggregate",
        "meta_ai_deployment_status_by_pk",
        "meta_ai_deployment_type",
        "meta_ai_deployment_type_aggregate",
        "meta_ai_deployment_type_by_pk",
        "meta_ai_environment",
        "meta_ai_environment_aggregate",
        "meta_ai_environment_by_pk",
        "meta_ai_instance",
        "meta_ai_instance_aggregate",
        "meta_ai_instance_by_pk",
        "meta_ai_model",
        "meta_ai_model_aggregate",
        "meta_ai_model_by_pk",
        "meta_ai_prediction",
        "meta_ai_prediction_aggregate",
        "meta_ai_prediction_by_pk",
        "meta_ai_prediction_state",
        "meta_ai_prediction_state_aggregate",
        "meta_ai_prediction_state_by_pk",
        "meta_ai_predictions_by_day",
        "meta_ai_predictions_by_day_aggregate",
        "meta_ai_task_registry",
        "meta_ai_task_registry_aggregate",
        "meta_ai_task_registry_by_pk",
        "meta_ai_training_instance",
        "meta_ai_training_instance_aggregate",
        "meta_ai_training_instance_by_pk",
        "meta_ai_training_state",
        "meta_ai_training_state_aggregate",
        "meta_ai_training_state_by_pk",
        "meta_ai_training_template",
        "meta_ai_training_template_aggregate",
        "meta_ai_training_template_by_pk",
        "meta_ai_visibility",
        "meta_ai_visibility_aggregate",
        "meta_ai_visibility_by_pk",
        "predict_with_deployment",
        "predict_with_deployment_async",
        "request_prediction_of_app",
        "request_prediction_of_job",
        "resolve_data_ref",
        "start_deployment",
        "turbine_app",
        "turbine_app_aggregate",
        "turbine_app_by_pk",
        "turbine_job",
        "turbine_job_aggregate",
        "turbine_job_by_pk",
        "turbine_task",
        "turbine_task_aggregate",
        "turbine_task_by_pk",
    )
    get_prelabel = sgqlc.types.Field(
        sgqlc.types.list_of(Prelabel),
        graphql_name="get_prelabel",
        args=sgqlc.types.ArgDict(
            (
                ("job_id", sgqlc.types.Arg(bigint, graphql_name="jobId", default=None)),
                ("task_id", sgqlc.types.Arg(bigint, graphql_name="taskId", default=None)),
            )
        ),
    )
    meta_ai_app = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_app"))),
        graphql_name="meta_ai_app",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_app_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_app_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_app_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_app_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("meta_ai_app_aggregate"),
        graphql_name="meta_ai_app_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_app_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_app_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_app_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_app_by_pk = sgqlc.types.Field(
        "meta_ai_app",
        graphql_name="meta_ai_app_by_pk",
        args=sgqlc.types.ArgDict(
            (
                (
                    "assigned",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_assignment_enum), graphql_name="assigned", default=None
                    ),
                ),
                ("id", sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name="id", default=None)),
                ("model_id", sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name="modelId", default=None)),
            )
        ),
    )
    meta_ai_assignment = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_assignment"))),
        graphql_name="meta_ai_assignment",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_assignment_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_assignment_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_assignment_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_assignment_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("meta_ai_assignment_aggregate"),
        graphql_name="meta_ai_assignment_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_assignment_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_assignment_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_assignment_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_assignment_by_pk = sgqlc.types.Field(
        "meta_ai_assignment",
        graphql_name="meta_ai_assignment_by_pk",
        args=sgqlc.types.ArgDict(
            (("type", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="type", default=None)),)
        ),
    )
    meta_ai_dataset = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_dataset"))),
        graphql_name="meta_ai_dataset",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_dataset_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_dataset_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_dataset_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_dataset_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("meta_ai_dataset_aggregate"),
        graphql_name="meta_ai_dataset_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_dataset_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_dataset_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_dataset_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_dataset_by_pk = sgqlc.types.Field(
        "meta_ai_dataset",
        graphql_name="meta_ai_dataset_by_pk",
        args=sgqlc.types.ArgDict(
            (("id", sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name="id", default=None)),)
        ),
    )
    meta_ai_dataset_metric = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_dataset_metric"))),
        graphql_name="meta_ai_dataset_metric",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_dataset_metric_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_dataset_metric_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_dataset_metric_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_dataset_metric_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("meta_ai_dataset_metric_aggregate"),
        graphql_name="meta_ai_dataset_metric_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_dataset_metric_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_dataset_metric_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_dataset_metric_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_dataset_metric_by_pk = sgqlc.types.Field(
        "meta_ai_dataset_metric",
        graphql_name="meta_ai_dataset_metric_by_pk",
        args=sgqlc.types.ArgDict(
            (("id", sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name="id", default=None)),)
        ),
    )
    meta_ai_deployment = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_deployment"))),
        graphql_name="meta_ai_deployment",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_deployment_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_deployment_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("meta_ai_deployment_aggregate"),
        graphql_name="meta_ai_deployment_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_deployment_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_deployment_by_pk = sgqlc.types.Field(
        "meta_ai_deployment",
        graphql_name="meta_ai_deployment_by_pk",
        args=sgqlc.types.ArgDict(
            (("id", sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name="id", default=None)),)
        ),
    )
    meta_ai_deployment_log = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_deployment_log"))),
        graphql_name="meta_ai_deployment_log",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_log_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_log_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_deployment_log_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_deployment_log_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("meta_ai_deployment_log_aggregate"),
        graphql_name="meta_ai_deployment_log_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_log_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_log_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_deployment_log_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_deployment_log_by_pk = sgqlc.types.Field(
        "meta_ai_deployment_log",
        graphql_name="meta_ai_deployment_log_by_pk",
        args=sgqlc.types.ArgDict(
            (
                (
                    "deployment_id",
                    sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name="deployment_id", default=None),
                ),
                ("id", sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name="id", default=None)),
            )
        ),
    )
    meta_ai_deployment_purpose = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_deployment_purpose"))),
        graphql_name="meta_ai_deployment_purpose",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_purpose_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_purpose_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_deployment_purpose_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_deployment_purpose_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("meta_ai_deployment_purpose_aggregate"),
        graphql_name="meta_ai_deployment_purpose_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_purpose_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_purpose_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_deployment_purpose_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_deployment_purpose_by_pk = sgqlc.types.Field(
        "meta_ai_deployment_purpose",
        graphql_name="meta_ai_deployment_purpose_by_pk",
        args=sgqlc.types.ArgDict(
            (("purpose", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="purpose", default=None)),)
        ),
    )
    meta_ai_deployment_status = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_deployment_status"))),
        graphql_name="meta_ai_deployment_status",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_status_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_status_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_deployment_status_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_deployment_status_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("meta_ai_deployment_status_aggregate"),
        graphql_name="meta_ai_deployment_status_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_status_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_status_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_deployment_status_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_deployment_status_by_pk = sgqlc.types.Field(
        "meta_ai_deployment_status",
        graphql_name="meta_ai_deployment_status_by_pk",
        args=sgqlc.types.ArgDict(
            (("status", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="status", default=None)),)
        ),
    )
    meta_ai_deployment_type = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_deployment_type"))),
        graphql_name="meta_ai_deployment_type",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_type_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_type_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_deployment_type_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_deployment_type_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("meta_ai_deployment_type_aggregate"),
        graphql_name="meta_ai_deployment_type_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_type_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_type_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_deployment_type_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_deployment_type_by_pk = sgqlc.types.Field(
        "meta_ai_deployment_type",
        graphql_name="meta_ai_deployment_type_by_pk",
        args=sgqlc.types.ArgDict(
            (("name", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="name", default=None)),)
        ),
    )
    meta_ai_environment = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_environment"))),
        graphql_name="meta_ai_environment",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_environment_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_environment_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_environment_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_environment_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("meta_ai_environment_aggregate"),
        graphql_name="meta_ai_environment_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_environment_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_environment_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_environment_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_environment_by_pk = sgqlc.types.Field(
        "meta_ai_environment",
        graphql_name="meta_ai_environment_by_pk",
        args=sgqlc.types.ArgDict(
            (("name", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="name", default=None)),)
        ),
    )
    meta_ai_instance = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_instance"))),
        graphql_name="meta_ai_instance",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_instance_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_instance_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_instance_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_instance_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("meta_ai_instance_aggregate"),
        graphql_name="meta_ai_instance_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_instance_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_instance_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_instance_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_instance_by_pk = sgqlc.types.Field(
        "meta_ai_instance",
        graphql_name="meta_ai_instance_by_pk",
        args=sgqlc.types.ArgDict(
            (
                ("id", sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name="id", default=None)),
                (
                    "prediction_id",
                    sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name="predictionId", default=None),
                ),
            )
        ),
    )
    meta_ai_model = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_model"))),
        graphql_name="meta_ai_model",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_model_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_model_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_model_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_model_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("meta_ai_model_aggregate"),
        graphql_name="meta_ai_model_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_model_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_model_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_model_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_model_by_pk = sgqlc.types.Field(
        "meta_ai_model",
        graphql_name="meta_ai_model_by_pk",
        args=sgqlc.types.ArgDict(
            (("id", sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name="id", default=None)),)
        ),
    )
    meta_ai_prediction = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_prediction"))),
        graphql_name="meta_ai_prediction",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_prediction_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_prediction_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("meta_ai_prediction_aggregate"),
        graphql_name="meta_ai_prediction_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_prediction_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_prediction_by_pk = sgqlc.types.Field(
        "meta_ai_prediction",
        graphql_name="meta_ai_prediction_by_pk",
        args=sgqlc.types.ArgDict(
            (("id", sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name="id", default=None)),)
        ),
    )
    meta_ai_prediction_state = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_prediction_state"))),
        graphql_name="meta_ai_prediction_state",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_state_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_state_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_prediction_state_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_prediction_state_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("meta_ai_prediction_state_aggregate"),
        graphql_name="meta_ai_prediction_state_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_state_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_state_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_prediction_state_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_prediction_state_by_pk = sgqlc.types.Field(
        "meta_ai_prediction_state",
        graphql_name="meta_ai_prediction_state_by_pk",
        args=sgqlc.types.ArgDict(
            (("state", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="state", default=None)),)
        ),
    )
    meta_ai_predictions_by_day = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_predictions_by_day"))),
        graphql_name="meta_ai_predictions_by_day",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_predictions_by_day_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_predictions_by_day_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_predictions_by_day_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_predictions_by_day_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("meta_ai_predictions_by_day_aggregate"),
        graphql_name="meta_ai_predictions_by_day_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_predictions_by_day_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_predictions_by_day_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_predictions_by_day_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_task_registry = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_task_registry"))),
        graphql_name="meta_ai_task_registry",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_task_registry_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_task_registry_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_task_registry_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_task_registry_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("meta_ai_task_registry_aggregate"),
        graphql_name="meta_ai_task_registry_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_task_registry_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_task_registry_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_task_registry_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_task_registry_by_pk = sgqlc.types.Field(
        "meta_ai_task_registry",
        graphql_name="meta_ai_task_registry_by_pk",
        args=sgqlc.types.ArgDict(
            (("id", sgqlc.types.Arg(sgqlc.types.non_null(bigint), graphql_name="id", default=None)),)
        ),
    )
    meta_ai_training_instance = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_training_instance"))),
        graphql_name="meta_ai_training_instance",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_training_instance_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_training_instance_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_training_instance_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_training_instance_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("meta_ai_training_instance_aggregate"),
        graphql_name="meta_ai_training_instance_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_training_instance_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_training_instance_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_training_instance_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_training_instance_by_pk = sgqlc.types.Field(
        "meta_ai_training_instance",
        graphql_name="meta_ai_training_instance_by_pk",
        args=sgqlc.types.ArgDict(
            (("id", sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name="id", default=None)),)
        ),
    )
    meta_ai_training_state = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_training_state"))),
        graphql_name="meta_ai_training_state",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_training_state_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_training_state_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_training_state_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_training_state_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("meta_ai_training_state_aggregate"),
        graphql_name="meta_ai_training_state_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_training_state_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_training_state_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_training_state_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_training_state_by_pk = sgqlc.types.Field(
        "meta_ai_training_state",
        graphql_name="meta_ai_training_state_by_pk",
        args=sgqlc.types.ArgDict(
            (("state", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="state", default=None)),)
        ),
    )
    meta_ai_training_template = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_training_template"))),
        graphql_name="meta_ai_training_template",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_training_template_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_training_template_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_training_template_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_training_template_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("meta_ai_training_template_aggregate"),
        graphql_name="meta_ai_training_template_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_training_template_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_training_template_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_training_template_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_training_template_by_pk = sgqlc.types.Field(
        "meta_ai_training_template",
        graphql_name="meta_ai_training_template_by_pk",
        args=sgqlc.types.ArgDict(
            (("id", sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name="id", default=None)),)
        ),
    )
    meta_ai_visibility = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_visibility"))),
        graphql_name="meta_ai_visibility",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_visibility_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_visibility_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_visibility_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_visibility_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("meta_ai_visibility_aggregate"),
        graphql_name="meta_ai_visibility_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_visibility_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_visibility_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_visibility_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_visibility_by_pk = sgqlc.types.Field(
        "meta_ai_visibility",
        graphql_name="meta_ai_visibility_by_pk",
        args=sgqlc.types.ArgDict(
            (("type", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="type", default=None)),)
        ),
    )
    predict_with_deployment = sgqlc.types.Field(
        sgqlc.types.list_of(RawPrediction),
        graphql_name="predict_with_deployment",
        args=sgqlc.types.ArgDict(
            (("request", sgqlc.types.Arg(PredictionRequest, graphql_name="request", default=None)),)
        ),
    )
    predict_with_deployment_async = sgqlc.types.Field(
        Prediction,
        graphql_name="predict_with_deployment_async",
        args=sgqlc.types.ArgDict(
            (("request", sgqlc.types.Arg(PredictionRequest, graphql_name="request", default=None)),)
        ),
    )
    request_prediction_of_app = sgqlc.types.Field(
        "request_prediction_of_app",
        graphql_name="request_prediction_of_app",
        args=sgqlc.types.ArgDict(
            (("id", sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name="id", default=None)),)
        ),
    )
    request_prediction_of_job = sgqlc.types.Field(
        sgqlc.types.list_of(Prediction),
        graphql_name="request_prediction_of_job",
        args=sgqlc.types.ArgDict(
            (
                ("app_id", sgqlc.types.Arg(uuid, graphql_name="app_id", default=None)),
                ("assignment", sgqlc.types.Arg(String, graphql_name="assignment", default=None)),
                ("job_id", sgqlc.types.Arg(bigint, graphql_name="job_id", default=None)),
            )
        ),
    )
    resolve_data_ref = sgqlc.types.Field(
        URL,
        graphql_name="resolve_data_ref",
        args=sgqlc.types.ArgDict(
            (
                ("data_ref", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="data_ref", default=None)),
                ("instance_id", sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name="instance_id", default=None)),
                (
                    "prediction_id",
                    sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name="prediction_id", default=None),
                ),
            )
        ),
    )
    start_deployment = sgqlc.types.Field(
        "start_deployment",
        graphql_name="start_deployment",
        args=sgqlc.types.ArgDict(
            (("id", sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name="id", default=None)),)
        ),
    )
    turbine_app = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("turbine_app"))),
        graphql_name="turbine_app",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(turbine_app_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(turbine_app_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(turbine_app_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    turbine_app_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("turbine_app_aggregate"),
        graphql_name="turbine_app_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(turbine_app_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(turbine_app_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(turbine_app_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    turbine_app_by_pk = sgqlc.types.Field(
        "turbine_app",
        graphql_name="turbine_app_by_pk",
        args=sgqlc.types.ArgDict(
            (("id", sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name="id", default=None)),)
        ),
    )
    turbine_job = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("turbine_job"))),
        graphql_name="turbine_job",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(turbine_job_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(turbine_job_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(turbine_job_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    turbine_job_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("turbine_job_aggregate"),
        graphql_name="turbine_job_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(turbine_job_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(turbine_job_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(turbine_job_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    turbine_job_by_pk = sgqlc.types.Field(
        "turbine_job",
        graphql_name="turbine_job_by_pk",
        args=sgqlc.types.ArgDict(
            (("id", sgqlc.types.Arg(sgqlc.types.non_null(bigint), graphql_name="id", default=None)),)
        ),
    )
    turbine_task = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("turbine_task"))),
        graphql_name="turbine_task",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(turbine_task_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(turbine_task_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(turbine_task_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    turbine_task_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("turbine_task_aggregate"),
        graphql_name="turbine_task_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(turbine_task_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(turbine_task_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(turbine_task_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    turbine_task_by_pk = sgqlc.types.Field(
        "turbine_task",
        graphql_name="turbine_task_by_pk",
        args=sgqlc.types.ArgDict(
            (("id", sgqlc.types.Arg(sgqlc.types.non_null(bigint), graphql_name="id", default=None)),)
        ),
    )


class request_prediction_of_app(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("created_at", "errors", "id", "output")
    created_at = sgqlc.types.Field(sgqlc.types.non_null(timestamptz), graphql_name="created_at")
    errors = sgqlc.types.Field(json, graphql_name="errors")
    id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name="id")
    output = sgqlc.types.Field(AppPredictions, graphql_name="output")


class start_deployment(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("created_at", "errors", "id", "output")
    created_at = sgqlc.types.Field(sgqlc.types.non_null(timestamptz), graphql_name="created_at")
    errors = sgqlc.types.Field(json, graphql_name="errors")
    id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name="id")
    output = sgqlc.types.Field(DeploymentStatus, graphql_name="output")


class subscription_root(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "meta_ai_app",
        "meta_ai_app_aggregate",
        "meta_ai_app_by_pk",
        "meta_ai_assignment",
        "meta_ai_assignment_aggregate",
        "meta_ai_assignment_by_pk",
        "meta_ai_dataset",
        "meta_ai_dataset_aggregate",
        "meta_ai_dataset_by_pk",
        "meta_ai_dataset_metric",
        "meta_ai_dataset_metric_aggregate",
        "meta_ai_dataset_metric_by_pk",
        "meta_ai_deployment",
        "meta_ai_deployment_aggregate",
        "meta_ai_deployment_by_pk",
        "meta_ai_deployment_log",
        "meta_ai_deployment_log_aggregate",
        "meta_ai_deployment_log_by_pk",
        "meta_ai_deployment_purpose",
        "meta_ai_deployment_purpose_aggregate",
        "meta_ai_deployment_purpose_by_pk",
        "meta_ai_deployment_status",
        "meta_ai_deployment_status_aggregate",
        "meta_ai_deployment_status_by_pk",
        "meta_ai_deployment_type",
        "meta_ai_deployment_type_aggregate",
        "meta_ai_deployment_type_by_pk",
        "meta_ai_environment",
        "meta_ai_environment_aggregate",
        "meta_ai_environment_by_pk",
        "meta_ai_instance",
        "meta_ai_instance_aggregate",
        "meta_ai_instance_by_pk",
        "meta_ai_model",
        "meta_ai_model_aggregate",
        "meta_ai_model_by_pk",
        "meta_ai_prediction",
        "meta_ai_prediction_aggregate",
        "meta_ai_prediction_by_pk",
        "meta_ai_prediction_state",
        "meta_ai_prediction_state_aggregate",
        "meta_ai_prediction_state_by_pk",
        "meta_ai_predictions_by_day",
        "meta_ai_predictions_by_day_aggregate",
        "meta_ai_task_registry",
        "meta_ai_task_registry_aggregate",
        "meta_ai_task_registry_by_pk",
        "meta_ai_training_instance",
        "meta_ai_training_instance_aggregate",
        "meta_ai_training_instance_by_pk",
        "meta_ai_training_state",
        "meta_ai_training_state_aggregate",
        "meta_ai_training_state_by_pk",
        "meta_ai_training_template",
        "meta_ai_training_template_aggregate",
        "meta_ai_training_template_by_pk",
        "meta_ai_visibility",
        "meta_ai_visibility_aggregate",
        "meta_ai_visibility_by_pk",
        "request_prediction_of_app",
        "start_deployment",
        "turbine_app",
        "turbine_app_aggregate",
        "turbine_app_by_pk",
        "turbine_job",
        "turbine_job_aggregate",
        "turbine_job_by_pk",
        "turbine_task",
        "turbine_task_aggregate",
        "turbine_task_by_pk",
    )
    meta_ai_app = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_app"))),
        graphql_name="meta_ai_app",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_app_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_app_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_app_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_app_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("meta_ai_app_aggregate"),
        graphql_name="meta_ai_app_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_app_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_app_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_app_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_app_by_pk = sgqlc.types.Field(
        "meta_ai_app",
        graphql_name="meta_ai_app_by_pk",
        args=sgqlc.types.ArgDict(
            (
                (
                    "assigned",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(meta_ai_assignment_enum), graphql_name="assigned", default=None
                    ),
                ),
                ("id", sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name="id", default=None)),
                ("model_id", sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name="modelId", default=None)),
            )
        ),
    )
    meta_ai_assignment = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_assignment"))),
        graphql_name="meta_ai_assignment",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_assignment_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_assignment_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_assignment_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_assignment_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("meta_ai_assignment_aggregate"),
        graphql_name="meta_ai_assignment_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_assignment_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_assignment_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_assignment_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_assignment_by_pk = sgqlc.types.Field(
        "meta_ai_assignment",
        graphql_name="meta_ai_assignment_by_pk",
        args=sgqlc.types.ArgDict(
            (("type", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="type", default=None)),)
        ),
    )
    meta_ai_dataset = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_dataset"))),
        graphql_name="meta_ai_dataset",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_dataset_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_dataset_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_dataset_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_dataset_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("meta_ai_dataset_aggregate"),
        graphql_name="meta_ai_dataset_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_dataset_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_dataset_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_dataset_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_dataset_by_pk = sgqlc.types.Field(
        "meta_ai_dataset",
        graphql_name="meta_ai_dataset_by_pk",
        args=sgqlc.types.ArgDict(
            (("id", sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name="id", default=None)),)
        ),
    )
    meta_ai_dataset_metric = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_dataset_metric"))),
        graphql_name="meta_ai_dataset_metric",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_dataset_metric_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_dataset_metric_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_dataset_metric_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_dataset_metric_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("meta_ai_dataset_metric_aggregate"),
        graphql_name="meta_ai_dataset_metric_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_dataset_metric_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_dataset_metric_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_dataset_metric_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_dataset_metric_by_pk = sgqlc.types.Field(
        "meta_ai_dataset_metric",
        graphql_name="meta_ai_dataset_metric_by_pk",
        args=sgqlc.types.ArgDict(
            (("id", sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name="id", default=None)),)
        ),
    )
    meta_ai_deployment = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_deployment"))),
        graphql_name="meta_ai_deployment",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_deployment_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_deployment_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("meta_ai_deployment_aggregate"),
        graphql_name="meta_ai_deployment_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_deployment_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_deployment_by_pk = sgqlc.types.Field(
        "meta_ai_deployment",
        graphql_name="meta_ai_deployment_by_pk",
        args=sgqlc.types.ArgDict(
            (("id", sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name="id", default=None)),)
        ),
    )
    meta_ai_deployment_log = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_deployment_log"))),
        graphql_name="meta_ai_deployment_log",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_log_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_log_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_deployment_log_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_deployment_log_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("meta_ai_deployment_log_aggregate"),
        graphql_name="meta_ai_deployment_log_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_log_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_log_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_deployment_log_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_deployment_log_by_pk = sgqlc.types.Field(
        "meta_ai_deployment_log",
        graphql_name="meta_ai_deployment_log_by_pk",
        args=sgqlc.types.ArgDict(
            (
                (
                    "deployment_id",
                    sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name="deployment_id", default=None),
                ),
                ("id", sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name="id", default=None)),
            )
        ),
    )
    meta_ai_deployment_purpose = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_deployment_purpose"))),
        graphql_name="meta_ai_deployment_purpose",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_purpose_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_purpose_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_deployment_purpose_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_deployment_purpose_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("meta_ai_deployment_purpose_aggregate"),
        graphql_name="meta_ai_deployment_purpose_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_purpose_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_purpose_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_deployment_purpose_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_deployment_purpose_by_pk = sgqlc.types.Field(
        "meta_ai_deployment_purpose",
        graphql_name="meta_ai_deployment_purpose_by_pk",
        args=sgqlc.types.ArgDict(
            (("purpose", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="purpose", default=None)),)
        ),
    )
    meta_ai_deployment_status = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_deployment_status"))),
        graphql_name="meta_ai_deployment_status",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_status_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_status_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_deployment_status_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_deployment_status_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("meta_ai_deployment_status_aggregate"),
        graphql_name="meta_ai_deployment_status_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_status_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_status_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_deployment_status_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_deployment_status_by_pk = sgqlc.types.Field(
        "meta_ai_deployment_status",
        graphql_name="meta_ai_deployment_status_by_pk",
        args=sgqlc.types.ArgDict(
            (("status", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="status", default=None)),)
        ),
    )
    meta_ai_deployment_type = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_deployment_type"))),
        graphql_name="meta_ai_deployment_type",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_type_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_type_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_deployment_type_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_deployment_type_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("meta_ai_deployment_type_aggregate"),
        graphql_name="meta_ai_deployment_type_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_type_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_type_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_deployment_type_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_deployment_type_by_pk = sgqlc.types.Field(
        "meta_ai_deployment_type",
        graphql_name="meta_ai_deployment_type_by_pk",
        args=sgqlc.types.ArgDict(
            (("name", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="name", default=None)),)
        ),
    )
    meta_ai_environment = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_environment"))),
        graphql_name="meta_ai_environment",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_environment_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_environment_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_environment_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_environment_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("meta_ai_environment_aggregate"),
        graphql_name="meta_ai_environment_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_environment_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_environment_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_environment_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_environment_by_pk = sgqlc.types.Field(
        "meta_ai_environment",
        graphql_name="meta_ai_environment_by_pk",
        args=sgqlc.types.ArgDict(
            (("name", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="name", default=None)),)
        ),
    )
    meta_ai_instance = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_instance"))),
        graphql_name="meta_ai_instance",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_instance_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_instance_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_instance_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_instance_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("meta_ai_instance_aggregate"),
        graphql_name="meta_ai_instance_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_instance_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_instance_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_instance_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_instance_by_pk = sgqlc.types.Field(
        "meta_ai_instance",
        graphql_name="meta_ai_instance_by_pk",
        args=sgqlc.types.ArgDict(
            (
                ("id", sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name="id", default=None)),
                (
                    "prediction_id",
                    sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name="predictionId", default=None),
                ),
            )
        ),
    )
    meta_ai_model = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_model"))),
        graphql_name="meta_ai_model",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_model_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_model_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_model_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_model_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("meta_ai_model_aggregate"),
        graphql_name="meta_ai_model_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_model_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_model_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_model_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_model_by_pk = sgqlc.types.Field(
        "meta_ai_model",
        graphql_name="meta_ai_model_by_pk",
        args=sgqlc.types.ArgDict(
            (("id", sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name="id", default=None)),)
        ),
    )
    meta_ai_prediction = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_prediction"))),
        graphql_name="meta_ai_prediction",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_prediction_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_prediction_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("meta_ai_prediction_aggregate"),
        graphql_name="meta_ai_prediction_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_prediction_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_prediction_by_pk = sgqlc.types.Field(
        "meta_ai_prediction",
        graphql_name="meta_ai_prediction_by_pk",
        args=sgqlc.types.ArgDict(
            (("id", sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name="id", default=None)),)
        ),
    )
    meta_ai_prediction_state = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_prediction_state"))),
        graphql_name="meta_ai_prediction_state",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_state_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_state_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_prediction_state_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_prediction_state_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("meta_ai_prediction_state_aggregate"),
        graphql_name="meta_ai_prediction_state_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_state_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_state_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_prediction_state_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_prediction_state_by_pk = sgqlc.types.Field(
        "meta_ai_prediction_state",
        graphql_name="meta_ai_prediction_state_by_pk",
        args=sgqlc.types.ArgDict(
            (("state", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="state", default=None)),)
        ),
    )
    meta_ai_predictions_by_day = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_predictions_by_day"))),
        graphql_name="meta_ai_predictions_by_day",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_predictions_by_day_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_predictions_by_day_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_predictions_by_day_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_predictions_by_day_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("meta_ai_predictions_by_day_aggregate"),
        graphql_name="meta_ai_predictions_by_day_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_predictions_by_day_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_predictions_by_day_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_predictions_by_day_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_task_registry = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_task_registry"))),
        graphql_name="meta_ai_task_registry",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_task_registry_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_task_registry_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_task_registry_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_task_registry_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("meta_ai_task_registry_aggregate"),
        graphql_name="meta_ai_task_registry_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_task_registry_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_task_registry_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_task_registry_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_task_registry_by_pk = sgqlc.types.Field(
        "meta_ai_task_registry",
        graphql_name="meta_ai_task_registry_by_pk",
        args=sgqlc.types.ArgDict(
            (("id", sgqlc.types.Arg(sgqlc.types.non_null(bigint), graphql_name="id", default=None)),)
        ),
    )
    meta_ai_training_instance = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_training_instance"))),
        graphql_name="meta_ai_training_instance",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_training_instance_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_training_instance_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_training_instance_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_training_instance_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("meta_ai_training_instance_aggregate"),
        graphql_name="meta_ai_training_instance_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_training_instance_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_training_instance_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_training_instance_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_training_instance_by_pk = sgqlc.types.Field(
        "meta_ai_training_instance",
        graphql_name="meta_ai_training_instance_by_pk",
        args=sgqlc.types.ArgDict(
            (("id", sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name="id", default=None)),)
        ),
    )
    meta_ai_training_state = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_training_state"))),
        graphql_name="meta_ai_training_state",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_training_state_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_training_state_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_training_state_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_training_state_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("meta_ai_training_state_aggregate"),
        graphql_name="meta_ai_training_state_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_training_state_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_training_state_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_training_state_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_training_state_by_pk = sgqlc.types.Field(
        "meta_ai_training_state",
        graphql_name="meta_ai_training_state_by_pk",
        args=sgqlc.types.ArgDict(
            (("state", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="state", default=None)),)
        ),
    )
    meta_ai_training_template = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_training_template"))),
        graphql_name="meta_ai_training_template",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_training_template_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_training_template_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_training_template_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_training_template_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("meta_ai_training_template_aggregate"),
        graphql_name="meta_ai_training_template_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_training_template_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_training_template_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_training_template_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_training_template_by_pk = sgqlc.types.Field(
        "meta_ai_training_template",
        graphql_name="meta_ai_training_template_by_pk",
        args=sgqlc.types.ArgDict(
            (("id", sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name="id", default=None)),)
        ),
    )
    meta_ai_visibility = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("meta_ai_visibility"))),
        graphql_name="meta_ai_visibility",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_visibility_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_visibility_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_visibility_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_visibility_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("meta_ai_visibility_aggregate"),
        graphql_name="meta_ai_visibility_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_visibility_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_visibility_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_visibility_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    meta_ai_visibility_by_pk = sgqlc.types.Field(
        "meta_ai_visibility",
        graphql_name="meta_ai_visibility_by_pk",
        args=sgqlc.types.ArgDict(
            (("type", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="type", default=None)),)
        ),
    )
    request_prediction_of_app = sgqlc.types.Field(
        "request_prediction_of_app",
        graphql_name="request_prediction_of_app",
        args=sgqlc.types.ArgDict(
            (("id", sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name="id", default=None)),)
        ),
    )
    start_deployment = sgqlc.types.Field(
        "start_deployment",
        graphql_name="start_deployment",
        args=sgqlc.types.ArgDict(
            (("id", sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name="id", default=None)),)
        ),
    )
    turbine_app = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("turbine_app"))),
        graphql_name="turbine_app",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(turbine_app_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(turbine_app_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(turbine_app_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    turbine_app_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("turbine_app_aggregate"),
        graphql_name="turbine_app_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(turbine_app_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(turbine_app_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(turbine_app_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    turbine_app_by_pk = sgqlc.types.Field(
        "turbine_app",
        graphql_name="turbine_app_by_pk",
        args=sgqlc.types.ArgDict(
            (("id", sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name="id", default=None)),)
        ),
    )
    turbine_job = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("turbine_job"))),
        graphql_name="turbine_job",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(turbine_job_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(turbine_job_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(turbine_job_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    turbine_job_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("turbine_job_aggregate"),
        graphql_name="turbine_job_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(turbine_job_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(turbine_job_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(turbine_job_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    turbine_job_by_pk = sgqlc.types.Field(
        "turbine_job",
        graphql_name="turbine_job_by_pk",
        args=sgqlc.types.ArgDict(
            (("id", sgqlc.types.Arg(sgqlc.types.non_null(bigint), graphql_name="id", default=None)),)
        ),
    )
    turbine_task = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("turbine_task"))),
        graphql_name="turbine_task",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(turbine_task_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(turbine_task_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(turbine_task_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    turbine_task_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("turbine_task_aggregate"),
        graphql_name="turbine_task_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(turbine_task_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(turbine_task_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(turbine_task_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    turbine_task_by_pk = sgqlc.types.Field(
        "turbine_task",
        graphql_name="turbine_task_by_pk",
        args=sgqlc.types.ArgDict(
            (("id", sgqlc.types.Arg(sgqlc.types.non_null(bigint), graphql_name="id", default=None)),)
        ),
    )


class turbine_app(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("datasets", "datasets_aggregate", "id", "jobs", "jobs_aggregate", "tasks", "tasks_aggregate")
    datasets = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_dataset))),
        graphql_name="datasets",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_dataset_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_dataset_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_dataset_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    datasets_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null(meta_ai_dataset_aggregate),
        graphql_name="datasets_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_dataset_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_dataset_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_dataset_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name="id")
    jobs = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("turbine_job"))),
        graphql_name="jobs",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(turbine_job_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(turbine_job_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(turbine_job_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    jobs_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("turbine_job_aggregate"),
        graphql_name="jobs_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(turbine_job_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(turbine_job_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(turbine_job_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    tasks = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("turbine_task"))),
        graphql_name="tasks",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(turbine_task_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(turbine_task_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(turbine_task_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    tasks_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("turbine_task_aggregate"),
        graphql_name="tasks_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(turbine_task_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(turbine_task_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(turbine_task_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )


class turbine_app_aggregate(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("aggregate", "nodes")
    aggregate = sgqlc.types.Field("turbine_app_aggregate_fields", graphql_name="aggregate")
    nodes = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(turbine_app))), graphql_name="nodes"
    )


class turbine_app_aggregate_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("count", "max", "min")
    count = sgqlc.types.Field(
        sgqlc.types.non_null(Int),
        graphql_name="count",
        args=sgqlc.types.ArgDict(
            (
                (
                    "columns",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(turbine_app_select_column)),
                        graphql_name="columns",
                        default=None,
                    ),
                ),
                ("distinct", sgqlc.types.Arg(Boolean, graphql_name="distinct", default=None)),
            )
        ),
    )
    max = sgqlc.types.Field("turbine_app_max_fields", graphql_name="max")
    min = sgqlc.types.Field("turbine_app_min_fields", graphql_name="min")


class turbine_app_max_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(uuid, graphql_name="id")


class turbine_app_min_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(uuid, graphql_name="id")


class turbine_app_mutation_response(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("affected_rows", "returning")
    affected_rows = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="affected_rows")
    returning = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(turbine_app))), graphql_name="returning"
    )


class turbine_job(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "app",
        "created",
        "data",
        "id",
        "payload",
        "predictions",
        "predictions_aggregate",
        "root_app_uuid",
        "started",
        "state",
        "type",
        "update_count",
        "workflow",
    )
    app = sgqlc.types.Field(turbine_app, graphql_name="app")
    created = sgqlc.types.Field(timestamp, graphql_name="created")
    data = sgqlc.types.Field(
        jsonb,
        graphql_name="data",
        args=sgqlc.types.ArgDict((("path", sgqlc.types.Arg(String, graphql_name="path", default=None)),)),
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(bigint), graphql_name="id")
    payload = sgqlc.types.Field(
        sgqlc.types.non_null(jsonb),
        graphql_name="payload",
        args=sgqlc.types.ArgDict((("path", sgqlc.types.Arg(String, graphql_name="path", default=None)),)),
    )
    predictions = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction))),
        graphql_name="predictions",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_prediction_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    predictions_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null(meta_ai_prediction_aggregate),
        graphql_name="predictions_aggregate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "distinct_on",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_select_column)),
                        graphql_name="distinct_on",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_order_by)),
                        graphql_name="order_by",
                        default=None,
                    ),
                ),
                ("where", sgqlc.types.Arg(meta_ai_prediction_bool_exp, graphql_name="where", default=None)),
            )
        ),
    )
    root_app_uuid = sgqlc.types.Field(uuid, graphql_name="root_app_uuid")
    started = sgqlc.types.Field(timestamp, graphql_name="started")
    state = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="state")
    type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="type")
    update_count = sgqlc.types.Field(Int, graphql_name="update_count")
    workflow = sgqlc.types.Field(String, graphql_name="workflow")


class turbine_job_aggregate(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("aggregate", "nodes")
    aggregate = sgqlc.types.Field("turbine_job_aggregate_fields", graphql_name="aggregate")
    nodes = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(turbine_job))), graphql_name="nodes"
    )


class turbine_job_aggregate_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "avg",
        "count",
        "max",
        "min",
        "stddev",
        "stddev_pop",
        "stddev_samp",
        "sum",
        "var_pop",
        "var_samp",
        "variance",
    )
    avg = sgqlc.types.Field("turbine_job_avg_fields", graphql_name="avg")
    count = sgqlc.types.Field(
        sgqlc.types.non_null(Int),
        graphql_name="count",
        args=sgqlc.types.ArgDict(
            (
                (
                    "columns",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(turbine_job_select_column)),
                        graphql_name="columns",
                        default=None,
                    ),
                ),
                ("distinct", sgqlc.types.Arg(Boolean, graphql_name="distinct", default=None)),
            )
        ),
    )
    max = sgqlc.types.Field("turbine_job_max_fields", graphql_name="max")
    min = sgqlc.types.Field("turbine_job_min_fields", graphql_name="min")
    stddev = sgqlc.types.Field("turbine_job_stddev_fields", graphql_name="stddev")
    stddev_pop = sgqlc.types.Field("turbine_job_stddev_pop_fields", graphql_name="stddev_pop")
    stddev_samp = sgqlc.types.Field("turbine_job_stddev_samp_fields", graphql_name="stddev_samp")
    sum = sgqlc.types.Field("turbine_job_sum_fields", graphql_name="sum")
    var_pop = sgqlc.types.Field("turbine_job_var_pop_fields", graphql_name="var_pop")
    var_samp = sgqlc.types.Field("turbine_job_var_samp_fields", graphql_name="var_samp")
    variance = sgqlc.types.Field("turbine_job_variance_fields", graphql_name="variance")


class turbine_job_avg_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "update_count")
    id = sgqlc.types.Field(Float, graphql_name="id")
    update_count = sgqlc.types.Field(Float, graphql_name="update_count")


class turbine_job_max_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("created", "id", "root_app_uuid", "started", "state", "type", "update_count", "workflow")
    created = sgqlc.types.Field(timestamp, graphql_name="created")
    id = sgqlc.types.Field(bigint, graphql_name="id")
    root_app_uuid = sgqlc.types.Field(uuid, graphql_name="root_app_uuid")
    started = sgqlc.types.Field(timestamp, graphql_name="started")
    state = sgqlc.types.Field(String, graphql_name="state")
    type = sgqlc.types.Field(String, graphql_name="type")
    update_count = sgqlc.types.Field(Int, graphql_name="update_count")
    workflow = sgqlc.types.Field(String, graphql_name="workflow")


class turbine_job_min_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("created", "id", "root_app_uuid", "started", "state", "type", "update_count", "workflow")
    created = sgqlc.types.Field(timestamp, graphql_name="created")
    id = sgqlc.types.Field(bigint, graphql_name="id")
    root_app_uuid = sgqlc.types.Field(uuid, graphql_name="root_app_uuid")
    started = sgqlc.types.Field(timestamp, graphql_name="started")
    state = sgqlc.types.Field(String, graphql_name="state")
    type = sgqlc.types.Field(String, graphql_name="type")
    update_count = sgqlc.types.Field(Int, graphql_name="update_count")
    workflow = sgqlc.types.Field(String, graphql_name="workflow")


class turbine_job_mutation_response(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("affected_rows", "returning")
    affected_rows = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="affected_rows")
    returning = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(turbine_job))), graphql_name="returning"
    )


class turbine_job_stddev_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "update_count")
    id = sgqlc.types.Field(Float, graphql_name="id")
    update_count = sgqlc.types.Field(Float, graphql_name="update_count")


class turbine_job_stddev_pop_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "update_count")
    id = sgqlc.types.Field(Float, graphql_name="id")
    update_count = sgqlc.types.Field(Float, graphql_name="update_count")


class turbine_job_stddev_samp_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "update_count")
    id = sgqlc.types.Field(Float, graphql_name="id")
    update_count = sgqlc.types.Field(Float, graphql_name="update_count")


class turbine_job_sum_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "update_count")
    id = sgqlc.types.Field(bigint, graphql_name="id")
    update_count = sgqlc.types.Field(Int, graphql_name="update_count")


class turbine_job_var_pop_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "update_count")
    id = sgqlc.types.Field(Float, graphql_name="id")
    update_count = sgqlc.types.Field(Float, graphql_name="update_count")


class turbine_job_var_samp_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "update_count")
    id = sgqlc.types.Field(Float, graphql_name="id")
    update_count = sgqlc.types.Field(Float, graphql_name="update_count")


class turbine_job_variance_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "update_count")
    id = sgqlc.types.Field(Float, graphql_name="id")
    update_count = sgqlc.types.Field(Float, graphql_name="update_count")


class turbine_task(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "app",
        "app_id",
        "completed",
        "created",
        "id",
        "job",
        "job_id",
        "name",
        "owner_id",
        "payload",
        "prediction",
        "state",
        "update_count",
        "worker_type",
    )
    app = sgqlc.types.Field(turbine_app, graphql_name="app")
    app_id = sgqlc.types.Field(uuid, graphql_name="app_id")
    completed = sgqlc.types.Field(timestamptz, graphql_name="completed")
    created = sgqlc.types.Field(timestamptz, graphql_name="created")
    id = sgqlc.types.Field(sgqlc.types.non_null(bigint), graphql_name="id")
    job = sgqlc.types.Field(turbine_job, graphql_name="job")
    job_id = sgqlc.types.Field(sgqlc.types.non_null(bigint), graphql_name="job_id")
    name = sgqlc.types.Field(String, graphql_name="name")
    owner_id = sgqlc.types.Field(bigint, graphql_name="owner_id")
    payload = sgqlc.types.Field(
        sgqlc.types.non_null(jsonb),
        graphql_name="payload",
        args=sgqlc.types.ArgDict((("path", sgqlc.types.Arg(String, graphql_name="path", default=None)),)),
    )
    prediction = sgqlc.types.Field(meta_ai_prediction, graphql_name="prediction")
    state = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="state")
    update_count = sgqlc.types.Field(Int, graphql_name="update_count")
    worker_type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="worker_type")


class turbine_task_aggregate(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("aggregate", "nodes")
    aggregate = sgqlc.types.Field("turbine_task_aggregate_fields", graphql_name="aggregate")
    nodes = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(turbine_task))), graphql_name="nodes"
    )


class turbine_task_aggregate_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "avg",
        "count",
        "max",
        "min",
        "stddev",
        "stddev_pop",
        "stddev_samp",
        "sum",
        "var_pop",
        "var_samp",
        "variance",
    )
    avg = sgqlc.types.Field("turbine_task_avg_fields", graphql_name="avg")
    count = sgqlc.types.Field(
        sgqlc.types.non_null(Int),
        graphql_name="count",
        args=sgqlc.types.ArgDict(
            (
                (
                    "columns",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(turbine_task_select_column)),
                        graphql_name="columns",
                        default=None,
                    ),
                ),
                ("distinct", sgqlc.types.Arg(Boolean, graphql_name="distinct", default=None)),
            )
        ),
    )
    max = sgqlc.types.Field("turbine_task_max_fields", graphql_name="max")
    min = sgqlc.types.Field("turbine_task_min_fields", graphql_name="min")
    stddev = sgqlc.types.Field("turbine_task_stddev_fields", graphql_name="stddev")
    stddev_pop = sgqlc.types.Field("turbine_task_stddev_pop_fields", graphql_name="stddev_pop")
    stddev_samp = sgqlc.types.Field("turbine_task_stddev_samp_fields", graphql_name="stddev_samp")
    sum = sgqlc.types.Field("turbine_task_sum_fields", graphql_name="sum")
    var_pop = sgqlc.types.Field("turbine_task_var_pop_fields", graphql_name="var_pop")
    var_samp = sgqlc.types.Field("turbine_task_var_samp_fields", graphql_name="var_samp")
    variance = sgqlc.types.Field("turbine_task_variance_fields", graphql_name="variance")


class turbine_task_avg_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "job_id", "owner_id", "update_count")
    id = sgqlc.types.Field(Float, graphql_name="id")
    job_id = sgqlc.types.Field(Float, graphql_name="job_id")
    owner_id = sgqlc.types.Field(Float, graphql_name="owner_id")
    update_count = sgqlc.types.Field(Float, graphql_name="update_count")


class turbine_task_max_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "app_id",
        "completed",
        "created",
        "id",
        "job_id",
        "name",
        "owner_id",
        "state",
        "update_count",
        "worker_type",
    )
    app_id = sgqlc.types.Field(uuid, graphql_name="app_id")
    completed = sgqlc.types.Field(timestamptz, graphql_name="completed")
    created = sgqlc.types.Field(timestamptz, graphql_name="created")
    id = sgqlc.types.Field(bigint, graphql_name="id")
    job_id = sgqlc.types.Field(bigint, graphql_name="job_id")
    name = sgqlc.types.Field(String, graphql_name="name")
    owner_id = sgqlc.types.Field(bigint, graphql_name="owner_id")
    state = sgqlc.types.Field(String, graphql_name="state")
    update_count = sgqlc.types.Field(Int, graphql_name="update_count")
    worker_type = sgqlc.types.Field(String, graphql_name="worker_type")


class turbine_task_min_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = (
        "app_id",
        "completed",
        "created",
        "id",
        "job_id",
        "name",
        "owner_id",
        "state",
        "update_count",
        "worker_type",
    )
    app_id = sgqlc.types.Field(uuid, graphql_name="app_id")
    completed = sgqlc.types.Field(timestamptz, graphql_name="completed")
    created = sgqlc.types.Field(timestamptz, graphql_name="created")
    id = sgqlc.types.Field(bigint, graphql_name="id")
    job_id = sgqlc.types.Field(bigint, graphql_name="job_id")
    name = sgqlc.types.Field(String, graphql_name="name")
    owner_id = sgqlc.types.Field(bigint, graphql_name="owner_id")
    state = sgqlc.types.Field(String, graphql_name="state")
    update_count = sgqlc.types.Field(Int, graphql_name="update_count")
    worker_type = sgqlc.types.Field(String, graphql_name="worker_type")


class turbine_task_mutation_response(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("affected_rows", "returning")
    affected_rows = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="affected_rows")
    returning = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(turbine_task))), graphql_name="returning"
    )


class turbine_task_stddev_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "job_id", "owner_id", "update_count")
    id = sgqlc.types.Field(Float, graphql_name="id")
    job_id = sgqlc.types.Field(Float, graphql_name="job_id")
    owner_id = sgqlc.types.Field(Float, graphql_name="owner_id")
    update_count = sgqlc.types.Field(Float, graphql_name="update_count")


class turbine_task_stddev_pop_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "job_id", "owner_id", "update_count")
    id = sgqlc.types.Field(Float, graphql_name="id")
    job_id = sgqlc.types.Field(Float, graphql_name="job_id")
    owner_id = sgqlc.types.Field(Float, graphql_name="owner_id")
    update_count = sgqlc.types.Field(Float, graphql_name="update_count")


class turbine_task_stddev_samp_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "job_id", "owner_id", "update_count")
    id = sgqlc.types.Field(Float, graphql_name="id")
    job_id = sgqlc.types.Field(Float, graphql_name="job_id")
    owner_id = sgqlc.types.Field(Float, graphql_name="owner_id")
    update_count = sgqlc.types.Field(Float, graphql_name="update_count")


class turbine_task_sum_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "job_id", "owner_id", "update_count")
    id = sgqlc.types.Field(bigint, graphql_name="id")
    job_id = sgqlc.types.Field(bigint, graphql_name="job_id")
    owner_id = sgqlc.types.Field(bigint, graphql_name="owner_id")
    update_count = sgqlc.types.Field(Int, graphql_name="update_count")


class turbine_task_var_pop_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "job_id", "owner_id", "update_count")
    id = sgqlc.types.Field(Float, graphql_name="id")
    job_id = sgqlc.types.Field(Float, graphql_name="job_id")
    owner_id = sgqlc.types.Field(Float, graphql_name="owner_id")
    update_count = sgqlc.types.Field(Float, graphql_name="update_count")


class turbine_task_var_samp_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "job_id", "owner_id", "update_count")
    id = sgqlc.types.Field(Float, graphql_name="id")
    job_id = sgqlc.types.Field(Float, graphql_name="job_id")
    owner_id = sgqlc.types.Field(Float, graphql_name="owner_id")
    update_count = sgqlc.types.Field(Float, graphql_name="update_count")


class turbine_task_variance_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ("id", "job_id", "owner_id", "update_count")
    id = sgqlc.types.Field(Float, graphql_name="id")
    job_id = sgqlc.types.Field(Float, graphql_name="job_id")
    owner_id = sgqlc.types.Field(Float, graphql_name="owner_id")
    update_count = sgqlc.types.Field(Float, graphql_name="update_count")


########################################################################
# Unions
########################################################################

########################################################################
# Schema Entry Points
########################################################################
meta_ai_graphql_schema.query_type = query_root
meta_ai_graphql_schema.mutation_type = mutation_root
meta_ai_graphql_schema.subscription_type = subscription_root
