from sklearn.metrics import accuracy_score, f1_score
from sklearn.preprocessing import MultiLabelBinarizer

from superai.data_program.combiner.schema_getters import get_exclusive_choice_tag, get_multiple_choice_tags


def agreement_basic(value, value_list):
    agreement_list = [value == v for v in value_list]
    return round(sum(agreement_list) / len(agreement_list), 3)


def agreement_exclusive_choice(instance, instance_list):
    tag = get_exclusive_choice_tag(instance)
    tag_list = [get_exclusive_choice_tag(i) for i in instance_list]
    return agreement_basic(tag, tag_list)


def agreement_multiple_choice(truth_instance, pred_instance_list):
    choice_tags = [c["tag"] for c in truth_instance["choices"]]
    truth_tags = get_multiple_choice_tags(truth_instance)
    pred_tags_list = [get_multiple_choice_tags(i) for i in pred_instance_list]
    mlb = MultiLabelBinarizer()
    mlb.fit(choice_tags)
    truths = mlb.transform([truth_tags] * len(pred_tags_list))
    preds = mlb.transform(pred_tags_list)
    if len(choice_tags) == 1:
        return round(float(accuracy_score(y_true=truths, y_pred=preds)), 3)
    else:
        f1_sample_scores = []
        for i in range(len(pred_tags_list)):
            if sum(truths[i]) + sum(preds[i]) == 0:
                f1_sample_scores.append(1)
            else:
                f1_sample_scores.append(float(f1_score(y_true=truths[i], y_pred=preds[i])))
        return round(float(sum(f1_sample_scores) / len(f1_sample_scores)), 3)
