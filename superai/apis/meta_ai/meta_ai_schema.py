import sgqlc.types


meta_ai_schema = sgqlc.types.Schema()



########################################################################
# Scalars and Enumerations
########################################################################
Boolean = sgqlc.types.Boolean

Float = sgqlc.types.Float

ID = sgqlc.types.ID

Int = sgqlc.types.Int

String = sgqlc.types.String

class bigint(sgqlc.types.Scalar):
    __schema__ = meta_ai_schema


class float8(sgqlc.types.Scalar):
    __schema__ = meta_ai_schema


class json(sgqlc.types.Scalar):
    __schema__ = meta_ai_schema


class jsonb(sgqlc.types.Scalar):
    __schema__ = meta_ai_schema


class meta_ai_app_constraint(sgqlc.types.Enum):
    __schema__ = meta_ai_schema
    __choices__ = ('app_modelId_id_assigned_key', 'app_pkey')


class meta_ai_app_select_column(sgqlc.types.Enum):
    __schema__ = meta_ai_schema
    __choices__ = ('active', 'assigned', 'id', 'modelId')


class meta_ai_app_update_column(sgqlc.types.Enum):
    __schema__ = meta_ai_schema
    __choices__ = ('active', 'assigned', 'modelId')


class meta_ai_assignment_enum(sgqlc.types.Enum):
    __schema__ = meta_ai_schema
    __choices__ = ('ACTIVE_LEARNING', 'PRELABEL')


class meta_ai_assignment_select_column(sgqlc.types.Enum):
    __schema__ = meta_ai_schema
    __choices__ = ('type',)


class meta_ai_instance_constraint(sgqlc.types.Enum):
    __schema__ = meta_ai_schema
    __choices__ = ('instance_pkey',)


class meta_ai_instance_select_column(sgqlc.types.Enum):
    __schema__ = meta_ai_schema
    __choices__ = ('id', 'output', 'predictionId', 'score')


class meta_ai_instance_update_column(sgqlc.types.Enum):
    __schema__ = meta_ai_schema
    __choices__ = ('output', 'score')


class meta_ai_model_constraint(sgqlc.types.Enum):
    __schema__ = meta_ai_schema
    __choices__ = ('model_name_ownerId_version_key', 'model_pkey')


class meta_ai_model_select_column(sgqlc.types.Enum):
    __schema__ = meta_ai_schema
    __choices__ = ('createdAt', 'description', 'endpoint', 'id', 'metadata', 'name', 'updatedAt', 'version', 'visibility')


class meta_ai_model_update_column(sgqlc.types.Enum):
    __schema__ = meta_ai_schema
    __choices__ = ('description', 'endpoint', 'metadata', 'name', 'version', 'visibility')


class meta_ai_prediction_select_column(sgqlc.types.Enum):
    __schema__ = meta_ai_schema
    __choices__ = ('appId', 'createdAt', 'id', 'jobId', 'modelId', 'taskId', 'type')


class meta_ai_visibility_enum(sgqlc.types.Enum):
    __schema__ = meta_ai_schema
    __choices__ = ('PRIVATE', 'PUBLIC')


class meta_ai_visibility_select_column(sgqlc.types.Enum):
    __schema__ = meta_ai_schema
    __choices__ = ('type',)


class order_by(sgqlc.types.Enum):
    __schema__ = meta_ai_schema
    __choices__ = ('asc', 'asc_nulls_first', 'asc_nulls_last', 'desc', 'desc_nulls_first', 'desc_nulls_last')


class timestamptz(sgqlc.types.Scalar):
    __schema__ = meta_ai_schema


class uuid(sgqlc.types.Scalar):
    __schema__ = meta_ai_schema



########################################################################
# Input Objects
########################################################################
class Boolean_comparison_exp(sgqlc.types.Input):
    __schema__ = meta_ai_schema
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
    __schema__ = meta_ai_schema
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


class String_comparison_exp(sgqlc.types.Input):
    __schema__ = meta_ai_schema
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
    __schema__ = meta_ai_schema
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


class float8_comparison_exp(sgqlc.types.Input):
    __schema__ = meta_ai_schema
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


class jsonb_comparison_exp(sgqlc.types.Input):
    __schema__ = meta_ai_schema
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


class meta_ai_app_arr_rel_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_schema
    __field_names__ = ('data', 'on_conflict')
    data = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('meta_ai_app_insert_input'))), graphql_name='data')
    on_conflict = sgqlc.types.Field('meta_ai_app_on_conflict', graphql_name='on_conflict')


