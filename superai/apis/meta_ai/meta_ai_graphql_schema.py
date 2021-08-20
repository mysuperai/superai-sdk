import sgqlc.types


meta_ai_graphql_schema = sgqlc.types.Schema()



########################################################################
# Scalars and Enumerations
########################################################################
Boolean = sgqlc.types.Boolean

Float = sgqlc.types.Float

ID = sgqlc.types.ID

class InsertMetaAiModelMutationMetaAiEnvironmentEnum(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ('DEV', 'LOCAL', 'PROD', 'SANDBOX', 'STAGING')


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
    __choices__ = ('app_modelId_id_assigned_key', 'app_pkey')


class meta_ai_app_select_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ('active', 'assigned', 'id', 'modelId', 'threshold')


class meta_ai_app_update_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ('active', 'assigned', 'id', 'modelId', 'threshold')


class meta_ai_assignment_constraint(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ('assignment_pkey',)


class meta_ai_assignment_enum(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ('ACTIVE_LEARNING', 'LABEL', 'PRELABEL')


class meta_ai_assignment_select_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ('type',)


class meta_ai_assignment_update_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ('type',)


class meta_ai_deployment_constraint(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ('deployment_pkey',)


class meta_ai_deployment_purpose_constraint(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ('deployment_purpose_pkey',)


class meta_ai_deployment_purpose_enum(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ('SERVING', 'TRAINING')


class meta_ai_deployment_purpose_select_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ('purpose',)


class meta_ai_deployment_purpose_update_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ('purpose',)


class meta_ai_deployment_select_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ('created_at', 'endpoint', 'image', 'modelId', 'ownerId', 'properties', 'purpose', 'status', 'target_status', 'type', 'updated_at')


class meta_ai_deployment_status_constraint(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ('model_status_pkey',)


class meta_ai_deployment_status_enum(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ('MAINTENANCE', 'OFFLINE', 'ONLINE', 'UNKNOWN')


class meta_ai_deployment_status_select_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ('status',)


class meta_ai_deployment_status_update_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ('status',)


class meta_ai_deployment_type_constraint(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ('deployment_type_pkey',)


class meta_ai_deployment_type_enum(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ('AWS_LAMBDA', 'AWS_SAGEMAKER')


class meta_ai_deployment_type_select_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ('name',)


class meta_ai_deployment_type_update_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ('name',)


class meta_ai_deployment_update_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ('created_at', 'endpoint', 'image', 'modelId', 'ownerId', 'properties', 'purpose', 'status', 'target_status', 'type', 'updated_at')


class meta_ai_environment_constraint(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ('environment_pkey',)


class meta_ai_environment_enum(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ('DEV', 'LOCAL', 'PROD', 'SANDBOX', 'STAGING')


class meta_ai_environment_select_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ('name',)


class meta_ai_environment_update_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ('name',)


class meta_ai_instance_constraint(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ('instance_pkey',)


class meta_ai_instance_select_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ('id', 'output', 'predictionId', 'score')


class meta_ai_instance_update_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ('id', 'output', 'predictionId', 'score')


class meta_ai_model_constraint(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ('model_name_ownerId_version_key', 'model_pkey')


class meta_ai_model_select_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ('createdAt', 'description', 'editorId', 'endpoint', 'id', 'inputSchema', 'metadata', 'modelSavePath', 'name', 'outputSchema', 'ownerId', 'stage', 'updatedAt', 'version', 'visibility', 'weightsPath')


class meta_ai_model_update_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ('createdAt', 'description', 'editorId', 'endpoint', 'id', 'inputSchema', 'metadata', 'modelSavePath', 'name', 'outputSchema', 'ownerId', 'stage', 'updatedAt', 'version', 'visibility', 'weightsPath')


class meta_ai_prediction_constraint(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ('prediction_modelId_jobId_type_taskId_key', 'prediction_pkey')


class meta_ai_prediction_select_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ('appId', 'createdAt', 'id', 'jobId', 'jobUUID', 'modelId', 'retries', 'state', 'taskId', 'type')


class meta_ai_prediction_state_constraint(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ('prediction_state_pkey',)


class meta_ai_prediction_state_enum(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ('CANCELED', 'COMPLETED', 'DELETED', 'ENQUEUED', 'EXPIRED', 'FAILED', 'INTERNAL_ERROR', 'IN_PROGRESS', 'PENDING', 'SCHEDULED', 'SUSPENDED')


class meta_ai_prediction_state_select_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ('state',)


class meta_ai_prediction_state_update_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ('state',)


class meta_ai_prediction_update_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ('appId', 'createdAt', 'id', 'jobId', 'jobUUID', 'modelId', 'retries', 'state', 'taskId', 'type')


class meta_ai_predictions_by_day_select_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ('appId', 'count', 'day', 'modelId', 'type')


class meta_ai_visibility_constraint(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ('visibility_pkey',)


class meta_ai_visibility_enum(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ('PRIVATE', 'PUBLIC')


class meta_ai_visibility_select_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ('type',)


class meta_ai_visibility_update_column(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ('type',)


class numeric(sgqlc.types.Scalar):
    __schema__ = meta_ai_graphql_schema


class order_by(sgqlc.types.Enum):
    __schema__ = meta_ai_graphql_schema
    __choices__ = ('asc', 'asc_nulls_first', 'asc_nulls_last', 'desc', 'desc_nulls_first', 'desc_nulls_last')


class timestamptz(sgqlc.types.Scalar):
    __schema__ = meta_ai_graphql_schema


class uuid(sgqlc.types.Scalar):
    __schema__ = meta_ai_graphql_schema



########################################################################
# Input Objects
########################################################################
class Boolean_comparison_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('_eq', '_gt', '_gte', '_in', '_is_null', '_lt', '_lte', '_neq', '_nin')
    _eq = sgqlc.types.Field(Boolean, graphql_name='_eq')
    _gt = sgqlc.types.Field(Boolean, graphql_name='_gt')
    _gte = sgqlc.types.Field(Boolean, graphql_name='_gte')
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(Boolean)), graphql_name='_in')
    _is_null = sgqlc.types.Field(Boolean, graphql_name='_is_null')
    _lt = sgqlc.types.Field(Boolean, graphql_name='_lt')
    _lte = sgqlc.types.Field(Boolean, graphql_name='_lte')
    _neq = sgqlc.types.Field(Boolean, graphql_name='_neq')
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(Boolean)), graphql_name='_nin')


class Int_comparison_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('_eq', '_gt', '_gte', '_in', '_is_null', '_lt', '_lte', '_neq', '_nin')
    _eq = sgqlc.types.Field(Int, graphql_name='_eq')
    _gt = sgqlc.types.Field(Int, graphql_name='_gt')
    _gte = sgqlc.types.Field(Int, graphql_name='_gte')
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(Int)), graphql_name='_in')
    _is_null = sgqlc.types.Field(Boolean, graphql_name='_is_null')
    _lt = sgqlc.types.Field(Int, graphql_name='_lt')
    _lte = sgqlc.types.Field(Int, graphql_name='_lte')
    _neq = sgqlc.types.Field(Int, graphql_name='_neq')
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(Int)), graphql_name='_nin')


class PredictionRequest(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('data', 'deployment_id', 'parameters')
    data = sgqlc.types.Field(json, graphql_name='data')
    deployment_id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name='deployment_id')
    parameters = sgqlc.types.Field(json, graphql_name='parameters')


class String_comparison_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('_eq', '_gt', '_gte', '_ilike', '_in', '_is_null', '_like', '_lt', '_lte', '_neq', '_nilike', '_nin', '_nlike', '_nsimilar', '_similar')
    _eq = sgqlc.types.Field(String, graphql_name='_eq')
    _gt = sgqlc.types.Field(String, graphql_name='_gt')
    _gte = sgqlc.types.Field(String, graphql_name='_gte')
    _ilike = sgqlc.types.Field(String, graphql_name='_ilike')
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='_in')
    _is_null = sgqlc.types.Field(Boolean, graphql_name='_is_null')
    _like = sgqlc.types.Field(String, graphql_name='_like')
    _lt = sgqlc.types.Field(String, graphql_name='_lt')
    _lte = sgqlc.types.Field(String, graphql_name='_lte')
    _neq = sgqlc.types.Field(String, graphql_name='_neq')
    _nilike = sgqlc.types.Field(String, graphql_name='_nilike')
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='_nin')
    _nlike = sgqlc.types.Field(String, graphql_name='_nlike')
    _nsimilar = sgqlc.types.Field(String, graphql_name='_nsimilar')
    _similar = sgqlc.types.Field(String, graphql_name='_similar')


class bigint_comparison_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('_eq', '_gt', '_gte', '_in', '_is_null', '_lt', '_lte', '_neq', '_nin')
    _eq = sgqlc.types.Field(bigint, graphql_name='_eq')
    _gt = sgqlc.types.Field(bigint, graphql_name='_gt')
    _gte = sgqlc.types.Field(bigint, graphql_name='_gte')
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(bigint)), graphql_name='_in')
    _is_null = sgqlc.types.Field(Boolean, graphql_name='_is_null')
    _lt = sgqlc.types.Field(bigint, graphql_name='_lt')
    _lte = sgqlc.types.Field(bigint, graphql_name='_lte')
    _neq = sgqlc.types.Field(bigint, graphql_name='_neq')
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(bigint)), graphql_name='_nin')


class date_comparison_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('_eq', '_gt', '_gte', '_in', '_is_null', '_lt', '_lte', '_neq', '_nin')
    _eq = sgqlc.types.Field(date, graphql_name='_eq')
    _gt = sgqlc.types.Field(date, graphql_name='_gt')
    _gte = sgqlc.types.Field(date, graphql_name='_gte')
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(date)), graphql_name='_in')
    _is_null = sgqlc.types.Field(Boolean, graphql_name='_is_null')
    _lt = sgqlc.types.Field(date, graphql_name='_lt')
    _lte = sgqlc.types.Field(date, graphql_name='_lte')
    _neq = sgqlc.types.Field(date, graphql_name='_neq')
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(date)), graphql_name='_nin')


class float8_comparison_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('_eq', '_gt', '_gte', '_in', '_is_null', '_lt', '_lte', '_neq', '_nin')
    _eq = sgqlc.types.Field(float8, graphql_name='_eq')
    _gt = sgqlc.types.Field(float8, graphql_name='_gt')
    _gte = sgqlc.types.Field(float8, graphql_name='_gte')
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(float8)), graphql_name='_in')
    _is_null = sgqlc.types.Field(Boolean, graphql_name='_is_null')
    _lt = sgqlc.types.Field(float8, graphql_name='_lt')
    _lte = sgqlc.types.Field(float8, graphql_name='_lte')
    _neq = sgqlc.types.Field(float8, graphql_name='_neq')
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(float8)), graphql_name='_nin')


class json_comparison_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('_eq', '_gt', '_gte', '_in', '_is_null', '_lt', '_lte', '_neq', '_nin')
    _eq = sgqlc.types.Field(json, graphql_name='_eq')
    _gt = sgqlc.types.Field(json, graphql_name='_gt')
    _gte = sgqlc.types.Field(json, graphql_name='_gte')
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(json)), graphql_name='_in')
    _is_null = sgqlc.types.Field(Boolean, graphql_name='_is_null')
    _lt = sgqlc.types.Field(json, graphql_name='_lt')
    _lte = sgqlc.types.Field(json, graphql_name='_lte')
    _neq = sgqlc.types.Field(json, graphql_name='_neq')
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(json)), graphql_name='_nin')


class jsonb_comparison_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('_contained_in', '_contains', '_eq', '_gt', '_gte', '_has_key', '_has_keys_all', '_has_keys_any', '_in', '_is_null', '_lt', '_lte', '_neq', '_nin')
    _contained_in = sgqlc.types.Field(jsonb, graphql_name='_contained_in')
    _contains = sgqlc.types.Field(jsonb, graphql_name='_contains')
    _eq = sgqlc.types.Field(jsonb, graphql_name='_eq')
    _gt = sgqlc.types.Field(jsonb, graphql_name='_gt')
    _gte = sgqlc.types.Field(jsonb, graphql_name='_gte')
    _has_key = sgqlc.types.Field(String, graphql_name='_has_key')
    _has_keys_all = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='_has_keys_all')
    _has_keys_any = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='_has_keys_any')
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(jsonb)), graphql_name='_in')
    _is_null = sgqlc.types.Field(Boolean, graphql_name='_is_null')
    _lt = sgqlc.types.Field(jsonb, graphql_name='_lt')
    _lte = sgqlc.types.Field(jsonb, graphql_name='_lte')
    _neq = sgqlc.types.Field(jsonb, graphql_name='_neq')
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(jsonb)), graphql_name='_nin')


class meta_ai_app_aggregate_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('avg', 'count', 'max', 'min', 'stddev', 'stddev_pop', 'stddev_samp', 'sum', 'var_pop', 'var_samp', 'variance')
    avg = sgqlc.types.Field('meta_ai_app_avg_order_by', graphql_name='avg')
    count = sgqlc.types.Field(order_by, graphql_name='count')
    max = sgqlc.types.Field('meta_ai_app_max_order_by', graphql_name='max')
    min = sgqlc.types.Field('meta_ai_app_min_order_by', graphql_name='min')
    stddev = sgqlc.types.Field('meta_ai_app_stddev_order_by', graphql_name='stddev')
    stddev_pop = sgqlc.types.Field('meta_ai_app_stddev_pop_order_by', graphql_name='stddev_pop')
    stddev_samp = sgqlc.types.Field('meta_ai_app_stddev_samp_order_by', graphql_name='stddev_samp')
    sum = sgqlc.types.Field('meta_ai_app_sum_order_by', graphql_name='sum')
    var_pop = sgqlc.types.Field('meta_ai_app_var_pop_order_by', graphql_name='var_pop')
    var_samp = sgqlc.types.Field('meta_ai_app_var_samp_order_by', graphql_name='var_samp')
    variance = sgqlc.types.Field('meta_ai_app_variance_order_by', graphql_name='variance')


class meta_ai_app_arr_rel_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('data', 'on_conflict')
    data = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('meta_ai_app_insert_input'))), graphql_name='data')
    on_conflict = sgqlc.types.Field('meta_ai_app_on_conflict', graphql_name='on_conflict')


class meta_ai_app_avg_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('threshold',)
    threshold = sgqlc.types.Field(order_by, graphql_name='threshold')


class meta_ai_app_bool_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('_and', '_not', '_or', 'active', 'assigned', 'id', 'model', 'model_id', 'predictions', 'statistics', 'threshold')
    _and = sgqlc.types.Field(sgqlc.types.list_of('meta_ai_app_bool_exp'), graphql_name='_and')
    _not = sgqlc.types.Field('meta_ai_app_bool_exp', graphql_name='_not')
    _or = sgqlc.types.Field(sgqlc.types.list_of('meta_ai_app_bool_exp'), graphql_name='_or')
    active = sgqlc.types.Field(Boolean_comparison_exp, graphql_name='active')
    assigned = sgqlc.types.Field('meta_ai_assignment_enum_comparison_exp', graphql_name='assigned')
    id = sgqlc.types.Field('uuid_comparison_exp', graphql_name='id')
    model = sgqlc.types.Field('meta_ai_model_bool_exp', graphql_name='model')
    model_id = sgqlc.types.Field('uuid_comparison_exp', graphql_name='modelId')
    predictions = sgqlc.types.Field('meta_ai_prediction_bool_exp', graphql_name='predictions')
    statistics = sgqlc.types.Field('meta_ai_predictions_by_day_bool_exp', graphql_name='statistics')
    threshold = sgqlc.types.Field('numeric_comparison_exp', graphql_name='threshold')


class meta_ai_app_inc_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('threshold',)
    threshold = sgqlc.types.Field(numeric, graphql_name='threshold')


class meta_ai_app_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('active', 'assigned', 'id', 'model', 'model_id', 'predictions', 'threshold')
    active = sgqlc.types.Field(Boolean, graphql_name='active')
    assigned = sgqlc.types.Field(meta_ai_assignment_enum, graphql_name='assigned')
    id = sgqlc.types.Field(uuid, graphql_name='id')
    model = sgqlc.types.Field('meta_ai_model_obj_rel_insert_input', graphql_name='model')
    model_id = sgqlc.types.Field(uuid, graphql_name='modelId')
    predictions = sgqlc.types.Field('meta_ai_prediction_arr_rel_insert_input', graphql_name='predictions')
    threshold = sgqlc.types.Field(numeric, graphql_name='threshold')


class meta_ai_app_max_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('id', 'model_id', 'threshold')
    id = sgqlc.types.Field(order_by, graphql_name='id')
    model_id = sgqlc.types.Field(order_by, graphql_name='modelId')
    threshold = sgqlc.types.Field(order_by, graphql_name='threshold')


class meta_ai_app_min_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('id', 'model_id', 'threshold')
    id = sgqlc.types.Field(order_by, graphql_name='id')
    model_id = sgqlc.types.Field(order_by, graphql_name='modelId')
    threshold = sgqlc.types.Field(order_by, graphql_name='threshold')


class meta_ai_app_obj_rel_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('data', 'on_conflict')
    data = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_app_insert_input), graphql_name='data')
    on_conflict = sgqlc.types.Field('meta_ai_app_on_conflict', graphql_name='on_conflict')


class meta_ai_app_on_conflict(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('constraint', 'update_columns', 'where')
    constraint = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_app_constraint), graphql_name='constraint')
    update_columns = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_app_update_column))), graphql_name='update_columns')
    where = sgqlc.types.Field(meta_ai_app_bool_exp, graphql_name='where')


class meta_ai_app_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('active', 'assigned', 'id', 'model', 'model_id', 'predictions_aggregate', 'statistics_aggregate', 'threshold')
    active = sgqlc.types.Field(order_by, graphql_name='active')
    assigned = sgqlc.types.Field(order_by, graphql_name='assigned')
    id = sgqlc.types.Field(order_by, graphql_name='id')
    model = sgqlc.types.Field('meta_ai_model_order_by', graphql_name='model')
    model_id = sgqlc.types.Field(order_by, graphql_name='modelId')
    predictions_aggregate = sgqlc.types.Field('meta_ai_prediction_aggregate_order_by', graphql_name='predictions_aggregate')
    statistics_aggregate = sgqlc.types.Field('meta_ai_predictions_by_day_aggregate_order_by', graphql_name='statistics_aggregate')
    threshold = sgqlc.types.Field(order_by, graphql_name='threshold')


class meta_ai_app_pk_columns_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('assigned', 'id', 'model_id')
    assigned = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_assignment_enum), graphql_name='assigned')
    id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name='id')
    model_id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name='modelId')


class meta_ai_app_set_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('active', 'assigned', 'id', 'model_id', 'threshold')
    active = sgqlc.types.Field(Boolean, graphql_name='active')
    assigned = sgqlc.types.Field(meta_ai_assignment_enum, graphql_name='assigned')
    id = sgqlc.types.Field(uuid, graphql_name='id')
    model_id = sgqlc.types.Field(uuid, graphql_name='modelId')
    threshold = sgqlc.types.Field(numeric, graphql_name='threshold')


class meta_ai_app_stddev_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('threshold',)
    threshold = sgqlc.types.Field(order_by, graphql_name='threshold')


class meta_ai_app_stddev_pop_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('threshold',)
    threshold = sgqlc.types.Field(order_by, graphql_name='threshold')


class meta_ai_app_stddev_samp_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('threshold',)
    threshold = sgqlc.types.Field(order_by, graphql_name='threshold')


class meta_ai_app_sum_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('threshold',)
    threshold = sgqlc.types.Field(order_by, graphql_name='threshold')


class meta_ai_app_var_pop_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('threshold',)
    threshold = sgqlc.types.Field(order_by, graphql_name='threshold')


class meta_ai_app_var_samp_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('threshold',)
    threshold = sgqlc.types.Field(order_by, graphql_name='threshold')


class meta_ai_app_variance_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('threshold',)
    threshold = sgqlc.types.Field(order_by, graphql_name='threshold')


class meta_ai_assignment_aggregate_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('count', 'max', 'min')
    count = sgqlc.types.Field(order_by, graphql_name='count')
    max = sgqlc.types.Field('meta_ai_assignment_max_order_by', graphql_name='max')
    min = sgqlc.types.Field('meta_ai_assignment_min_order_by', graphql_name='min')


class meta_ai_assignment_arr_rel_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('data', 'on_conflict')
    data = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('meta_ai_assignment_insert_input'))), graphql_name='data')
    on_conflict = sgqlc.types.Field('meta_ai_assignment_on_conflict', graphql_name='on_conflict')


class meta_ai_assignment_bool_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('_and', '_not', '_or', 'apps', 'type')
    _and = sgqlc.types.Field(sgqlc.types.list_of('meta_ai_assignment_bool_exp'), graphql_name='_and')
    _not = sgqlc.types.Field('meta_ai_assignment_bool_exp', graphql_name='_not')
    _or = sgqlc.types.Field(sgqlc.types.list_of('meta_ai_assignment_bool_exp'), graphql_name='_or')
    apps = sgqlc.types.Field(meta_ai_app_bool_exp, graphql_name='apps')
    type = sgqlc.types.Field(String_comparison_exp, graphql_name='type')


class meta_ai_assignment_enum_comparison_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('_eq', '_in', '_is_null', '_neq', '_nin')
    _eq = sgqlc.types.Field(meta_ai_assignment_enum, graphql_name='_eq')
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_assignment_enum)), graphql_name='_in')
    _is_null = sgqlc.types.Field(Boolean, graphql_name='_is_null')
    _neq = sgqlc.types.Field(meta_ai_assignment_enum, graphql_name='_neq')
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_assignment_enum)), graphql_name='_nin')


class meta_ai_assignment_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('apps', 'type')
    apps = sgqlc.types.Field(meta_ai_app_arr_rel_insert_input, graphql_name='apps')
    type = sgqlc.types.Field(String, graphql_name='type')


class meta_ai_assignment_max_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('type',)
    type = sgqlc.types.Field(order_by, graphql_name='type')


class meta_ai_assignment_min_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('type',)
    type = sgqlc.types.Field(order_by, graphql_name='type')


class meta_ai_assignment_obj_rel_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('data', 'on_conflict')
    data = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_assignment_insert_input), graphql_name='data')
    on_conflict = sgqlc.types.Field('meta_ai_assignment_on_conflict', graphql_name='on_conflict')


class meta_ai_assignment_on_conflict(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('constraint', 'update_columns', 'where')
    constraint = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_assignment_constraint), graphql_name='constraint')
    update_columns = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_assignment_update_column))), graphql_name='update_columns')
    where = sgqlc.types.Field(meta_ai_assignment_bool_exp, graphql_name='where')


class meta_ai_assignment_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('apps_aggregate', 'type')
    apps_aggregate = sgqlc.types.Field(meta_ai_app_aggregate_order_by, graphql_name='apps_aggregate')
    type = sgqlc.types.Field(order_by, graphql_name='type')


class meta_ai_assignment_pk_columns_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('type',)
    type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='type')


class meta_ai_assignment_set_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('type',)
    type = sgqlc.types.Field(String, graphql_name='type')


class meta_ai_deployment_aggregate_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('avg', 'count', 'max', 'min', 'stddev', 'stddev_pop', 'stddev_samp', 'sum', 'var_pop', 'var_samp', 'variance')
    avg = sgqlc.types.Field('meta_ai_deployment_avg_order_by', graphql_name='avg')
    count = sgqlc.types.Field(order_by, graphql_name='count')
    max = sgqlc.types.Field('meta_ai_deployment_max_order_by', graphql_name='max')
    min = sgqlc.types.Field('meta_ai_deployment_min_order_by', graphql_name='min')
    stddev = sgqlc.types.Field('meta_ai_deployment_stddev_order_by', graphql_name='stddev')
    stddev_pop = sgqlc.types.Field('meta_ai_deployment_stddev_pop_order_by', graphql_name='stddev_pop')
    stddev_samp = sgqlc.types.Field('meta_ai_deployment_stddev_samp_order_by', graphql_name='stddev_samp')
    sum = sgqlc.types.Field('meta_ai_deployment_sum_order_by', graphql_name='sum')
    var_pop = sgqlc.types.Field('meta_ai_deployment_var_pop_order_by', graphql_name='var_pop')
    var_samp = sgqlc.types.Field('meta_ai_deployment_var_samp_order_by', graphql_name='var_samp')
    variance = sgqlc.types.Field('meta_ai_deployment_variance_order_by', graphql_name='variance')


class meta_ai_deployment_append_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('properties',)
    properties = sgqlc.types.Field(jsonb, graphql_name='properties')


class meta_ai_deployment_arr_rel_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('data', 'on_conflict')
    data = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('meta_ai_deployment_insert_input'))), graphql_name='data')
    on_conflict = sgqlc.types.Field('meta_ai_deployment_on_conflict', graphql_name='on_conflict')


class meta_ai_deployment_avg_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('owner_id',)
    owner_id = sgqlc.types.Field(order_by, graphql_name='ownerId')


