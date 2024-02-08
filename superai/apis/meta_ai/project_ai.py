import json
from typing import List, Union

from sgqlc.operation import Operation

from superai.log import logger

from .base import AiApiBase

log = logger.get_logger(__name__)

from superai.apis.meta_ai.meta_ai_graphql_schema import (
    Boolean_comparison_exp,
    meta_ai_app_bool_exp,
    meta_ai_app_constraint,
    meta_ai_app_insert_input,
    meta_ai_app_on_conflict,
    meta_ai_assignment_enum,
    meta_ai_assignment_enum_comparison_exp,
    meta_ai_instance_insert_input,
    meta_ai_prediction_insert_input,
    mutation_root,
    query_root,
    uuid_comparison_exp,
)


class ProjectAiApiMixin(AiApiBase):
    _resource = "project_ai"

    def get_models(self, app_id: str, assignment: str = None, active=None):
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
        data = self.ai_session.perform_op(op, app_id=app_id)
        try:
            return (op + data).meta_ai_app
        except AttributeError:
            log.info(f"No models for project with id: {app_id} and assignment type {assignment}")

    def project_set_model(
        self,
        app_id: str,
        assignment: meta_ai_assignment_enum,
        active: bool = None,
        threshold: float = None,
        instance_id: str = None,
    ):
        op = Operation(mutation_root)
        if not instance_id:
            raise ValueError("AI instance_id must be provided")
        input_args = {"id": app_id, "assigned": assignment}
        if active is not None:
            input_args["active"] = active
        if threshold is not None:
            input_args["threshold"] = threshold
        if instance_id is not None:
            input_args["instance_id"] = instance_id
        insert_input = meta_ai_app_insert_input(input_args)
        conflict_handler = meta_ai_app_on_conflict(
            constraint=meta_ai_app_constraint("app_instanceId_assigned_id_key"),
            update_columns=["active", "threshold"],
        )
        op.insert_meta_ai_app_one(object=insert_input, on_conflict=conflict_handler).__fields__(
            "id", "assigned", "active", "instance_id"
        )
        data = self.ai_session.perform_op(op, app_id=app_id)
        print(data)
        return (op + data).insert_meta_ai_app_one

    def delete_ai_project_assignment(
        self, app_id: str, assignment: meta_ai_assignment_enum = "TASK", instance_id: str = None
    ) -> int:
        """Delete the assignment of a model to a project.
        Args:
            app_id: The project id
            assignment: The assignment type
            instance_id: The AI instance id

        Return the number of rows affected.
        """
        op = Operation(mutation_root)

        if not instance_id:
            raise ValueError("AI instance_id must be provided")
        check = meta_ai_app_bool_exp(
            id=uuid_comparison_exp(_eq=app_id),
            assigned=meta_ai_assignment_enum_comparison_exp(_eq=assignment),
        )
        if instance_id is not None:
            check.instance_id = uuid_comparison_exp(_eq=instance_id)

        op.delete_meta_ai_app(where=check).__fields__("affected_rows")
        data = self.ai_session.perform_op(op, app_id=app_id)
        return (op + data).delete_meta_ai_app.affected_rows

    def list_prediction_instances(self, app_id: str, prediction_id: str):
        op = Operation(query_root)
        instance = op.meta_ai_prediction_by_pk(id=prediction_id).instances.id()
        data = self.ai_session.perform_op(op, app_id=app_id)
        try:
            return (op + data).meta_ai_prediction_by_pk.instances
        except AttributeError:
            log.info(f"No prediction instances found for prediction_id:{prediction_id}.")

    def view_prediction_instance(self, app_id: str, prediction_id: str, instance_id):
        op = Operation(query_root)
        instance = op.meta_ai_instance_by_pk(id=instance_id, prediction_id=prediction_id)
        instance.id()
        instance.score()
        instance.output()
        data = self.ai_session.perform_op(op, app_id=app_id)
        try:
            output = (op + data).meta_ai_instance_by_pk
            return output
        except AttributeError:
            log.info(f"No prediction instance found for prediction_id:{prediction_id} and instance_id:{instance_id}")

    def view_prediction(self, app_id: str, prediction_id: str):
        """View the prediction object, which acts as a container for potentially multiple concrete instances.
        Currently only returns the current state of the prediction.
        Args:
            app_id:
            prediction_id:

        Returns:

        """
        op = Operation(query_root)
        op.meta_ai_prediction_by_pk(id=prediction_id).__fields__("id", "state")
        data = self.ai_session.perform_op(op, app_id=app_id)
        try:
            return (op + data).meta_ai_prediction_by_pk
        except AttributeError:
            log.info(f"No prediction found for prediction_id:{prediction_id}.")

    def submit_prelabel(
        self,
        model_output: Union[str, List[str]],
        app_id: str,
        job_id: int,
        checkpoint_id,
        assignment: meta_ai_assignment_enum = "PRELABEL",
    ):
        if type(model_output) is list and len(model_output) > 1:
            log.info("Multiple instances in model output.")
        else:
            model_output = [model_output]
        op = Operation(mutation_root)
        input_args = {"app_id": app_id, "checkpoint_id": checkpoint_id, "type": assignment, "job_id": job_id}
        insert_input = meta_ai_prediction_insert_input(input_args)
        op.insert_meta_ai_prediction_one(object=insert_input).__fields__("id")
        data = self.ai_session.perform_op(op, app_id=app_id)
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
            data = self.ai_session.perform_op(op, app_id=app_id)
            instance_id = (op + data).insert_meta_ai_instance_one.id
            log.debug(
                f"Inserted output instance {instance_id} for checkpoint {checkpoint_id} under prediction_id {prediction_id}."
            )

        return prediction_id

    def delete_prelabel(self, app_id, id):
        op = Operation(mutation_root)
        op.delete_meta_ai_prediction_by_pk(id=id).id()
        data = self.ai_session.perform_op(op, app_id=app_id)
        return (op + data).delete_meta_ai_prediction_by_pk.id

    def request_prediction_of_job(
        self, app_id: str, job_id: int, assignment: meta_ai_assignment_enum = "PRELABEL"
    ) -> List[str]:
        """Request to run predictions on the data contained in a job for all active models for a given `assignment`.
        Returns list of ids of prediction objects. Can be queried for completion status and output.

        Args:
            job_id
            assignment

        Returns:
            str
        """
        opq = Operation(query_root)
        opq.request_prediction_of_job(app_id=app_id, job_id=job_id, assignment=assignment).predictions.id()
        data = self.ai_session(opq, app_id=app_id)
        res = (opq + data).request_prediction_of_job
        if len(res) == 0:
            raise Exception(f"No predictions could be requested. Does the job {job_id} exist?")
        ids = []
        for r in res:
            ids.extend(r.predictions)
        return ids

    def resolve_data_reference(self, prediction_id: str, instance_id: int, reference: str) -> str:
        """Files in the output of models are referenced by a service specific URI and are not accessible directly.
        This function resolves the reference to an accessible URL.
        Each referenced file is assigned to a specific prediction and instance.

        Args:
            prediction_id: str
                UUID of prediction.
            instance_id: int
                Integer id of instance.
            reference: str
                Reference string given in the prediction output itself.
                E.g. `data://ai/21ef3013-1ba4-437f-a7ba-77d9260e5699/1/image1.png`

        Returns:
            Accessible URL of file
        """
        opq = Operation(query_root)
        opq.resolve_data_ref(prediction_id=prediction_id, instance_id=instance_id, data_ref=reference).url()
        data = self.ai_session(opq)
        res = (opq + data).resolve_data_ref
        return res.url