class meta_ai_app_bool_exp(sgqlc.types.Input):
    __schema__ = meta_ai_schema
    __field_names__ = ('_and', '_not', '_or', 'active', 'assigned', 'assignment', 'id', 'model', 'model_id', 'predictions')
    _and = sgqlc.types.Field(sgqlc.types.list_of('meta_ai_app_bool_exp'), graphql_name='_and')
    _not = sgqlc.types.Field('meta_ai_app_bool_exp', graphql_name='_not')
    _or = sgqlc.types.Field(sgqlc.types.list_of('meta_ai_app_bool_exp'), graphql_name='_or')
    active = sgqlc.types.Field(Boolean_comparison_exp, graphql_name='active')
    assigned = sgqlc.types.Field('meta_ai_assignment_enum_comparison_exp', graphql_name='assigned')
    assignment = sgqlc.types.Field('meta_ai_assignment_bool_exp', graphql_name='assignment')
    id = sgqlc.types.Field('uuid_comparison_exp', graphql_name='id')
    model = sgqlc.types.Field('meta_ai_model_bool_exp', graphql_name='model')
    model_id = sgqlc.types.Field('uuid_comparison_exp', graphql_name='modelId')
    predictions = sgqlc.types.Field('meta_ai_prediction_bool_exp', graphql_name='predictions')


class meta_ai_app_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_schema
    __field_names__ = ('active', 'assigned', 'id', 'model', 'model_id', 'predictions')
    active = sgqlc.types.Field(Boolean, graphql_name='active')
    assigned = sgqlc.types.Field(meta_ai_assignment_enum, graphql_name='assigned')
    id = sgqlc.types.Field(uuid, graphql_name='id')
    model = sgqlc.types.Field('meta_ai_model_obj_rel_insert_input', graphql_name='model')
    model_id = sgqlc.types.Field(uuid, graphql_name='modelId')
    predictions = sgqlc.types.Field('meta_ai_prediction_arr_rel_insert_input', graphql_name='predictions')


class meta_ai_app_obj_rel_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_schema
    __field_names__ = ('data', 'on_conflict')
    data = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_app_insert_input), graphql_name='data')
    on_conflict = sgqlc.types.Field('meta_ai_app_on_conflict', graphql_name='on_conflict')


class meta_ai_app_on_conflict(sgqlc.types.Input):
    __schema__ = meta_ai_schema
    __field_names__ = ('constraint', 'update_columns', 'where')
    constraint = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_app_constraint), graphql_name='constraint')
    update_columns = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_app_update_column))), graphql_name='update_columns')
    where = sgqlc.types.Field(meta_ai_app_bool_exp, graphql_name='where')


class meta_ai_app_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_schema
    __field_names__ = ('active', 'assigned', 'assignment', 'id', 'model', 'model_id')
    active = sgqlc.types.Field(order_by, graphql_name='active')
    assigned = sgqlc.types.Field(order_by, graphql_name='assigned')
    assignment = sgqlc.types.Field('meta_ai_assignment_order_by', graphql_name='assignment')
    id = sgqlc.types.Field(order_by, graphql_name='id')
    model = sgqlc.types.Field('meta_ai_model_order_by', graphql_name='model')
    model_id = sgqlc.types.Field(order_by, graphql_name='modelId')


class meta_ai_app_pk_columns_input(sgqlc.types.Input):
    __schema__ = meta_ai_schema
    __field_names__ = ('assigned', 'id', 'model_id')
    assigned = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_assignment_enum), graphql_name='assigned')
    id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name='id')
    model_id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name='modelId')


class meta_ai_app_set_input(sgqlc.types.Input):
    __schema__ = meta_ai_schema
    __field_names__ = ('active', 'assigned', 'model_id')
    active = sgqlc.types.Field(Boolean, graphql_name='active')
    assigned = sgqlc.types.Field(meta_ai_assignment_enum, graphql_name='assigned')
    model_id = sgqlc.types.Field(uuid, graphql_name='modelId')


class meta_ai_assignment_bool_exp(sgqlc.types.Input):
    __schema__ = meta_ai_schema
    __field_names__ = ('_and', '_not', '_or', 'apps', 'type')
    _and = sgqlc.types.Field(sgqlc.types.list_of('meta_ai_assignment_bool_exp'), graphql_name='_and')
    _not = sgqlc.types.Field('meta_ai_assignment_bool_exp', graphql_name='_not')
    _or = sgqlc.types.Field(sgqlc.types.list_of('meta_ai_assignment_bool_exp'), graphql_name='_or')
    apps = sgqlc.types.Field(meta_ai_app_bool_exp, graphql_name='apps')
    type = sgqlc.types.Field(String_comparison_exp, graphql_name='type')


