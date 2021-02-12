from sgqlc.endpoint.requests import RequestsEndpoint
from sgqlc.operation import Operation
from superai.config import settings
from superai.log import logger
from superai.utils.apikey_manager import load_api_key

log = logger.get_logger(__name__)
from superai.apis.meta_ai_schema import (
    meta_ai_app_on_conflict,
    meta_ai_app_update_column,
    query_root,
    mutation_root,
    meta_ai_model_insert_input,
    meta_ai_model_set_input,
    meta_ai_model_pk_columns_input,
    meta_ai_app_insert_input,
    meta_ai_app_constraint,
)

app_id = "f771605e-7ae6-4431-82f6-4d5651226f44"


class MetaAISession(RequestsEndpoint):
    def __init__(self, app_id=None, timeout=20):
        base_url = settings.get("meta_ai_base")
        headers = {"x-api-key": load_api_key(), "x-app-id": app_id}
        super().__init__(base_url, headers, timeout=timeout)


def get_all_models():
    sess = MetaAISession()
    op = Operation(query_root)
    op.meta_ai_model().__fields__("name", "version", "id", "endpoint")
    data = sess(op)
    return (op + data).meta_ai_model


def get_model(id):
    sess = MetaAISession()
    op = Operation(query_root)
    op.meta_ai_model_by_pk(id=id).__fields__("name", "version", "id", "endpoint")
    data = sess(op)
    return (op + data).meta_ai_model_by_pk


def add_model(name: str, version: int = 1, metadata: str = None, endpoint: str = ""):
    sess = MetaAISession()
    op = Operation(mutation_root)
    op.insert_meta_ai_model_one(
        object=meta_ai_model_insert_input(name=name, version=version, metadata=metadata, endpoint=endpoint)
    ).__fields__("name", "version", "id", "endpoint")
    data = sess(op)
    return (op + data).insert_meta_ai_model_one.id


def update_model(id, **kwargs):
    sess = MetaAISession()
    op = Operation(mutation_root)
    op.update_meta_ai_model_by_pk(
        _set=meta_ai_model_set_input(**kwargs), pk_columns=meta_ai_model_pk_columns_input(id=id)
    ).__fields__("name", "version", "id", "endpoint")
    data = sess(op)
    return (op + data).update_meta_ai_model_by_pk.id


def delete_model(id):
    sess = MetaAISession()
    op = Operation(mutation_root)
    op.delete_meta_ai_model_by_pk(id=id).__fields__("name", "version", "id", "endpoint")
    data = sess(op)
    print(data)
    return (op + data).delete_meta_ai_model_by_pk.id


def get_active_model(app_id):
    sess = MetaAISession(app_id=app_id)
    op = Operation(query_root)
    op.meta_ai_app_by_pk(id=app_id).model.__fields__("name", "version", "id", "endpoint")
    data = sess(op)
    return (op + data).meta_ai_app_by_pk.model


def upsert_app_mapping(app_id, model_id):
    sess = MetaAISession(app_id=app_id)
    op = Operation(mutation_root)
    insert_input = meta_ai_app_insert_input(id=app_id, model_id=model_id)
    conflict_handler = meta_ai_app_on_conflict(
        constraint=meta_ai_app_constraint('app_to_model_pkey'), update_columns=['modelId'], where=None
    )
    op.insert_meta_ai_app_one(
        object=insert_input, on_conflict=conflict_handler
    ).__fields__("id", "model_id")
    data = sess(op)
    return (op + data).insert_meta_ai_app_one

def deactivate_model(id):
    sess = MetaAISession()
    op = Operation(mutation_root)
    op.delete_meta_ai_app_by_pk(id=id).__fields__("name", "version", "id", "endpoint")
    data = sess(op)
    print(data)
    return (op + data).delete_meta_ai_model_by_pk.id


if __name__ == "__main__":
    sess = MetaAISession()
    m_id = "8220ada2-24fc-4466-85ca-1bbf757d6f92"
    other_m = "ccf0bee2-f029-43f2-8db8-380024db6b1e"
    m = get_model(m_id)
    print(m)
    m = get_all_models()
    print(m)

    # m = get_app("f771605e-7ae6-4431-82f6-4d5651226f44")
    # print(m)
    # a = get_apps()
    # print(a)

    a = add_model("AddedModel")
    print(a)
    b = update_model(a, name="ChangedModel", version=2)
    print(b)
    c = delete_model(a)
    print(c)

    active = get_active_model(app_id)
    print(active)

    new_active = upsert_app_mapping(app_id, other_m)
    print(new_active)
    new_active = upsert_app_mapping(app_id, m_id)
    # op = Operation(query_root)
    # op.meta_ai_model_by_pk(id=m_id)
    # data = sess(op)
    # print(data)
    # print(op+data)
    # preds = sess.get_predictions("8220ada2-24fc-4466-85ca-1bbf757d6f92", 123)
    # #print(list(preds))
    # print(sess)

    # op = Operation(Query,name="GetModel")
    # print(op.model(id=m_id))
    # #name = op.model()
    # #print(name)
    # data = sess(op)
    # print(data)

    # obj = op+data
    # print(obj)

    # op2 = Operation(Mutation, name="AddModel")
    # add = op2.addModel(name="Test2", version=1,endpoint="localhost")
    # print(add)
    # added = sess(op2)
    # print(added)