class meta_ai_deployment_bool_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('_and', '_not', '_or', 'created_at', 'endpoint', 'image', 'model', 'model_id', 'owner_id', 'properties', 'purpose', 'status', 'target_status', 'type', 'updated_at')
    _and = sgqlc.types.Field(sgqlc.types.list_of('meta_ai_deployment_bool_exp'), graphql_name='_and')
    _not = sgqlc.types.Field('meta_ai_deployment_bool_exp', graphql_name='_not')
    _or = sgqlc.types.Field(sgqlc.types.list_of('meta_ai_deployment_bool_exp'), graphql_name='_or')
    created_at = sgqlc.types.Field('timestamptz_comparison_exp', graphql_name='created_at')
    endpoint = sgqlc.types.Field(String_comparison_exp, graphql_name='endpoint')
    image = sgqlc.types.Field(String_comparison_exp, graphql_name='image')
    model = sgqlc.types.Field('meta_ai_model_bool_exp', graphql_name='model')
    model_id = sgqlc.types.Field('uuid_comparison_exp', graphql_name='modelId')
    owner_id = sgqlc.types.Field(bigint_comparison_exp, graphql_name='ownerId')
    properties = sgqlc.types.Field(jsonb_comparison_exp, graphql_name='properties')
    purpose = sgqlc.types.Field('meta_ai_deployment_purpose_enum_comparison_exp', graphql_name='purpose')
    status = sgqlc.types.Field('meta_ai_deployment_status_enum_comparison_exp', graphql_name='status')
    target_status = sgqlc.types.Field('meta_ai_deployment_status_enum_comparison_exp', graphql_name='target_status')
    type = sgqlc.types.Field('meta_ai_deployment_type_enum_comparison_exp', graphql_name='type')
    updated_at = sgqlc.types.Field('timestamptz_comparison_exp', graphql_name='updated_at')


class meta_ai_deployment_delete_at_path_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('properties',)
    properties = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='properties')


class meta_ai_deployment_delete_elem_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('properties',)
    properties = sgqlc.types.Field(Int, graphql_name='properties')


class meta_ai_deployment_delete_key_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('properties',)
    properties = sgqlc.types.Field(String, graphql_name='properties')


class meta_ai_deployment_inc_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('owner_id',)
    owner_id = sgqlc.types.Field(bigint, graphql_name='ownerId')


class meta_ai_deployment_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('created_at', 'endpoint', 'image', 'model', 'model_id', 'owner_id', 'properties', 'purpose', 'status', 'target_status', 'type', 'updated_at')
    created_at = sgqlc.types.Field(timestamptz, graphql_name='created_at')
    endpoint = sgqlc.types.Field(String, graphql_name='endpoint')
    image = sgqlc.types.Field(String, graphql_name='image')
    model = sgqlc.types.Field('meta_ai_model_obj_rel_insert_input', graphql_name='model')
    model_id = sgqlc.types.Field(uuid, graphql_name='modelId')
    owner_id = sgqlc.types.Field(bigint, graphql_name='ownerId')
    properties = sgqlc.types.Field(jsonb, graphql_name='properties')
    purpose = sgqlc.types.Field(meta_ai_deployment_purpose_enum, graphql_name='purpose')
    status = sgqlc.types.Field(meta_ai_deployment_status_enum, graphql_name='status')
    target_status = sgqlc.types.Field(meta_ai_deployment_status_enum, graphql_name='target_status')
    type = sgqlc.types.Field(meta_ai_deployment_type_enum, graphql_name='type')
    updated_at = sgqlc.types.Field(timestamptz, graphql_name='updated_at')


class meta_ai_deployment_max_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('created_at', 'endpoint', 'image', 'model_id', 'owner_id', 'updated_at')
    created_at = sgqlc.types.Field(order_by, graphql_name='created_at')
    endpoint = sgqlc.types.Field(order_by, graphql_name='endpoint')
    image = sgqlc.types.Field(order_by, graphql_name='image')
    model_id = sgqlc.types.Field(order_by, graphql_name='modelId')
    owner_id = sgqlc.types.Field(order_by, graphql_name='ownerId')
    updated_at = sgqlc.types.Field(order_by, graphql_name='updated_at')


class meta_ai_deployment_min_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('created_at', 'endpoint', 'image', 'model_id', 'owner_id', 'updated_at')
    created_at = sgqlc.types.Field(order_by, graphql_name='created_at')
    endpoint = sgqlc.types.Field(order_by, graphql_name='endpoint')
    image = sgqlc.types.Field(order_by, graphql_name='image')
    model_id = sgqlc.types.Field(order_by, graphql_name='modelId')
    owner_id = sgqlc.types.Field(order_by, graphql_name='ownerId')
    updated_at = sgqlc.types.Field(order_by, graphql_name='updated_at')


class meta_ai_deployment_obj_rel_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('data', 'on_conflict')
    data = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_deployment_insert_input), graphql_name='data')
    on_conflict = sgqlc.types.Field('meta_ai_deployment_on_conflict', graphql_name='on_conflict')


class meta_ai_deployment_on_conflict(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('constraint', 'update_columns', 'where')
    constraint = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_deployment_constraint), graphql_name='constraint')
    update_columns = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_update_column))), graphql_name='update_columns')
    where = sgqlc.types.Field(meta_ai_deployment_bool_exp, graphql_name='where')


class meta_ai_deployment_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('created_at', 'endpoint', 'image', 'model', 'model_id', 'owner_id', 'properties', 'purpose', 'status', 'target_status', 'type', 'updated_at')
    created_at = sgqlc.types.Field(order_by, graphql_name='created_at')
    endpoint = sgqlc.types.Field(order_by, graphql_name='endpoint')
    image = sgqlc.types.Field(order_by, graphql_name='image')
    model = sgqlc.types.Field('meta_ai_model_order_by', graphql_name='model')
    model_id = sgqlc.types.Field(order_by, graphql_name='modelId')
    owner_id = sgqlc.types.Field(order_by, graphql_name='ownerId')
    properties = sgqlc.types.Field(order_by, graphql_name='properties')
    purpose = sgqlc.types.Field(order_by, graphql_name='purpose')
    status = sgqlc.types.Field(order_by, graphql_name='status')
    target_status = sgqlc.types.Field(order_by, graphql_name='target_status')
    type = sgqlc.types.Field(order_by, graphql_name='type')
    updated_at = sgqlc.types.Field(order_by, graphql_name='updated_at')


class meta_ai_deployment_pk_columns_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('model_id',)
    model_id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name='modelId')


class meta_ai_deployment_prepend_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('properties',)
    properties = sgqlc.types.Field(jsonb, graphql_name='properties')


class meta_ai_deployment_purpose_aggregate_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('count', 'max', 'min')
    count = sgqlc.types.Field(order_by, graphql_name='count')
    max = sgqlc.types.Field('meta_ai_deployment_purpose_max_order_by', graphql_name='max')
    min = sgqlc.types.Field('meta_ai_deployment_purpose_min_order_by', graphql_name='min')


class meta_ai_deployment_purpose_arr_rel_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('data', 'on_conflict')
    data = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('meta_ai_deployment_purpose_insert_input'))), graphql_name='data')
    on_conflict = sgqlc.types.Field('meta_ai_deployment_purpose_on_conflict', graphql_name='on_conflict')


class meta_ai_deployment_purpose_bool_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('_and', '_not', '_or', 'deployments', 'purpose')
    _and = sgqlc.types.Field(sgqlc.types.list_of('meta_ai_deployment_purpose_bool_exp'), graphql_name='_and')
    _not = sgqlc.types.Field('meta_ai_deployment_purpose_bool_exp', graphql_name='_not')
    _or = sgqlc.types.Field(sgqlc.types.list_of('meta_ai_deployment_purpose_bool_exp'), graphql_name='_or')
    deployments = sgqlc.types.Field(meta_ai_deployment_bool_exp, graphql_name='deployments')
    purpose = sgqlc.types.Field(String_comparison_exp, graphql_name='purpose')


class meta_ai_deployment_purpose_enum_comparison_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('_eq', '_in', '_is_null', '_neq', '_nin')
    _eq = sgqlc.types.Field(meta_ai_deployment_purpose_enum, graphql_name='_eq')
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_purpose_enum)), graphql_name='_in')
    _is_null = sgqlc.types.Field(Boolean, graphql_name='_is_null')
    _neq = sgqlc.types.Field(meta_ai_deployment_purpose_enum, graphql_name='_neq')
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_purpose_enum)), graphql_name='_nin')


class meta_ai_deployment_purpose_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('deployments', 'purpose')
    deployments = sgqlc.types.Field(meta_ai_deployment_arr_rel_insert_input, graphql_name='deployments')
    purpose = sgqlc.types.Field(String, graphql_name='purpose')


class meta_ai_deployment_purpose_max_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('purpose',)
    purpose = sgqlc.types.Field(order_by, graphql_name='purpose')


class meta_ai_deployment_purpose_min_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('purpose',)
    purpose = sgqlc.types.Field(order_by, graphql_name='purpose')


class meta_ai_deployment_purpose_obj_rel_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('data', 'on_conflict')
    data = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_deployment_purpose_insert_input), graphql_name='data')
    on_conflict = sgqlc.types.Field('meta_ai_deployment_purpose_on_conflict', graphql_name='on_conflict')


class meta_ai_deployment_purpose_on_conflict(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('constraint', 'update_columns', 'where')
    constraint = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_deployment_purpose_constraint), graphql_name='constraint')
    update_columns = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_purpose_update_column))), graphql_name='update_columns')
    where = sgqlc.types.Field(meta_ai_deployment_purpose_bool_exp, graphql_name='where')


class meta_ai_deployment_purpose_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('deployments_aggregate', 'purpose')
    deployments_aggregate = sgqlc.types.Field(meta_ai_deployment_aggregate_order_by, graphql_name='deployments_aggregate')
    purpose = sgqlc.types.Field(order_by, graphql_name='purpose')


class meta_ai_deployment_purpose_pk_columns_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('purpose',)
    purpose = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='purpose')


class meta_ai_deployment_purpose_set_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('purpose',)
    purpose = sgqlc.types.Field(String, graphql_name='purpose')


class meta_ai_deployment_set_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('created_at', 'endpoint', 'image', 'model_id', 'owner_id', 'properties', 'purpose', 'status', 'target_status', 'type', 'updated_at')
    created_at = sgqlc.types.Field(timestamptz, graphql_name='created_at')
    endpoint = sgqlc.types.Field(String, graphql_name='endpoint')
    image = sgqlc.types.Field(String, graphql_name='image')
    model_id = sgqlc.types.Field(uuid, graphql_name='modelId')
    owner_id = sgqlc.types.Field(bigint, graphql_name='ownerId')
    properties = sgqlc.types.Field(jsonb, graphql_name='properties')
    purpose = sgqlc.types.Field(meta_ai_deployment_purpose_enum, graphql_name='purpose')
    status = sgqlc.types.Field(meta_ai_deployment_status_enum, graphql_name='status')
    target_status = sgqlc.types.Field(meta_ai_deployment_status_enum, graphql_name='target_status')
    type = sgqlc.types.Field(meta_ai_deployment_type_enum, graphql_name='type')
    updated_at = sgqlc.types.Field(timestamptz, graphql_name='updated_at')


class meta_ai_deployment_status_aggregate_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('count', 'max', 'min')
    count = sgqlc.types.Field(order_by, graphql_name='count')
    max = sgqlc.types.Field('meta_ai_deployment_status_max_order_by', graphql_name='max')
    min = sgqlc.types.Field('meta_ai_deployment_status_min_order_by', graphql_name='min')


class meta_ai_deployment_status_arr_rel_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('data', 'on_conflict')
    data = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('meta_ai_deployment_status_insert_input'))), graphql_name='data')
    on_conflict = sgqlc.types.Field('meta_ai_deployment_status_on_conflict', graphql_name='on_conflict')


class meta_ai_deployment_status_bool_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('_and', '_not', '_or', 'deployments', 'deployments_by_target_status', 'status')
    _and = sgqlc.types.Field(sgqlc.types.list_of('meta_ai_deployment_status_bool_exp'), graphql_name='_and')
    _not = sgqlc.types.Field('meta_ai_deployment_status_bool_exp', graphql_name='_not')
    _or = sgqlc.types.Field(sgqlc.types.list_of('meta_ai_deployment_status_bool_exp'), graphql_name='_or')
    deployments = sgqlc.types.Field(meta_ai_deployment_bool_exp, graphql_name='deployments')
    deployments_by_target_status = sgqlc.types.Field(meta_ai_deployment_bool_exp, graphql_name='deploymentsByTargetStatus')
    status = sgqlc.types.Field(String_comparison_exp, graphql_name='status')


class meta_ai_deployment_status_enum_comparison_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('_eq', '_in', '_is_null', '_neq', '_nin')
    _eq = sgqlc.types.Field(meta_ai_deployment_status_enum, graphql_name='_eq')
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_status_enum)), graphql_name='_in')
    _is_null = sgqlc.types.Field(Boolean, graphql_name='_is_null')
    _neq = sgqlc.types.Field(meta_ai_deployment_status_enum, graphql_name='_neq')
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_status_enum)), graphql_name='_nin')


class meta_ai_deployment_status_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('deployments', 'deployments_by_target_status', 'status')
    deployments = sgqlc.types.Field(meta_ai_deployment_arr_rel_insert_input, graphql_name='deployments')
    deployments_by_target_status = sgqlc.types.Field(meta_ai_deployment_arr_rel_insert_input, graphql_name='deploymentsByTargetStatus')
    status = sgqlc.types.Field(String, graphql_name='status')


class meta_ai_deployment_status_max_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('status',)
    status = sgqlc.types.Field(order_by, graphql_name='status')


class meta_ai_deployment_status_min_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('status',)
    status = sgqlc.types.Field(order_by, graphql_name='status')


class meta_ai_deployment_status_obj_rel_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('data', 'on_conflict')
    data = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_deployment_status_insert_input), graphql_name='data')
    on_conflict = sgqlc.types.Field('meta_ai_deployment_status_on_conflict', graphql_name='on_conflict')


class meta_ai_deployment_status_on_conflict(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('constraint', 'update_columns', 'where')
    constraint = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_deployment_status_constraint), graphql_name='constraint')
    update_columns = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_status_update_column))), graphql_name='update_columns')
    where = sgqlc.types.Field(meta_ai_deployment_status_bool_exp, graphql_name='where')


class meta_ai_deployment_status_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('deployments_by_target_status_aggregate', 'deployments_aggregate', 'status')
    deployments_by_target_status_aggregate = sgqlc.types.Field(meta_ai_deployment_aggregate_order_by, graphql_name='deploymentsByTargetStatus_aggregate')
    deployments_aggregate = sgqlc.types.Field(meta_ai_deployment_aggregate_order_by, graphql_name='deployments_aggregate')
    status = sgqlc.types.Field(order_by, graphql_name='status')


class meta_ai_deployment_status_pk_columns_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('status',)
    status = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='status')


class meta_ai_deployment_status_set_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('status',)
    status = sgqlc.types.Field(String, graphql_name='status')


class meta_ai_deployment_stddev_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('owner_id',)
    owner_id = sgqlc.types.Field(order_by, graphql_name='ownerId')


class meta_ai_deployment_stddev_pop_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('owner_id',)
    owner_id = sgqlc.types.Field(order_by, graphql_name='ownerId')


class meta_ai_deployment_stddev_samp_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('owner_id',)
    owner_id = sgqlc.types.Field(order_by, graphql_name='ownerId')


class meta_ai_deployment_sum_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('owner_id',)
    owner_id = sgqlc.types.Field(order_by, graphql_name='ownerId')


class meta_ai_deployment_type_aggregate_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('count', 'max', 'min')
    count = sgqlc.types.Field(order_by, graphql_name='count')
    max = sgqlc.types.Field('meta_ai_deployment_type_max_order_by', graphql_name='max')
    min = sgqlc.types.Field('meta_ai_deployment_type_min_order_by', graphql_name='min')


class meta_ai_deployment_type_arr_rel_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('data', 'on_conflict')
    data = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('meta_ai_deployment_type_insert_input'))), graphql_name='data')
    on_conflict = sgqlc.types.Field('meta_ai_deployment_type_on_conflict', graphql_name='on_conflict')


class meta_ai_deployment_type_bool_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('_and', '_not', '_or', 'deployments', 'name')
    _and = sgqlc.types.Field(sgqlc.types.list_of('meta_ai_deployment_type_bool_exp'), graphql_name='_and')
    _not = sgqlc.types.Field('meta_ai_deployment_type_bool_exp', graphql_name='_not')
    _or = sgqlc.types.Field(sgqlc.types.list_of('meta_ai_deployment_type_bool_exp'), graphql_name='_or')
    deployments = sgqlc.types.Field(meta_ai_deployment_bool_exp, graphql_name='deployments')
    name = sgqlc.types.Field(String_comparison_exp, graphql_name='name')


class meta_ai_deployment_type_enum_comparison_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('_eq', '_in', '_is_null', '_neq', '_nin')
    _eq = sgqlc.types.Field(meta_ai_deployment_type_enum, graphql_name='_eq')
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_type_enum)), graphql_name='_in')
    _is_null = sgqlc.types.Field(Boolean, graphql_name='_is_null')
    _neq = sgqlc.types.Field(meta_ai_deployment_type_enum, graphql_name='_neq')
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_type_enum)), graphql_name='_nin')


class meta_ai_deployment_type_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('deployments', 'name')
    deployments = sgqlc.types.Field(meta_ai_deployment_arr_rel_insert_input, graphql_name='deployments')
    name = sgqlc.types.Field(String, graphql_name='name')


class meta_ai_deployment_type_max_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('name',)
    name = sgqlc.types.Field(order_by, graphql_name='name')


class meta_ai_deployment_type_min_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('name',)
    name = sgqlc.types.Field(order_by, graphql_name='name')


class meta_ai_deployment_type_obj_rel_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('data', 'on_conflict')
    data = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_deployment_type_insert_input), graphql_name='data')
    on_conflict = sgqlc.types.Field('meta_ai_deployment_type_on_conflict', graphql_name='on_conflict')


class meta_ai_deployment_type_on_conflict(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('constraint', 'update_columns', 'where')
    constraint = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_deployment_type_constraint), graphql_name='constraint')
    update_columns = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_type_update_column))), graphql_name='update_columns')
    where = sgqlc.types.Field(meta_ai_deployment_type_bool_exp, graphql_name='where')


class meta_ai_deployment_type_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('deployments_aggregate', 'name')
    deployments_aggregate = sgqlc.types.Field(meta_ai_deployment_aggregate_order_by, graphql_name='deployments_aggregate')
    name = sgqlc.types.Field(order_by, graphql_name='name')


class meta_ai_deployment_type_pk_columns_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('name',)
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')


class meta_ai_deployment_type_set_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('name',)
    name = sgqlc.types.Field(String, graphql_name='name')


class meta_ai_deployment_var_pop_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('owner_id',)
    owner_id = sgqlc.types.Field(order_by, graphql_name='ownerId')


class meta_ai_deployment_var_samp_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('owner_id',)
    owner_id = sgqlc.types.Field(order_by, graphql_name='ownerId')


class meta_ai_deployment_variance_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('owner_id',)
    owner_id = sgqlc.types.Field(order_by, graphql_name='ownerId')


class meta_ai_environment_aggregate_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('count', 'max', 'min')
    count = sgqlc.types.Field(order_by, graphql_name='count')
    max = sgqlc.types.Field('meta_ai_environment_max_order_by', graphql_name='max')
    min = sgqlc.types.Field('meta_ai_environment_min_order_by', graphql_name='min')


class meta_ai_environment_arr_rel_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('data', 'on_conflict')
    data = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('meta_ai_environment_insert_input'))), graphql_name='data')
    on_conflict = sgqlc.types.Field('meta_ai_environment_on_conflict', graphql_name='on_conflict')


class meta_ai_environment_bool_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('_and', '_not', '_or', 'name')
    _and = sgqlc.types.Field(sgqlc.types.list_of('meta_ai_environment_bool_exp'), graphql_name='_and')
    _not = sgqlc.types.Field('meta_ai_environment_bool_exp', graphql_name='_not')
    _or = sgqlc.types.Field(sgqlc.types.list_of('meta_ai_environment_bool_exp'), graphql_name='_or')
    name = sgqlc.types.Field(String_comparison_exp, graphql_name='name')


class meta_ai_environment_enum_comparison_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('_eq', '_in', '_is_null', '_neq', '_nin')
    _eq = sgqlc.types.Field(meta_ai_environment_enum, graphql_name='_eq')
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_environment_enum)), graphql_name='_in')
    _is_null = sgqlc.types.Field(Boolean, graphql_name='_is_null')
    _neq = sgqlc.types.Field(meta_ai_environment_enum, graphql_name='_neq')
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_environment_enum)), graphql_name='_nin')


class meta_ai_environment_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('name',)
    name = sgqlc.types.Field(String, graphql_name='name')


class meta_ai_environment_max_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('name',)
    name = sgqlc.types.Field(order_by, graphql_name='name')


class meta_ai_environment_min_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('name',)
    name = sgqlc.types.Field(order_by, graphql_name='name')


class meta_ai_environment_obj_rel_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('data', 'on_conflict')
    data = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_environment_insert_input), graphql_name='data')
    on_conflict = sgqlc.types.Field('meta_ai_environment_on_conflict', graphql_name='on_conflict')


class meta_ai_environment_on_conflict(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('constraint', 'update_columns', 'where')
    constraint = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_environment_constraint), graphql_name='constraint')
    update_columns = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_environment_update_column))), graphql_name='update_columns')
    where = sgqlc.types.Field(meta_ai_environment_bool_exp, graphql_name='where')


class meta_ai_environment_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('name',)
    name = sgqlc.types.Field(order_by, graphql_name='name')


class meta_ai_environment_pk_columns_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('name',)
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')


class meta_ai_environment_set_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('name',)
    name = sgqlc.types.Field(String, graphql_name='name')


class meta_ai_instance_aggregate_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('avg', 'count', 'max', 'min', 'stddev', 'stddev_pop', 'stddev_samp', 'sum', 'var_pop', 'var_samp', 'variance')
    avg = sgqlc.types.Field('meta_ai_instance_avg_order_by', graphql_name='avg')
    count = sgqlc.types.Field(order_by, graphql_name='count')
    max = sgqlc.types.Field('meta_ai_instance_max_order_by', graphql_name='max')
    min = sgqlc.types.Field('meta_ai_instance_min_order_by', graphql_name='min')
    stddev = sgqlc.types.Field('meta_ai_instance_stddev_order_by', graphql_name='stddev')
    stddev_pop = sgqlc.types.Field('meta_ai_instance_stddev_pop_order_by', graphql_name='stddev_pop')
    stddev_samp = sgqlc.types.Field('meta_ai_instance_stddev_samp_order_by', graphql_name='stddev_samp')
    sum = sgqlc.types.Field('meta_ai_instance_sum_order_by', graphql_name='sum')
    var_pop = sgqlc.types.Field('meta_ai_instance_var_pop_order_by', graphql_name='var_pop')
    var_samp = sgqlc.types.Field('meta_ai_instance_var_samp_order_by', graphql_name='var_samp')
    variance = sgqlc.types.Field('meta_ai_instance_variance_order_by', graphql_name='variance')


class meta_ai_instance_append_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('output',)
    output = sgqlc.types.Field(jsonb, graphql_name='output')


class meta_ai_instance_arr_rel_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('data', 'on_conflict')
    data = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('meta_ai_instance_insert_input'))), graphql_name='data')
    on_conflict = sgqlc.types.Field('meta_ai_instance_on_conflict', graphql_name='on_conflict')


class meta_ai_instance_avg_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('id', 'score')
    id = sgqlc.types.Field(order_by, graphql_name='id')
    score = sgqlc.types.Field(order_by, graphql_name='score')


class meta_ai_instance_bool_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('_and', '_not', '_or', 'id', 'output', 'prediction', 'prediction_id', 'score')
    _and = sgqlc.types.Field(sgqlc.types.list_of('meta_ai_instance_bool_exp'), graphql_name='_and')
    _not = sgqlc.types.Field('meta_ai_instance_bool_exp', graphql_name='_not')
    _or = sgqlc.types.Field(sgqlc.types.list_of('meta_ai_instance_bool_exp'), graphql_name='_or')
    id = sgqlc.types.Field(Int_comparison_exp, graphql_name='id')
    output = sgqlc.types.Field(jsonb_comparison_exp, graphql_name='output')
    prediction = sgqlc.types.Field('meta_ai_prediction_bool_exp', graphql_name='prediction')
    prediction_id = sgqlc.types.Field('uuid_comparison_exp', graphql_name='predictionId')
    score = sgqlc.types.Field(float8_comparison_exp, graphql_name='score')


class meta_ai_instance_delete_at_path_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('output',)
    output = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='output')


class meta_ai_instance_delete_elem_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('output',)
    output = sgqlc.types.Field(Int, graphql_name='output')


class meta_ai_instance_delete_key_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('output',)
    output = sgqlc.types.Field(String, graphql_name='output')


class meta_ai_instance_inc_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('id', 'score')
    id = sgqlc.types.Field(Int, graphql_name='id')
    score = sgqlc.types.Field(float8, graphql_name='score')


class meta_ai_instance_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('id', 'output', 'prediction', 'prediction_id', 'score')
    id = sgqlc.types.Field(Int, graphql_name='id')
    output = sgqlc.types.Field(jsonb, graphql_name='output')
    prediction = sgqlc.types.Field('meta_ai_prediction_obj_rel_insert_input', graphql_name='prediction')
    prediction_id = sgqlc.types.Field(uuid, graphql_name='predictionId')
    score = sgqlc.types.Field(float8, graphql_name='score')


class meta_ai_instance_max_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('id', 'prediction_id', 'score')
    id = sgqlc.types.Field(order_by, graphql_name='id')
    prediction_id = sgqlc.types.Field(order_by, graphql_name='predictionId')
    score = sgqlc.types.Field(order_by, graphql_name='score')


class meta_ai_instance_min_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('id', 'prediction_id', 'score')
    id = sgqlc.types.Field(order_by, graphql_name='id')
    prediction_id = sgqlc.types.Field(order_by, graphql_name='predictionId')
    score = sgqlc.types.Field(order_by, graphql_name='score')