class meta_ai_assignment_enum_comparison_exp(sgqlc.types.Input):
    __schema__ = meta_ai_schema
    __field_names__ = ('_eq', '_in', '_is_null', '_neq', '_nin')
    _eq = sgqlc.types.Field(meta_ai_assignment_enum, graphql_name='_eq')
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_assignment_enum)), graphql_name='_in')
    _is_null = sgqlc.types.Field(Boolean, graphql_name='_is_null')
    _neq = sgqlc.types.Field(meta_ai_assignment_enum, graphql_name='_neq')
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_assignment_enum)), graphql_name='_nin')


class meta_ai_assignment_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_schema
    __field_names__ = ('type',)
    type = sgqlc.types.Field(order_by, graphql_name='type')


class meta_ai_assignment_pk_columns_input(sgqlc.types.Input):
    __schema__ = meta_ai_schema
    __field_names__ = ('type',)
    type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='type')


class meta_ai_instance_append_input(sgqlc.types.Input):
    __schema__ = meta_ai_schema
    __field_names__ = ('output',)
    output = sgqlc.types.Field(jsonb, graphql_name='output')


class meta_ai_instance_arr_rel_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_schema
    __field_names__ = ('data', 'on_conflict')
    data = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('meta_ai_instance_insert_input'))), graphql_name='data')
    on_conflict = sgqlc.types.Field('meta_ai_instance_on_conflict', graphql_name='on_conflict')


class meta_ai_instance_bool_exp(sgqlc.types.Input):
    __schema__ = meta_ai_schema
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
    __schema__ = meta_ai_schema
    __field_names__ = ('output',)
    output = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='output')


class meta_ai_instance_delete_elem_input(sgqlc.types.Input):
    __schema__ = meta_ai_schema
    __field_names__ = ('output',)
    output = sgqlc.types.Field(Int, graphql_name='output')


class meta_ai_instance_delete_key_input(sgqlc.types.Input):
    __schema__ = meta_ai_schema
    __field_names__ = ('output',)
    output = sgqlc.types.Field(String, graphql_name='output')


class meta_ai_instance_inc_input(sgqlc.types.Input):
    __schema__ = meta_ai_schema
    __field_names__ = ('score',)
    score = sgqlc.types.Field(float8, graphql_name='score')


class meta_ai_instance_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_schema
    __field_names__ = ('output', 'prediction', 'prediction_id', 'score')
    output = sgqlc.types.Field(jsonb, graphql_name='output')
    prediction = sgqlc.types.Field('meta_ai_prediction_obj_rel_insert_input', graphql_name='prediction')
    prediction_id = sgqlc.types.Field(uuid, graphql_name='predictionId')
    score = sgqlc.types.Field(float8, graphql_name='score')


class meta_ai_instance_obj_rel_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_schema
    __field_names__ = ('data', 'on_conflict')
    data = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_instance_insert_input), graphql_name='data')
    on_conflict = sgqlc.types.Field('meta_ai_instance_on_conflict', graphql_name='on_conflict')


class meta_ai_instance_on_conflict(sgqlc.types.Input):
    __schema__ = meta_ai_schema
    __field_names__ = ('constraint', 'update_columns', 'where')
    constraint = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_instance_constraint), graphql_name='constraint')
    update_columns = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_instance_update_column))), graphql_name='update_columns')
    where = sgqlc.types.Field(meta_ai_instance_bool_exp, graphql_name='where')


class meta_ai_instance_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_schema
    __field_names__ = ('id', 'output', 'prediction', 'prediction_id', 'score')
    id = sgqlc.types.Field(order_by, graphql_name='id')
    output = sgqlc.types.Field(order_by, graphql_name='output')
    prediction = sgqlc.types.Field('meta_ai_prediction_order_by', graphql_name='prediction')
    prediction_id = sgqlc.types.Field(order_by, graphql_name='predictionId')
    score = sgqlc.types.Field(order_by, graphql_name='score')


class meta_ai_instance_pk_columns_input(sgqlc.types.Input):
    __schema__ = meta_ai_schema
    __field_names__ = ('id', 'prediction_id')
    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='id')
    prediction_id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name='predictionId')


