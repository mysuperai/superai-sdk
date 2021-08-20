import uuid

import cv2
import superai_schema.universal_schema.data_types as dt
import superai_schema.universal_schema.task_schema_functions as df

from superai.data_program import DataProgram, Project, Task, Worker
from superai.data_program.utils import download_content, sign_url

dp_definition = {
    "input_schema": dt.bundle(video_url=dt.VIDEO),
    "parameter_schema": dt.bundle(instructions=dt.TEXT, keypoint_specs_url=dt.URL),
    "output_schema": dt.bundle(label=dt.VIDEO_BOUNDING_BOX_KEYPOINT),
}

DP_NAME = "VideoBoundingBoxKeypoint" + str(uuid.getnode())

dp = DataProgram(name=DP_NAME, definition=dp_definition, add_basic_workflow=False)


def single_task_workflow(inputs, params):
    video_url = inputs["video_url"]

    # Sign video URL if it is a datasets URL
    signed_url = sign_url(inputs["video_url"])

    # Get video frame rate
    vid = cv2.VideoCapture(signed_url)
    if not vid.isOpened():
        raise IOError("Couldn't open video file {}".format(signed_url))
    frames_per_sec = vid.get(cv2.CAP_PROP_FPS)

    # Get keypoint specs json
    # This should contain boxChoices, keypointChoices and keypointTemplates in a form compliant with
    # the VIDEO_BOUNDING_BOX_KEYPOINT schema
    keypoint_specs = download_content(params["keypoint_specs_url"])

    task = Task(name="annotate_vbbk", max_attempts=10)
    task_inputs = [df.text(params["instructions"])]
    task_outputs = [
        df.video_bounding_box_keypoint(
            video_url=video_url,
            frame_rate=frames_per_sec,
            box_choices_obj=keypoint_specs.get("boxChoices"),
            keypoint_choices_obj=keypoint_specs.get("keypointChoices"),
            keypoint_templates=keypoint_specs.get("keypointTemplates"),
            keypoint_edges=keypoint_specs.get("keypointEdges"),
            keypoint_polygons=keypoint_specs.get("keypointPolygons"),
        )
    ]
    task.process(task_inputs, task_outputs)

    return {"label": task.output.get("values", [])[0].get("schema_instance")}


dp.add_workflow(single_task_workflow, name="basic_vbbk", default=True)

# ------------------------------------------------------------------------------------

# Create a project
project = Project(
    dataprogram=dp,
    name="My Facial Keypoint Project",
    params={
        "instructions": "Please track keypoints for all facial parts visible in the video. "
        "Detailed instructions are provided for each facial part below.",
        "keypoint_specs_url": "https://superai-public.s3.amazonaws.com/keypoint_template_with_polygon.json",
    },
)

# Submit data for labelling
input_urls = [
    "https://superai-public.s3.amazonaws.com/example_imgs/vbbk/sample_eye_1.mp4",
    "https://superai-public.s3.amazonaws.com/example_imgs/vbbk/sample_mouth_1.mp4",
]
job_inputs = [{"video_url": u} for u in input_urls]
labels = project.process(inputs=job_inputs, worker=Worker.me, open_browser=True)
