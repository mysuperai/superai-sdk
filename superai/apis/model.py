from sgqlc.endpoint.requests import RequestsEndpoint
from sgqlc.types import Arg, ArgDict, ID, Int, Interface, Scalar, Schema, String, Type, Field, list_of, global_schema, Input
from sgqlc.types.datetime import DateTime
from sgqlc.types.relay import Connection, connection_args
from sgqlc.operation import Operation
from superai.config import settings
from superai.log import logger
from superai.utils.apikey_manager import load_api_key
import json
log = logger.get_logger(__name__)

from meta_ai_schema import query_root

class MetaAISession(RequestsEndpoint):
    def __init__(self, timeout=20):
        base_url = settings.get("meta_ai_base")
        headers = {
            "x-api-key" : load_api_key(),
            #"x-app-id" : "f771605e-7ae6-4431-82f6-4d5651226f44"
        }
        super().__init__(base_url,headers, timeout=timeout)


    def get_endpoint(self, model_id):
        pass

sess = MetaAISession()

class pk_columns(Input):
    id = ID

class Model(Type):
    id  = ID
    name = String
    version = Int
    endpoint = String
    metadata =  String # JSON

class ModelInput(Input):
    name = String
    version = Int
    endpoint = String
    metadata =  String # JSON

class ModelUpdate(Input):
    _set = Field(ModelInput,graphql_name="_set")
    pk_columns = Field(pk_columns, graphql_name="pk_columns")

class App(Type):
    id = ID
    modelId = ID
    model = Model

class Prediction(Type):
    id = ID
    modelId = ID
    model = Model
    jobId = Int
    taskId = Int
    createdAt = DateTime
    appId = ID
    app = App
    output = String




class Query(Type):
    model = Field(Model, graphql_name="meta_ai_model_by_pk", args={"id":str})
    all_models = Field(list_of(Model), graphql_name="meta_ai_model")
    app = Field(App, graphql_name="meta_ai_app_by_pk",  args={"id":str})
    all_apps = Field(list_of(App), graphql_name="meta_ai_app")

class Mutation(Type):
    add_model = Field(Model, graphql_name="insert_meta_ai_model_one",args={"object":ModelInput})
    update_model = Field(Model, graphql_name="update_meta_ai_model_by_pk", args={"test":ModelUpdate})


def get_all_models():
    op = Operation(Query)
    op.all_models()
    data = sess(op)
    return (op + data).all_models

def get_model(id):
    op = Operation(Query)
    op.model(id=id)
    data = sess(op)
    return (op + data).model  

def add_model(name:str, version:int=1, metadata:str=None, endpoint:str=""):
    op = Operation(Mutation)
    op.add_model(object=ModelInput(name=name, version=version, metadata=metadata, endpoint=endpoint))
    data = sess(op)
    return (op + data).add_model  

def update_model(id, **kwargs):
    op = Operation(Mutation)
    new_model = ModelInput(**kwargs)
    print(new_model)
    up_model  = ModelUpdate(**kwargs, pk_columns=pk_columns(id))
    print(up_model)
    op.update_model(ModelUpdate(new_model,id))
    print(op)
    data = sess(op)
    return (op + data).update_model  

def get_apps():
    op = Operation(Query)
    op.all_apps()
    data = sess(op)
    return (op + data).all_apps

def get_app(id):
    op = Operation(Query)
    op.app(id=id)
    data = sess(op)
    return (op + data).app

if __name__ == "__main__":
    sess = MetaAISession()
    m_id = "8220ada2-24fc-4466-85ca-1bbf757d6f92"
    # m = get_model(m_id)
    # print(m)
    # m = get_all_models()
    # print(m)

    # m = get_app("f771605e-7ae6-4431-82f6-4d5651226f44")
    # print(m)
    # a = get_apps()
    # print(a)

    #a = add_model("AddedModel")
    #print(a)
    #b = update_model("e185d9e3-b2c3-4b5e-96df-62b913bfe8b1", name="ChangedModel")
    op = Operation(query_root)
    op.meta_ai_model_by_pk(id=m_id)
    print(op)
    data = sess(op)
    print(data)
    print(op+data)
    #preds = sess.get_predictions("8220ada2-24fc-4466-85ca-1bbf757d6f92", 123)
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