import base64
import json
import os
import zlib
from urllib.request import urlretrieve

import boto3
import mrcnn.model as modellib
import numpy as np
import pandas as pd
import skimage.io
from mrcnn import utils
from mrcnn.config import Config

from superai.meta_ai import BaseModel

s3 = boto3.client("s3")

_MODEL_PATH = os.path.join("sagify_base/local_test/test_dir/", "model")
# _MODEL_PATH = "s3://canotic-ai/model/mask-rcnn-model.tar.gz"
# _MODEL_PATH = 'Mask_RCNN'  # Path for models

# COCO Class names
# Index of the class in the list is its ID. For example, to get ID of
# the teddy bear class, use: class_names.index('teddy bear')
class_names = [
    "BG",
    "person",
    "bicycle",
    "car",
    "motorcycle",
    "airplane",
    "bus",
    "train",
    "truck",
    "boat",
    "traffic light",
    "fire hydrant",
    "stop sign",
    "parking meter",
    "bench",
    "bird",
    "cat",
    "dog",
    "horse",
    "sheep",
    "cow",
    "elephant",
    "bear",
    "zebra",
    "giraffe",
    "backpack",
    "umbrella",
    "handbag",
    "tie",
    "suitcase",
    "frisbee",
    "skis",
    "snowboard",
    "sports ball",
    "kite",
    "baseball bat",
    "baseball glove",
    "skateboard",
    "surfboard",
    "tennis racket",
    "bottle",
    "wine glass",
    "cup",
    "fork",
    "knife",
    "spoon",
    "bowl",
    "banana",
    "apple",
    "sandwich",
    "orange",
    "broccoli",
    "carrot",
    "hot dog",
    "pizza",
    "donut",
    "cake",
    "chair",
    "couch",
    "potted plant",
    "bed",
    "dining table",
    "toilet",
    "tv",
    "laptop",
    "mouse",
    "remote",
    "keyboard",
    "cell phone",
    "microwave",
    "oven",
    "toaster",
    "sink",
    "refrigerator",
    "book",
    "clock",
    "vase",
    "scissors",
    "teddy bear",
    "hair drier",
    "toothbrush",
]


