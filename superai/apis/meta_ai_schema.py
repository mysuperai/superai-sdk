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


class jsonb(sgqlc.types.Scalar):
    __schema__ = meta_ai_schema


class meta_ai_app_constraint(sgqlc.types.Enum):
    __schema__ = meta_ai_schema
    __choices__ = ('app_model_id_app_id_key', 'app_to_model_pkey')


class meta_ai_app_select_column(sgqlc.types.Enum):
    __schema__ = meta_ai_schema
    __choices__ = ('id', 'modelId')


class meta_ai_app_update_column(sgqlc.types.Enum):
    __schema__ = meta_ai_schema
    __choices__ = ('modelId',)


class meta_ai_model_constraint(sgqlc.types.Enum):
    __schema__ = meta_ai_schema
    __choices__ = ('model_name_ownerId_version_key', 'model_pkey')


class meta_ai_model_select_column(sgqlc.types.Enum):
    __schema__ = meta_ai_schema
    __choices__ = ('createdAt', 'endpoint', 'id', 'metadata', 'name', 'version')


class meta_ai_model_update_column(sgqlc.types.Enum):
    __schema__ = meta_ai_schema
    __choices__ = ('endpoint', 'metadata', 'name', 'version')


class meta_ai_prediction_select_column(sgqlc.types.Enum):
    __schema__ = meta_ai_schema
    __choices__ = ('appId', 'createdAt', 'id', 'jobId', 'modelId', 'output', 'taskId')


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
    __field_names__ = ('_and', '_not', '_or', 'id', 'model', 'model_id', 'predictions')
    _and = sgqlc.types.Field(sgqlc.types.list_of('meta_ai_app_bool_exp'), graphql_name='_and')
    _not = sgqlc.types.Field('meta_ai_app_bool_exp', graphql_name='_not')
    _or = sgqlc.types.Field(sgqlc.types.list_of('meta_ai_app_bool_exp'), graphql_name='_or')
    id = sgqlc.types.Field('uuid_comparison_exp', graphql_name='id')
    model = sgqlc.types.Field('meta_ai_model_bool_exp', graphql_name='model')
    model_id = sgqlc.types.Field('uuid_comparison_exp', graphql_name='modelId')
    predictions = sgqlc.types.Field('meta_ai_prediction_bool_exp', graphql_name='predictions')


class meta_ai_app_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_schema
    __field_names__ = ('id', 'model', 'model_id', 'predictions')
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
    __field_names__ = ('id', 'model', 'model_id')
    id = sgqlc.types.Field(order_by, graphql_name='id')
    model = sgqlc.types.Field('meta_ai_model_order_by', graphql_name='model')
    model_id = sgqlc.types.Field(order_by, graphql_name='modelId')


class meta_ai_app_pk_columns_input(sgqlc.types.Input):
    __schema__ = meta_ai_schema
    __field_names__ = ('id',)
    id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name='id')


class meta_ai_app_set_input(sgqlc.types.Input):
    __schema__ = meta_ai_schema
    __field_names__ = ('model_id',)
    model_id = sgqlc.types.Field(uuid, graphql_name='modelId')


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
    __field_names__ = ('_and', '_not', '_or', 'apps', 'created_at', 'endpoint', 'id', 'metadata', 'name', 'predictions', 'version')
    _and = sgqlc.types.Field(sgqlc.types.list_of('meta_ai_model_bool_exp'), graphql_name='_and')
    _not = sgqlc.types.Field('meta_ai_model_bool_exp', graphql_name='_not')
    _or = sgqlc.types.Field(sgqlc.types.list_of('meta_ai_model_bool_exp'), graphql_name='_or')
    apps = sgqlc.types.Field(meta_ai_app_bool_exp, graphql_name='apps')
    created_at = sgqlc.types.Field('timestamptz_comparison_exp', graphql_name='createdAt')
    endpoint = sgqlc.types.Field(String_comparison_exp, graphql_name='endpoint')
    id = sgqlc.types.Field('uuid_comparison_exp', graphql_name='id')
    metadata = sgqlc.types.Field(jsonb_comparison_exp, graphql_name='metadata')
    name = sgqlc.types.Field(String_comparison_exp, graphql_name='name')
    predictions = sgqlc.types.Field('meta_ai_prediction_bool_exp', graphql_name='predictions')
    version = sgqlc.types.Field(Int_comparison_exp, graphql_name='version')


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
    __field_names__ = ('apps', 'endpoint', 'metadata', 'name', 'predictions', 'version')
    apps = sgqlc.types.Field(meta_ai_app_arr_rel_insert_input, graphql_name='apps')
    endpoint = sgqlc.types.Field(String, graphql_name='endpoint')
    metadata = sgqlc.types.Field(jsonb, graphql_name='metadata')
    name = sgqlc.types.Field(String, graphql_name='name')
    predictions = sgqlc.types.Field('meta_ai_prediction_arr_rel_insert_input', graphql_name='predictions')
    version = sgqlc.types.Field(Int, graphql_name='version')


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
    __field_names__ = ('created_at', 'endpoint', 'id', 'metadata', 'name', 'version')
    created_at = sgqlc.types.Field(order_by, graphql_name='createdAt')
    endpoint = sgqlc.types.Field(order_by, graphql_name='endpoint')
    id = sgqlc.types.Field(order_by, graphql_name='id')
    metadata = sgqlc.types.Field(order_by, graphql_name='metadata')
    name = sgqlc.types.Field(order_by, graphql_name='name')
    version = sgqlc.types.Field(order_by, graphql_name='version')


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
    __field_names__ = ('endpoint', 'metadata', 'name', 'version')
    endpoint = sgqlc.types.Field(String, graphql_name='endpoint')
    metadata = sgqlc.types.Field(jsonb, graphql_name='metadata')
    name = sgqlc.types.Field(String, graphql_name='name')
    version = sgqlc.types.Field(Int, graphql_name='version')