class meta_ai_instance_prepend_input(sgqlc.types.Input):
    __schema__ = meta_ai_schema
    __field_names__ = ('output',)
    output = sgqlc.types.Field(jsonb, graphql_name='output')


class meta_ai_instance_set_input(sgqlc.types.Input):
    __schema__ = meta_ai_schema
    __field_names__ = ('output', 'score')
    output = sgqlc.types.Field(jsonb, graphql_name='output')
    score = sgqlc.types.Field(float8, graphql_name='score')


class meta_ai_model_append_input(sgqlc.types.Input):
    __schema__ = meta_ai_schema
    __field_names__ = ('metadata',)
    metadata = sgqlc.types.Field(jsonb, graphql_name='metadata')


class meta_ai_model_arr_rel_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_schema
    __field_names__ = ('data', 'on_conflict')
    data = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('meta_ai_model_insert_input'))), graphql_name='data')
    on_conflict = sgqlc.types.Field('meta_ai_model_on_conflict', graphql_name='on_conflict')


class meta_ai_model_bool_exp(sgqlc.types.Input):
    __schema__ = meta_ai_schema
    __field_names__ = ('_and', '_not', '_or', 'apps', 'created_at', 'description', 'endpoint', 'id', 'metadata', 'name', 'predictions', 'updated_at', 'version', 'visibility', 'visibility_by_visibility')
    _and = sgqlc.types.Field(sgqlc.types.list_of('meta_ai_model_bool_exp'), graphql_name='_and')
    _not = sgqlc.types.Field('meta_ai_model_bool_exp', graphql_name='_not')
    _or = sgqlc.types.Field(sgqlc.types.list_of('meta_ai_model_bool_exp'), graphql_name='_or')
    apps = sgqlc.types.Field(meta_ai_app_bool_exp, graphql_name='apps')
    created_at = sgqlc.types.Field('timestamptz_comparison_exp', graphql_name='createdAt')
    description = sgqlc.types.Field(String_comparison_exp, graphql_name='description')
    endpoint = sgqlc.types.Field(String_comparison_exp, graphql_name='endpoint')
    id = sgqlc.types.Field('uuid_comparison_exp', graphql_name='id')
    metadata = sgqlc.types.Field(jsonb_comparison_exp, graphql_name='metadata')
    name = sgqlc.types.Field(String_comparison_exp, graphql_name='name')
    predictions = sgqlc.types.Field('meta_ai_prediction_bool_exp', graphql_name='predictions')
    updated_at = sgqlc.types.Field('timestamptz_comparison_exp', graphql_name='updatedAt')
    version = sgqlc.types.Field(Int_comparison_exp, graphql_name='version')
    visibility = sgqlc.types.Field('meta_ai_visibility_enum_comparison_exp', graphql_name='visibility')
    visibility_by_visibility = sgqlc.types.Field('meta_ai_visibility_bool_exp', graphql_name='visibilityByVisibility')


class meta_ai_model_delete_at_path_input(sgqlc.types.Input):
    __schema__ = meta_ai_schema
    __field_names__ = ('metadata',)
    metadata = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='metadata')


class meta_ai_model_delete_elem_input(sgqlc.types.Input):
    __schema__ = meta_ai_schema
    __field_names__ = ('metadata',)
    metadata = sgqlc.types.Field(Int, graphql_name='metadata')


class meta_ai_model_delete_key_input(sgqlc.types.Input):
    __schema__ = meta_ai_schema
    __field_names__ = ('metadata',)
    metadata = sgqlc.types.Field(String, graphql_name='metadata')


class meta_ai_model_inc_input(sgqlc.types.Input):
    __schema__ = meta_ai_schema
    __field_names__ = ('version',)
    version = sgqlc.types.Field(Int, graphql_name='version')


class meta_ai_model_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_schema
    __field_names__ = ('apps', 'description', 'endpoint', 'metadata', 'name', 'predictions', 'version', 'visibility')
    apps = sgqlc.types.Field(meta_ai_app_arr_rel_insert_input, graphql_name='apps')
    description = sgqlc.types.Field(String, graphql_name='description')
    endpoint = sgqlc.types.Field(String, graphql_name='endpoint')
    metadata = sgqlc.types.Field(jsonb, graphql_name='metadata')
    name = sgqlc.types.Field(String, graphql_name='name')
    predictions = sgqlc.types.Field('meta_ai_prediction_arr_rel_insert_input', graphql_name='predictions')
    version = sgqlc.types.Field(Int, graphql_name='version')
    visibility = sgqlc.types.Field(meta_ai_visibility_enum, graphql_name='visibility')