class meta_ai_instance_obj_rel_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('data', 'on_conflict')
    data = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_instance_insert_input), graphql_name='data')
    on_conflict = sgqlc.types.Field('meta_ai_instance_on_conflict', graphql_name='on_conflict')


class meta_ai_instance_on_conflict(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('constraint', 'update_columns', 'where')
    constraint = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_instance_constraint), graphql_name='constraint')
    update_columns = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_instance_update_column))), graphql_name='update_columns')
    where = sgqlc.types.Field(meta_ai_instance_bool_exp, graphql_name='where')


class meta_ai_instance_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('id', 'output', 'prediction', 'prediction_id', 'score')
    id = sgqlc.types.Field(order_by, graphql_name='id')
    output = sgqlc.types.Field(order_by, graphql_name='output')
    prediction = sgqlc.types.Field('meta_ai_prediction_order_by', graphql_name='prediction')
    prediction_id = sgqlc.types.Field(order_by, graphql_name='predictionId')
    score = sgqlc.types.Field(order_by, graphql_name='score')


class meta_ai_instance_pk_columns_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('id', 'prediction_id')
    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='id')
    prediction_id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name='predictionId')


class meta_ai_instance_prepend_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('output',)
    output = sgqlc.types.Field(jsonb, graphql_name='output')


class meta_ai_instance_set_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('id', 'output', 'prediction_id', 'score')
    id = sgqlc.types.Field(Int, graphql_name='id')
    output = sgqlc.types.Field(jsonb, graphql_name='output')
    prediction_id = sgqlc.types.Field(uuid, graphql_name='predictionId')
    score = sgqlc.types.Field(float8, graphql_name='score')


class meta_ai_instance_stddev_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('id', 'score')
    id = sgqlc.types.Field(order_by, graphql_name='id')
    score = sgqlc.types.Field(order_by, graphql_name='score')


class meta_ai_instance_stddev_pop_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('id', 'score')
    id = sgqlc.types.Field(order_by, graphql_name='id')
    score = sgqlc.types.Field(order_by, graphql_name='score')


class meta_ai_instance_stddev_samp_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('id', 'score')
    id = sgqlc.types.Field(order_by, graphql_name='id')
    score = sgqlc.types.Field(order_by, graphql_name='score')


class meta_ai_instance_sum_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('id', 'score')
    id = sgqlc.types.Field(order_by, graphql_name='id')
    score = sgqlc.types.Field(order_by, graphql_name='score')


class meta_ai_instance_var_pop_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('id', 'score')
    id = sgqlc.types.Field(order_by, graphql_name='id')
    score = sgqlc.types.Field(order_by, graphql_name='score')


class meta_ai_instance_var_samp_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('id', 'score')
    id = sgqlc.types.Field(order_by, graphql_name='id')
    score = sgqlc.types.Field(order_by, graphql_name='score')


class meta_ai_instance_variance_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('id', 'score')
    id = sgqlc.types.Field(order_by, graphql_name='id')
    score = sgqlc.types.Field(order_by, graphql_name='score')


class meta_ai_model_aggregate_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('avg', 'count', 'max', 'min', 'stddev', 'stddev_pop', 'stddev_samp', 'sum', 'var_pop', 'var_samp', 'variance')
    avg = sgqlc.types.Field('meta_ai_model_avg_order_by', graphql_name='avg')
    count = sgqlc.types.Field(order_by, graphql_name='count')
    max = sgqlc.types.Field('meta_ai_model_max_order_by', graphql_name='max')
    min = sgqlc.types.Field('meta_ai_model_min_order_by', graphql_name='min')
    stddev = sgqlc.types.Field('meta_ai_model_stddev_order_by', graphql_name='stddev')
    stddev_pop = sgqlc.types.Field('meta_ai_model_stddev_pop_order_by', graphql_name='stddev_pop')
    stddev_samp = sgqlc.types.Field('meta_ai_model_stddev_samp_order_by', graphql_name='stddev_samp')
    sum = sgqlc.types.Field('meta_ai_model_sum_order_by', graphql_name='sum')
    var_pop = sgqlc.types.Field('meta_ai_model_var_pop_order_by', graphql_name='var_pop')
    var_samp = sgqlc.types.Field('meta_ai_model_var_samp_order_by', graphql_name='var_samp')
    variance = sgqlc.types.Field('meta_ai_model_variance_order_by', graphql_name='variance')


class meta_ai_model_append_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('input_schema', 'metadata', 'output_schema')
    input_schema = sgqlc.types.Field(jsonb, graphql_name='inputSchema')
    metadata = sgqlc.types.Field(jsonb, graphql_name='metadata')
    output_schema = sgqlc.types.Field(jsonb, graphql_name='outputSchema')


class meta_ai_model_arr_rel_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('data', 'on_conflict')
    data = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('meta_ai_model_insert_input'))), graphql_name='data')
    on_conflict = sgqlc.types.Field('meta_ai_model_on_conflict', graphql_name='on_conflict')


class meta_ai_model_avg_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('editor_id', 'owner_id', 'version')
    editor_id = sgqlc.types.Field(order_by, graphql_name='editorId')
    owner_id = sgqlc.types.Field(order_by, graphql_name='ownerId')
    version = sgqlc.types.Field(order_by, graphql_name='version')


class meta_ai_model_bool_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('_and', '_not', '_or', 'apps', 'created_at', 'deployment', 'description', 'editor_id', 'endpoint', 'id', 'input_schema', 'metadata', 'model_save_path', 'name', 'output_schema', 'owner_id', 'predictions', 'stage', 'updated_at', 'version', 'visibility', 'weights_path')
    _and = sgqlc.types.Field(sgqlc.types.list_of('meta_ai_model_bool_exp'), graphql_name='_and')
    _not = sgqlc.types.Field('meta_ai_model_bool_exp', graphql_name='_not')
    _or = sgqlc.types.Field(sgqlc.types.list_of('meta_ai_model_bool_exp'), graphql_name='_or')
    apps = sgqlc.types.Field(meta_ai_app_bool_exp, graphql_name='apps')
    created_at = sgqlc.types.Field('timestamptz_comparison_exp', graphql_name='createdAt')
    deployment = sgqlc.types.Field(meta_ai_deployment_bool_exp, graphql_name='deployment')
    description = sgqlc.types.Field(String_comparison_exp, graphql_name='description')
    editor_id = sgqlc.types.Field(bigint_comparison_exp, graphql_name='editorId')
    endpoint = sgqlc.types.Field(String_comparison_exp, graphql_name='endpoint')
    id = sgqlc.types.Field('uuid_comparison_exp', graphql_name='id')
    input_schema = sgqlc.types.Field(jsonb_comparison_exp, graphql_name='inputSchema')
    metadata = sgqlc.types.Field(jsonb_comparison_exp, graphql_name='metadata')
    model_save_path = sgqlc.types.Field(String_comparison_exp, graphql_name='modelSavePath')
    name = sgqlc.types.Field(String_comparison_exp, graphql_name='name')
    output_schema = sgqlc.types.Field(jsonb_comparison_exp, graphql_name='outputSchema')
    owner_id = sgqlc.types.Field(bigint_comparison_exp, graphql_name='ownerId')
    predictions = sgqlc.types.Field('meta_ai_prediction_bool_exp', graphql_name='predictions')
    stage = sgqlc.types.Field(meta_ai_environment_enum_comparison_exp, graphql_name='stage')
    updated_at = sgqlc.types.Field('timestamptz_comparison_exp', graphql_name='updatedAt')
    version = sgqlc.types.Field(Int_comparison_exp, graphql_name='version')
    visibility = sgqlc.types.Field('meta_ai_visibility_enum_comparison_exp', graphql_name='visibility')
    weights_path = sgqlc.types.Field(String_comparison_exp, graphql_name='weightsPath')


class meta_ai_model_delete_at_path_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('input_schema', 'metadata', 'output_schema')
    input_schema = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='inputSchema')
    metadata = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='metadata')
    output_schema = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='outputSchema')


class meta_ai_model_delete_elem_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('input_schema', 'metadata', 'output_schema')
    input_schema = sgqlc.types.Field(Int, graphql_name='inputSchema')
    metadata = sgqlc.types.Field(Int, graphql_name='metadata')
    output_schema = sgqlc.types.Field(Int, graphql_name='outputSchema')


class meta_ai_model_delete_key_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('input_schema', 'metadata', 'output_schema')
    input_schema = sgqlc.types.Field(String, graphql_name='inputSchema')
    metadata = sgqlc.types.Field(String, graphql_name='metadata')
    output_schema = sgqlc.types.Field(String, graphql_name='outputSchema')


class meta_ai_model_inc_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('editor_id', 'owner_id', 'version')
    editor_id = sgqlc.types.Field(bigint, graphql_name='editorId')
    owner_id = sgqlc.types.Field(bigint, graphql_name='ownerId')
    version = sgqlc.types.Field(Int, graphql_name='version')


class meta_ai_model_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('apps', 'created_at', 'deployment', 'description', 'editor_id', 'endpoint', 'id', 'input_schema', 'metadata', 'model_save_path', 'name', 'output_schema', 'owner_id', 'predictions', 'stage', 'updated_at', 'version', 'visibility', 'weights_path')
    apps = sgqlc.types.Field(meta_ai_app_arr_rel_insert_input, graphql_name='apps')
    created_at = sgqlc.types.Field(timestamptz, graphql_name='createdAt')
    deployment = sgqlc.types.Field(meta_ai_deployment_obj_rel_insert_input, graphql_name='deployment')
    description = sgqlc.types.Field(String, graphql_name='description')
    editor_id = sgqlc.types.Field(bigint, graphql_name='editorId')
    endpoint = sgqlc.types.Field(String, graphql_name='endpoint')
    id = sgqlc.types.Field(uuid, graphql_name='id')
    input_schema = sgqlc.types.Field(jsonb, graphql_name='inputSchema')
    metadata = sgqlc.types.Field(jsonb, graphql_name='metadata')
    model_save_path = sgqlc.types.Field(String, graphql_name='modelSavePath')
    name = sgqlc.types.Field(String, graphql_name='name')
    output_schema = sgqlc.types.Field(jsonb, graphql_name='outputSchema')
    owner_id = sgqlc.types.Field(bigint, graphql_name='ownerId')
    predictions = sgqlc.types.Field('meta_ai_prediction_arr_rel_insert_input', graphql_name='predictions')
    stage = sgqlc.types.Field(meta_ai_environment_enum, graphql_name='stage')
    updated_at = sgqlc.types.Field(timestamptz, graphql_name='updatedAt')
    version = sgqlc.types.Field(Int, graphql_name='version')
    visibility = sgqlc.types.Field(meta_ai_visibility_enum, graphql_name='visibility')
    weights_path = sgqlc.types.Field(String, graphql_name='weightsPath')


class meta_ai_model_max_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('created_at', 'description', 'editor_id', 'endpoint', 'id', 'model_save_path', 'name', 'owner_id', 'updated_at', 'version', 'weights_path')
    created_at = sgqlc.types.Field(order_by, graphql_name='createdAt')
    description = sgqlc.types.Field(order_by, graphql_name='description')
    editor_id = sgqlc.types.Field(order_by, graphql_name='editorId')
    endpoint = sgqlc.types.Field(order_by, graphql_name='endpoint')
    id = sgqlc.types.Field(order_by, graphql_name='id')
    model_save_path = sgqlc.types.Field(order_by, graphql_name='modelSavePath')
    name = sgqlc.types.Field(order_by, graphql_name='name')
    owner_id = sgqlc.types.Field(order_by, graphql_name='ownerId')
    updated_at = sgqlc.types.Field(order_by, graphql_name='updatedAt')
    version = sgqlc.types.Field(order_by, graphql_name='version')
    weights_path = sgqlc.types.Field(order_by, graphql_name='weightsPath')


class meta_ai_model_min_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('created_at', 'description', 'editor_id', 'endpoint', 'id', 'model_save_path', 'name', 'owner_id', 'updated_at', 'version', 'weights_path')
    created_at = sgqlc.types.Field(order_by, graphql_name='createdAt')
    description = sgqlc.types.Field(order_by, graphql_name='description')
    editor_id = sgqlc.types.Field(order_by, graphql_name='editorId')
    endpoint = sgqlc.types.Field(order_by, graphql_name='endpoint')
    id = sgqlc.types.Field(order_by, graphql_name='id')
    model_save_path = sgqlc.types.Field(order_by, graphql_name='modelSavePath')
    name = sgqlc.types.Field(order_by, graphql_name='name')
    owner_id = sgqlc.types.Field(order_by, graphql_name='ownerId')
    updated_at = sgqlc.types.Field(order_by, graphql_name='updatedAt')
    version = sgqlc.types.Field(order_by, graphql_name='version')
    weights_path = sgqlc.types.Field(order_by, graphql_name='weightsPath')


class meta_ai_model_obj_rel_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('data', 'on_conflict')
    data = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_model_insert_input), graphql_name='data')
    on_conflict = sgqlc.types.Field('meta_ai_model_on_conflict', graphql_name='on_conflict')


class meta_ai_model_on_conflict(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('constraint', 'update_columns', 'where')
    constraint = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_model_constraint), graphql_name='constraint')
    update_columns = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_model_update_column))), graphql_name='update_columns')
    where = sgqlc.types.Field(meta_ai_model_bool_exp, graphql_name='where')


class meta_ai_model_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('apps_aggregate', 'created_at', 'deployment', 'description', 'editor_id', 'endpoint', 'id', 'input_schema', 'metadata', 'model_save_path', 'name', 'output_schema', 'owner_id', 'predictions_aggregate', 'stage', 'updated_at', 'version', 'visibility', 'weights_path')
    apps_aggregate = sgqlc.types.Field(meta_ai_app_aggregate_order_by, graphql_name='apps_aggregate')
    created_at = sgqlc.types.Field(order_by, graphql_name='createdAt')
    deployment = sgqlc.types.Field(meta_ai_deployment_order_by, graphql_name='deployment')
    description = sgqlc.types.Field(order_by, graphql_name='description')
    editor_id = sgqlc.types.Field(order_by, graphql_name='editorId')
    endpoint = sgqlc.types.Field(order_by, graphql_name='endpoint')
    id = sgqlc.types.Field(order_by, graphql_name='id')
    input_schema = sgqlc.types.Field(order_by, graphql_name='inputSchema')
    metadata = sgqlc.types.Field(order_by, graphql_name='metadata')
    model_save_path = sgqlc.types.Field(order_by, graphql_name='modelSavePath')
    name = sgqlc.types.Field(order_by, graphql_name='name')
    output_schema = sgqlc.types.Field(order_by, graphql_name='outputSchema')
    owner_id = sgqlc.types.Field(order_by, graphql_name='ownerId')
    predictions_aggregate = sgqlc.types.Field('meta_ai_prediction_aggregate_order_by', graphql_name='predictions_aggregate')
    stage = sgqlc.types.Field(order_by, graphql_name='stage')
    updated_at = sgqlc.types.Field(order_by, graphql_name='updatedAt')
    version = sgqlc.types.Field(order_by, graphql_name='version')
    visibility = sgqlc.types.Field(order_by, graphql_name='visibility')
    weights_path = sgqlc.types.Field(order_by, graphql_name='weightsPath')


class meta_ai_model_pk_columns_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('id',)
    id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name='id')


class meta_ai_model_prepend_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('input_schema', 'metadata', 'output_schema')
    input_schema = sgqlc.types.Field(jsonb, graphql_name='inputSchema')
    metadata = sgqlc.types.Field(jsonb, graphql_name='metadata')
    output_schema = sgqlc.types.Field(jsonb, graphql_name='outputSchema')


class meta_ai_model_set_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('created_at', 'description', 'editor_id', 'endpoint', 'id', 'input_schema', 'metadata', 'model_save_path', 'name', 'output_schema', 'owner_id', 'stage', 'updated_at', 'version', 'visibility', 'weights_path')
    created_at = sgqlc.types.Field(timestamptz, graphql_name='createdAt')
    description = sgqlc.types.Field(String, graphql_name='description')
    editor_id = sgqlc.types.Field(bigint, graphql_name='editorId')
    endpoint = sgqlc.types.Field(String, graphql_name='endpoint')
    id = sgqlc.types.Field(uuid, graphql_name='id')
    input_schema = sgqlc.types.Field(jsonb, graphql_name='inputSchema')
    metadata = sgqlc.types.Field(jsonb, graphql_name='metadata')
    model_save_path = sgqlc.types.Field(String, graphql_name='modelSavePath')
    name = sgqlc.types.Field(String, graphql_name='name')
    output_schema = sgqlc.types.Field(jsonb, graphql_name='outputSchema')
    owner_id = sgqlc.types.Field(bigint, graphql_name='ownerId')
    stage = sgqlc.types.Field(meta_ai_environment_enum, graphql_name='stage')
    updated_at = sgqlc.types.Field(timestamptz, graphql_name='updatedAt')
    version = sgqlc.types.Field(Int, graphql_name='version')
    visibility = sgqlc.types.Field(meta_ai_visibility_enum, graphql_name='visibility')
    weights_path = sgqlc.types.Field(String, graphql_name='weightsPath')


class meta_ai_model_stddev_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('editor_id', 'owner_id', 'version')
    editor_id = sgqlc.types.Field(order_by, graphql_name='editorId')
    owner_id = sgqlc.types.Field(order_by, graphql_name='ownerId')
    version = sgqlc.types.Field(order_by, graphql_name='version')


class meta_ai_model_stddev_pop_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('editor_id', 'owner_id', 'version')
    editor_id = sgqlc.types.Field(order_by, graphql_name='editorId')
    owner_id = sgqlc.types.Field(order_by, graphql_name='ownerId')
    version = sgqlc.types.Field(order_by, graphql_name='version')


class meta_ai_model_stddev_samp_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('editor_id', 'owner_id', 'version')
    editor_id = sgqlc.types.Field(order_by, graphql_name='editorId')
    owner_id = sgqlc.types.Field(order_by, graphql_name='ownerId')
    version = sgqlc.types.Field(order_by, graphql_name='version')


class meta_ai_model_sum_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('editor_id', 'owner_id', 'version')
    editor_id = sgqlc.types.Field(order_by, graphql_name='editorId')
    owner_id = sgqlc.types.Field(order_by, graphql_name='ownerId')
    version = sgqlc.types.Field(order_by, graphql_name='version')


class meta_ai_model_var_pop_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('editor_id', 'owner_id', 'version')
    editor_id = sgqlc.types.Field(order_by, graphql_name='editorId')
    owner_id = sgqlc.types.Field(order_by, graphql_name='ownerId')
    version = sgqlc.types.Field(order_by, graphql_name='version')


class meta_ai_model_var_samp_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('editor_id', 'owner_id', 'version')
    editor_id = sgqlc.types.Field(order_by, graphql_name='editorId')
    owner_id = sgqlc.types.Field(order_by, graphql_name='ownerId')
    version = sgqlc.types.Field(order_by, graphql_name='version')


class meta_ai_model_variance_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('editor_id', 'owner_id', 'version')
    editor_id = sgqlc.types.Field(order_by, graphql_name='editorId')
    owner_id = sgqlc.types.Field(order_by, graphql_name='ownerId')
    version = sgqlc.types.Field(order_by, graphql_name='version')


class meta_ai_prediction_aggregate_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('avg', 'count', 'max', 'min', 'stddev', 'stddev_pop', 'stddev_samp', 'sum', 'var_pop', 'var_samp', 'variance')
    avg = sgqlc.types.Field('meta_ai_prediction_avg_order_by', graphql_name='avg')
    count = sgqlc.types.Field(order_by, graphql_name='count')
    max = sgqlc.types.Field('meta_ai_prediction_max_order_by', graphql_name='max')
    min = sgqlc.types.Field('meta_ai_prediction_min_order_by', graphql_name='min')
    stddev = sgqlc.types.Field('meta_ai_prediction_stddev_order_by', graphql_name='stddev')
    stddev_pop = sgqlc.types.Field('meta_ai_prediction_stddev_pop_order_by', graphql_name='stddev_pop')
    stddev_samp = sgqlc.types.Field('meta_ai_prediction_stddev_samp_order_by', graphql_name='stddev_samp')
    sum = sgqlc.types.Field('meta_ai_prediction_sum_order_by', graphql_name='sum')
    var_pop = sgqlc.types.Field('meta_ai_prediction_var_pop_order_by', graphql_name='var_pop')
    var_samp = sgqlc.types.Field('meta_ai_prediction_var_samp_order_by', graphql_name='var_samp')
    variance = sgqlc.types.Field('meta_ai_prediction_variance_order_by', graphql_name='variance')


class meta_ai_prediction_arr_rel_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('data', 'on_conflict')
    data = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('meta_ai_prediction_insert_input'))), graphql_name='data')
    on_conflict = sgqlc.types.Field('meta_ai_prediction_on_conflict', graphql_name='on_conflict')


class meta_ai_prediction_avg_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('job_id', 'retries', 'task_id')
    job_id = sgqlc.types.Field(order_by, graphql_name='jobId')
    retries = sgqlc.types.Field(order_by, graphql_name='retries')
    task_id = sgqlc.types.Field(order_by, graphql_name='taskId')


class meta_ai_prediction_bool_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('_and', '_not', '_or', 'app_id', 'created_at', 'id', 'instances', 'job_id', 'job_uuid', 'model', 'model_id', 'retries', 'state', 'task_id', 'type')
    _and = sgqlc.types.Field(sgqlc.types.list_of('meta_ai_prediction_bool_exp'), graphql_name='_and')
    _not = sgqlc.types.Field('meta_ai_prediction_bool_exp', graphql_name='_not')
    _or = sgqlc.types.Field(sgqlc.types.list_of('meta_ai_prediction_bool_exp'), graphql_name='_or')
    app_id = sgqlc.types.Field('uuid_comparison_exp', graphql_name='appId')
    created_at = sgqlc.types.Field('timestamptz_comparison_exp', graphql_name='createdAt')
    id = sgqlc.types.Field('uuid_comparison_exp', graphql_name='id')
    instances = sgqlc.types.Field(meta_ai_instance_bool_exp, graphql_name='instances')
    job_id = sgqlc.types.Field(bigint_comparison_exp, graphql_name='jobId')
    job_uuid = sgqlc.types.Field('uuid_comparison_exp', graphql_name='jobUUID')
    model = sgqlc.types.Field(meta_ai_model_bool_exp, graphql_name='model')
    model_id = sgqlc.types.Field('uuid_comparison_exp', graphql_name='modelId')
    retries = sgqlc.types.Field(Int_comparison_exp, graphql_name='retries')
    state = sgqlc.types.Field('meta_ai_prediction_state_enum_comparison_exp', graphql_name='state')
    task_id = sgqlc.types.Field(bigint_comparison_exp, graphql_name='taskId')
    type = sgqlc.types.Field(meta_ai_assignment_enum_comparison_exp, graphql_name='type')


class meta_ai_prediction_inc_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('job_id', 'retries', 'task_id')
    job_id = sgqlc.types.Field(bigint, graphql_name='jobId')
    retries = sgqlc.types.Field(Int, graphql_name='retries')
    task_id = sgqlc.types.Field(bigint, graphql_name='taskId')


class meta_ai_prediction_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('app_id', 'created_at', 'id', 'instances', 'job_id', 'job_uuid', 'model', 'model_id', 'retries', 'state', 'task_id', 'type')
    app_id = sgqlc.types.Field(uuid, graphql_name='appId')
    created_at = sgqlc.types.Field(timestamptz, graphql_name='createdAt')
    id = sgqlc.types.Field(uuid, graphql_name='id')
    instances = sgqlc.types.Field(meta_ai_instance_arr_rel_insert_input, graphql_name='instances')
    job_id = sgqlc.types.Field(bigint, graphql_name='jobId')
    job_uuid = sgqlc.types.Field(uuid, graphql_name='jobUUID')
    model = sgqlc.types.Field(meta_ai_model_obj_rel_insert_input, graphql_name='model')
    model_id = sgqlc.types.Field(uuid, graphql_name='modelId')
    retries = sgqlc.types.Field(Int, graphql_name='retries')
    state = sgqlc.types.Field(meta_ai_prediction_state_enum, graphql_name='state')
    task_id = sgqlc.types.Field(bigint, graphql_name='taskId')
    type = sgqlc.types.Field(meta_ai_assignment_enum, graphql_name='type')


class meta_ai_prediction_max_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('app_id', 'created_at', 'id', 'job_id', 'job_uuid', 'model_id', 'retries', 'task_id')
    app_id = sgqlc.types.Field(order_by, graphql_name='appId')
    created_at = sgqlc.types.Field(order_by, graphql_name='createdAt')
    id = sgqlc.types.Field(order_by, graphql_name='id')
    job_id = sgqlc.types.Field(order_by, graphql_name='jobId')
    job_uuid = sgqlc.types.Field(order_by, graphql_name='jobUUID')
    model_id = sgqlc.types.Field(order_by, graphql_name='modelId')
    retries = sgqlc.types.Field(order_by, graphql_name='retries')
    task_id = sgqlc.types.Field(order_by, graphql_name='taskId')


class meta_ai_prediction_min_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('app_id', 'created_at', 'id', 'job_id', 'job_uuid', 'model_id', 'retries', 'task_id')
    app_id = sgqlc.types.Field(order_by, graphql_name='appId')
    created_at = sgqlc.types.Field(order_by, graphql_name='createdAt')
    id = sgqlc.types.Field(order_by, graphql_name='id')
    job_id = sgqlc.types.Field(order_by, graphql_name='jobId')
    job_uuid = sgqlc.types.Field(order_by, graphql_name='jobUUID')
    model_id = sgqlc.types.Field(order_by, graphql_name='modelId')
    retries = sgqlc.types.Field(order_by, graphql_name='retries')
    task_id = sgqlc.types.Field(order_by, graphql_name='taskId')


