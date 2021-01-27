def standard_filter(metric_name: str):
    if not metric_name or not isinstance(metric_name, str):
        raise AttributeError("expected metric_name of type str instead type: {}".format(type(metric_name)))

    def router_filter(app_metrics, measured_metrics):
        at_least_one_measurement = measured_metrics["quality"]["quantity"] > 0

        measured_acc = measured_metrics["quality"][metric_name]["value"]
        guaranteed_acc = app_metrics["quality"][metric_name]["ci"][0]

        if at_least_one_measurement:
            return (measured_acc >= guaranteed_acc) & (measured_metrics["cost"] <= app_metrics["cost"])
        else:
            return False

    return router_filter