class ModelService(BaseModel):
    def __init__(self):
        super().__init__()
        self.model = None
        self.initialized = False

    def initialize(self, context):
        class InferenceConfig(Config):
            # Set batch size to 1 since we'll be running inference on
            # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
            NAME = "inference"
            GPU_COUNT = 1
            IMAGES_PER_GPU = 1
            # Number of classes (including background)
            NUM_CLASSES = 1 + 80  # COCO has 80 classes

        config = InferenceConfig()
        config.display()

        print("Initialised class...")
        self.initialized = True
        properties = context.system_properties
        _MODEL_PATH = properties.get("model_dir")
        if self.model is None:
            print("Model Content : ", os.listdir(_MODEL_PATH))
            # Local path to trained weights file
            COCO_MODEL_PATH = os.path.join(_MODEL_PATH, "mask_rcnn_coco.h5")
            # Download COCO trained weights from Releases if needed
            try:
                if not os.path.exists(COCO_MODEL_PATH):
                    utils.download_trained_weights(COCO_MODEL_PATH)
                # Create model object in inference mode.
                model = modellib.MaskRCNN(mode="inference", model_dir=os.path.join("logs"), config=config)

                # Load weights trained on MS-COCO
                model.load_weights(COCO_MODEL_PATH, by_name=True)
                self.model = model
            except RuntimeError:
                raise MemoryError

        return self.model

    def predict_from_image(self, path, class_id=3):
        image = skimage.io.imread(path)

        # Run detection
        clf = self.model
        print("model retrieved.")
        results = clf.detect([image], verbose=0)
        print("detection on image done.")
        # Visualize results
        r = results[0]

        # get indices corresponding to unwanted classes
        indices_to_remove = np.where(r["class_ids"] != class_id)

        # remove corresponding entries from `r`
        new_masks = np.delete(r["masks"], indices_to_remove, axis=2)
        scores = np.delete(r["scores"], indices_to_remove, axis=0)
        aggregate_mask = np.logical_not(new_masks.any(axis=2))
        class_ids = np.delete(r["class_ids"], indices_to_remove, axis=0)

        return {
            "new_masks": new_masks,
            "aggregate_mask": aggregate_mask,
            "scores": scores,
            "class_ids": class_ids,
        }

    def predict_intermediate(self, input):
        image_urls = input["image_url"]
        predictions = []
        for i, url in enumerate(image_urls):
            image_path = f"image_{i}.jpg"
            # download image
            urlretrieve(url, image_path)
            print("image retrieved")
            image_path = os.getcwd() + "/" + image_path
            prediction = self.predict_from_image(image_path)
            print("predict from image done.")
            new_masks = prediction["new_masks"]
            aggregate_mask = prediction["aggregate_mask"]
            n_masks = new_masks.shape[-1]
            pred = []
            for inst in range(n_masks):
                pred.append(self._handle_mask(prediction, inst))
                print(f"processing mask number {inst} done")
            # num_workers = mp.cpu_count() // 4
            # with Pool(num_workers) as pool:
            #     result = [pool.apply_async(_handle_mask, (prediction, i),) for i in range(n_masks)]
            #     pred = [res.get(timeout=15) for res in result]
            print("everything done, uploading data.")
            # data_uri = save_and_upload(aggregate_mask)
            # pred.append({
            #     "category": "Background",
            #     "maskUrl": data_uri,
            #     "instance": 0
            # })
            predictions.append(pred)

        return predictions

    def predict(self, json_input):
        """
        Prediction given the request input
        :param json_input: [dict], request input
        :return: [dict], prediction
        """

        # transform json_input and assign the transformed value to model_input
        print("json input", json_input)
        json_input = json_input[0]["body"]
        json_input = json_input.decode("utf-8")
        print("Fixed json input", json_input)
        try:
            model_input = pd.read_json(json.loads(json_input))
        except ValueError:
            model_input = pd.read_json(json_input)
        predictions = self.predict_intermediate(model_input)
        print("Predictions: ", predictions)

        # TODO If we have more than 1 model, then create additional classes similar to ModelService
        # TODO where each of one will load one of your models

        # # transform predictions to a list and assign and return it
        # prediction_list = []
        # output_keys = set([key.split("_")[0] for key in predictions.keys()])
        # for index, row in predictions.iterrows():
        #     out_row = {key: {} for key in output_keys}
        #     for i, j in row.items():
        #         name, p_type = i.split("_")
        #         if p_type == "predictions":
        #             p_type = "prediction"
        #         if p_type == "probabilities":
        #             p_type = "probability"
        #         out_row[name][p_type] = j
        #     prediction_list.append(out_row)

        return predictions

    def train(self, input_data_path, model_save_path, hyperparams_path=None):
        pass

    @classmethod
    def load_weights(cls, weights_path):
        pass

    @staticmethod
    def get_encoding_string(mask):
        data = zlib.compress(mask)
        encoded_string = base64.b64encode(data).decode("utf-8")
        return encoded_string

    def _handle_mask(self, prediction, inst):
        new_masks = prediction["new_masks"]
        scores = prediction["scores"]
        class_ids = prediction["class_ids"]
        print(f"processing mask number {inst}")
        mask = new_masks[..., inst]
        mask_data = self.get_encoding_string(mask)
        class_id = class_ids[inst]
        w, h = mask.shape[:2]
        print(f"processing mask number {inst} done")
        return {
            "category": class_names[class_id],
            "class_id": int(class_id),
            "maskData": mask_data,
            "instance": inst,
            "score": float(scores[inst]),
            "width": w,
            "height": h,
        }
