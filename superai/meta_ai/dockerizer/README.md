# Dockerizer Notes

###Building a container

To build a container which can run with Sagemaker, now we have a helpful function
```bash
superai ai docker build --image-name <name> --entry-point <file> --dockerfile <path> --command <optional; command> --worker-count <optional;worker-count> --entry-point-method <optional;method> --use-shell <optional:false>
```

Here are some points to note for this command
1. `entry-point` refers to a `.py` file that will run as entry point in the container. The folder where the entry-point script is placed will be copied on the container to maintain dependencies. The structure of the entry-point file should be like the following
    - The entry point file should have the predict method which accesses a model weight file and returns the prediction for a given input
    - It should have a _handler method_ which calls an **initializer** and **predictor**

```python
class ModelHandler():
    def __init__(self):
        self.initialized = False
        self.predictor_obj = None

    def initialize(self, context):
        self.initialized = True
        properties = context.system_properties
        # Contains the url parameter passed to the load request
        model_dir = properties.get("model_dir")
        self.predictor_obj = self.load_model(model_dir)

    def load_model(self, model_dir):
        try:
            # implementation of model loading from model_dir, should raise a RuntimeError or MemoryError when OOM
            pass
        except RuntimeError as memerr:
            import re
            if re.search('Failed to allocate (.*) Memory', str(memerr), re.IGNORECASE):
                print("Memory allocation exception: {}".format(memerr))
                raise MemoryError
            raise

    def handle(self, data):
        # Preprocess and post process the data as necessary. Returning JSON is a good idea
        return self.predictor_obj.predict(data)
    
_service = ModelHandler()


def handle(data, context):
    if not _service.initialized:
        _service.initialize(context)

    if data is None:
        return None

    return _service.handle(data)

```
2. `--entry-point-method` refers to the `handle` method above. If you use a different method name, pass it to the command.

3. With `--dockerfile` you can specify the path to a `Dockerfile` as well. Make sure there is `ENTRYPOINT` and `CMD` specified. That will be added automatically. Please use a python base or install python if you use this feature.

4. You can place a `requirements.txt` in the same folder as entry-point script location. If you mention one, its contents will be automatically installed. We use python 3.7 as default.

5. Basic information about the command can be found with 
    ```bash
    superai ai docker-build --help
   ```
6. If you use a ModelHandler class derived from BaseModel object, entry-point-method needs to be changed a bit

```python
from superai.meta_ai.base.base_ai import BaseModel


class ModelHandler(BaseModel):
   def __init__(self):
      super().__init__()

   @classmethod
   def load_weights(cls, weights_path):
      pass

   def initialize(self, context: "BaseModelContext"):
      pass

   def predict(self, input):
      pass
```
> Pass the entry point method as  `--entry-point-method ModelHandler.handle`. Every other parameter usage remains unchanged.


### Pushing the container
With the `image_name` you gave in the previous instruction, you can push the container to ECR with the command
```bash
superai ai docker push --image-name <> --region <optional;AWS region>
```


### Create an endpoint
Once the container is built and pushed to ECR, to deploy it to an endpoint, try the following command
```bash
superai ai sagemaker create-endpoint --help
# to test the endpoint creation
superai ai sagemaker test-endpoint --help
```
> Note: You must have the permissions to create an endpoint. Otherwise you would need an ARN role which can be passed using the `--arn` option

The usage of the instruction can be found by
```bash
superai ai sagemaker create-endpoint --help
```

### Deploy and test container locally
Not being able to test the container locally can be quite a nightmare during development. Here are two very necessary commands to facilitate that

```bash
superai ai docker run-local --help
superai ai docker invoke-local --help
```