class meta_ai_model_obj_rel_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_schema
    __field_names__ = ('data', 'on_conflict')
    data = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_model_insert_input), graphql_name='data')
    on_conflict = sgqlc.types.Field('meta_ai_model_on_conflict', graphql_name='on_conflict')


class meta_ai_model_on_conflict(sgqlc.types.Input):
    __schema__ = meta_ai_schema
    __field_names__ = ('constraint', 'update_columns', 'where')
    constraint = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_model_constraint), graphql_name='constraint')
    update_columns = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_model_update_column))), graphql_name='update_columns')
    where = sgqlc.types.Field(meta_ai_model_bool_exp, graphql_name='where')


class meta_ai_model_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_schema
    __field_names__ = ('created_at', 'description', 'endpoint', 'id', 'metadata', 'name', 'updated_at', 'version', 'visibility', 'visibility_by_visibility')
    created_at = sgqlc.types.Field(order_by, graphql_name='createdAt')
    description = sgqlc.types.Field(order_by, graphql_name='description')
    endpoint = sgqlc.types.Field(order_by, graphql_name='endpoint')
    id = sgqlc.types.Field(order_by, graphql_name='id')
    metadata = sgqlc.types.Field(order_by, graphql_name='metadata')
    name = sgqlc.types.Field(order_by, graphql_name='name')
    updated_at = sgqlc.types.Field(order_by, graphql_name='updatedAt')
    version = sgqlc.types.Field(order_by, graphql_name='version')
    visibility = sgqlc.types.Field(order_by, graphql_name='visibility')
    visibility_by_visibility = sgqlc.types.Field('meta_ai_visibility_order_by', graphql_name='visibilityByVisibility')


class meta_ai_model_pk_columns_input(sgqlc.types.Input):
    __schema__ = meta_ai_schema
    __field_names__ = ('id',)
    id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name='id')


class meta_ai_model_prepend_input(sgqlc.types.Input):
    __schema__ = meta_ai_schema
    __field_names__ = ('metadata',)
    metadata = sgqlc.types.Field(jsonb, graphql_name='metadata')


class meta_ai_model_set_input(sgqlc.types.Input):
    __schema__ = meta_ai_schema
    __field_names__ = ('description', 'endpoint', 'metadata', 'name', 'version', 'visibility')
    description = sgqlc.types.Field(String, graphql_name='description')
    endpoint = sgqlc.types.Field(String, graphql_name='endpoint')
    metadata = sgqlc.types.Field(jsonb, graphql_name='metadata')
    name = sgqlc.types.Field(String, graphql_name='name')
    version = sgqlc.types.Field(Int, graphql_name='version')
    visibility = sgqlc.types.Field(meta_ai_visibility_enum, graphql_name='visibility')


class meta_ai_prediction_arr_rel_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_schema
    __field_names__ = ('data',)
    data = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('meta_ai_prediction_insert_input'))), graphql_name='data')


class meta_ai_prediction_bool_exp(sgqlc.types.Input):
    __schema__ = meta_ai_schema
    __field_names__ = ('_and', '_not', '_or', 'app_id', 'created_at', 'id', 'instances', 'job_id', 'model', 'model_id', 'task_id', 'type')
    _and = sgqlc.types.Field(sgqlc.types.list_of('meta_ai_prediction_bool_exp'), graphql_name='_and')
    _not = sgqlc.types.Field('meta_ai_prediction_bool_exp', graphql_name='_not')
    _or = sgqlc.types.Field(sgqlc.types.list_of('meta_ai_prediction_bool_exp'), graphql_name='_or')
    app_id = sgqlc.types.Field('uuid_comparison_exp', graphql_name='appId')
    created_at = sgqlc.types.Field('timestamptz_comparison_exp', graphql_name='createdAt')
    id = sgqlc.types.Field('uuid_comparison_exp', graphql_name='id')
    instances = sgqlc.types.Field(meta_ai_instance_bool_exp, graphql_name='instances')
    job_id = sgqlc.types.Field(bigint_comparison_exp, graphql_name='jobId')
    model = sgqlc.types.Field(meta_ai_model_bool_exp, graphql_name='model')
    model_id = sgqlc.types.Field('uuid_comparison_exp', graphql_name='modelId')
    task_id = sgqlc.types.Field(bigint_comparison_exp, graphql_name='taskId')
    type = sgqlc.types.Field(meta_ai_assignment_enum_comparison_exp, graphql_name='type')