class meta_ai_prediction_obj_rel_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('data', 'on_conflict')
    data = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_prediction_insert_input), graphql_name='data')
    on_conflict = sgqlc.types.Field('meta_ai_prediction_on_conflict', graphql_name='on_conflict')


class meta_ai_prediction_on_conflict(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('constraint', 'update_columns', 'where')
    constraint = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_prediction_constraint), graphql_name='constraint')
    update_columns = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_update_column))), graphql_name='update_columns')
    where = sgqlc.types.Field(meta_ai_prediction_bool_exp, graphql_name='where')


class meta_ai_prediction_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('app_id', 'created_at', 'id', 'instances_aggregate', 'job_id', 'job_uuid', 'model', 'model_id', 'retries', 'state', 'task_id', 'type')
    app_id = sgqlc.types.Field(order_by, graphql_name='appId')
    created_at = sgqlc.types.Field(order_by, graphql_name='createdAt')
    id = sgqlc.types.Field(order_by, graphql_name='id')
    instances_aggregate = sgqlc.types.Field(meta_ai_instance_aggregate_order_by, graphql_name='instances_aggregate')
    job_id = sgqlc.types.Field(order_by, graphql_name='jobId')
    job_uuid = sgqlc.types.Field(order_by, graphql_name='jobUUID')
    model = sgqlc.types.Field(meta_ai_model_order_by, graphql_name='model')
    model_id = sgqlc.types.Field(order_by, graphql_name='modelId')
    retries = sgqlc.types.Field(order_by, graphql_name='retries')
    state = sgqlc.types.Field(order_by, graphql_name='state')
    task_id = sgqlc.types.Field(order_by, graphql_name='taskId')
    type = sgqlc.types.Field(order_by, graphql_name='type')


class meta_ai_prediction_pk_columns_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('id',)
    id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name='id')


class meta_ai_prediction_set_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('app_id', 'created_at', 'id', 'job_id', 'job_uuid', 'model_id', 'retries', 'state', 'task_id', 'type')
    app_id = sgqlc.types.Field(uuid, graphql_name='appId')
    created_at = sgqlc.types.Field(timestamptz, graphql_name='createdAt')
    id = sgqlc.types.Field(uuid, graphql_name='id')
    job_id = sgqlc.types.Field(bigint, graphql_name='jobId')
    job_uuid = sgqlc.types.Field(uuid, graphql_name='jobUUID')
    model_id = sgqlc.types.Field(uuid, graphql_name='modelId')
    retries = sgqlc.types.Field(Int, graphql_name='retries')
    state = sgqlc.types.Field(meta_ai_prediction_state_enum, graphql_name='state')
    task_id = sgqlc.types.Field(bigint, graphql_name='taskId')
    type = sgqlc.types.Field(meta_ai_assignment_enum, graphql_name='type')


class meta_ai_prediction_state_aggregate_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('count', 'max', 'min')
    count = sgqlc.types.Field(order_by, graphql_name='count')
    max = sgqlc.types.Field('meta_ai_prediction_state_max_order_by', graphql_name='max')
    min = sgqlc.types.Field('meta_ai_prediction_state_min_order_by', graphql_name='min')


class meta_ai_prediction_state_arr_rel_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('data', 'on_conflict')
    data = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('meta_ai_prediction_state_insert_input'))), graphql_name='data')
    on_conflict = sgqlc.types.Field('meta_ai_prediction_state_on_conflict', graphql_name='on_conflict')


class meta_ai_prediction_state_bool_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('_and', '_not', '_or', 'predictions', 'state')
    _and = sgqlc.types.Field(sgqlc.types.list_of('meta_ai_prediction_state_bool_exp'), graphql_name='_and')
    _not = sgqlc.types.Field('meta_ai_prediction_state_bool_exp', graphql_name='_not')
    _or = sgqlc.types.Field(sgqlc.types.list_of('meta_ai_prediction_state_bool_exp'), graphql_name='_or')
    predictions = sgqlc.types.Field(meta_ai_prediction_bool_exp, graphql_name='predictions')
    state = sgqlc.types.Field(String_comparison_exp, graphql_name='state')


class meta_ai_prediction_state_enum_comparison_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('_eq', '_in', '_is_null', '_neq', '_nin')
    _eq = sgqlc.types.Field(meta_ai_prediction_state_enum, graphql_name='_eq')
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_state_enum)), graphql_name='_in')
    _is_null = sgqlc.types.Field(Boolean, graphql_name='_is_null')
    _neq = sgqlc.types.Field(meta_ai_prediction_state_enum, graphql_name='_neq')
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_state_enum)), graphql_name='_nin')


class meta_ai_prediction_state_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('predictions', 'state')
    predictions = sgqlc.types.Field(meta_ai_prediction_arr_rel_insert_input, graphql_name='predictions')
    state = sgqlc.types.Field(String, graphql_name='state')


class meta_ai_prediction_state_max_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('state',)
    state = sgqlc.types.Field(order_by, graphql_name='state')


class meta_ai_prediction_state_min_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('state',)
    state = sgqlc.types.Field(order_by, graphql_name='state')


class meta_ai_prediction_state_obj_rel_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('data', 'on_conflict')
    data = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_prediction_state_insert_input), graphql_name='data')
    on_conflict = sgqlc.types.Field('meta_ai_prediction_state_on_conflict', graphql_name='on_conflict')


class meta_ai_prediction_state_on_conflict(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('constraint', 'update_columns', 'where')
    constraint = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_prediction_state_constraint), graphql_name='constraint')
    update_columns = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_state_update_column))), graphql_name='update_columns')
    where = sgqlc.types.Field(meta_ai_prediction_state_bool_exp, graphql_name='where')


class meta_ai_prediction_state_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('predictions_aggregate', 'state')
    predictions_aggregate = sgqlc.types.Field(meta_ai_prediction_aggregate_order_by, graphql_name='predictions_aggregate')
    state = sgqlc.types.Field(order_by, graphql_name='state')


class meta_ai_prediction_state_pk_columns_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('state',)
    state = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='state')


class meta_ai_prediction_state_set_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('state',)
    state = sgqlc.types.Field(String, graphql_name='state')


class meta_ai_prediction_stddev_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('job_id', 'retries', 'task_id')
    job_id = sgqlc.types.Field(order_by, graphql_name='jobId')
    retries = sgqlc.types.Field(order_by, graphql_name='retries')
    task_id = sgqlc.types.Field(order_by, graphql_name='taskId')


class meta_ai_prediction_stddev_pop_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('job_id', 'retries', 'task_id')
    job_id = sgqlc.types.Field(order_by, graphql_name='jobId')
    retries = sgqlc.types.Field(order_by, graphql_name='retries')
    task_id = sgqlc.types.Field(order_by, graphql_name='taskId')


class meta_ai_prediction_stddev_samp_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('job_id', 'retries', 'task_id')
    job_id = sgqlc.types.Field(order_by, graphql_name='jobId')
    retries = sgqlc.types.Field(order_by, graphql_name='retries')
    task_id = sgqlc.types.Field(order_by, graphql_name='taskId')


class meta_ai_prediction_sum_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('job_id', 'retries', 'task_id')
    job_id = sgqlc.types.Field(order_by, graphql_name='jobId')
    retries = sgqlc.types.Field(order_by, graphql_name='retries')
    task_id = sgqlc.types.Field(order_by, graphql_name='taskId')


class meta_ai_prediction_var_pop_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('job_id', 'retries', 'task_id')
    job_id = sgqlc.types.Field(order_by, graphql_name='jobId')
    retries = sgqlc.types.Field(order_by, graphql_name='retries')
    task_id = sgqlc.types.Field(order_by, graphql_name='taskId')


class meta_ai_prediction_var_samp_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('job_id', 'retries', 'task_id')
    job_id = sgqlc.types.Field(order_by, graphql_name='jobId')
    retries = sgqlc.types.Field(order_by, graphql_name='retries')
    task_id = sgqlc.types.Field(order_by, graphql_name='taskId')


class meta_ai_prediction_variance_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('job_id', 'retries', 'task_id')
    job_id = sgqlc.types.Field(order_by, graphql_name='jobId')
    retries = sgqlc.types.Field(order_by, graphql_name='retries')
    task_id = sgqlc.types.Field(order_by, graphql_name='taskId')


class meta_ai_predictions_by_day_aggregate_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('avg', 'count', 'max', 'min', 'stddev', 'stddev_pop', 'stddev_samp', 'sum', 'var_pop', 'var_samp', 'variance')
    avg = sgqlc.types.Field('meta_ai_predictions_by_day_avg_order_by', graphql_name='avg')
    count = sgqlc.types.Field(order_by, graphql_name='count')
    max = sgqlc.types.Field('meta_ai_predictions_by_day_max_order_by', graphql_name='max')
    min = sgqlc.types.Field('meta_ai_predictions_by_day_min_order_by', graphql_name='min')
    stddev = sgqlc.types.Field('meta_ai_predictions_by_day_stddev_order_by', graphql_name='stddev')
    stddev_pop = sgqlc.types.Field('meta_ai_predictions_by_day_stddev_pop_order_by', graphql_name='stddev_pop')
    stddev_samp = sgqlc.types.Field('meta_ai_predictions_by_day_stddev_samp_order_by', graphql_name='stddev_samp')
    sum = sgqlc.types.Field('meta_ai_predictions_by_day_sum_order_by', graphql_name='sum')
    var_pop = sgqlc.types.Field('meta_ai_predictions_by_day_var_pop_order_by', graphql_name='var_pop')
    var_samp = sgqlc.types.Field('meta_ai_predictions_by_day_var_samp_order_by', graphql_name='var_samp')
    variance = sgqlc.types.Field('meta_ai_predictions_by_day_variance_order_by', graphql_name='variance')


class meta_ai_predictions_by_day_avg_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('count',)
    count = sgqlc.types.Field(order_by, graphql_name='count')


class meta_ai_predictions_by_day_bool_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('_and', '_not', '_or', 'app_id', 'count', 'day', 'model_id', 'type')
    _and = sgqlc.types.Field(sgqlc.types.list_of('meta_ai_predictions_by_day_bool_exp'), graphql_name='_and')
    _not = sgqlc.types.Field('meta_ai_predictions_by_day_bool_exp', graphql_name='_not')
    _or = sgqlc.types.Field(sgqlc.types.list_of('meta_ai_predictions_by_day_bool_exp'), graphql_name='_or')
    app_id = sgqlc.types.Field('uuid_comparison_exp', graphql_name='appId')
    count = sgqlc.types.Field(bigint_comparison_exp, graphql_name='count')
    day = sgqlc.types.Field(date_comparison_exp, graphql_name='day')
    model_id = sgqlc.types.Field('uuid_comparison_exp', graphql_name='modelId')
    type = sgqlc.types.Field(String_comparison_exp, graphql_name='type')


class meta_ai_predictions_by_day_max_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('app_id', 'count', 'day', 'model_id', 'type')
    app_id = sgqlc.types.Field(order_by, graphql_name='appId')
    count = sgqlc.types.Field(order_by, graphql_name='count')
    day = sgqlc.types.Field(order_by, graphql_name='day')
    model_id = sgqlc.types.Field(order_by, graphql_name='modelId')
    type = sgqlc.types.Field(order_by, graphql_name='type')


class meta_ai_predictions_by_day_min_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('app_id', 'count', 'day', 'model_id', 'type')
    app_id = sgqlc.types.Field(order_by, graphql_name='appId')
    count = sgqlc.types.Field(order_by, graphql_name='count')
    day = sgqlc.types.Field(order_by, graphql_name='day')
    model_id = sgqlc.types.Field(order_by, graphql_name='modelId')
    type = sgqlc.types.Field(order_by, graphql_name='type')


class meta_ai_predictions_by_day_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('app_id', 'count', 'day', 'model_id', 'type')
    app_id = sgqlc.types.Field(order_by, graphql_name='appId')
    count = sgqlc.types.Field(order_by, graphql_name='count')
    day = sgqlc.types.Field(order_by, graphql_name='day')
    model_id = sgqlc.types.Field(order_by, graphql_name='modelId')
    type = sgqlc.types.Field(order_by, graphql_name='type')


class meta_ai_predictions_by_day_stddev_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('count',)
    count = sgqlc.types.Field(order_by, graphql_name='count')


class meta_ai_predictions_by_day_stddev_pop_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('count',)
    count = sgqlc.types.Field(order_by, graphql_name='count')


class meta_ai_predictions_by_day_stddev_samp_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('count',)
    count = sgqlc.types.Field(order_by, graphql_name='count')


class meta_ai_predictions_by_day_sum_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('count',)
    count = sgqlc.types.Field(order_by, graphql_name='count')


class meta_ai_predictions_by_day_var_pop_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('count',)
    count = sgqlc.types.Field(order_by, graphql_name='count')


class meta_ai_predictions_by_day_var_samp_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('count',)
    count = sgqlc.types.Field(order_by, graphql_name='count')


class meta_ai_predictions_by_day_variance_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('count',)
    count = sgqlc.types.Field(order_by, graphql_name='count')


class meta_ai_visibility_aggregate_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('count', 'max', 'min')
    count = sgqlc.types.Field(order_by, graphql_name='count')
    max = sgqlc.types.Field('meta_ai_visibility_max_order_by', graphql_name='max')
    min = sgqlc.types.Field('meta_ai_visibility_min_order_by', graphql_name='min')


class meta_ai_visibility_arr_rel_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('data', 'on_conflict')
    data = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('meta_ai_visibility_insert_input'))), graphql_name='data')
    on_conflict = sgqlc.types.Field('meta_ai_visibility_on_conflict', graphql_name='on_conflict')


class meta_ai_visibility_bool_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('_and', '_not', '_or', 'models', 'type')
    _and = sgqlc.types.Field(sgqlc.types.list_of('meta_ai_visibility_bool_exp'), graphql_name='_and')
    _not = sgqlc.types.Field('meta_ai_visibility_bool_exp', graphql_name='_not')
    _or = sgqlc.types.Field(sgqlc.types.list_of('meta_ai_visibility_bool_exp'), graphql_name='_or')
    models = sgqlc.types.Field(meta_ai_model_bool_exp, graphql_name='models')
    type = sgqlc.types.Field(String_comparison_exp, graphql_name='type')


class meta_ai_visibility_enum_comparison_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('_eq', '_in', '_is_null', '_neq', '_nin')
    _eq = sgqlc.types.Field(meta_ai_visibility_enum, graphql_name='_eq')
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_visibility_enum)), graphql_name='_in')
    _is_null = sgqlc.types.Field(Boolean, graphql_name='_is_null')
    _neq = sgqlc.types.Field(meta_ai_visibility_enum, graphql_name='_neq')
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_visibility_enum)), graphql_name='_nin')


class meta_ai_visibility_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('models', 'type')
    models = sgqlc.types.Field(meta_ai_model_arr_rel_insert_input, graphql_name='models')
    type = sgqlc.types.Field(String, graphql_name='type')


class meta_ai_visibility_max_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('type',)
    type = sgqlc.types.Field(order_by, graphql_name='type')


class meta_ai_visibility_min_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('type',)
    type = sgqlc.types.Field(order_by, graphql_name='type')


class meta_ai_visibility_obj_rel_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('data', 'on_conflict')
    data = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_visibility_insert_input), graphql_name='data')
    on_conflict = sgqlc.types.Field('meta_ai_visibility_on_conflict', graphql_name='on_conflict')


class meta_ai_visibility_on_conflict(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('constraint', 'update_columns', 'where')
    constraint = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_visibility_constraint), graphql_name='constraint')
    update_columns = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_visibility_update_column))), graphql_name='update_columns')
    where = sgqlc.types.Field(meta_ai_visibility_bool_exp, graphql_name='where')


class meta_ai_visibility_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('models_aggregate', 'type')
    models_aggregate = sgqlc.types.Field(meta_ai_model_aggregate_order_by, graphql_name='models_aggregate')
    type = sgqlc.types.Field(order_by, graphql_name='type')


class meta_ai_visibility_pk_columns_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('type',)
    type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='type')


class meta_ai_visibility_set_input(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('type',)
    type = sgqlc.types.Field(String, graphql_name='type')


class numeric_comparison_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('_eq', '_gt', '_gte', '_in', '_is_null', '_lt', '_lte', '_neq', '_nin')
    _eq = sgqlc.types.Field(numeric, graphql_name='_eq')
    _gt = sgqlc.types.Field(numeric, graphql_name='_gt')
    _gte = sgqlc.types.Field(numeric, graphql_name='_gte')
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(numeric)), graphql_name='_in')
    _is_null = sgqlc.types.Field(Boolean, graphql_name='_is_null')
    _lt = sgqlc.types.Field(numeric, graphql_name='_lt')
    _lte = sgqlc.types.Field(numeric, graphql_name='_lte')
    _neq = sgqlc.types.Field(numeric, graphql_name='_neq')
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(numeric)), graphql_name='_nin')


class timestamptz_comparison_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('_eq', '_gt', '_gte', '_in', '_is_null', '_lt', '_lte', '_neq', '_nin')
    _eq = sgqlc.types.Field(timestamptz, graphql_name='_eq')
    _gt = sgqlc.types.Field(timestamptz, graphql_name='_gt')
    _gte = sgqlc.types.Field(timestamptz, graphql_name='_gte')
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(timestamptz)), graphql_name='_in')
    _is_null = sgqlc.types.Field(Boolean, graphql_name='_is_null')
    _lt = sgqlc.types.Field(timestamptz, graphql_name='_lt')
    _lte = sgqlc.types.Field(timestamptz, graphql_name='_lte')
    _neq = sgqlc.types.Field(timestamptz, graphql_name='_neq')
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(timestamptz)), graphql_name='_nin')


class uuid_comparison_exp(sgqlc.types.Input):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('_eq', '_gt', '_gte', '_in', '_is_null', '_lt', '_lte', '_neq', '_nin')
    _eq = sgqlc.types.Field(uuid, graphql_name='_eq')
    _gt = sgqlc.types.Field(uuid, graphql_name='_gt')
    _gte = sgqlc.types.Field(uuid, graphql_name='_gte')
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(uuid)), graphql_name='_in')
    _is_null = sgqlc.types.Field(Boolean, graphql_name='_is_null')
    _lt = sgqlc.types.Field(uuid, graphql_name='_lt')
    _lte = sgqlc.types.Field(uuid, graphql_name='_lte')
    _neq = sgqlc.types.Field(uuid, graphql_name='_neq')
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(uuid)), graphql_name='_nin')



########################################################################
# Output Objects and Interfaces
########################################################################
class InsertMetaAiModelMutationOutput(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('id',)
    id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name='id')


class Prediction(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('prediction_id', 'predictions')
    prediction_id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name='predictionId')
    predictions = sgqlc.types.Field(sgqlc.types.list_of('meta_ai_prediction'), graphql_name='predictions')


class Prelabel(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('prediction', 'prediction_id')
    prediction = sgqlc.types.Field('meta_ai_prediction', graphql_name='prediction')
    prediction_id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name='predictionId')


class RawPrediction(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('output', 'score')
    output = sgqlc.types.Field(json, graphql_name='output')
    score = sgqlc.types.Field(numeric, graphql_name='score')


class URL(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('url',)
    url = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='url')


class meta_ai_app(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('active', 'assigned', 'id', 'model', 'model_id', 'predictions', 'predictions_aggregate', 'statistics', 'statistics_aggregate', 'threshold')
    active = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='active')
    assigned = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_assignment_enum), graphql_name='assigned')
    id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name='id')
    model = sgqlc.types.Field(sgqlc.types.non_null('meta_ai_model'), graphql_name='model')
    model_id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name='modelId')
    predictions = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('meta_ai_prediction'))), graphql_name='predictions', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_prediction_bool_exp, graphql_name='where', default=None)),
))
    )
    predictions_aggregate = sgqlc.types.Field(sgqlc.types.non_null('meta_ai_prediction_aggregate'), graphql_name='predictions_aggregate', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_prediction_bool_exp, graphql_name='where', default=None)),
))
    )
    statistics = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('meta_ai_predictions_by_day'))), graphql_name='statistics', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_predictions_by_day_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_predictions_by_day_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_predictions_by_day_bool_exp, graphql_name='where', default=None)),
))
    )
    statistics_aggregate = sgqlc.types.Field(sgqlc.types.non_null('meta_ai_predictions_by_day_aggregate'), graphql_name='statistics_aggregate', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_predictions_by_day_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_predictions_by_day_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_predictions_by_day_bool_exp, graphql_name='where', default=None)),
))
    )
    threshold = sgqlc.types.Field(numeric, graphql_name='threshold')


class meta_ai_app_aggregate(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('aggregate', 'nodes')
    aggregate = sgqlc.types.Field('meta_ai_app_aggregate_fields', graphql_name='aggregate')
    nodes = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_app))), graphql_name='nodes')


class meta_ai_app_aggregate_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('avg', 'count', 'max', 'min', 'stddev', 'stddev_pop', 'stddev_samp', 'sum', 'var_pop', 'var_samp', 'variance')
    avg = sgqlc.types.Field('meta_ai_app_avg_fields', graphql_name='avg')
    count = sgqlc.types.Field(Int, graphql_name='count', args=sgqlc.types.ArgDict((
        ('columns', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_app_select_column)), graphql_name='columns', default=None)),
        ('distinct', sgqlc.types.Arg(Boolean, graphql_name='distinct', default=None)),
))
    )
    max = sgqlc.types.Field('meta_ai_app_max_fields', graphql_name='max')
    min = sgqlc.types.Field('meta_ai_app_min_fields', graphql_name='min')
    stddev = sgqlc.types.Field('meta_ai_app_stddev_fields', graphql_name='stddev')
    stddev_pop = sgqlc.types.Field('meta_ai_app_stddev_pop_fields', graphql_name='stddev_pop')
    stddev_samp = sgqlc.types.Field('meta_ai_app_stddev_samp_fields', graphql_name='stddev_samp')
    sum = sgqlc.types.Field('meta_ai_app_sum_fields', graphql_name='sum')
    var_pop = sgqlc.types.Field('meta_ai_app_var_pop_fields', graphql_name='var_pop')
    var_samp = sgqlc.types.Field('meta_ai_app_var_samp_fields', graphql_name='var_samp')
    variance = sgqlc.types.Field('meta_ai_app_variance_fields', graphql_name='variance')


class meta_ai_app_avg_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('threshold',)
    threshold = sgqlc.types.Field(Float, graphql_name='threshold')


class meta_ai_app_max_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('id', 'model_id', 'threshold')
    id = sgqlc.types.Field(uuid, graphql_name='id')
    model_id = sgqlc.types.Field(uuid, graphql_name='modelId')
    threshold = sgqlc.types.Field(numeric, graphql_name='threshold')


class meta_ai_app_min_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('id', 'model_id', 'threshold')
    id = sgqlc.types.Field(uuid, graphql_name='id')
    model_id = sgqlc.types.Field(uuid, graphql_name='modelId')
    threshold = sgqlc.types.Field(numeric, graphql_name='threshold')


class meta_ai_app_mutation_response(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('affected_rows', 'returning')
    affected_rows = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='affected_rows')
    returning = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_app))), graphql_name='returning')


class meta_ai_app_stddev_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('threshold',)
    threshold = sgqlc.types.Field(Float, graphql_name='threshold')


class meta_ai_app_stddev_pop_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('threshold',)
    threshold = sgqlc.types.Field(Float, graphql_name='threshold')


class meta_ai_app_stddev_samp_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('threshold',)
    threshold = sgqlc.types.Field(Float, graphql_name='threshold')


class meta_ai_app_sum_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('threshold',)
    threshold = sgqlc.types.Field(numeric, graphql_name='threshold')


class meta_ai_app_var_pop_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('threshold',)
    threshold = sgqlc.types.Field(Float, graphql_name='threshold')


class meta_ai_app_var_samp_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('threshold',)
    threshold = sgqlc.types.Field(Float, graphql_name='threshold')


class meta_ai_app_variance_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('threshold',)
    threshold = sgqlc.types.Field(Float, graphql_name='threshold')


class meta_ai_assignment(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('apps', 'apps_aggregate', 'type')
    apps = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_app))), graphql_name='apps', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_app_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_app_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_app_bool_exp, graphql_name='where', default=None)),
))
    )
    apps_aggregate = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_app_aggregate), graphql_name='apps_aggregate', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_app_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_app_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_app_bool_exp, graphql_name='where', default=None)),
))
    )
    type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='type')


class meta_ai_assignment_aggregate(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('aggregate', 'nodes')
    aggregate = sgqlc.types.Field('meta_ai_assignment_aggregate_fields', graphql_name='aggregate')
    nodes = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_assignment))), graphql_name='nodes')


class meta_ai_assignment_aggregate_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('count', 'max', 'min')
    count = sgqlc.types.Field(Int, graphql_name='count', args=sgqlc.types.ArgDict((
        ('columns', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_assignment_select_column)), graphql_name='columns', default=None)),
        ('distinct', sgqlc.types.Arg(Boolean, graphql_name='distinct', default=None)),
))
    )
    max = sgqlc.types.Field('meta_ai_assignment_max_fields', graphql_name='max')
    min = sgqlc.types.Field('meta_ai_assignment_min_fields', graphql_name='min')


class meta_ai_assignment_max_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('type',)
    type = sgqlc.types.Field(String, graphql_name='type')


class meta_ai_assignment_min_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('type',)
    type = sgqlc.types.Field(String, graphql_name='type')


class meta_ai_assignment_mutation_response(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('affected_rows', 'returning')
    affected_rows = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='affected_rows')
    returning = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_assignment))), graphql_name='returning')


