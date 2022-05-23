import os.path
import shutil

from superai.meta_ai.ai import AI, AITemplate, TrainingOrchestrator
from superai.meta_ai.parameters import (
    Config,
    HyperParameterSpec,
    ModelParameters,
    TrainingParameters,
)
from superai.meta_ai.schema import Schema

#%%
if os.path.exists(".AISave"):
    shutil.rmtree(".AISave")
#%%
template = AITemplate(
    input_schema=Schema(),
    output_schema=Schema(),
    configuration=Config(),
    name="MnistTrainingTemplate",
    description="Template of Sample MNIST training",
    model_class="MnistModel",
    requirements=["tensorflow==2.3.0", "polyaxon"],
    code_path=["resources/runDir"],
    artifacts={"run": "resources/runDir/run_this.sh"},
)
ai = AI(
    ai_template=template,
    input_params=template.input_schema.parameters(),
    output_params=template.output_schema.parameters(),
    name="mnist_training",
    version=1,
    description="AI instance of sample MNIST training",
)
#%%
ai.push(overwrite=True)
#%%
ai.training_deploy(
    orchestrator=TrainingOrchestrator.AWS_EKS,
    training_data_dir="./training_data",
    build_all_layers=False,
    training_parameters=TrainingParameters(
        hyperparameters=HyperParameterSpec(trainable=True, optimizer="adam", log_learning_rate=-3, epochs=10),
        model_parameter=ModelParameters(conv1_size=32, conv2_size=64, hidden1_size=500, dropout=0.8),
    ),
)
#%%