class meta_ai_prediction_arr_rel_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_schema
    __field_names__ = ('data',)
    data = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('meta_ai_prediction_insert_input'))), graphql_name='data')


class meta_ai_prediction_bool_exp(sgqlc.types.Input):
    __schema__ = meta_ai_schema
    __field_names__ = ('_and', '_not', '_or', 'app', 'app_id', 'created_at', 'id', 'job_id', 'model', 'model_id', 'output', 'task_id')
    _and = sgqlc.types.Field(sgqlc.types.list_of('meta_ai_prediction_bool_exp'), graphql_name='_and')
    _not = sgqlc.types.Field('meta_ai_prediction_bool_exp', graphql_name='_not')
    _or = sgqlc.types.Field(sgqlc.types.list_of('meta_ai_prediction_bool_exp'), graphql_name='_or')
    app = sgqlc.types.Field(meta_ai_app_bool_exp, graphql_name='app')
    app_id = sgqlc.types.Field('uuid_comparison_exp', graphql_name='appId')
    created_at = sgqlc.types.Field('timestamptz_comparison_exp', graphql_name='createdAt')
    id = sgqlc.types.Field('uuid_comparison_exp', graphql_name='id')
    job_id = sgqlc.types.Field(bigint_comparison_exp, graphql_name='jobId')
    model = sgqlc.types.Field(meta_ai_model_bool_exp, graphql_name='model')
    model_id = sgqlc.types.Field('uuid_comparison_exp', graphql_name='modelId')
    output = sgqlc.types.Field(jsonb_comparison_exp, graphql_name='output')
    task_id = sgqlc.types.Field(bigint_comparison_exp, graphql_name='taskId')


class meta_ai_prediction_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_schema
    __field_names__ = ('app', 'model', 'model_id', 'output')
    app = sgqlc.types.Field(meta_ai_app_obj_rel_insert_input, graphql_name='app')
    model = sgqlc.types.Field(meta_ai_model_obj_rel_insert_input, graphql_name='model')
    model_id = sgqlc.types.Field(uuid, graphql_name='modelId')
    output = sgqlc.types.Field(jsonb, graphql_name='output')


class meta_ai_prediction_obj_rel_insert_input(sgqlc.types.Input):
    __schema__ = meta_ai_schema
    __field_names__ = ('data',)
    data = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_prediction_insert_input), graphql_name='data')


class meta_ai_prediction_order_by(sgqlc.types.Input):
    __schema__ = meta_ai_schema
    __field_names__ = ('app', 'app_id', 'created_at', 'id', 'job_id', 'model', 'model_id', 'output', 'task_id')
    app = sgqlc.types.Field(meta_ai_app_order_by, graphql_name='app')
    app_id = sgqlc.types.Field(order_by, graphql_name='appId')
    created_at = sgqlc.types.Field(order_by, graphql_name='createdAt')
    id = sgqlc.types.Field(order_by, graphql_name='id')
    job_id = sgqlc.types.Field(order_by, graphql_name='jobId')
    model = sgqlc.types.Field(meta_ai_model_order_by, graphql_name='model')
    model_id = sgqlc.types.Field(order_by, graphql_name='modelId')
    output = sgqlc.types.Field(order_by, graphql_name='output')
    task_id = sgqlc.types.Field(order_by, graphql_name='taskId')


class meta_ai_prediction_pk_columns_input(sgqlc.types.Input):
    __schema__ = meta_ai_schema
    __field_names__ = ('id',)
    id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name='id')


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
class meta_ai_app(sgqlc.types.Type):
    __schema__ = meta_ai_schema
    __field_names__ = ('id', 'model', 'model_id', 'predictions')
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


