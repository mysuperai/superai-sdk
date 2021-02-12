from collections import Counter

import superai_schema.universal_schema.task_schema_functions as df

from superai.data_program.combiner.schema_getters import get_exclusive_choice_tag, get_multiple_choice_tags


def basic_majority(value_list):
    return Counter(value_list).most_common(1)[0][0]


def multivalue_majority(values_list, threshold=0.5):
    flattened_values = [item for sublist in values_list for item in sublist]
    category_counts = Counter(flattened_values)
    # What fraction of heroes selected each category?
    category_frac = {ri: count / len(values_list) for ri, count in category_counts.items()}
    return [category for category, count in category_frac.items() if count >= threshold]


def _get_tag_value_map(choices_obj):
    return {c["tag"]: c["value"] for c in choices_obj}


def exclusive_choice_majority(instance_list):
    """Combine exclusive-choice schema instances using majority vote.

    :param instance_list: A list of objects that comply with the exclusive-choice schema.
    :return: A single exclusive-choice object.
    """
    tags = [get_exclusive_choice_tag(i) for i in instance_list]
    majority_vote_tag = basic_majority(tags)
    return df.exclusive_choice(choices_obj=instance_list[0]["choices"], selection=int(majority_vote_tag))[
        "schema_instance"
    ]


def multiple_choice_majority(instance_list):
    """Combine multiple-choice schema objects using majority vote.

    :param instance_list: A list of objects that comply with the multiple-choice schema.
    :return: A single multiple-choice object.
    """
    tag_list = [get_multiple_choice_tags(i) for i in instance_list]
    majority_vote_tags = multivalue_majority(tag_list)
    return df.multiple_choice(choices_obj=instance_list[0]["choices"], selections=[int(t) for t in majority_vote_tags])[
        "schema_instance"
    ]