class meta_ai_deployment(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('created_at', 'endpoint', 'image', 'model', 'model_id', 'owner_id', 'properties', 'purpose', 'status', 'target_status', 'type', 'updated_at')
    created_at = sgqlc.types.Field(sgqlc.types.non_null(timestamptz), graphql_name='created_at')
    endpoint = sgqlc.types.Field(String, graphql_name='endpoint')
    image = sgqlc.types.Field(String, graphql_name='image')
    model = sgqlc.types.Field(sgqlc.types.non_null('meta_ai_model'), graphql_name='model')
    model_id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name='modelId')
    owner_id = sgqlc.types.Field(bigint, graphql_name='ownerId')
    properties = sgqlc.types.Field(jsonb, graphql_name='properties', args=sgqlc.types.ArgDict((
        ('path', sgqlc.types.Arg(String, graphql_name='path', default=None)),
))
    )
    purpose = sgqlc.types.Field(meta_ai_deployment_purpose_enum, graphql_name='purpose')
    status = sgqlc.types.Field(meta_ai_deployment_status_enum, graphql_name='status')
    target_status = sgqlc.types.Field(meta_ai_deployment_status_enum, graphql_name='target_status')
    type = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_deployment_type_enum), graphql_name='type')
    updated_at = sgqlc.types.Field(sgqlc.types.non_null(timestamptz), graphql_name='updated_at')


class meta_ai_deployment_aggregate(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('aggregate', 'nodes')
    aggregate = sgqlc.types.Field('meta_ai_deployment_aggregate_fields', graphql_name='aggregate')
    nodes = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment))), graphql_name='nodes')


class meta_ai_deployment_aggregate_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('avg', 'count', 'max', 'min', 'stddev', 'stddev_pop', 'stddev_samp', 'sum', 'var_pop', 'var_samp', 'variance')
    avg = sgqlc.types.Field('meta_ai_deployment_avg_fields', graphql_name='avg')
    count = sgqlc.types.Field(Int, graphql_name='count', args=sgqlc.types.ArgDict((
        ('columns', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_select_column)), graphql_name='columns', default=None)),
        ('distinct', sgqlc.types.Arg(Boolean, graphql_name='distinct', default=None)),
))
    )
    max = sgqlc.types.Field('meta_ai_deployment_max_fields', graphql_name='max')
    min = sgqlc.types.Field('meta_ai_deployment_min_fields', graphql_name='min')
    stddev = sgqlc.types.Field('meta_ai_deployment_stddev_fields', graphql_name='stddev')
    stddev_pop = sgqlc.types.Field('meta_ai_deployment_stddev_pop_fields', graphql_name='stddev_pop')
    stddev_samp = sgqlc.types.Field('meta_ai_deployment_stddev_samp_fields', graphql_name='stddev_samp')
    sum = sgqlc.types.Field('meta_ai_deployment_sum_fields', graphql_name='sum')
    var_pop = sgqlc.types.Field('meta_ai_deployment_var_pop_fields', graphql_name='var_pop')
    var_samp = sgqlc.types.Field('meta_ai_deployment_var_samp_fields', graphql_name='var_samp')
    variance = sgqlc.types.Field('meta_ai_deployment_variance_fields', graphql_name='variance')


class meta_ai_deployment_avg_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('owner_id',)
    owner_id = sgqlc.types.Field(Float, graphql_name='ownerId')


class meta_ai_deployment_max_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('created_at', 'endpoint', 'image', 'model_id', 'owner_id', 'updated_at')
    created_at = sgqlc.types.Field(timestamptz, graphql_name='created_at')
    endpoint = sgqlc.types.Field(String, graphql_name='endpoint')
    image = sgqlc.types.Field(String, graphql_name='image')
    model_id = sgqlc.types.Field(uuid, graphql_name='modelId')
    owner_id = sgqlc.types.Field(bigint, graphql_name='ownerId')
    updated_at = sgqlc.types.Field(timestamptz, graphql_name='updated_at')


class meta_ai_deployment_min_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('created_at', 'endpoint', 'image', 'model_id', 'owner_id', 'updated_at')
    created_at = sgqlc.types.Field(timestamptz, graphql_name='created_at')
    endpoint = sgqlc.types.Field(String, graphql_name='endpoint')
    image = sgqlc.types.Field(String, graphql_name='image')
    model_id = sgqlc.types.Field(uuid, graphql_name='modelId')
    owner_id = sgqlc.types.Field(bigint, graphql_name='ownerId')
    updated_at = sgqlc.types.Field(timestamptz, graphql_name='updated_at')


class meta_ai_deployment_mutation_response(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('affected_rows', 'returning')
    affected_rows = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='affected_rows')
    returning = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment))), graphql_name='returning')


class meta_ai_deployment_purpose(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('deployments', 'deployments_aggregate', 'purpose')
    deployments = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment))), graphql_name='deployments', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_deployment_bool_exp, graphql_name='where', default=None)),
))
    )
    deployments_aggregate = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_deployment_aggregate), graphql_name='deployments_aggregate', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_deployment_bool_exp, graphql_name='where', default=None)),
))
    )
    purpose = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='purpose')


class meta_ai_deployment_purpose_aggregate(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('aggregate', 'nodes')
    aggregate = sgqlc.types.Field('meta_ai_deployment_purpose_aggregate_fields', graphql_name='aggregate')
    nodes = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_purpose))), graphql_name='nodes')


class meta_ai_deployment_purpose_aggregate_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('count', 'max', 'min')
    count = sgqlc.types.Field(Int, graphql_name='count', args=sgqlc.types.ArgDict((
        ('columns', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_purpose_select_column)), graphql_name='columns', default=None)),
        ('distinct', sgqlc.types.Arg(Boolean, graphql_name='distinct', default=None)),
))
    )
    max = sgqlc.types.Field('meta_ai_deployment_purpose_max_fields', graphql_name='max')
    min = sgqlc.types.Field('meta_ai_deployment_purpose_min_fields', graphql_name='min')


class meta_ai_deployment_purpose_max_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('purpose',)
    purpose = sgqlc.types.Field(String, graphql_name='purpose')


class meta_ai_deployment_purpose_min_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('purpose',)
    purpose = sgqlc.types.Field(String, graphql_name='purpose')


class meta_ai_deployment_purpose_mutation_response(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('affected_rows', 'returning')
    affected_rows = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='affected_rows')
    returning = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_purpose))), graphql_name='returning')


class meta_ai_deployment_status(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('deployments', 'deployments_by_target_status', 'deployments_by_target_status_aggregate', 'deployments_aggregate', 'status')
    deployments = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment))), graphql_name='deployments', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_deployment_bool_exp, graphql_name='where', default=None)),
))
    )
    deployments_by_target_status = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment))), graphql_name='deploymentsByTargetStatus', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_deployment_bool_exp, graphql_name='where', default=None)),
))
    )
    deployments_by_target_status_aggregate = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_deployment_aggregate), graphql_name='deploymentsByTargetStatus_aggregate', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_deployment_bool_exp, graphql_name='where', default=None)),
))
    )
    deployments_aggregate = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_deployment_aggregate), graphql_name='deployments_aggregate', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_deployment_bool_exp, graphql_name='where', default=None)),
))
    )
    status = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='status')


class meta_ai_deployment_status_aggregate(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('aggregate', 'nodes')
    aggregate = sgqlc.types.Field('meta_ai_deployment_status_aggregate_fields', graphql_name='aggregate')
    nodes = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_status))), graphql_name='nodes')


class meta_ai_deployment_status_aggregate_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('count', 'max', 'min')
    count = sgqlc.types.Field(Int, graphql_name='count', args=sgqlc.types.ArgDict((
        ('columns', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_status_select_column)), graphql_name='columns', default=None)),
        ('distinct', sgqlc.types.Arg(Boolean, graphql_name='distinct', default=None)),
))
    )
    max = sgqlc.types.Field('meta_ai_deployment_status_max_fields', graphql_name='max')
    min = sgqlc.types.Field('meta_ai_deployment_status_min_fields', graphql_name='min')


class meta_ai_deployment_status_max_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('status',)
    status = sgqlc.types.Field(String, graphql_name='status')


class meta_ai_deployment_status_min_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('status',)
    status = sgqlc.types.Field(String, graphql_name='status')


class meta_ai_deployment_status_mutation_response(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('affected_rows', 'returning')
    affected_rows = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='affected_rows')
    returning = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_status))), graphql_name='returning')


class meta_ai_deployment_stddev_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('owner_id',)
    owner_id = sgqlc.types.Field(Float, graphql_name='ownerId')


class meta_ai_deployment_stddev_pop_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('owner_id',)
    owner_id = sgqlc.types.Field(Float, graphql_name='ownerId')


class meta_ai_deployment_stddev_samp_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('owner_id',)
    owner_id = sgqlc.types.Field(Float, graphql_name='ownerId')


class meta_ai_deployment_sum_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('owner_id',)
    owner_id = sgqlc.types.Field(bigint, graphql_name='ownerId')


class meta_ai_deployment_type(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('deployments', 'deployments_aggregate', 'name')
    deployments = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment))), graphql_name='deployments', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_deployment_bool_exp, graphql_name='where', default=None)),
))
    )
    deployments_aggregate = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_deployment_aggregate), graphql_name='deployments_aggregate', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_deployment_bool_exp, graphql_name='where', default=None)),
))
    )
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')


class meta_ai_deployment_type_aggregate(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('aggregate', 'nodes')
    aggregate = sgqlc.types.Field('meta_ai_deployment_type_aggregate_fields', graphql_name='aggregate')
    nodes = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_type))), graphql_name='nodes')


class meta_ai_deployment_type_aggregate_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('count', 'max', 'min')
    count = sgqlc.types.Field(Int, graphql_name='count', args=sgqlc.types.ArgDict((
        ('columns', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_type_select_column)), graphql_name='columns', default=None)),
        ('distinct', sgqlc.types.Arg(Boolean, graphql_name='distinct', default=None)),
))
    )
    max = sgqlc.types.Field('meta_ai_deployment_type_max_fields', graphql_name='max')
    min = sgqlc.types.Field('meta_ai_deployment_type_min_fields', graphql_name='min')


class meta_ai_deployment_type_max_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('name',)
    name = sgqlc.types.Field(String, graphql_name='name')


class meta_ai_deployment_type_min_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('name',)
    name = sgqlc.types.Field(String, graphql_name='name')


class meta_ai_deployment_type_mutation_response(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('affected_rows', 'returning')
    affected_rows = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='affected_rows')
    returning = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_type))), graphql_name='returning')


class meta_ai_deployment_var_pop_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('owner_id',)
    owner_id = sgqlc.types.Field(Float, graphql_name='ownerId')


class meta_ai_deployment_var_samp_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('owner_id',)
    owner_id = sgqlc.types.Field(Float, graphql_name='ownerId')


class meta_ai_deployment_variance_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('owner_id',)
    owner_id = sgqlc.types.Field(Float, graphql_name='ownerId')


class meta_ai_environment(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('name',)
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')


class meta_ai_environment_aggregate(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('aggregate', 'nodes')
    aggregate = sgqlc.types.Field('meta_ai_environment_aggregate_fields', graphql_name='aggregate')
    nodes = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_environment))), graphql_name='nodes')


class meta_ai_environment_aggregate_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('count', 'max', 'min')
    count = sgqlc.types.Field(Int, graphql_name='count', args=sgqlc.types.ArgDict((
        ('columns', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_environment_select_column)), graphql_name='columns', default=None)),
        ('distinct', sgqlc.types.Arg(Boolean, graphql_name='distinct', default=None)),
))
    )
    max = sgqlc.types.Field('meta_ai_environment_max_fields', graphql_name='max')
    min = sgqlc.types.Field('meta_ai_environment_min_fields', graphql_name='min')


class meta_ai_environment_max_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('name',)
    name = sgqlc.types.Field(String, graphql_name='name')


class meta_ai_environment_min_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('name',)
    name = sgqlc.types.Field(String, graphql_name='name')


class meta_ai_environment_mutation_response(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('affected_rows', 'returning')
    affected_rows = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='affected_rows')
    returning = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_environment))), graphql_name='returning')


class meta_ai_instance(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('id', 'output', 'prediction', 'prediction_id', 'score')
    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='id')
    output = sgqlc.types.Field(jsonb, graphql_name='output', args=sgqlc.types.ArgDict((
        ('path', sgqlc.types.Arg(String, graphql_name='path', default=None)),
))
    )
    prediction = sgqlc.types.Field(sgqlc.types.non_null('meta_ai_prediction'), graphql_name='prediction')
    prediction_id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name='predictionId')
    score = sgqlc.types.Field(float8, graphql_name='score')


class meta_ai_instance_aggregate(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('aggregate', 'nodes')
    aggregate = sgqlc.types.Field('meta_ai_instance_aggregate_fields', graphql_name='aggregate')
    nodes = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_instance))), graphql_name='nodes')


class meta_ai_instance_aggregate_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('avg', 'count', 'max', 'min', 'stddev', 'stddev_pop', 'stddev_samp', 'sum', 'var_pop', 'var_samp', 'variance')
    avg = sgqlc.types.Field('meta_ai_instance_avg_fields', graphql_name='avg')
    count = sgqlc.types.Field(Int, graphql_name='count', args=sgqlc.types.ArgDict((
        ('columns', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_instance_select_column)), graphql_name='columns', default=None)),
        ('distinct', sgqlc.types.Arg(Boolean, graphql_name='distinct', default=None)),
))
    )
    max = sgqlc.types.Field('meta_ai_instance_max_fields', graphql_name='max')
    min = sgqlc.types.Field('meta_ai_instance_min_fields', graphql_name='min')
    stddev = sgqlc.types.Field('meta_ai_instance_stddev_fields', graphql_name='stddev')
    stddev_pop = sgqlc.types.Field('meta_ai_instance_stddev_pop_fields', graphql_name='stddev_pop')
    stddev_samp = sgqlc.types.Field('meta_ai_instance_stddev_samp_fields', graphql_name='stddev_samp')
    sum = sgqlc.types.Field('meta_ai_instance_sum_fields', graphql_name='sum')
    var_pop = sgqlc.types.Field('meta_ai_instance_var_pop_fields', graphql_name='var_pop')
    var_samp = sgqlc.types.Field('meta_ai_instance_var_samp_fields', graphql_name='var_samp')
    variance = sgqlc.types.Field('meta_ai_instance_variance_fields', graphql_name='variance')


class meta_ai_instance_avg_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('id', 'score')
    id = sgqlc.types.Field(Float, graphql_name='id')
    score = sgqlc.types.Field(Float, graphql_name='score')


class meta_ai_instance_max_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('id', 'prediction_id', 'score')
    id = sgqlc.types.Field(Int, graphql_name='id')
    prediction_id = sgqlc.types.Field(uuid, graphql_name='predictionId')
    score = sgqlc.types.Field(float8, graphql_name='score')


class meta_ai_instance_min_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('id', 'prediction_id', 'score')
    id = sgqlc.types.Field(Int, graphql_name='id')
    prediction_id = sgqlc.types.Field(uuid, graphql_name='predictionId')
    score = sgqlc.types.Field(float8, graphql_name='score')


class meta_ai_instance_mutation_response(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('affected_rows', 'returning')
    affected_rows = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='affected_rows')
    returning = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_instance))), graphql_name='returning')


class meta_ai_instance_stddev_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('id', 'score')
    id = sgqlc.types.Field(Float, graphql_name='id')
    score = sgqlc.types.Field(Float, graphql_name='score')


class meta_ai_instance_stddev_pop_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('id', 'score')
    id = sgqlc.types.Field(Float, graphql_name='id')
    score = sgqlc.types.Field(Float, graphql_name='score')


class meta_ai_instance_stddev_samp_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('id', 'score')
    id = sgqlc.types.Field(Float, graphql_name='id')
    score = sgqlc.types.Field(Float, graphql_name='score')


class meta_ai_instance_sum_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('id', 'score')
    id = sgqlc.types.Field(Int, graphql_name='id')
    score = sgqlc.types.Field(float8, graphql_name='score')


class meta_ai_instance_var_pop_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('id', 'score')
    id = sgqlc.types.Field(Float, graphql_name='id')
    score = sgqlc.types.Field(Float, graphql_name='score')


class meta_ai_instance_var_samp_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('id', 'score')
    id = sgqlc.types.Field(Float, graphql_name='id')
    score = sgqlc.types.Field(Float, graphql_name='score')


class meta_ai_instance_variance_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('id', 'score')
    id = sgqlc.types.Field(Float, graphql_name='id')
    score = sgqlc.types.Field(Float, graphql_name='score')


class meta_ai_model(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('apps', 'apps_aggregate', 'created_at', 'deployment', 'description', 'editor_id', 'endpoint', 'id', 'input_schema', 'metadata', 'model_save_path', 'name', 'output_schema', 'owner_id', 'predictions', 'predictions_aggregate', 'stage', 'updated_at', 'version', 'visibility', 'weights_path')
    apps = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_app))), graphql_name='apps', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_app_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_app_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_app_bool_exp, graphql_name='where', default=None)),
))
    )
    apps_aggregate = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_app_aggregate), graphql_name='apps_aggregate', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_app_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_app_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_app_bool_exp, graphql_name='where', default=None)),
))
    )
    created_at = sgqlc.types.Field(sgqlc.types.non_null(timestamptz), graphql_name='createdAt')
    deployment = sgqlc.types.Field(meta_ai_deployment, graphql_name='deployment')
    description = sgqlc.types.Field(String, graphql_name='description')
    editor_id = sgqlc.types.Field(bigint, graphql_name='editorId')
    endpoint = sgqlc.types.Field(String, graphql_name='endpoint')
    id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name='id')
    input_schema = sgqlc.types.Field(jsonb, graphql_name='inputSchema', args=sgqlc.types.ArgDict((
        ('path', sgqlc.types.Arg(String, graphql_name='path', default=None)),
))
    )
    metadata = sgqlc.types.Field(jsonb, graphql_name='metadata', args=sgqlc.types.ArgDict((
        ('path', sgqlc.types.Arg(String, graphql_name='path', default=None)),
))
    )
    model_save_path = sgqlc.types.Field(String, graphql_name='modelSavePath')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    output_schema = sgqlc.types.Field(jsonb, graphql_name='outputSchema', args=sgqlc.types.ArgDict((
        ('path', sgqlc.types.Arg(String, graphql_name='path', default=None)),
))
    )
    owner_id = sgqlc.types.Field(sgqlc.types.non_null(bigint), graphql_name='ownerId')
    predictions = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('meta_ai_prediction'))), graphql_name='predictions', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_prediction_bool_exp, graphql_name='where', default=None)),
))
    )
    predictions_aggregate = sgqlc.types.Field(sgqlc.types.non_null('meta_ai_prediction_aggregate'), graphql_name='predictions_aggregate', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_prediction_bool_exp, graphql_name='where', default=None)),
))
    )
    stage = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_environment_enum), graphql_name='stage')
    updated_at = sgqlc.types.Field(timestamptz, graphql_name='updatedAt')
    version = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='version')
    visibility = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_visibility_enum), graphql_name='visibility')
    weights_path = sgqlc.types.Field(String, graphql_name='weightsPath')


class meta_ai_model_aggregate(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('aggregate', 'nodes')
    aggregate = sgqlc.types.Field('meta_ai_model_aggregate_fields', graphql_name='aggregate')
    nodes = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_model))), graphql_name='nodes')


class meta_ai_model_aggregate_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('avg', 'count', 'max', 'min', 'stddev', 'stddev_pop', 'stddev_samp', 'sum', 'var_pop', 'var_samp', 'variance')
    avg = sgqlc.types.Field('meta_ai_model_avg_fields', graphql_name='avg')
    count = sgqlc.types.Field(Int, graphql_name='count', args=sgqlc.types.ArgDict((
        ('columns', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_model_select_column)), graphql_name='columns', default=None)),
        ('distinct', sgqlc.types.Arg(Boolean, graphql_name='distinct', default=None)),
))
    )
    max = sgqlc.types.Field('meta_ai_model_max_fields', graphql_name='max')
    min = sgqlc.types.Field('meta_ai_model_min_fields', graphql_name='min')
    stddev = sgqlc.types.Field('meta_ai_model_stddev_fields', graphql_name='stddev')
    stddev_pop = sgqlc.types.Field('meta_ai_model_stddev_pop_fields', graphql_name='stddev_pop')
    stddev_samp = sgqlc.types.Field('meta_ai_model_stddev_samp_fields', graphql_name='stddev_samp')
    sum = sgqlc.types.Field('meta_ai_model_sum_fields', graphql_name='sum')
    var_pop = sgqlc.types.Field('meta_ai_model_var_pop_fields', graphql_name='var_pop')
    var_samp = sgqlc.types.Field('meta_ai_model_var_samp_fields', graphql_name='var_samp')
    variance = sgqlc.types.Field('meta_ai_model_variance_fields', graphql_name='variance')


class meta_ai_model_avg_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('editor_id', 'owner_id', 'version')
    editor_id = sgqlc.types.Field(Float, graphql_name='editorId')
    owner_id = sgqlc.types.Field(Float, graphql_name='ownerId')
    version = sgqlc.types.Field(Float, graphql_name='version')


class meta_ai_model_max_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('created_at', 'description', 'editor_id', 'endpoint', 'id', 'model_save_path', 'name', 'owner_id', 'updated_at', 'version', 'weights_path')
    created_at = sgqlc.types.Field(timestamptz, graphql_name='createdAt')
    description = sgqlc.types.Field(String, graphql_name='description')
    editor_id = sgqlc.types.Field(bigint, graphql_name='editorId')
    endpoint = sgqlc.types.Field(String, graphql_name='endpoint')
    id = sgqlc.types.Field(uuid, graphql_name='id')
    model_save_path = sgqlc.types.Field(String, graphql_name='modelSavePath')
    name = sgqlc.types.Field(String, graphql_name='name')
    owner_id = sgqlc.types.Field(bigint, graphql_name='ownerId')
    updated_at = sgqlc.types.Field(timestamptz, graphql_name='updatedAt')
    version = sgqlc.types.Field(Int, graphql_name='version')
    weights_path = sgqlc.types.Field(String, graphql_name='weightsPath')


class meta_ai_model_min_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('created_at', 'description', 'editor_id', 'endpoint', 'id', 'model_save_path', 'name', 'owner_id', 'updated_at', 'version', 'weights_path')
    created_at = sgqlc.types.Field(timestamptz, graphql_name='createdAt')
    description = sgqlc.types.Field(String, graphql_name='description')
    editor_id = sgqlc.types.Field(bigint, graphql_name='editorId')
    endpoint = sgqlc.types.Field(String, graphql_name='endpoint')
    id = sgqlc.types.Field(uuid, graphql_name='id')
    model_save_path = sgqlc.types.Field(String, graphql_name='modelSavePath')
    name = sgqlc.types.Field(String, graphql_name='name')
    owner_id = sgqlc.types.Field(bigint, graphql_name='ownerId')
    updated_at = sgqlc.types.Field(timestamptz, graphql_name='updatedAt')
    version = sgqlc.types.Field(Int, graphql_name='version')
    weights_path = sgqlc.types.Field(String, graphql_name='weightsPath')


class meta_ai_model_mutation_response(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('affected_rows', 'returning')
    affected_rows = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='affected_rows')
    returning = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_model))), graphql_name='returning')


class meta_ai_model_stddev_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('editor_id', 'owner_id', 'version')
    editor_id = sgqlc.types.Field(Float, graphql_name='editorId')
    owner_id = sgqlc.types.Field(Float, graphql_name='ownerId')
    version = sgqlc.types.Field(Float, graphql_name='version')


class meta_ai_model_stddev_pop_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('editor_id', 'owner_id', 'version')
    editor_id = sgqlc.types.Field(Float, graphql_name='editorId')
    owner_id = sgqlc.types.Field(Float, graphql_name='ownerId')
    version = sgqlc.types.Field(Float, graphql_name='version')


class meta_ai_model_stddev_samp_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('editor_id', 'owner_id', 'version')
    editor_id = sgqlc.types.Field(Float, graphql_name='editorId')
    owner_id = sgqlc.types.Field(Float, graphql_name='ownerId')
    version = sgqlc.types.Field(Float, graphql_name='version')


class meta_ai_model_sum_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('editor_id', 'owner_id', 'version')
    editor_id = sgqlc.types.Field(bigint, graphql_name='editorId')
    owner_id = sgqlc.types.Field(bigint, graphql_name='ownerId')
    version = sgqlc.types.Field(Int, graphql_name='version')


class meta_ai_model_var_pop_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('editor_id', 'owner_id', 'version')
    editor_id = sgqlc.types.Field(Float, graphql_name='editorId')
    owner_id = sgqlc.types.Field(Float, graphql_name='ownerId')
    version = sgqlc.types.Field(Float, graphql_name='version')


class meta_ai_model_var_samp_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('editor_id', 'owner_id', 'version')
    editor_id = sgqlc.types.Field(Float, graphql_name='editorId')
    owner_id = sgqlc.types.Field(Float, graphql_name='ownerId')
    version = sgqlc.types.Field(Float, graphql_name='version')


class meta_ai_model_variance_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('editor_id', 'owner_id', 'version')
    editor_id = sgqlc.types.Field(Float, graphql_name='editorId')
    owner_id = sgqlc.types.Field(Float, graphql_name='ownerId')
    version = sgqlc.types.Field(Float, graphql_name='version')