class meta_ai_model(sgqlc.types.Type):
    __schema__ = meta_ai_schema
    __field_names__ = ('apps', 'created_at', 'endpoint', 'id', 'metadata', 'name', 'predictions', 'version')
    apps = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_app))), graphql_name='apps', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_app_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_app_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_app_bool_exp, graphql_name='where', default=None)),
))
    )
    created_at = sgqlc.types.Field(sgqlc.types.non_null(timestamptz), graphql_name='createdAt')
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
    version = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='version')


class meta_ai_model_mutation_response(sgqlc.types.Type):
    __schema__ = meta_ai_schema
    __field_names__ = ('affected_rows', 'returning')
    affected_rows = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='affected_rows')
    returning = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_model))), graphql_name='returning')


class meta_ai_prediction(sgqlc.types.Type):
    __schema__ = meta_ai_schema
    __field_names__ = ('app', 'app_id', 'created_at', 'id', 'job_id', 'model', 'model_id', 'output', 'task_id')
    app = sgqlc.types.Field(meta_ai_app, graphql_name='app')
    app_id = sgqlc.types.Field(uuid, graphql_name='appId')
    created_at = sgqlc.types.Field(sgqlc.types.non_null(timestamptz), graphql_name='createdAt')
    id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name='id')
    job_id = sgqlc.types.Field(bigint, graphql_name='jobId')
    model = sgqlc.types.Field(sgqlc.types.non_null(meta_ai_model), graphql_name='model')
    model_id = sgqlc.types.Field(sgqlc.types.non_null(uuid), graphql_name='modelId')
    output = sgqlc.types.Field(jsonb, graphql_name='output', args=sgqlc.types.ArgDict((
        ('path', sgqlc.types.Arg(String, graphql_name='path', default=None)),
))
    )
    task_id = sgqlc.types.Field(bigint, graphql_name='taskId')


class meta_ai_prediction_mutation_response(sgqlc.types.Type):
    __schema__ = meta_ai_schema
    __field_names__ = ('affected_rows', 'returning')
    affected_rows = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='affected_rows')
    returning = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_prediction))), graphql_name='returning')


class mutation_root(sgqlc.types.Type):
    __schema__ = meta_ai_schema
    __field_names__ = ('delete_meta_ai_app', 'delete_meta_ai_app_by_pk', 'delete_meta_ai_model', 'delete_meta_ai_model_by_pk', 'delete_meta_ai_prediction', 'delete_meta_ai_prediction_by_pk', 'insert_meta_ai_app', 'insert_meta_ai_app_one', 'insert_meta_ai_model', 'insert_meta_ai_model_one', 'insert_meta_ai_prediction', 'insert_meta_ai_prediction_one', 'update_meta_ai_app', 'update_meta_ai_app_by_pk', 'update_meta_ai_model', 'update_meta_ai_model_by_pk')
    delete_meta_ai_app = sgqlc.types.Field(meta_ai_app_mutation_response, graphql_name='delete_meta_ai_app', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(sgqlc.types.non_null(meta_ai_app_bool_exp), graphql_name='where', default=None)),
))
    )
    delete_meta_ai_app_by_pk = sgqlc.types.Field(meta_ai_app, graphql_name='delete_meta_ai_app_by_pk', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name='id', default=None)),
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
    __field_names__ = ('meta_ai_app', 'meta_ai_app_by_pk', 'meta_ai_model', 'meta_ai_model_by_pk', 'meta_ai_prediction', 'meta_ai_prediction_by_pk')
    meta_ai_app = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('meta_ai_app'))), graphql_name='meta_ai_app', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_app_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_app_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_app_bool_exp, graphql_name='where', default=None)),
))
    )
    meta_ai_app_by_pk = sgqlc.types.Field('meta_ai_app', graphql_name='meta_ai_app_by_pk', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name='id', default=None)),
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


class subscription_root(sgqlc.types.Type):
    __schema__ = meta_ai_schema
    __field_names__ = ('meta_ai_app', 'meta_ai_app_by_pk', 'meta_ai_model', 'meta_ai_model_by_pk', 'meta_ai_prediction', 'meta_ai_prediction_by_pk')
    meta_ai_app = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('meta_ai_app'))), graphql_name='meta_ai_app', args=sgqlc.types.ArgDict((
        ('distinct_on', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_app_select_column)), graphql_name='distinct_on', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(meta_ai_app_order_by)), graphql_name='order_by', default=None)),
        ('where', sgqlc.types.Arg(meta_ai_app_bool_exp, graphql_name='where', default=None)),
))
    )
    meta_ai_app_by_pk = sgqlc.types.Field('meta_ai_app', graphql_name='meta_ai_app_by_pk', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(uuid), graphql_name='id', default=None)),
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



########################################################################
# Unions
########################################################################

########################################################################
# Schema Entry Points
########################################################################
meta_ai_schema.query_type = query_root
meta_ai_schema.mutation_type = mutation_root
meta_ai_schema.subscription_type = subscription_root