class meta_ai_prediction_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_schema
    __field_names__ = ('app_id', 'instances', 'job_id', 'model', 'model_id', 'task_id', 'type')
    app_id = sgqlc.types.Field(uuid, graphql_name='appId')
    instances = sgqlc.types.Field(meta_ai_instance_arr_rel_insert_input, graphql_name='instances')
    job_id = sgqlc.types.Field(bigint, graphql_name='jobId')
    model = sgqlc.types.Field(meta_ai_model_obj_rel_insert_input, graphql_name='model')
    model_id = sgqlc.types.Field(uuid, graphql_name='modelId')
    task_id = sgqlc.types.Field(bigint, graphql_name='taskId')
    type = sgqlc.types.Field(meta_ai_assignment_enum, graphql_name='type')


class meta_ai_prediction_obj_rel_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_schema
    __field_names__ = ('data',)
    data = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_prediction_insert_input), graphql_name='data')


class meta_ai_prediction_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_schema
    __field_names__ = ('app_id', 'created_at', 'id', 'job_id', 'model', 'model_id', 'task_id', 'type')
    app_id = sgqlc.types.Field(order_by, graphql_name='appId')
    created_at = sgqlc.types.Field(order_by, graphql_name='createdAt')
    id = sgqlc.types.Field(order_by, graphql_name='id')
    job_id = sgqlc.types.Field(order_by, graphql_name='jobId')
    model = sgqlc.types.Field(meta_ai_model_order_by, graphql_name='model')
    model_id = sgqlc.types.Field(order_by, graphql_name='modelId')
    task_id = sgqlc.types.Field(order_by, graphql_name='taskId')
    type = sgqlc.types.Field(order_by, graphql_name='type')


class meta_ai_prediction_pk_columns_input(sgqlc.types.Input):
    __schema__ = meta_ai_schema
    __field_names__ = ('id',)
    id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name='id')


class meta_ai_visibility_bool_exp(sgqlc.types.Input):
    __schema__ = meta_ai_schema
    __field_names__ = ('_and', '_not', '_or', 'models', 'type')
    _and = sgqlc.types.Field(sgqlc.types.list_of('meta_ai_visibility_bool_exp'), graphql_name='_and')
    _not = sgqlc.types.Field('meta_ai_visibility_bool_exp', graphql_name='_not')
    _or = sgqlc.types.Field(sgqlc.types.list_of('meta_ai_visibility_bool_exp'), graphql_name='_or')
    models = sgqlc.types.Field(meta_ai_model_bool_exp, graphql_name='models')
    type = sgqlc.types.Field(String_comparison_exp, graphql_name='type')


class meta_ai_visibility_enum_comparison_exp(sgqlc.types.Input):
    __schema__ = meta_ai_schema
    __field_names__ = ('_eq', '_in', '_is_null', '_neq', '_nin')
    _eq = sgqlc.types.Field(meta_ai_visibility_enum, graphql_name='_eq')
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_visibility_enum)), graphql_name='_in')
    _is_null = sgqlc.types.Field(Boolean, graphql_name='_is_null')
    _neq = sgqlc.types.Field(meta_ai_visibility_enum, graphql_name='_neq')
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_visibility_enum)), graphql_name='_nin')


class meta_ai_visibility_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_schema
    __field_names__ = ('type',)
    type = sgqlc.types.Field(order_by, graphql_name='type')


class meta_ai_visibility_pk_columns_input(sgqlc.types.Input):
    __schema__ = meta_ai_schema
    __field_names__ = ('type',)
    type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='type')


class timestamptz_comparison_exp(sgqlc.types.Input):
    __schema__ = meta_ai_schema
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
    __schema__ = meta_ai_schema
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
class Prelabel(sgqlc.types.Type):
    __schema__ = meta_ai_schema
    __field_names__ = ('prediction', 'prediction_id')
    prediction = sgqlc.types.Field('meta_ai_prediction', graphql_name='prediction')
    prediction_id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name='predictionId')


class meta_ai_app(sgqlc.types.Type):
    __schema__ = meta_ai_schema
    __field_names__ = ('active', 'assigned', 'assignment', 'id', 'model', 'model_id', 'predictions')
    active = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='active')
    assigned = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_assignment_enum), graphql_name='assigned')
    assignment = sgqlc.types.Field(sgqlc.types.non_null('meta_ai_assignment'), graphql_name='assignment')
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