class meta_ai_prediction(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('app_id', 'created_at', 'id', 'instances', 'instances_aggregate', 'job_id', 'job_uuid', 'model', 'model_id', 'retries', 'state', 'task_id', 'type')
    app_id = sgqlc.types.Field(uuid, graphql_name='appId')
    created_at = sgqlc.types.Field(sgqlc.types.non_null(timestamptz), graphql_name='createdAt')
    id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name='id')
    instances = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_instance))), graphql_name='instances', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_instance_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_instance_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_instance_bool_exp, graphql_name='where', default=None)),
))
    )
    instances_aggregate = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_instance_aggregate), graphql_name='instances_aggregate', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_instance_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_instance_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_instance_bool_exp, graphql_name='where', default=None)),
))
    )
    job_id = sgqlc.types.Field(bigint, graphql_name='jobId')
    job_uuid = sgqlc.types.Field(uuid, graphql_name='jobUUID')
    model = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_model), graphql_name='model')
    model_id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name='modelId')
    retries = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='retries')
    state = sgqlc.types.Field(meta_ai_prediction_state_enum, graphql_name='state')
    task_id = sgqlc.types.Field(bigint, graphql_name='taskId')
    type = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_assignment_enum), graphql_name='type')


class meta_ai_prediction_aggregate(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('aggregate', 'nodes')
    aggregate = sgqlc.types.Field('meta_ai_prediction_aggregate_fields', graphql_name='aggregate')
    nodes = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction))), graphql_name='nodes')


class meta_ai_prediction_aggregate_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('avg', 'count', 'max', 'min', 'stddev', 'stddev_pop', 'stddev_samp', 'sum', 'var_pop', 'var_samp', 'variance')
    avg = sgqlc.types.Field('meta_ai_prediction_avg_fields', graphql_name='avg')
    count = sgqlc.types.Field(Int, graphql_name='count', args=sgqlc.types.ArgDict((
        ('columns', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_select_column)), graphql_name='columns', default=None)),
        ('distinct', sgqlc.types.Arg(Boolean, graphql_name='distinct', default=None)),
))
    )
    max = sgqlc.types.Field('meta_ai_prediction_max_fields', graphql_name='max')
    min = sgqlc.types.Field('meta_ai_prediction_min_fields', graphql_name='min')
    stddev = sgqlc.types.Field('meta_ai_prediction_stddev_fields', graphql_name='stddev')
    stddev_pop = sgqlc.types.Field('meta_ai_prediction_stddev_pop_fields', graphql_name='stddev_pop')
    stddev_samp = sgqlc.types.Field('meta_ai_prediction_stddev_samp_fields', graphql_name='stddev_samp')
    sum = sgqlc.types.Field('meta_ai_prediction_sum_fields', graphql_name='sum')
    var_pop = sgqlc.types.Field('meta_ai_prediction_var_pop_fields', graphql_name='var_pop')
    var_samp = sgqlc.types.Field('meta_ai_prediction_var_samp_fields', graphql_name='var_samp')
    variance = sgqlc.types.Field('meta_ai_prediction_variance_fields', graphql_name='variance')


class meta_ai_prediction_avg_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('job_id', 'retries', 'task_id')
    job_id = sgqlc.types.Field(Float, graphql_name='jobId')
    retries = sgqlc.types.Field(Float, graphql_name='retries')
    task_id = sgqlc.types.Field(Float, graphql_name='taskId')


class meta_ai_prediction_max_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('app_id', 'created_at', 'id', 'job_id', 'job_uuid', 'model_id', 'retries', 'task_id')
    app_id = sgqlc.types.Field(uuid, graphql_name='appId')
    created_at = sgqlc.types.Field(timestamptz, graphql_name='createdAt')
    id = sgqlc.types.Field(uuid, graphql_name='id')
    job_id = sgqlc.types.Field(bigint, graphql_name='jobId')
    job_uuid = sgqlc.types.Field(uuid, graphql_name='jobUUID')
    model_id = sgqlc.types.Field(uuid, graphql_name='modelId')
    retries = sgqlc.types.Field(Int, graphql_name='retries')
    task_id = sgqlc.types.Field(bigint, graphql_name='taskId')


class meta_ai_prediction_min_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('app_id', 'created_at', 'id', 'job_id', 'job_uuid', 'model_id', 'retries', 'task_id')
    app_id = sgqlc.types.Field(uuid, graphql_name='appId')
    created_at = sgqlc.types.Field(timestamptz, graphql_name='createdAt')
    id = sgqlc.types.Field(uuid, graphql_name='id')
    job_id = sgqlc.types.Field(bigint, graphql_name='jobId')
    job_uuid = sgqlc.types.Field(uuid, graphql_name='jobUUID')
    model_id = sgqlc.types.Field(uuid, graphql_name='modelId')
    retries = sgqlc.types.Field(Int, graphql_name='retries')
    task_id = sgqlc.types.Field(bigint, graphql_name='taskId')


class meta_ai_prediction_mutation_response(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('affected_rows', 'returning')
    affected_rows = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='affected_rows')
    returning = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction))), graphql_name='returning')


class meta_ai_prediction_state(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('predictions', 'predictions_aggregate', 'state')
    predictions = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction))), graphql_name='predictions', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_prediction_bool_exp, graphql_name='where', default=None)),
))
    )
    predictions_aggregate = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_prediction_aggregate), graphql_name='predictions_aggregate', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_prediction_bool_exp, graphql_name='where', default=None)),
))
    )
    state = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='state')


class meta_ai_prediction_state_aggregate(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('aggregate', 'nodes')
    aggregate = sgqlc.types.Field('meta_ai_prediction_state_aggregate_fields', graphql_name='aggregate')
    nodes = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_state))), graphql_name='nodes')


class meta_ai_prediction_state_aggregate_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('count', 'max', 'min')
    count = sgqlc.types.Field(Int, graphql_name='count', args=sgqlc.types.ArgDict((
        ('columns', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_state_select_column)), graphql_name='columns', default=None)),
        ('distinct', sgqlc.types.Arg(Boolean, graphql_name='distinct', default=None)),
))
    )
    max = sgqlc.types.Field('meta_ai_prediction_state_max_fields', graphql_name='max')
    min = sgqlc.types.Field('meta_ai_prediction_state_min_fields', graphql_name='min')


class meta_ai_prediction_state_max_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('state',)
    state = sgqlc.types.Field(String, graphql_name='state')


class meta_ai_prediction_state_min_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('state',)
    state = sgqlc.types.Field(String, graphql_name='state')


class meta_ai_prediction_state_mutation_response(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('affected_rows', 'returning')
    affected_rows = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='affected_rows')
    returning = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_state))), graphql_name='returning')


class meta_ai_prediction_stddev_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('job_id', 'retries', 'task_id')
    job_id = sgqlc.types.Field(Float, graphql_name='jobId')
    retries = sgqlc.types.Field(Float, graphql_name='retries')
    task_id = sgqlc.types.Field(Float, graphql_name='taskId')


class meta_ai_prediction_stddev_pop_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('job_id', 'retries', 'task_id')
    job_id = sgqlc.types.Field(Float, graphql_name='jobId')
    retries = sgqlc.types.Field(Float, graphql_name='retries')
    task_id = sgqlc.types.Field(Float, graphql_name='taskId')


class meta_ai_prediction_stddev_samp_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('job_id', 'retries', 'task_id')
    job_id = sgqlc.types.Field(Float, graphql_name='jobId')
    retries = sgqlc.types.Field(Float, graphql_name='retries')
    task_id = sgqlc.types.Field(Float, graphql_name='taskId')


class meta_ai_prediction_sum_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('job_id', 'retries', 'task_id')
    job_id = sgqlc.types.Field(bigint, graphql_name='jobId')
    retries = sgqlc.types.Field(Int, graphql_name='retries')
    task_id = sgqlc.types.Field(bigint, graphql_name='taskId')


class meta_ai_prediction_var_pop_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('job_id', 'retries', 'task_id')
    job_id = sgqlc.types.Field(Float, graphql_name='jobId')
    retries = sgqlc.types.Field(Float, graphql_name='retries')
    task_id = sgqlc.types.Field(Float, graphql_name='taskId')


class meta_ai_prediction_var_samp_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('job_id', 'retries', 'task_id')
    job_id = sgqlc.types.Field(Float, graphql_name='jobId')
    retries = sgqlc.types.Field(Float, graphql_name='retries')
    task_id = sgqlc.types.Field(Float, graphql_name='taskId')


class meta_ai_prediction_variance_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('job_id', 'retries', 'task_id')
    job_id = sgqlc.types.Field(Float, graphql_name='jobId')
    retries = sgqlc.types.Field(Float, graphql_name='retries')
    task_id = sgqlc.types.Field(Float, graphql_name='taskId')


class meta_ai_predictions_by_day(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('app_id', 'count', 'day', 'model_id', 'type')
    app_id = sgqlc.types.Field(uuid, graphql_name='appId')
    count = sgqlc.types.Field(bigint, graphql_name='count')
    day = sgqlc.types.Field(date, graphql_name='day')
    model_id = sgqlc.types.Field(uuid, graphql_name='modelId')
    type = sgqlc.types.Field(String, graphql_name='type')


class meta_ai_predictions_by_day_aggregate(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('aggregate', 'nodes')
    aggregate = sgqlc.types.Field('meta_ai_predictions_by_day_aggregate_fields', graphql_name='aggregate')
    nodes = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_predictions_by_day))), graphql_name='nodes')


class meta_ai_predictions_by_day_aggregate_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('avg', 'count', 'max', 'min', 'stddev', 'stddev_pop', 'stddev_samp', 'sum', 'var_pop', 'var_samp', 'variance')
    avg = sgqlc.types.Field('meta_ai_predictions_by_day_avg_fields', graphql_name='avg')
    count = sgqlc.types.Field(Int, graphql_name='count', args=sgqlc.types.ArgDict((
        ('columns', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_predictions_by_day_select_column)), graphql_name='columns', default=None)),
        ('distinct', sgqlc.types.Arg(Boolean, graphql_name='distinct', default=None)),
))
    )
    max = sgqlc.types.Field('meta_ai_predictions_by_day_max_fields', graphql_name='max')
    min = sgqlc.types.Field('meta_ai_predictions_by_day_min_fields', graphql_name='min')
    stddev = sgqlc.types.Field('meta_ai_predictions_by_day_stddev_fields', graphql_name='stddev')
    stddev_pop = sgqlc.types.Field('meta_ai_predictions_by_day_stddev_pop_fields', graphql_name='stddev_pop')
    stddev_samp = sgqlc.types.Field('meta_ai_predictions_by_day_stddev_samp_fields', graphql_name='stddev_samp')
    sum = sgqlc.types.Field('meta_ai_predictions_by_day_sum_fields', graphql_name='sum')
    var_pop = sgqlc.types.Field('meta_ai_predictions_by_day_var_pop_fields', graphql_name='var_pop')
    var_samp = sgqlc.types.Field('meta_ai_predictions_by_day_var_samp_fields', graphql_name='var_samp')
    variance = sgqlc.types.Field('meta_ai_predictions_by_day_variance_fields', graphql_name='variance')


class meta_ai_predictions_by_day_avg_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('count',)
    count = sgqlc.types.Field(Float, graphql_name='count')


class meta_ai_predictions_by_day_max_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('app_id', 'count', 'day', 'model_id', 'type')
    app_id = sgqlc.types.Field(uuid, graphql_name='appId')
    count = sgqlc.types.Field(bigint, graphql_name='count')
    day = sgqlc.types.Field(date, graphql_name='day')
    model_id = sgqlc.types.Field(uuid, graphql_name='modelId')
    type = sgqlc.types.Field(String, graphql_name='type')


class meta_ai_predictions_by_day_min_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('app_id', 'count', 'day', 'model_id', 'type')
    app_id = sgqlc.types.Field(uuid, graphql_name='appId')
    count = sgqlc.types.Field(bigint, graphql_name='count')
    day = sgqlc.types.Field(date, graphql_name='day')
    model_id = sgqlc.types.Field(uuid, graphql_name='modelId')
    type = sgqlc.types.Field(String, graphql_name='type')


class meta_ai_predictions_by_day_stddev_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('count',)
    count = sgqlc.types.Field(Float, graphql_name='count')


class meta_ai_predictions_by_day_stddev_pop_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('count',)
    count = sgqlc.types.Field(Float, graphql_name='count')


class meta_ai_predictions_by_day_stddev_samp_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('count',)
    count = sgqlc.types.Field(Float, graphql_name='count')


class meta_ai_predictions_by_day_sum_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('count',)
    count = sgqlc.types.Field(bigint, graphql_name='count')


class meta_ai_predictions_by_day_var_pop_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('count',)
    count = sgqlc.types.Field(Float, graphql_name='count')


class meta_ai_predictions_by_day_var_samp_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('count',)
    count = sgqlc.types.Field(Float, graphql_name='count')


class meta_ai_predictions_by_day_variance_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('count',)
    count = sgqlc.types.Field(Float, graphql_name='count')


class meta_ai_visibility(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('models', 'models_aggregate', 'type')
    models = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_model))), graphql_name='models', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_model_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_model_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_model_bool_exp, graphql_name='where', default=None)),
))
    )
    models_aggregate = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_model_aggregate), graphql_name='models_aggregate', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_model_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_model_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_model_bool_exp, graphql_name='where', default=None)),
))
    )
    type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='type')


class meta_ai_visibility_aggregate(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('aggregate', 'nodes')
    aggregate = sgqlc.types.Field('meta_ai_visibility_aggregate_fields', graphql_name='aggregate')
    nodes = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_visibility))), graphql_name='nodes')


class meta_ai_visibility_aggregate_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('count', 'max', 'min')
    count = sgqlc.types.Field(Int, graphql_name='count', args=sgqlc.types.ArgDict((
        ('columns', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_visibility_select_column)), graphql_name='columns', default=None)),
        ('distinct', sgqlc.types.Arg(Boolean, graphql_name='distinct', default=None)),
))
    )
    max = sgqlc.types.Field('meta_ai_visibility_max_fields', graphql_name='max')
    min = sgqlc.types.Field('meta_ai_visibility_min_fields', graphql_name='min')


class meta_ai_visibility_max_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('type',)
    type = sgqlc.types.Field(String, graphql_name='type')


class meta_ai_visibility_min_fields(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('type',)
    type = sgqlc.types.Field(String, graphql_name='type')


class meta_ai_visibility_mutation_response(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('affected_rows', 'returning')
    affected_rows = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='affected_rows')
    returning = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_visibility))), graphql_name='returning')


