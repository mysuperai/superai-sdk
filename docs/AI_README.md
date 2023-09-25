## AI models

You can create an AI model repository and deploy it in our EKS infrastructure. Our CI/CD automation will run code quality checks and deploy the models automatically.
Though not necessary, we recommend that certain conventions are followed so the directory structure is fairly uniform across different AI model repos. You will need:

- A `config.yml` file. This is where you will specify the name and version of your AI model, any deployment parameters, input / output schema, and requirements of your model.
- The model requirements can be specified via a conda `environment.yml` file or a pip `requirements.txt` file, or both. In the general case we recommend to list your requirements in a conda environment file, which can also contain pip requirements, unless your model is simple enough in which case the `requirements.txt` file may suffice.
- A `setup.sh` script. This script runs after installation of your model requirements in a context where you have full control over your model files. Use this optional shell script to setup any model dependencies that require shell scripting and cannot be easily captured by conda or pip requirements.
- The Python files for your model should be located inside the directory `model_class_path`. The name of the directory is not important, so feel free to add a meaningful name for your application. Though less common, if you would like to split your Python files in multiple directories then list your other code folders using `code_path`.
- Your model file should subclass `superai.meta_ai.BaseAI` and follow camel case convention (e.g. MyFancyModel.py). Write the model file name under `model_class` in your `config.yml` file. In this model file define a Python class with the same name as your model. Put any helper functions in other Python files in the same directory.
- A test folder with one or multiple files in JSON format. These test inputs will be used to test your model during CI/CD execution. You can run these tests locally by running `superai ai predictor-test` after running `superai ai local-deploy`. Add `--log` to `superai ai local-deploy` to follow your model logs during testing.
- Though not necessary, please consider adding a `README.md` explaining briefly the purpose of your AI model with some links for further reading and a `LICENSE` file if your model is to be made public.
- Code linting checks can be specified with a `.pre-commit-config.yaml` file. To ensure the CI/CD pipeline runs for your AI model repo copy a `Jenkinsfile` from one existing model repo into the project root directory.


### Installing Custom Dependencies

Sometimes, PIP or Conda packages may not suffice due to system-level dependencies. To address this:

- Create a bash script named `setup.sh` in your AI model repository's root directory.
- This script will execute at the end of the build process, post PIP and Conda installations.
- Specify the script path in your config file as shown below:

```yaml
artifacts:
    run: setup.sh
```

##  AI Cookbook

Check out the [AI Cookbook](./cookbook.md) for common use cases and examples.