class meta_ai_app_mutation_response(sgqlc.types.Type):
    __schema__ = meta_ai_schema
    __field_names__ = ('affected_rows', 'returning')
    affected_rows = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='affected_rows')
    returning = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_app))), graphql_name='returning')


class meta_ai_assignment(sgqlc.types.Type):
    __schema__ = meta_ai_schema
    __field_names__ = ('apps', 'type')
    apps = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_app))), graphql_name='apps', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_app_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_app_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_app_bool_exp, graphql_name='where', default=None)),
))
    )
    type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='type')


class meta_ai_instance(sgqlc.types.Type):
    __schema__ = meta_ai_schema
    __field_names__ = ('id', 'output', 'prediction', 'prediction_id', 'score')
    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='id')
    output = sgqlc.types.Field(jsonb, graphql_name='output', args=sgqlc.types.ArgDict((
        ('path', sgqlc.types.Arg(String, graphql_name='path', default=None)),
))
    )
    prediction = sgqlc.types.Field(sgqlc.types.non_null('meta_ai_prediction'), graphql_name='prediction')
    prediction_id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name='predictionId')
    score = sgqlc.types.Field(float8, graphql_name='score')


class meta_ai_instance_mutation_response(sgqlc.types.Type):
    __schema__ = meta_ai_schema
    __field_names__ = ('affected_rows', 'returning')
    affected_rows = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='affected_rows')
    returning = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_instance))), graphql_name='returning')


class meta_ai_model(sgqlc.types.Type):
    __schema__ = meta_ai_schema
    __field_names__ = ('apps', 'created_at', 'description', 'endpoint', 'id', 'metadata', 'name', 'predictions', 'updated_at', 'version', 'visibility', 'visibility_by_visibility')
    apps = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_app))), graphql_name='apps', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_app_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_app_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_app_bool_exp, graphql_name='where', default=None)),
))
    )
    created_at = sgqlc.types.Field(sgqlc.types.non_null(timestamptz), graphql_name='createdAt')
    description = sgqlc.types.Field(String, graphql_name='description')
    endpoint = sgqlc.types.Field(String, graphql_name='endpoint')
    id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name='id')
    metadata = sgqlc.types.Field(jsonb, graphql_name='metadata', args=sgqlc.types.ArgDict((
        ('path', sgqlc.types.Arg(String, graphql_name='path', default=None)),
))
    )
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    predictions = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('meta_ai_prediction'))), graphql_name='predictions', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_prediction_bool_exp, graphql_name='where', default=None)),
))
    )
    updated_at = sgqlc.types.Field(timestamptz, graphql_name='updatedAt')
    version = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='version')
    visibility = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_visibility_enum), graphql_name='visibility')
    visibility_by_visibility = sgqlc.types.Field(sgqlc.types.non_null('meta_ai_visibility'), graphql_name='visibilityByVisibility')


class meta_ai_model_mutation_response(sgqlc.types.Type):
    __schema__ = meta_ai_schema
    __field_names__ = ('affected_rows', 'returning')
    affected_rows = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='affected_rows')
    returning = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_model))), graphql_name='returning')


class meta_ai_prediction(sgqlc.types.Type):
    __schema__ = meta_ai_schema
    __field_names__ = ('app_id', 'created_at', 'id', 'instances', 'job_id', 'model', 'model_id', 'task_id', 'type')
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
    job_id = sgqlc.types.Field(bigint, graphql_name='jobId')
    model = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_model), graphql_name='model')
    model_id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name='modelId')
    task_id = sgqlc.types.Field(bigint, graphql_name='taskId')
    type = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_assignment_enum), graphql_name='type')


class meta_ai_prediction_mutation_response(sgqlc.types.Type):
    __schema__ = meta_ai_schema
    __field_names__ = ('affected_rows', 'returning')
    affected_rows = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='affected_rows')
    returning = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction))), graphql_name='returning')


class meta_ai_visibility(sgqlc.types.Type):
    __schema__ = meta_ai_schema
    __field_names__ = ('models', 'type')
    models = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_model))), graphql_name='models', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_model_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_model_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_model_bool_exp, graphql_name='where', default=None)),
))
    )
    type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='type')