class mutation_root(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('add_model', 'delete_meta_ai_app', 'delete_meta_ai_app_by_pk', 'delete_meta_ai_assignment', 'delete_meta_ai_assignment_by_pk', 'delete_meta_ai_deployment', 'delete_meta_ai_deployment_by_pk', 'delete_meta_ai_deployment_purpose', 'delete_meta_ai_deployment_purpose_by_pk', 'delete_meta_ai_deployment_status', 'delete_meta_ai_deployment_status_by_pk', 'delete_meta_ai_deployment_type', 'delete_meta_ai_deployment_type_by_pk', 'delete_meta_ai_environment', 'delete_meta_ai_environment_by_pk', 'delete_meta_ai_instance', 'delete_meta_ai_instance_by_pk', 'delete_meta_ai_model', 'delete_meta_ai_model_by_pk', 'delete_meta_ai_prediction', 'delete_meta_ai_prediction_by_pk', 'delete_meta_ai_prediction_state', 'delete_meta_ai_prediction_state_by_pk', 'delete_meta_ai_visibility', 'delete_meta_ai_visibility_by_pk', 'insert_meta_ai_app', 'insert_meta_ai_app_one', 'insert_meta_ai_assignment', 'insert_meta_ai_assignment_one', 'insert_meta_ai_deployment', 'insert_meta_ai_deployment_one', 'insert_meta_ai_deployment_purpose', 'insert_meta_ai_deployment_purpose_one', 'insert_meta_ai_deployment_status', 'insert_meta_ai_deployment_status_one', 'insert_meta_ai_deployment_type', 'insert_meta_ai_deployment_type_one', 'insert_meta_ai_environment', 'insert_meta_ai_environment_one', 'insert_meta_ai_instance', 'insert_meta_ai_instance_one', 'insert_meta_ai_model', 'insert_meta_ai_model_one', 'insert_meta_ai_prediction', 'insert_meta_ai_prediction_one', 'insert_meta_ai_prediction_state', 'insert_meta_ai_prediction_state_one', 'insert_meta_ai_visibility', 'insert_meta_ai_visibility_one', 'update_meta_ai_app', 'update_meta_ai_app_by_pk', 'update_meta_ai_assignment', 'update_meta_ai_assignment_by_pk', 'update_meta_ai_deployment', 'update_meta_ai_deployment_by_pk', 'update_meta_ai_deployment_purpose', 'update_meta_ai_deployment_purpose_by_pk', 'update_meta_ai_deployment_status', 'update_meta_ai_deployment_status_by_pk', 'update_meta_ai_deployment_type', 'update_meta_ai_deployment_type_by_pk', 'update_meta_ai_environment', 'update_meta_ai_environment_by_pk', 'update_meta_ai_instance', 'update_meta_ai_instance_by_pk', 'update_meta_ai_model', 'update_meta_ai_model_by_pk', 'update_meta_ai_prediction', 'update_meta_ai_prediction_by_pk', 'update_meta_ai_prediction_state', 'update_meta_ai_prediction_state_by_pk', 'update_meta_ai_visibility', 'update_meta_ai_visibility_by_pk')
    add_model = sgqlc.types.Field(InsertMetaAiModelMutationOutput, graphql_name='add_model', args=sgqlc.types.ArgDict((
        ('description', sgqlc.types.Arg(String, graphql_name='description', default=None)),
        ('input_schema', sgqlc.types.Arg(jsonb, graphql_name='inputSchema', default=None)),
        ('model_save_path', sgqlc.types.Arg(String, graphql_name='modelSavePath', default=None)),
        ('name', sgqlc.types.Arg(String, graphql_name='name', default=None)),
        ('output_schema', sgqlc.types.Arg(jsonb, graphql_name='outputSchema', default=None)),
        ('owner_id', sgqlc.types.Arg(bigint, graphql_name='ownerId', default=None)),
        ('stage', sgqlc.types.Arg(InsertMetaAiModelMutationMetaAiEnvironmentEnum, graphql_name='stage', default=None)),
        ('version', sgqlc.types.Arg(Int, graphql_name='version', default=None)),
        ('weights_path', sgqlc.types.Arg(String, graphql_name='weightsPath', default=None)),
))
    )
    delete_meta_ai_app = sgqlc.types.Field(meta_ai_app_mutation_response, graphql_name='delete_meta_ai_app', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(sgqlc.types.non_null(meta_ai_app_bool_exp), graphql_name='where', default=None)),
))
    )
    delete_meta_ai_app_by_pk = sgqlc.types.Field(meta_ai_app, graphql_name='delete_meta_ai_app_by_pk', args=sgqlc.types.ArgDict((
        ('assigned', sgqlc.types.Arg(sgqlc.types.non_null(meta_ai_assignment_enum), graphql_name='assigned', default=None)),
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name='id', default=None)),
        ('model_id', sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name='modelId', default=None)),
))
    )
    delete_meta_ai_assignment = sgqlc.types.Field(meta_ai_assignment_mutation_response, graphql_name='delete_meta_ai_assignment', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(sgqlc.types.non_null(meta_ai_assignment_bool_exp), graphql_name='where', default=None)),
))
    )
    delete_meta_ai_assignment_by_pk = sgqlc.types.Field(meta_ai_assignment, graphql_name='delete_meta_ai_assignment_by_pk', args=sgqlc.types.ArgDict((
        ('type', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='type', default=None)),
))
    )
    delete_meta_ai_deployment = sgqlc.types.Field(meta_ai_deployment_mutation_response, graphql_name='delete_meta_ai_deployment', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(sgqlc.types.non_null(meta_ai_deployment_bool_exp), graphql_name='where', default=None)),
))
    )
    delete_meta_ai_deployment_by_pk = sgqlc.types.Field(meta_ai_deployment, graphql_name='delete_meta_ai_deployment_by_pk', args=sgqlc.types.ArgDict((
        ('model_id', sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name='modelId', default=None)),
))
    )
    delete_meta_ai_deployment_purpose = sgqlc.types.Field(meta_ai_deployment_purpose_mutation_response, graphql_name='delete_meta_ai_deployment_purpose', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(sgqlc.types.non_null(meta_ai_deployment_purpose_bool_exp), graphql_name='where', default=None)),
))
    )
    delete_meta_ai_deployment_purpose_by_pk = sgqlc.types.Field(meta_ai_deployment_purpose, graphql_name='delete_meta_ai_deployment_purpose_by_pk', args=sgqlc.types.ArgDict((
        ('purpose', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='purpose', default=None)),
))
    )
    delete_meta_ai_deployment_status = sgqlc.types.Field(meta_ai_deployment_status_mutation_response, graphql_name='delete_meta_ai_deployment_status', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(sgqlc.types.non_null(meta_ai_deployment_status_bool_exp), graphql_name='where', default=None)),
))
    )
    delete_meta_ai_deployment_status_by_pk = sgqlc.types.Field(meta_ai_deployment_status, graphql_name='delete_meta_ai_deployment_status_by_pk', args=sgqlc.types.ArgDict((
        ('status', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='status', default=None)),
))
    )
    delete_meta_ai_deployment_type = sgqlc.types.Field(meta_ai_deployment_type_mutation_response, graphql_name='delete_meta_ai_deployment_type', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(sgqlc.types.non_null(meta_ai_deployment_type_bool_exp), graphql_name='where', default=None)),
))
    )
    delete_meta_ai_deployment_type_by_pk = sgqlc.types.Field(meta_ai_deployment_type, graphql_name='delete_meta_ai_deployment_type_by_pk', args=sgqlc.types.ArgDict((
        ('name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='name', default=None)),
))
    )
    delete_meta_ai_environment = sgqlc.types.Field(meta_ai_environment_mutation_response, graphql_name='delete_meta_ai_environment', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(sgqlc.types.non_null(meta_ai_environment_bool_exp), graphql_name='where', default=None)),
))
    )
    delete_meta_ai_environment_by_pk = sgqlc.types.Field(meta_ai_environment, graphql_name='delete_meta_ai_environment_by_pk', args=sgqlc.types.ArgDict((
        ('name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='name', default=None)),
))
    )
    delete_meta_ai_instance = sgqlc.types.Field(meta_ai_instance_mutation_response, graphql_name='delete_meta_ai_instance', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(sgqlc.types.non_null(meta_ai_instance_bool_exp), graphql_name='where', default=None)),
))
    )
    delete_meta_ai_instance_by_pk = sgqlc.types.Field(meta_ai_instance, graphql_name='delete_meta_ai_instance_by_pk', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='id', default=None)),
        ('prediction_id', sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name='predictionId', default=None)),
))
    )
    delete_meta_ai_model = sgqlc.types.Field(meta_ai_model_mutation_response, graphql_name='delete_meta_ai_model', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(sgqlc.types.non_null(meta_ai_model_bool_exp), graphql_name='where', default=None)),
))
    )
    delete_meta_ai_model_by_pk = sgqlc.types.Field(meta_ai_model, graphql_name='delete_meta_ai_model_by_pk', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name='id', default=None)),
))
    )
    delete_meta_ai_prediction = sgqlc.types.Field(meta_ai_prediction_mutation_response, graphql_name='delete_meta_ai_prediction', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(sgqlc.types.non_null(meta_ai_prediction_bool_exp), graphql_name='where', default=None)),
))
    )
    delete_meta_ai_prediction_by_pk = sgqlc.types.Field(meta_ai_prediction, graphql_name='delete_meta_ai_prediction_by_pk', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name='id', default=None)),
))
    )
    delete_meta_ai_prediction_state = sgqlc.types.Field(meta_ai_prediction_state_mutation_response, graphql_name='delete_meta_ai_prediction_state', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(sgqlc.types.non_null(meta_ai_prediction_state_bool_exp), graphql_name='where', default=None)),
))
    )
    delete_meta_ai_prediction_state_by_pk = sgqlc.types.Field(meta_ai_prediction_state, graphql_name='delete_meta_ai_prediction_state_by_pk', args=sgqlc.types.ArgDict((
        ('state', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='state', default=None)),
))
    )
    delete_meta_ai_visibility = sgqlc.types.Field(meta_ai_visibility_mutation_response, graphql_name='delete_meta_ai_visibility', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(sgqlc.types.non_null(meta_ai_visibility_bool_exp), graphql_name='where', default=None)),
))
    )
    delete_meta_ai_visibility_by_pk = sgqlc.types.Field(meta_ai_visibility, graphql_name='delete_meta_ai_visibility_by_pk', args=sgqlc.types.ArgDict((
        ('type', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='type', default=None)),
))
    )
    insert_meta_ai_app = sgqlc.types.Field(meta_ai_app_mutation_response, graphql_name='insert_meta_ai_app', args=sgqlc.types.ArgDict((
        ('objects', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_app_insert_input))), graphql_name='objects', default=None)),
        ('on_conflict', sgqlc.types.Arg(meta_ai_app_on_conflict, graphql_name='on_conflict', default=None)),
))
    )
    insert_meta_ai_app_one = sgqlc.types.Field(meta_ai_app, graphql_name='insert_meta_ai_app_one', args=sgqlc.types.ArgDict((
        ('object', sgqlc.types.Arg(sgqlc.types.non_null(meta_ai_app_insert_input), graphql_name='object', default=None)),
        ('on_conflict', sgqlc.types.Arg(meta_ai_app_on_conflict, graphql_name='on_conflict', default=None)),
))
    )
    insert_meta_ai_assignment = sgqlc.types.Field(meta_ai_assignment_mutation_response, graphql_name='insert_meta_ai_assignment', args=sgqlc.types.ArgDict((
        ('objects', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_assignment_insert_input))), graphql_name='objects', default=None)),
        ('on_conflict', sgqlc.types.Arg(meta_ai_assignment_on_conflict, graphql_name='on_conflict', default=None)),
))
    )
    insert_meta_ai_assignment_one = sgqlc.types.Field(meta_ai_assignment, graphql_name='insert_meta_ai_assignment_one', args=sgqlc.types.ArgDict((
        ('object', sgqlc.types.Arg(sgqlc.types.non_null(meta_ai_assignment_insert_input), graphql_name='object', default=None)),
        ('on_conflict', sgqlc.types.Arg(meta_ai_assignment_on_conflict, graphql_name='on_conflict', default=None)),
))
    )
    insert_meta_ai_deployment = sgqlc.types.Field(meta_ai_deployment_mutation_response, graphql_name='insert_meta_ai_deployment', args=sgqlc.types.ArgDict((
        ('objects', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_insert_input))), graphql_name='objects', default=None)),
        ('on_conflict', sgqlc.types.Arg(meta_ai_deployment_on_conflict, graphql_name='on_conflict', default=None)),
))
    )
    insert_meta_ai_deployment_one = sgqlc.types.Field(meta_ai_deployment, graphql_name='insert_meta_ai_deployment_one', args=sgqlc.types.ArgDict((
        ('object', sgqlc.types.Arg(sgqlc.types.non_null(meta_ai_deployment_insert_input), graphql_name='object', default=None)),
        ('on_conflict', sgqlc.types.Arg(meta_ai_deployment_on_conflict, graphql_name='on_conflict', default=None)),
))
    )
    insert_meta_ai_deployment_purpose = sgqlc.types.Field(meta_ai_deployment_purpose_mutation_response, graphql_name='insert_meta_ai_deployment_purpose', args=sgqlc.types.ArgDict((
        ('objects', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_purpose_insert_input))), graphql_name='objects', default=None)),
        ('on_conflict', sgqlc.types.Arg(meta_ai_deployment_purpose_on_conflict, graphql_name='on_conflict', default=None)),
))
    )
    insert_meta_ai_deployment_purpose_one = sgqlc.types.Field(meta_ai_deployment_purpose, graphql_name='insert_meta_ai_deployment_purpose_one', args=sgqlc.types.ArgDict((
        ('object', sgqlc.types.Arg(sgqlc.types.non_null(meta_ai_deployment_purpose_insert_input), graphql_name='object', default=None)),
        ('on_conflict', sgqlc.types.Arg(meta_ai_deployment_purpose_on_conflict, graphql_name='on_conflict', default=None)),
))
    )
    insert_meta_ai_deployment_status = sgqlc.types.Field(meta_ai_deployment_status_mutation_response, graphql_name='insert_meta_ai_deployment_status', args=sgqlc.types.ArgDict((
        ('objects', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_status_insert_input))), graphql_name='objects', default=None)),
        ('on_conflict', sgqlc.types.Arg(meta_ai_deployment_status_on_conflict, graphql_name='on_conflict', default=None)),
))
    )
    insert_meta_ai_deployment_status_one = sgqlc.types.Field(meta_ai_deployment_status, graphql_name='insert_meta_ai_deployment_status_one', args=sgqlc.types.ArgDict((
        ('object', sgqlc.types.Arg(sgqlc.types.non_null(meta_ai_deployment_status_insert_input), graphql_name='object', default=None)),
        ('on_conflict', sgqlc.types.Arg(meta_ai_deployment_status_on_conflict, graphql_name='on_conflict', default=None)),
))
    )
    insert_meta_ai_deployment_type = sgqlc.types.Field(meta_ai_deployment_type_mutation_response, graphql_name='insert_meta_ai_deployment_type', args=sgqlc.types.ArgDict((
        ('objects', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_type_insert_input))), graphql_name='objects', default=None)),
        ('on_conflict', sgqlc.types.Arg(meta_ai_deployment_type_on_conflict, graphql_name='on_conflict', default=None)),
))
    )
    insert_meta_ai_deployment_type_one = sgqlc.types.Field(meta_ai_deployment_type, graphql_name='insert_meta_ai_deployment_type_one', args=sgqlc.types.ArgDict((
        ('object', sgqlc.types.Arg(sgqlc.types.non_null(meta_ai_deployment_type_insert_input), graphql_name='object', default=None)),
        ('on_conflict', sgqlc.types.Arg(meta_ai_deployment_type_on_conflict, graphql_name='on_conflict', default=None)),
))
    )
    insert_meta_ai_environment = sgqlc.types.Field(meta_ai_environment_mutation_response, graphql_name='insert_meta_ai_environment', args=sgqlc.types.ArgDict((
        ('objects', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_environment_insert_input))), graphql_name='objects', default=None)),
        ('on_conflict', sgqlc.types.Arg(meta_ai_environment_on_conflict, graphql_name='on_conflict', default=None)),
))
    )
    insert_meta_ai_environment_one = sgqlc.types.Field(meta_ai_environment, graphql_name='insert_meta_ai_environment_one', args=sgqlc.types.ArgDict((
        ('object', sgqlc.types.Arg(sgqlc.types.non_null(meta_ai_environment_insert_input), graphql_name='object', default=None)),
        ('on_conflict', sgqlc.types.Arg(meta_ai_environment_on_conflict, graphql_name='on_conflict', default=None)),
))
    )
    insert_meta_ai_instance = sgqlc.types.Field(meta_ai_instance_mutation_response, graphql_name='insert_meta_ai_instance', args=sgqlc.types.ArgDict((
        ('objects', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_instance_insert_input))), graphql_name='objects', default=None)),
        ('on_conflict', sgqlc.types.Arg(meta_ai_instance_on_conflict, graphql_name='on_conflict', default=None)),
))
    )
    insert_meta_ai_instance_one = sgqlc.types.Field(meta_ai_instance, graphql_name='insert_meta_ai_instance_one', args=sgqlc.types.ArgDict((
        ('object', sgqlc.types.Arg(sgqlc.types.non_null(meta_ai_instance_insert_input), graphql_name='object', default=None)),
        ('on_conflict', sgqlc.types.Arg(meta_ai_instance_on_conflict, graphql_name='on_conflict', default=None)),
))
    )
    insert_meta_ai_model = sgqlc.types.Field(meta_ai_model_mutation_response, graphql_name='insert_meta_ai_model', args=sgqlc.types.ArgDict((
        ('objects', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_model_insert_input))), graphql_name='objects', default=None)),
        ('on_conflict', sgqlc.types.Arg(meta_ai_model_on_conflict, graphql_name='on_conflict', default=None)),
))
    )
    insert_meta_ai_model_one = sgqlc.types.Field(meta_ai_model, graphql_name='insert_meta_ai_model_one', args=sgqlc.types.ArgDict((
        ('object', sgqlc.types.Arg(sgqlc.types.non_null(meta_ai_model_insert_input), graphql_name='object', default=None)),
        ('on_conflict', sgqlc.types.Arg(meta_ai_model_on_conflict, graphql_name='on_conflict', default=None)),
))
    )
    insert_meta_ai_prediction = sgqlc.types.Field(meta_ai_prediction_mutation_response, graphql_name='insert_meta_ai_prediction', args=sgqlc.types.ArgDict((
        ('objects', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_insert_input))), graphql_name='objects', default=None)),
        ('on_conflict', sgqlc.types.Arg(meta_ai_prediction_on_conflict, graphql_name='on_conflict', default=None)),
))
    )
    insert_meta_ai_prediction_one = sgqlc.types.Field(meta_ai_prediction, graphql_name='insert_meta_ai_prediction_one', args=sgqlc.types.ArgDict((
        ('object', sgqlc.types.Arg(sgqlc.types.non_null(meta_ai_prediction_insert_input), graphql_name='object', default=None)),
        ('on_conflict', sgqlc.types.Arg(meta_ai_prediction_on_conflict, graphql_name='on_conflict', default=None)),
))
    )
    insert_meta_ai_prediction_state = sgqlc.types.Field(meta_ai_prediction_state_mutation_response, graphql_name='insert_meta_ai_prediction_state', args=sgqlc.types.ArgDict((
        ('objects', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_state_insert_input))), graphql_name='objects', default=None)),
        ('on_conflict', sgqlc.types.Arg(meta_ai_prediction_state_on_conflict, graphql_name='on_conflict', default=None)),
))
    )
    insert_meta_ai_prediction_state_one = sgqlc.types.Field(meta_ai_prediction_state, graphql_name='insert_meta_ai_prediction_state_one', args=sgqlc.types.ArgDict((
        ('object', sgqlc.types.Arg(sgqlc.types.non_null(meta_ai_prediction_state_insert_input), graphql_name='object', default=None)),
        ('on_conflict', sgqlc.types.Arg(meta_ai_prediction_state_on_conflict, graphql_name='on_conflict', default=None)),
))
    )
    insert_meta_ai_visibility = sgqlc.types.Field(meta_ai_visibility_mutation_response, graphql_name='insert_meta_ai_visibility', args=sgqlc.types.ArgDict((
        ('objects', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_visibility_insert_input))), graphql_name='objects', default=None)),
        ('on_conflict', sgqlc.types.Arg(meta_ai_visibility_on_conflict, graphql_name='on_conflict', default=None)),
))
    )
    insert_meta_ai_visibility_one = sgqlc.types.Field(meta_ai_visibility, graphql_name='insert_meta_ai_visibility_one', args=sgqlc.types.ArgDict((
        ('object', sgqlc.types.Arg(sgqlc.types.non_null(meta_ai_visibility_insert_input), graphql_name='object', default=None)),
        ('on_conflict', sgqlc.types.Arg(meta_ai_visibility_on_conflict, graphql_name='on_conflict', default=None)),
))
    )
    update_meta_ai_app = sgqlc.types.Field(meta_ai_app_mutation_response, graphql_name='update_meta_ai_app', args=sgqlc.types.ArgDict((
        ('_inc', sgqlc.types.Arg(meta_ai_app_inc_input, graphql_name='_inc', default=None)),
        ('_set', sgqlc.types.Arg(meta_ai_app_set_input, graphql_name='_set', default=None)),
        ('where', sgqlc.types.Arg(sgqlc.types.non_null(meta_ai_app_bool_exp), graphql_name='where', default=None)),
))
    )
    update_meta_ai_app_by_pk = sgqlc.types.Field(meta_ai_app, graphql_name='update_meta_ai_app_by_pk', args=sgqlc.types.ArgDict((
        ('_inc', sgqlc.types.Arg(meta_ai_app_inc_input, graphql_name='_inc', default=None)),
        ('_set', sgqlc.types.Arg(meta_ai_app_set_input, graphql_name='_set', default=None)),
        ('pk_columns', sgqlc.types.Arg(sgqlc.types.non_null(meta_ai_app_pk_columns_input), graphql_name='pk_columns', default=None)),
))
    )
    update_meta_ai_assignment = sgqlc.types.Field(meta_ai_assignment_mutation_response, graphql_name='update_meta_ai_assignment', args=sgqlc.types.ArgDict((
        ('_set', sgqlc.types.Arg(meta_ai_assignment_set_input, graphql_name='_set', default=None)),
        ('where', sgqlc.types.Arg(sgqlc.types.non_null(meta_ai_assignment_bool_exp), graphql_name='where', default=None)),
))
    )
    update_meta_ai_assignment_by_pk = sgqlc.types.Field(meta_ai_assignment, graphql_name='update_meta_ai_assignment_by_pk', args=sgqlc.types.ArgDict((
        ('_set', sgqlc.types.Arg(meta_ai_assignment_set_input, graphql_name='_set', default=None)),
        ('pk_columns', sgqlc.types.Arg(sgqlc.types.non_null(meta_ai_assignment_pk_columns_input), graphql_name='pk_columns', default=None)),
))
    )
    update_meta_ai_deployment = sgqlc.types.Field(meta_ai_deployment_mutation_response, graphql_name='update_meta_ai_deployment', args=sgqlc.types.ArgDict((
        ('_append', sgqlc.types.Arg(meta_ai_deployment_append_input, graphql_name='_append', default=None)),
        ('_delete_at_path', sgqlc.types.Arg(meta_ai_deployment_delete_at_path_input, graphql_name='_delete_at_path', default=None)),
        ('_delete_elem', sgqlc.types.Arg(meta_ai_deployment_delete_elem_input, graphql_name='_delete_elem', default=None)),
        ('_delete_key', sgqlc.types.Arg(meta_ai_deployment_delete_key_input, graphql_name='_delete_key', default=None)),
        ('_inc', sgqlc.types.Arg(meta_ai_deployment_inc_input, graphql_name='_inc', default=None)),
        ('_prepend', sgqlc.types.Arg(meta_ai_deployment_prepend_input, graphql_name='_prepend', default=None)),
        ('_set', sgqlc.types.Arg(meta_ai_deployment_set_input, graphql_name='_set', default=None)),
        ('where', sgqlc.types.Arg(sgqlc.types.non_null(meta_ai_deployment_bool_exp), graphql_name='where', default=None)),
))
    )
    update_meta_ai_deployment_by_pk = sgqlc.types.Field(meta_ai_deployment, graphql_name='update_meta_ai_deployment_by_pk', args=sgqlc.types.ArgDict((
        ('_append', sgqlc.types.Arg(meta_ai_deployment_append_input, graphql_name='_append', default=None)),
        ('_delete_at_path', sgqlc.types.Arg(meta_ai_deployment_delete_at_path_input, graphql_name='_delete_at_path', default=None)),
        ('_delete_elem', sgqlc.types.Arg(meta_ai_deployment_delete_elem_input, graphql_name='_delete_elem', default=None)),
        ('_delete_key', sgqlc.types.Arg(meta_ai_deployment_delete_key_input, graphql_name='_delete_key', default=None)),
        ('_inc', sgqlc.types.Arg(meta_ai_deployment_inc_input, graphql_name='_inc', default=None)),
        ('_prepend', sgqlc.types.Arg(meta_ai_deployment_prepend_input, graphql_name='_prepend', default=None)),
        ('_set', sgqlc.types.Arg(meta_ai_deployment_set_input, graphql_name='_set', default=None)),
        ('pk_columns', sgqlc.types.Arg(sgqlc.types.non_null(meta_ai_deployment_pk_columns_input), graphql_name='pk_columns', default=None)),
))
    )
    update_meta_ai_deployment_purpose = sgqlc.types.Field(meta_ai_deployment_purpose_mutation_response, graphql_name='update_meta_ai_deployment_purpose', args=sgqlc.types.ArgDict((
        ('_set', sgqlc.types.Arg(meta_ai_deployment_purpose_set_input, graphql_name='_set', default=None)),
        ('where', sgqlc.types.Arg(sgqlc.types.non_null(meta_ai_deployment_purpose_bool_exp), graphql_name='where', default=None)),
))
    )
    update_meta_ai_deployment_purpose_by_pk = sgqlc.types.Field(meta_ai_deployment_purpose, graphql_name='update_meta_ai_deployment_purpose_by_pk', args=sgqlc.types.ArgDict((
        ('_set', sgqlc.types.Arg(meta_ai_deployment_purpose_set_input, graphql_name='_set', default=None)),
        ('pk_columns', sgqlc.types.Arg(sgqlc.types.non_null(meta_ai_deployment_purpose_pk_columns_input), graphql_name='pk_columns', default=None)),
))
    )
    update_meta_ai_deployment_status = sgqlc.types.Field(meta_ai_deployment_status_mutation_response, graphql_name='update_meta_ai_deployment_status', args=sgqlc.types.ArgDict((
        ('_set', sgqlc.types.Arg(meta_ai_deployment_status_set_input, graphql_name='_set', default=None)),
        ('where', sgqlc.types.Arg(sgqlc.types.non_null(meta_ai_deployment_status_bool_exp), graphql_name='where', default=None)),
))
    )
    update_meta_ai_deployment_status_by_pk = sgqlc.types.Field(meta_ai_deployment_status, graphql_name='update_meta_ai_deployment_status_by_pk', args=sgqlc.types.ArgDict((
        ('_set', sgqlc.types.Arg(meta_ai_deployment_status_set_input, graphql_name='_set', default=None)),
        ('pk_columns', sgqlc.types.Arg(sgqlc.types.non_null(meta_ai_deployment_status_pk_columns_input), graphql_name='pk_columns', default=None)),
))
    )
    update_meta_ai_deployment_type = sgqlc.types.Field(meta_ai_deployment_type_mutation_response, graphql_name='update_meta_ai_deployment_type', args=sgqlc.types.ArgDict((
        ('_set', sgqlc.types.Arg(meta_ai_deployment_type_set_input, graphql_name='_set', default=None)),
        ('where', sgqlc.types.Arg(sgqlc.types.non_null(meta_ai_deployment_type_bool_exp), graphql_name='where', default=None)),
))
    )
    update_meta_ai_deployment_type_by_pk = sgqlc.types.Field(meta_ai_deployment_type, graphql_name='update_meta_ai_deployment_type_by_pk', args=sgqlc.types.ArgDict((
        ('_set', sgqlc.types.Arg(meta_ai_deployment_type_set_input, graphql_name='_set', default=None)),
        ('pk_columns', sgqlc.types.Arg(sgqlc.types.non_null(meta_ai_deployment_type_pk_columns_input), graphql_name='pk_columns', default=None)),
))
    )
    update_meta_ai_environment = sgqlc.types.Field(meta_ai_environment_mutation_response, graphql_name='update_meta_ai_environment', args=sgqlc.types.ArgDict((
        ('_set', sgqlc.types.Arg(meta_ai_environment_set_input, graphql_name='_set', default=None)),
        ('where', sgqlc.types.Arg(sgqlc.types.non_null(meta_ai_environment_bool_exp), graphql_name='where', default=None)),
))
    )
    update_meta_ai_environment_by_pk = sgqlc.types.Field(meta_ai_environment, graphql_name='update_meta_ai_environment_by_pk', args=sgqlc.types.ArgDict((
        ('_set', sgqlc.types.Arg(meta_ai_environment_set_input, graphql_name='_set', default=None)),
        ('pk_columns', sgqlc.types.Arg(sgqlc.types.non_null(meta_ai_environment_pk_columns_input), graphql_name='pk_columns', default=None)),
))
    )
    update_meta_ai_instance = sgqlc.types.Field(meta_ai_instance_mutation_response, graphql_name='update_meta_ai_instance', args=sgqlc.types.ArgDict((
        ('_append', sgqlc.types.Arg(meta_ai_instance_append_input, graphql_name='_append', default=None)),
        ('_delete_at_path', sgqlc.types.Arg(meta_ai_instance_delete_at_path_input, graphql_name='_delete_at_path', default=None)),
        ('_delete_elem', sgqlc.types.Arg(meta_ai_instance_delete_elem_input, graphql_name='_delete_elem', default=None)),
        ('_delete_key', sgqlc.types.Arg(meta_ai_instance_delete_key_input, graphql_name='_delete_key', default=None)),
        ('_inc', sgqlc.types.Arg(meta_ai_instance_inc_input, graphql_name='_inc', default=None)),
        ('_prepend', sgqlc.types.Arg(meta_ai_instance_prepend_input, graphql_name='_prepend', default=None)),
        ('_set', sgqlc.types.Arg(meta_ai_instance_set_input, graphql_name='_set', default=None)),
        ('where', sgqlc.types.Arg(sgqlc.types.non_null(meta_ai_instance_bool_exp), graphql_name='where', default=None)),
))
    )
    update_meta_ai_instance_by_pk = sgqlc.types.Field(meta_ai_instance, graphql_name='update_meta_ai_instance_by_pk', args=sgqlc.types.ArgDict((
        ('_append', sgqlc.types.Arg(meta_ai_instance_append_input, graphql_name='_append', default=None)),
        ('_delete_at_path', sgqlc.types.Arg(meta_ai_instance_delete_at_path_input, graphql_name='_delete_at_path', default=None)),
        ('_delete_elem', sgqlc.types.Arg(meta_ai_instance_delete_elem_input, graphql_name='_delete_elem', default=None)),
        ('_delete_key', sgqlc.types.Arg(meta_ai_instance_delete_key_input, graphql_name='_delete_key', default=None)),
        ('_inc', sgqlc.types.Arg(meta_ai_instance_inc_input, graphql_name='_inc', default=None)),
        ('_prepend', sgqlc.types.Arg(meta_ai_instance_prepend_input, graphql_name='_prepend', default=None)),
        ('_set', sgqlc.types.Arg(meta_ai_instance_set_input, graphql_name='_set', default=None)),
        ('pk_columns', sgqlc.types.Arg(sgqlc.types.non_null(meta_ai_instance_pk_columns_input), graphql_name='pk_columns', default=None)),
))
    )
    update_meta_ai_model = sgqlc.types.Field(meta_ai_model_mutation_response, graphql_name='update_meta_ai_model', args=sgqlc.types.ArgDict((
        ('_append', sgqlc.types.Arg(meta_ai_model_append_input, graphql_name='_append', default=None)),
        ('_delete_at_path', sgqlc.types.Arg(meta_ai_model_delete_at_path_input, graphql_name='_delete_at_path', default=None)),
        ('_delete_elem', sgqlc.types.Arg(meta_ai_model_delete_elem_input, graphql_name='_delete_elem', default=None)),
        ('_delete_key', sgqlc.types.Arg(meta_ai_model_delete_key_input, graphql_name='_delete_key', default=None)),
        ('_inc', sgqlc.types.Arg(meta_ai_model_inc_input, graphql_name='_inc', default=None)),
        ('_prepend', sgqlc.types.Arg(meta_ai_model_prepend_input, graphql_name='_prepend', default=None)),
        ('_set', sgqlc.types.Arg(meta_ai_model_set_input, graphql_name='_set', default=None)),
        ('where', sgqlc.types.Arg(sgqlc.types.non_null(meta_ai_model_bool_exp), graphql_name='where', default=None)),
))
    )
    update_meta_ai_model_by_pk = sgqlc.types.Field(meta_ai_model, graphql_name='update_meta_ai_model_by_pk', args=sgqlc.types.ArgDict((
        ('_append', sgqlc.types.Arg(meta_ai_model_append_input, graphql_name='_append', default=None)),
        ('_delete_at_path', sgqlc.types.Arg(meta_ai_model_delete_at_path_input, graphql_name='_delete_at_path', default=None)),
        ('_delete_elem', sgqlc.types.Arg(meta_ai_model_delete_elem_input, graphql_name='_delete_elem', default=None)),
        ('_delete_key', sgqlc.types.Arg(meta_ai_model_delete_key_input, graphql_name='_delete_key', default=None)),
        ('_inc', sgqlc.types.Arg(meta_ai_model_inc_input, graphql_name='_inc', default=None)),
        ('_prepend', sgqlc.types.Arg(meta_ai_model_prepend_input, graphql_name='_prepend', default=None)),
        ('_set', sgqlc.types.Arg(meta_ai_model_set_input, graphql_name='_set', default=None)),
        ('pk_columns', sgqlc.types.Arg(sgqlc.types.non_null(meta_ai_model_pk_columns_input), graphql_name='pk_columns', default=None)),
))
    )
    update_meta_ai_prediction = sgqlc.types.Field(meta_ai_prediction_mutation_response, graphql_name='update_meta_ai_prediction', args=sgqlc.types.ArgDict((
        ('_inc', sgqlc.types.Arg(meta_ai_prediction_inc_input, graphql_name='_inc', default=None)),
        ('_set', sgqlc.types.Arg(meta_ai_prediction_set_input, graphql_name='_set', default=None)),
        ('where', sgqlc.types.Arg(sgqlc.types.non_null(meta_ai_prediction_bool_exp), graphql_name='where', default=None)),
))
    )
    update_meta_ai_prediction_by_pk = sgqlc.types.Field(meta_ai_prediction, graphql_name='update_meta_ai_prediction_by_pk', args=sgqlc.types.ArgDict((
        ('_inc', sgqlc.types.Arg(meta_ai_prediction_inc_input, graphql_name='_inc', default=None)),
        ('_set', sgqlc.types.Arg(meta_ai_prediction_set_input, graphql_name='_set', default=None)),
        ('pk_columns', sgqlc.types.Arg(sgqlc.types.non_null(meta_ai_prediction_pk_columns_input), graphql_name='pk_columns', default=None)),
))
    )
    update_meta_ai_prediction_state = sgqlc.types.Field(meta_ai_prediction_state_mutation_response, graphql_name='update_meta_ai_prediction_state', args=sgqlc.types.ArgDict((
        ('_set', sgqlc.types.Arg(meta_ai_prediction_state_set_input, graphql_name='_set', default=None)),
        ('where', sgqlc.types.Arg(sgqlc.types.non_null(meta_ai_prediction_state_bool_exp), graphql_name='where', default=None)),
))
    )
    update_meta_ai_prediction_state_by_pk = sgqlc.types.Field(meta_ai_prediction_state, graphql_name='update_meta_ai_prediction_state_by_pk', args=sgqlc.types.ArgDict((
        ('_set', sgqlc.types.Arg(meta_ai_prediction_state_set_input, graphql_name='_set', default=None)),
        ('pk_columns', sgqlc.types.Arg(sgqlc.types.non_null(meta_ai_prediction_state_pk_columns_input), graphql_name='pk_columns', default=None)),
))
    )
    update_meta_ai_visibility = sgqlc.types.Field(meta_ai_visibility_mutation_response, graphql_name='update_meta_ai_visibility', args=sgqlc.types.ArgDict((
        ('_set', sgqlc.types.Arg(meta_ai_visibility_set_input, graphql_name='_set', default=None)),
        ('where', sgqlc.types.Arg(sgqlc.types.non_null(meta_ai_visibility_bool_exp), graphql_name='where', default=None)),
))
    )
    update_meta_ai_visibility_by_pk = sgqlc.types.Field(meta_ai_visibility, graphql_name='update_meta_ai_visibility_by_pk', args=sgqlc.types.ArgDict((
        ('_set', sgqlc.types.Arg(meta_ai_visibility_set_input, graphql_name='_set', default=None)),
        ('pk_columns', sgqlc.types.Arg(sgqlc.types.non_null(meta_ai_visibility_pk_columns_input), graphql_name='pk_columns', default=None)),
))
    )


