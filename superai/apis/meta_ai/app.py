def get_active_model(app_id, assignment: meta_ai_assignment_enum):
    sess = MetaAISession(app_id=app_id)
    op = Operation(query_root)
    op.meta_ai_app(id=app_id, assigned=assignment, active=True).model.__fields__(
        "name", "version", "id", "endpoint", "description", "active"
    )
    data = sess.perform_op(op)
    try:
        output = (op + data).meta_ai_app.model
        return output
    except AttributeError as e:
        log.info(f"No active model for app_id: {app_id}")


def set_active_model(app_id, model_id):
    sess = MetaAISession(app_id=app_id)
    op = Operation(mutation_root)
    insert_input = meta_ai_app_insert_input(id=app_id, model_id=model_id)
    conflict_handler = meta_ai_app_on_conflict(
        constraint=meta_ai_app_constraint("app_to_model_pkey"), update_columns=["modelId"], where=None
    )
    op.insert_meta_ai_app_one(object=insert_input, on_conflict=conflict_handler).__fields__("id", "model_id")
    data = sess.perform_op(op)
    return (op + data).insert_meta_ai_app_one


def deactivate_app(app_id):
    sess = MetaAISession(app_id=app_id)
    op = Operation(mutation_root)
    op.delete_meta_ai_app_by_pk(id=app_id).__fields__("id")
    data = sess.perform_op(op)
    output = (op + data).delete_meta_ai_app_by_pk.id
    if output == app_id:
        log.info(f"Deactivated model for app_id: {app_id}")
        return output