class mutation_root(sgqlc.types.Type):
    __schema__ = meta_ai_schema
    __field_names__ = ('delete_meta_ai_app', 'delete_meta_ai_app_by_pk', 'delete_meta_ai_instance', 'delete_meta_ai_instance_by_pk', 'delete_meta_ai_model', 'delete_meta_ai_model_by_pk', 'delete_meta_ai_prediction', 'delete_meta_ai_prediction_by_pk', 'insert_meta_ai_app', 'insert_meta_ai_app_one', 'insert_meta_ai_instance', 'insert_meta_ai_instance_one', 'insert_meta_ai_model', 'insert_meta_ai_model_one', 'insert_meta_ai_prediction', 'insert_meta_ai_prediction_one', 'update_meta_ai_app', 'update_meta_ai_app_by_pk', 'update_meta_ai_instance', 'update_meta_ai_instance_by_pk', 'update_meta_ai_model', 'update_meta_ai_model_by_pk')
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
))
    )
    insert_meta_ai_prediction_one = sgqlc.types.Field(meta_ai_prediction, graphql_name='insert_meta_ai_prediction_one', args=sgqlc.types.ArgDict((
        ('object', sgqlc.types.Arg(sgqlc.types.non_null(meta_ai_prediction_insert_input), graphql_name='object', default=None)),
))
    )
    update_meta_ai_app = sgqlc.types.Field(meta_ai_app_mutation_response, graphql_name='update_meta_ai_app', args=sgqlc.types.ArgDict((
        ('_set', sgqlc.types.Arg(meta_ai_app_set_input, graphql_name='_set', default=None)),
        ('where', sgqlc.types.Arg(sgqlc.types.non_null(meta_ai_app_bool_exp), graphql_name='where', default=None)),
))
    )
    update_meta_ai_app_by_pk = sgqlc.types.Field(meta_ai_app, graphql_name='update_meta_ai_app_by_pk', args=sgqlc.types.ArgDict((
        ('_set', sgqlc.types.Arg(meta_ai_app_set_input, graphql_name='_set', default=None)),
        ('pk_columns', sgqlc.types.Arg(sgqlc.types.non_null(meta_ai_app_pk_columns_input), graphql_name='pk_columns', default=None)),
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


class query_root(sgqlc.types.Type):
    __schema__ = meta_ai_schema
    __field_names__ = ('get_prelabel', 'meta_ai_app', 'meta_ai_app_by_pk', 'meta_ai_assignment', 'meta_ai_assignment_by_pk', 'meta_ai_instance', 'meta_ai_instance_by_pk', 'meta_ai_model', 'meta_ai_model_by_pk', 'meta_ai_prediction', 'meta_ai_prediction_by_pk', 'meta_ai_visibility', 'meta_ai_visibility_by_pk')
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
    meta_ai_assignment_by_pk = sgqlc.types.Field('meta_ai_assignment', graphql_name='meta_ai_assignment_by_pk', args=sgqlc.types.ArgDict((
        ('type', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='type', default=None)),
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
    meta_ai_prediction_by_pk = sgqlc.types.Field('meta_ai_prediction', graphql_name='meta_ai_prediction_by_pk', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name='id', default=None)),
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
    meta_ai_visibility_by_pk = sgqlc.types.Field('meta_ai_visibility', graphql_name='meta_ai_visibility_by_pk', args=sgqlc.types.ArgDict((
        ('type', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='type', default=None)),
))
    )


class subscription_root(sgqlc.types.Type):
    __schema__ = meta_ai_schema
    __field_names__ = ('get_prelabel', 'meta_ai_app', 'meta_ai_app_by_pk', 'meta_ai_assignment', 'meta_ai_assignment_by_pk', 'meta_ai_instance', 'meta_ai_instance_by_pk', 'meta_ai_model', 'meta_ai_model_by_pk', 'meta_ai_prediction', 'meta_ai_prediction_by_pk', 'meta_ai_visibility', 'meta_ai_visibility_by_pk')
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
    meta_ai_assignment_by_pk = sgqlc.types.Field('meta_ai_assignment', graphql_name='meta_ai_assignment_by_pk', args=sgqlc.types.ArgDict((
        ('type', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='type', default=None)),
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
    meta_ai_prediction_by_pk = sgqlc.types.Field('meta_ai_prediction', graphql_name='meta_ai_prediction_by_pk', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name='id', default=None)),
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
    meta_ai_visibility_by_pk = sgqlc.types.Field('meta_ai_visibility', graphql_name='meta_ai_visibility_by_pk', args=sgqlc.types.ArgDict((
        ('type', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='type', default=None)),
))
    )



########################################################################
# Unions
########################################################################

########################################################################
# Schema Entry Points
########################################################################
meta_ai_schema.query_type = query_root
meta_ai_schema.mutation_type = mutation_root
meta_ai_schema.subscription_type = subscription_root