class query_root(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('get_prelabel', 'meta_ai_app', 'meta_ai_app_aggregate', 'meta_ai_app_by_pk', 'meta_ai_assignment', 'meta_ai_assignment_aggregate', 'meta_ai_assignment_by_pk', 'meta_ai_deployment', 'meta_ai_deployment_aggregate', 'meta_ai_deployment_by_pk', 'meta_ai_deployment_purpose', 'meta_ai_deployment_purpose_aggregate', 'meta_ai_deployment_purpose_by_pk', 'meta_ai_deployment_status', 'meta_ai_deployment_status_aggregate', 'meta_ai_deployment_status_by_pk', 'meta_ai_deployment_type', 'meta_ai_deployment_type_aggregate', 'meta_ai_deployment_type_by_pk', 'meta_ai_environment', 'meta_ai_environment_aggregate', 'meta_ai_environment_by_pk', 'meta_ai_instance', 'meta_ai_instance_aggregate', 'meta_ai_instance_by_pk', 'meta_ai_model', 'meta_ai_model_aggregate', 'meta_ai_model_by_pk', 'meta_ai_prediction', 'meta_ai_prediction_aggregate', 'meta_ai_prediction_by_pk', 'meta_ai_prediction_state', 'meta_ai_prediction_state_aggregate', 'meta_ai_prediction_state_by_pk', 'meta_ai_predictions_by_day', 'meta_ai_predictions_by_day_aggregate', 'meta_ai_visibility', 'meta_ai_visibility_aggregate', 'meta_ai_visibility_by_pk', 'predict_with_deployment', 'request_prediction_of_job', 'resolve_data_ref')
    get_prelabel = sgqlc.types.Field(sgqlc.types.list_of(Prelabel), graphql_name='get_prelabel', args=sgqlc.types.ArgDict((
        ('job_id', sgqlc.types.Arg(bigint, graphql_name='jobId', default=None)),
        ('task_id', sgqlc.types.Arg(bigint, graphql_name='taskId', default=None)),
))
    )
    meta_ai_app = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('meta_ai_app'))), graphql_name='meta_ai_app', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_app_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_app_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_app_bool_exp, graphql_name='where', default=None)),
))
    )
    meta_ai_app_aggregate = sgqlc.types.Field(sgqlc.types.non_null('meta_ai_app_aggregate'), graphql_name='meta_ai_app_aggregate', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_app_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_app_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_app_bool_exp, graphql_name='where', default=None)),
))
    )
    meta_ai_app_by_pk = sgqlc.types.Field('meta_ai_app', graphql_name='meta_ai_app_by_pk', args=sgqlc.types.ArgDict((
        ('assigned', sgqlc.types.Arg(sgqlc.types.non_null(meta_ai_assignment_enum), graphql_name='assigned', default=None)),
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name='id', default=None)),
        ('model_id', sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name='modelId', default=None)),
))
    )
    meta_ai_assignment = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('meta_ai_assignment'))), graphql_name='meta_ai_assignment', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_assignment_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_assignment_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_assignment_bool_exp, graphql_name='where', default=None)),
))
    )
    meta_ai_assignment_aggregate = sgqlc.types.Field(sgqlc.types.non_null('meta_ai_assignment_aggregate'), graphql_name='meta_ai_assignment_aggregate', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_assignment_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_assignment_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_assignment_bool_exp, graphql_name='where', default=None)),
))
    )
    meta_ai_assignment_by_pk = sgqlc.types.Field('meta_ai_assignment', graphql_name='meta_ai_assignment_by_pk', args=sgqlc.types.ArgDict((
        ('type', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='type', default=None)),
))
    )
    meta_ai_deployment = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('meta_ai_deployment'))), graphql_name='meta_ai_deployment', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_deployment_bool_exp, graphql_name='where', default=None)),
))
    )
    meta_ai_deployment_aggregate = sgqlc.types.Field(sgqlc.types.non_null('meta_ai_deployment_aggregate'), graphql_name='meta_ai_deployment_aggregate', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_deployment_bool_exp, graphql_name='where', default=None)),
))
    )
    meta_ai_deployment_by_pk = sgqlc.types.Field('meta_ai_deployment', graphql_name='meta_ai_deployment_by_pk', args=sgqlc.types.ArgDict((
        ('model_id', sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name='modelId', default=None)),
))
    )
    meta_ai_deployment_purpose = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('meta_ai_deployment_purpose'))), graphql_name='meta_ai_deployment_purpose', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_purpose_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_purpose_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_deployment_purpose_bool_exp, graphql_name='where', default=None)),
))
    )
    meta_ai_deployment_purpose_aggregate = sgqlc.types.Field(sgqlc.types.non_null('meta_ai_deployment_purpose_aggregate'), graphql_name='meta_ai_deployment_purpose_aggregate', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_purpose_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_purpose_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_deployment_purpose_bool_exp, graphql_name='where', default=None)),
))
    )
    meta_ai_deployment_purpose_by_pk = sgqlc.types.Field('meta_ai_deployment_purpose', graphql_name='meta_ai_deployment_purpose_by_pk', args=sgqlc.types.ArgDict((
        ('purpose', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='purpose', default=None)),
))
    )
    meta_ai_deployment_status = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('meta_ai_deployment_status'))), graphql_name='meta_ai_deployment_status', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_status_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_status_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_deployment_status_bool_exp, graphql_name='where', default=None)),
))
    )
    meta_ai_deployment_status_aggregate = sgqlc.types.Field(sgqlc.types.non_null('meta_ai_deployment_status_aggregate'), graphql_name='meta_ai_deployment_status_aggregate', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_status_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_status_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_deployment_status_bool_exp, graphql_name='where', default=None)),
))
    )
    meta_ai_deployment_status_by_pk = sgqlc.types.Field('meta_ai_deployment_status', graphql_name='meta_ai_deployment_status_by_pk', args=sgqlc.types.ArgDict((
        ('status', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='status', default=None)),
))
    )
    meta_ai_deployment_type = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('meta_ai_deployment_type'))), graphql_name='meta_ai_deployment_type', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_type_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_type_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_deployment_type_bool_exp, graphql_name='where', default=None)),
))
    )
    meta_ai_deployment_type_aggregate = sgqlc.types.Field(sgqlc.types.non_null('meta_ai_deployment_type_aggregate'), graphql_name='meta_ai_deployment_type_aggregate', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_type_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_type_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_deployment_type_bool_exp, graphql_name='where', default=None)),
))
    )
    meta_ai_deployment_type_by_pk = sgqlc.types.Field('meta_ai_deployment_type', graphql_name='meta_ai_deployment_type_by_pk', args=sgqlc.types.ArgDict((
        ('name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='name', default=None)),
))
    )
    meta_ai_environment = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('meta_ai_environment'))), graphql_name='meta_ai_environment', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_environment_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_environment_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_environment_bool_exp, graphql_name='where', default=None)),
))
    )
    meta_ai_environment_aggregate = sgqlc.types.Field(sgqlc.types.non_null('meta_ai_environment_aggregate'), graphql_name='meta_ai_environment_aggregate', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_environment_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_environment_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_environment_bool_exp, graphql_name='where', default=None)),
))
    )
    meta_ai_environment_by_pk = sgqlc.types.Field('meta_ai_environment', graphql_name='meta_ai_environment_by_pk', args=sgqlc.types.ArgDict((
        ('name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='name', default=None)),
))
    )
    meta_ai_instance = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('meta_ai_instance'))), graphql_name='meta_ai_instance', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_instance_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_instance_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_instance_bool_exp, graphql_name='where', default=None)),
))
    )
    meta_ai_instance_aggregate = sgqlc.types.Field(sgqlc.types.non_null('meta_ai_instance_aggregate'), graphql_name='meta_ai_instance_aggregate', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_instance_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_instance_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_instance_bool_exp, graphql_name='where', default=None)),
))
    )
    meta_ai_instance_by_pk = sgqlc.types.Field('meta_ai_instance', graphql_name='meta_ai_instance_by_pk', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='id', default=None)),
        ('prediction_id', sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name='predictionId', default=None)),
))
    )
    meta_ai_model = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('meta_ai_model'))), graphql_name='meta_ai_model', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_model_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_model_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_model_bool_exp, graphql_name='where', default=None)),
))
    )
    meta_ai_model_aggregate = sgqlc.types.Field(sgqlc.types.non_null('meta_ai_model_aggregate'), graphql_name='meta_ai_model_aggregate', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_model_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_model_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_model_bool_exp, graphql_name='where', default=None)),
))
    )
    meta_ai_model_by_pk = sgqlc.types.Field('meta_ai_model', graphql_name='meta_ai_model_by_pk', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name='id', default=None)),
))
    )
    meta_ai_prediction = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('meta_ai_prediction'))), graphql_name='meta_ai_prediction', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_prediction_bool_exp, graphql_name='where', default=None)),
))
    )
    meta_ai_prediction_aggregate = sgqlc.types.Field(sgqlc.types.non_null('meta_ai_prediction_aggregate'), graphql_name='meta_ai_prediction_aggregate', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_prediction_bool_exp, graphql_name='where', default=None)),
))
    )
    meta_ai_prediction_by_pk = sgqlc.types.Field('meta_ai_prediction', graphql_name='meta_ai_prediction_by_pk', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name='id', default=None)),
))
    )
    meta_ai_prediction_state = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('meta_ai_prediction_state'))), graphql_name='meta_ai_prediction_state', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_state_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_state_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_prediction_state_bool_exp, graphql_name='where', default=None)),
))
    )
    meta_ai_prediction_state_aggregate = sgqlc.types.Field(sgqlc.types.non_null('meta_ai_prediction_state_aggregate'), graphql_name='meta_ai_prediction_state_aggregate', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_state_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_state_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_prediction_state_bool_exp, graphql_name='where', default=None)),
))
    )
    meta_ai_prediction_state_by_pk = sgqlc.types.Field('meta_ai_prediction_state', graphql_name='meta_ai_prediction_state_by_pk', args=sgqlc.types.ArgDict((
        ('state', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='state', default=None)),
))
    )
    meta_ai_predictions_by_day = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('meta_ai_predictions_by_day'))), graphql_name='meta_ai_predictions_by_day', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_predictions_by_day_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_predictions_by_day_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_predictions_by_day_bool_exp, graphql_name='where', default=None)),
))
    )
    meta_ai_predictions_by_day_aggregate = sgqlc.types.Field(sgqlc.types.non_null('meta_ai_predictions_by_day_aggregate'), graphql_name='meta_ai_predictions_by_day_aggregate', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_predictions_by_day_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_predictions_by_day_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_predictions_by_day_bool_exp, graphql_name='where', default=None)),
))
    )
    meta_ai_visibility = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('meta_ai_visibility'))), graphql_name='meta_ai_visibility', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_visibility_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_visibility_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_visibility_bool_exp, graphql_name='where', default=None)),
))
    )
    meta_ai_visibility_aggregate = sgqlc.types.Field(sgqlc.types.non_null('meta_ai_visibility_aggregate'), graphql_name='meta_ai_visibility_aggregate', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_visibility_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_visibility_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_visibility_bool_exp, graphql_name='where', default=None)),
))
    )
    meta_ai_visibility_by_pk = sgqlc.types.Field('meta_ai_visibility', graphql_name='meta_ai_visibility_by_pk', args=sgqlc.types.ArgDict((
        ('type', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='type', default=None)),
))
    )
    predict_with_deployment = sgqlc.types.Field(sgqlc.types.list_of(RawPrediction), graphql_name='predict_with_deployment', args=sgqlc.types.ArgDict((
        ('request', sgqlc.types.Arg(PredictionRequest, graphql_name='request', default=None)),
))
    )
    request_prediction_of_job = sgqlc.types.Field(sgqlc.types.list_of(Prediction), graphql_name='request_prediction_of_job', args=sgqlc.types.ArgDict((
        ('app_id', sgqlc.types.Arg(uuid, graphql_name='app_id', default=None)),
        ('assignment', sgqlc.types.Arg(String, graphql_name='assignment', default=None)),
        ('job_id', sgqlc.types.Arg(bigint, graphql_name='job_id', default=None)),
))
    )
    resolve_data_ref = sgqlc.types.Field(URL, graphql_name='resolve_data_ref', args=sgqlc.types.ArgDict((
        ('data_ref', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='data_ref', default=None)),
        ('instance_id', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='instance_id', default=None)),
        ('prediction_id', sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name='prediction_id', default=None)),
))
    )


class subscription_root(sgqlc.types.Type):
    __schema__ = meta_ai_graphql_schema
    __field_names__ = ('get_prelabel', 'meta_ai_app', 'meta_ai_app_aggregate', 'meta_ai_app_by_pk', 'meta_ai_assignment', 'meta_ai_assignment_aggregate', 'meta_ai_assignment_by_pk', 'meta_ai_deployment', 'meta_ai_deployment_aggregate', 'meta_ai_deployment_by_pk', 'meta_ai_deployment_purpose', 'meta_ai_deployment_purpose_aggregate', 'meta_ai_deployment_purpose_by_pk', 'meta_ai_deployment_status', 'meta_ai_deployment_status_aggregate', 'meta_ai_deployment_status_by_pk', 'meta_ai_deployment_type', 'meta_ai_deployment_type_aggregate', 'meta_ai_deployment_type_by_pk', 'meta_ai_environment', 'meta_ai_environment_aggregate', 'meta_ai_environment_by_pk', 'meta_ai_instance', 'meta_ai_instance_aggregate', 'meta_ai_instance_by_pk', 'meta_ai_model', 'meta_ai_model_aggregate', 'meta_ai_model_by_pk', 'meta_ai_prediction', 'meta_ai_prediction_aggregate', 'meta_ai_prediction_by_pk', 'meta_ai_prediction_state', 'meta_ai_prediction_state_aggregate', 'meta_ai_prediction_state_by_pk', 'meta_ai_predictions_by_day', 'meta_ai_predictions_by_day_aggregate', 'meta_ai_visibility', 'meta_ai_visibility_aggregate', 'meta_ai_visibility_by_pk', 'predict_with_deployment', 'request_prediction_of_job', 'resolve_data_ref')
    get_prelabel = sgqlc.types.Field(sgqlc.types.list_of(Prelabel), graphql_name='get_prelabel', args=sgqlc.types.ArgDict((
        ('job_id', sgqlc.types.Arg(bigint, graphql_name='jobId', default=None)),
        ('task_id', sgqlc.types.Arg(bigint, graphql_name='taskId', default=None)),
))
    )
    meta_ai_app = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('meta_ai_app'))), graphql_name='meta_ai_app', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_app_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_app_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_app_bool_exp, graphql_name='where', default=None)),
))
    )
    meta_ai_app_aggregate = sgqlc.types.Field(sgqlc.types.non_null('meta_ai_app_aggregate'), graphql_name='meta_ai_app_aggregate', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_app_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_app_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_app_bool_exp, graphql_name='where', default=None)),
))
    )
    meta_ai_app_by_pk = sgqlc.types.Field('meta_ai_app', graphql_name='meta_ai_app_by_pk', args=sgqlc.types.ArgDict((
        ('assigned', sgqlc.types.Arg(sgqlc.types.non_null(meta_ai_assignment_enum), graphql_name='assigned', default=None)),
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name='id', default=None)),
        ('model_id', sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name='modelId', default=None)),
))
    )
    meta_ai_assignment = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('meta_ai_assignment'))), graphql_name='meta_ai_assignment', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_assignment_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_assignment_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_assignment_bool_exp, graphql_name='where', default=None)),
))
    )
    meta_ai_assignment_aggregate = sgqlc.types.Field(sgqlc.types.non_null('meta_ai_assignment_aggregate'), graphql_name='meta_ai_assignment_aggregate', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_assignment_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_assignment_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_assignment_bool_exp, graphql_name='where', default=None)),
))
    )
    meta_ai_assignment_by_pk = sgqlc.types.Field('meta_ai_assignment', graphql_name='meta_ai_assignment_by_pk', args=sgqlc.types.ArgDict((
        ('type', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='type', default=None)),
))
    )
    meta_ai_deployment = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('meta_ai_deployment'))), graphql_name='meta_ai_deployment', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_deployment_bool_exp, graphql_name='where', default=None)),
))
    )
    meta_ai_deployment_aggregate = sgqlc.types.Field(sgqlc.types.non_null('meta_ai_deployment_aggregate'), graphql_name='meta_ai_deployment_aggregate', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_deployment_bool_exp, graphql_name='where', default=None)),
))
    )
    meta_ai_deployment_by_pk = sgqlc.types.Field('meta_ai_deployment', graphql_name='meta_ai_deployment_by_pk', args=sgqlc.types.ArgDict((
        ('model_id', sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name='modelId', default=None)),
))
    )
    meta_ai_deployment_purpose = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('meta_ai_deployment_purpose'))), graphql_name='meta_ai_deployment_purpose', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_purpose_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_purpose_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_deployment_purpose_bool_exp, graphql_name='where', default=None)),
))
    )
    meta_ai_deployment_purpose_aggregate = sgqlc.types.Field(sgqlc.types.non_null('meta_ai_deployment_purpose_aggregate'), graphql_name='meta_ai_deployment_purpose_aggregate', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_purpose_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_purpose_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_deployment_purpose_bool_exp, graphql_name='where', default=None)),
))
    )
    meta_ai_deployment_purpose_by_pk = sgqlc.types.Field('meta_ai_deployment_purpose', graphql_name='meta_ai_deployment_purpose_by_pk', args=sgqlc.types.ArgDict((
        ('purpose', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='purpose', default=None)),
))
    )
    meta_ai_deployment_status = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('meta_ai_deployment_status'))), graphql_name='meta_ai_deployment_status', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_status_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_status_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_deployment_status_bool_exp, graphql_name='where', default=None)),
))
    )
    meta_ai_deployment_status_aggregate = sgqlc.types.Field(sgqlc.types.non_null('meta_ai_deployment_status_aggregate'), graphql_name='meta_ai_deployment_status_aggregate', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_status_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_status_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_deployment_status_bool_exp, graphql_name='where', default=None)),
))
    )
    meta_ai_deployment_status_by_pk = sgqlc.types.Field('meta_ai_deployment_status', graphql_name='meta_ai_deployment_status_by_pk', args=sgqlc.types.ArgDict((
        ('status', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='status', default=None)),
))
    )
    meta_ai_deployment_type = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('meta_ai_deployment_type'))), graphql_name='meta_ai_deployment_type', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_type_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_type_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_deployment_type_bool_exp, graphql_name='where', default=None)),
))
    )
    meta_ai_deployment_type_aggregate = sgqlc.types.Field(sgqlc.types.non_null('meta_ai_deployment_type_aggregate'), graphql_name='meta_ai_deployment_type_aggregate', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_type_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_deployment_type_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_deployment_type_bool_exp, graphql_name='where', default=None)),
))
    )
    meta_ai_deployment_type_by_pk = sgqlc.types.Field('meta_ai_deployment_type', graphql_name='meta_ai_deployment_type_by_pk', args=sgqlc.types.ArgDict((
        ('name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='name', default=None)),
))
    )
    meta_ai_environment = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('meta_ai_environment'))), graphql_name='meta_ai_environment', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_environment_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_environment_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_environment_bool_exp, graphql_name='where', default=None)),
))
    )
    meta_ai_environment_aggregate = sgqlc.types.Field(sgqlc.types.non_null('meta_ai_environment_aggregate'), graphql_name='meta_ai_environment_aggregate', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_environment_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_environment_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_environment_bool_exp, graphql_name='where', default=None)),
))
    )
    meta_ai_environment_by_pk = sgqlc.types.Field('meta_ai_environment', graphql_name='meta_ai_environment_by_pk', args=sgqlc.types.ArgDict((
        ('name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='name', default=None)),
))
    )
    meta_ai_instance = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('meta_ai_instance'))), graphql_name='meta_ai_instance', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_instance_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_instance_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_instance_bool_exp, graphql_name='where', default=None)),
))
    )
    meta_ai_instance_aggregate = sgqlc.types.Field(sgqlc.types.non_null('meta_ai_instance_aggregate'), graphql_name='meta_ai_instance_aggregate', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_instance_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_instance_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_instance_bool_exp, graphql_name='where', default=None)),
))
    )
    meta_ai_instance_by_pk = sgqlc.types.Field('meta_ai_instance', graphql_name='meta_ai_instance_by_pk', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='id', default=None)),
        ('prediction_id', sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name='predictionId', default=None)),
))
    )
    meta_ai_model = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('meta_ai_model'))), graphql_name='meta_ai_model', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_model_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_model_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_model_bool_exp, graphql_name='where', default=None)),
))
    )
    meta_ai_model_aggregate = sgqlc.types.Field(sgqlc.types.non_null('meta_ai_model_aggregate'), graphql_name='meta_ai_model_aggregate', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_model_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_model_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_model_bool_exp, graphql_name='where', default=None)),
))
    )
    meta_ai_model_by_pk = sgqlc.types.Field('meta_ai_model', graphql_name='meta_ai_model_by_pk', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name='id', default=None)),
))
    )
    meta_ai_prediction = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('meta_ai_prediction'))), graphql_name='meta_ai_prediction', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_prediction_bool_exp, graphql_name='where', default=None)),
))
    )
    meta_ai_prediction_aggregate = sgqlc.types.Field(sgqlc.types.non_null('meta_ai_prediction_aggregate'), graphql_name='meta_ai_prediction_aggregate', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_prediction_bool_exp, graphql_name='where', default=None)),
))
    )
    meta_ai_prediction_by_pk = sgqlc.types.Field('meta_ai_prediction', graphql_name='meta_ai_prediction_by_pk', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name='id', default=None)),
))
    )
    meta_ai_prediction_state = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('meta_ai_prediction_state'))), graphql_name='meta_ai_prediction_state', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_state_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_state_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_prediction_state_bool_exp, graphql_name='where', default=None)),
))
    )
    meta_ai_prediction_state_aggregate = sgqlc.types.Field(sgqlc.types.non_null('meta_ai_prediction_state_aggregate'), graphql_name='meta_ai_prediction_state_aggregate', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_state_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_state_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_prediction_state_bool_exp, graphql_name='where', default=None)),
))
    )
    meta_ai_prediction_state_by_pk = sgqlc.types.Field('meta_ai_prediction_state', graphql_name='meta_ai_prediction_state_by_pk', args=sgqlc.types.ArgDict((
        ('state', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='state', default=None)),
))
    )
    meta_ai_predictions_by_day = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('meta_ai_predictions_by_day'))), graphql_name='meta_ai_predictions_by_day', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_predictions_by_day_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_predictions_by_day_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_predictions_by_day_bool_exp, graphql_name='where', default=None)),
))
    )
    meta_ai_predictions_by_day_aggregate = sgqlc.types.Field(sgqlc.types.non_null('meta_ai_predictions_by_day_aggregate'), graphql_name='meta_ai_predictions_by_day_aggregate', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_predictions_by_day_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_predictions_by_day_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_predictions_by_day_bool_exp, graphql_name='where', default=None)),
))
    )
    meta_ai_visibility = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('meta_ai_visibility'))), graphql_name='meta_ai_visibility', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_visibility_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_visibility_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_visibility_bool_exp, graphql_name='where', default=None)),
))
    )
    meta_ai_visibility_aggregate = sgqlc.types.Field(sgqlc.types.non_null('meta_ai_visibility_aggregate'), graphql_name='meta_ai_visibility_aggregate', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_visibility_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_visibility_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_visibility_bool_exp, graphql_name='where', default=None)),
))
    )
    meta_ai_visibility_by_pk = sgqlc.types.Field('meta_ai_visibility', graphql_name='meta_ai_visibility_by_pk', args=sgqlc.types.ArgDict((
        ('type', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='type', default=None)),
))
    )
    predict_with_deployment = sgqlc.types.Field(sgqlc.types.list_of(RawPrediction), graphql_name='predict_with_deployment', args=sgqlc.types.ArgDict((
        ('request', sgqlc.types.Arg(PredictionRequest, graphql_name='request', default=None)),
))
    )
    request_prediction_of_job = sgqlc.types.Field(sgqlc.types.list_of(Prediction), graphql_name='request_prediction_of_job', args=sgqlc.types.ArgDict((
        ('app_id', sgqlc.types.Arg(uuid, graphql_name='app_id', default=None)),
        ('assignment', sgqlc.types.Arg(String, graphql_name='assignment', default=None)),
        ('job_id', sgqlc.types.Arg(bigint, graphql_name='job_id', default=None)),
))
    )
    resolve_data_ref = sgqlc.types.Field(URL, graphql_name='resolve_data_ref', args=sgqlc.types.ArgDict((
        ('data_ref', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='data_ref', default=None)),
        ('instance_id', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='instance_id', default=None)),
        ('prediction_id', sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name='prediction_id', default=None)),
))
    )



########################################################################
# Unions
########################################################################

########################################################################
# Schema Entry Points
########################################################################
meta_ai_graphql_schema.query_type = query_root
meta_ai_graphql_schema.mutation_type = mutation_root
meta_ai_graphql_schema.subscription_type = subscription_root

