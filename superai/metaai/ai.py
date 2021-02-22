from __future__ import annotations

from typing import Dict, List, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from superai.metaai import BaseAI


class AI:
    def __init__(
        self,
        ai_definition,
        name,
        version: int = None,
        stage: str = None,
        description: str = None,
        weights_path: str = None,
        requirements: Union[str, List] = None,
        code_path: Union[str, List] = None,
        conda_env: Union[str, Dict] = None,
        ai_class: "BaseAI" = None,
        artifacts: Dict = None,
    ):
        """
        Create an ai with custom inference logic and optional data dependencies as an superai artifact.

        :param ai_definition: A dictionary representation of the input and output schema. The dictionary requires two
                              keys: ``input_schema`` and ``output_schema``. The following is an *example* dictionary
                              representation of the schema:

                                {
                                    "input_schema": Schema(my_image=dt.IMAGE),
                                    "output_schema": Schema(mnist_class=dt.EXCLUSIVE_CHOICE),
                                }
        :param name: Name of the AI. If the name already exsists, an exception will be raised

        :param version: AI integer version. If no version is specified the AI will get version 1

        :param stage: The deployment stage. Over the course of the ai’s lifecycle, an ai evolves—from development
                      to staging to production. You can transition a registered ai to one of the stages: Development,
                      Staging, Production or Archived.

        :param description: A free text description. Allows the user to describe the ai's intention.

        :param weights_path: Path to a file or directory containing model data. This is accessible in the
                          :func:`BaseAI.load_weights(weights_path) <superai.metaai.base.BaseAI.load_weights>

        :param requirements: A list of pypi requirements or the path to a requirements.txt file. If the both this
                             parameter and the :param: conda_env is specified an ValaueError is raised.

        :param code_path: A list of local filesystem paths to Python file dependencies (or directories containing file
                          dependencies). These files are *prepended* to the system path before the ai is loaded.

        :param conda_env: Either a dictionary representation of a Conda environment or the path to a Conda environment
                          yaml file. This describes the environment this ai should be run in. If ``ai_class`` is not
                          ``None``, the Conda environment must at least specify the dependencies contained in
                          :func:`get_default_conda_env()`. If `None`, the default :func:`get_default_conda_env()`
                          environment is added to the ai. The following is an *example* dictionary representation of a
                          Conda environment::

                            {
                                'name': 'superai-env',
                                'channels': ['defaults'],
                                'dependencies': [
                                    'python=3.7.2',
                                    'cloudpickle==0.5.8'
                                ]
                            }

        :param ai_class: An instance of a subclass of :class:`~AIModel`. This class is serialized using the CloudPickle
                         library. Any dependencies of the class should be included in one of the following locations:

                                - The SuperAI library.
                                - Package(s) listed in the model's Conda environment, specified by
                                  the ``conda_env`` parameter.
                                - One or more of the files specified by the ``code_path`` parameter.

                             Note: If the class is imported from another module, as opposed to being defined in the
                             ``__main__`` scope, the defining module should also be included in one of the listed
                             locations.

        :param artifacts: A dictionary containing ``<name, artifact_uri>`` entries. Remote artifact URIs are resolved
                          to absolute filesystem paths, producing a dictionary of ``<name, absolute_path>`` entries.
                          ``ai_class`` can reference these resolved entries as the ``artifacts`` property of the
                          ``context`` parameter in :func:`AIModel.load_context() <superai.metaai.models.AIModel.load_context>`
                          and :func:`AIModel.predict() <superai.metaai.models.AIModel.predict>`.

                          For example, consider the following ``artifacts`` dictionary::

                            {
                                "my_file": "s3://my-bucket/path/to/my/file"
                            }

                          In this case, the ``"my_file"`` artifact is downloaded from S3. The
                          ``ai_class`` can then refer to ``"my_file"`` as an absolute filesystem
                          path via ``context.artifacts["my_file"]``.

                          If ``None``, no artifacts are added to the model.
        """
        pass

    @classmethod
    def load(cls, name, version: int = None, stage: str = None) -> AI:
        """
        Loads an AI by name. If the version OR stage are specified that speicifc version will be loaded.

        :param name: AI name. *Required.
        :param version: An version number. *Required.
        :param stage: The AI stage. *Required.
        :return: AI object
        """
        raise NotImplementedError("Method not supported")

    def transition_model_version_stage(self, version: int, stage: str, archive_existing: bool = True):
        """
        Transitions an AI version number to the specify stage.

        :param version: AI version number. *Required.
        :param stage: Transition ai version to new stage. *Required.
        :param archive_existing: When transitioning an AI version to a particular stage, this flag dictates whether
                                 all existing ai versions in that stage should be atomically moved to the “archived”
                                 stage. This ensures that at-most-one ai version exists in the target stage. This
                                 field is by default set to True.
        :return: Updated ai version
        """
        pass

    def update_weights_path(self, weights_path: str):
        """
        Updates model weight file. Running this operation will increase the ai version.

        :param weights_path: Path to a file or directory containing model data.
        :return:
        """
        pass

    def update_ai_class(self, ai_class: str):
        """
        Updates the ai_class. Running this operation will increase the ai version.

        :param ai_class: An instance of a subclass of :class:`~AIModel`.
        :return:
        """
        pass

    def update(self, version: int = None, stage: str = None, weights_path: str = None, ai_class=None):
        """
        Update AI.

        :param version: New AI version number. If the version number already exists, this method will fail.
        :param stage: New AI stage.
        :param weights_path: New path to a file or directory containing model data.
        :param ai_class: An instance of a subclass of :class:`~AIModel`.
        :return:
        """
        pass
