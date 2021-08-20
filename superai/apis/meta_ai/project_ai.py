import json
from abc import ABC
from typing import List, Union

from sgqlc.operation import Operation

from superai.log import logger
from .session import MetaAISession

log = logger.get_logger(__name__)

from superai.apis.meta_ai.meta_ai_graphql_schema import (
    Boolean_comparison_exp,
    String_comparison_exp,
    meta_ai_app_bool_exp,
    meta_ai_app_constraint,
    meta_ai_app_insert_input,
    meta_ai_app_on_conflict,
    meta_ai_assignment_bool_exp,
    meta_ai_assignment_enum,
    meta_ai_instance_insert_input,
    meta_ai_prediction_insert_input,
    mutation_root,
    query_root,
    uuid_comparison_exp,
    meta_ai_assignment_enum_comparison_exp,
)


class ProjectAiApiMixin(ABC):
    _resource = "project_ai"

    @property
    def resource(self):
        return self._resource

    def get_models(self, app_id: str, assignment: str = None, active=None):
        sess = MetaAISession(app_id=app_id)
        op = Operation(query_root)
        check = meta_ai_app_bool_exp(
            active=Boolean_comparison_exp(_eq=active),
            id=uuid_comparison_exp(_eq=app_id),
            assigned=meta_ai_assignment_enum_comparison_exp(_eq=assignment),
        )
        app_assignments = op.meta_ai_app(where=check)
        app_assignments.threshold()
        models = app_assignments.model
        models.id()
        models.name()
        data = sess.perform_op(op)
        try:
            output = (op + data).meta_ai_app
            return output
        except AttributeError as e:
            log.info(f"No models for project with id: {app_id} and assignment type {assignment}")

    def project_set_model(
        self,
        app_id: str,
        assignment: meta_ai_assignment_enum,
        model_id: str,
        active: bool = None,
        threshold: float = None,
    ):
        sess = MetaAISession(app_id=app_id)
        op = Operation(mutation_root)
        input_args = {"id": app_id, "model_id": model_id, "assigned": assignment}
        if active is not None:
            input_args["active"] = active
        if threshold is not None:
            input_args["threshold"] = threshold
        insert_input = meta_ai_app_insert_input(input_args)
        conflict_handler = meta_ai_app_on_conflict(
            constraint=meta_ai_app_constraint("app_modelId_id_assigned_key"),
            update_columns=["modelId", "active", "threshold"],
            where=None,
        )
        op.insert_meta_ai_app_one(object=insert_input, on_conflict=conflict_handler).__fields__(
            "id", "model_id", "assigned", "active"
        )
        data = sess.perform_op(op)
        print(data)
        return (op + data).insert_meta_ai_app_one

    def list_prelabels(self, app_id: str, model_id: str):
        sess = MetaAISession(app_id=app_id)
        op = Operation(query_root)
        model = op.meta_ai_app_by_pk(id=app_id, model_id=model_id, assigned="PRELABEL").model
        predictions = model.predictions()
        predictions.id()
        predictions.instances().id()
        data = sess.perform_op(op)
        try:
            output = (op + data).meta_ai_app_by_pk.model.predictions
            return output
        except AttributeError as e:
            log.info(f"No predictions for project with id: {app_id} and model_id:{model_id}")

    def list_prediction_instances(self, app_id: str, prediction_id: str):
        sess = MetaAISession(app_id=app_id)
        op = Operation(query_root)
        instance = op.meta_ai_prediction_by_pk(id=prediction_id).instances.id()
        data = sess.perform_op(op)
        try:
            output = (op + data).meta_ai_prediction_by_pk.instances
            return output
        except AttributeError as e:
            log.info(f"No prediction instances found for prediction_id:{prediction_id}.")

    def view_prediction_instance(self, app_id: str, prediction_id: str, instance_id):
        sess = MetaAISession(app_id=app_id)
        op = Operation(query_root)
        instance = op.meta_ai_instance_by_pk(id=instance_id, prediction_id=prediction_id)
        instance.id()
        instance.score()
        instance.output()
        data = sess.perform_op(op)
        try:
            output = (op + data).meta_ai_instance_by_pk
            return output
        except AttributeError as e:
            log.info(f"No prediction instance found for prediction_id:{prediction_id} and instance_id:{instance_id}")

    def view_prediction(self, app_id: str, prediction_id: str):
        """
        View the prediction object, which acts as a container for potentially multiple concrete instances.
        Currently only returns the current state of the prediction.
        Args:
            app_id:
            prediction_id:

        Returns:

        """
        sess = MetaAISession(app_id=app_id)
        op = Operation(query_root)
        op.meta_ai_prediction_by_pk(id=prediction_id).__fields__("id", "state")
        data = sess.perform_op(op)
        try:
            output = (op + data).meta_ai_prediction_by_pk
            return output
        except AttributeError as e:
            log.info(f"No prediction found for prediction_id:{prediction_id}.")

    def submit_prelabel(
        self,
        model_output: Union[str, List[str]],
        app_id: str,
        job_id: int,
        model_id: str,
        assignment: meta_ai_assignment_enum = "PRELABEL",
    ):
        sess = MetaAISession(app_id=app_id)
        if type(model_output) is list and len(model_output) > 1:
            log.info("Multiple instances in model output.")
        else:
            model_output = [model_output]
        op = Operation(mutation_root)
        input_args = {"app_id": app_id, "model_id": model_id, "type": assignment, "job_id": job_id}
        insert_input = meta_ai_prediction_insert_input(input_args)
        op.insert_meta_ai_prediction_one(object=insert_input).__fields__("id")
        data = sess.perform_op(op)
        prediction_id = (op + data).insert_meta_ai_prediction_one.id

        for i, instance in enumerate(model_output):
            op = Operation(mutation_root)
            if type(instance) is str:
                instance = json.loads(instance)
            input_args = {"prediction_id": prediction_id}

            if "output" in instance.keys():
                input_args["output"] = instance["output"]
            if "score" in instance.keys():
                input_args["score"] = instance["score"]
            input_args["id"] = i
            insert_input = meta_ai_instance_insert_input(input_args)
            op.insert_meta_ai_instance_one(object=insert_input).__fields__("id")
            data = sess.perform_op(op)
            instance_id = (op + data).insert_meta_ai_instance_one.id
            log.debug(
                f"Inserted output instance {instance_id} for model {model_id} under prediction_id {prediction_id}."
            )

        return prediction_id

    def delete_prelabel(self, app_id, id):
        sess = MetaAISession(app_id=app_id)
        op = Operation(mutation_root)
        op.delete_meta_ai_prediction_by_pk(id=id).id()
        data = sess.perform_op(op)
        return (op + data).delete_meta_ai_prediction_by_pk.id

    def request_prediction_of_job(
        self, app_id: str, job_id: int, assignment: meta_ai_assignment_enum = "PRELABEL"
    ) -> List[str]:
        """
        Request to run predictions on the data contained in a job for all active models for a given `assignment`.
        Returns list of ids of prediction objects. Can be queried for completion status and output.


        :param job_id:
        :param assignment:
        :rtype: str
        """
        sess = MetaAISession(app_id=app_id)
        opq = Operation(query_root)
        opq.request_prediction_of_job(app_id=app_id, job_id=job_id, assignment=assignment).predictions.id()
        data = sess.perform_op(opq)
        res = (opq + data).request_prediction_of_job
        if len(res) == 0:
            raise Exception(f"No predictions could be requested. Does the job {job_id} exist?")
        ids = []
        for r in res:
            ids.extend(r.predictions)
        return ids
