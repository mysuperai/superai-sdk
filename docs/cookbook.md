# SuperAI Cookbook

## Instantiating an AI Instance from a Public AI (Template)

1. **List Public AIs**: Use the following command to find public AIs available for instantiation.
    ```shell
    superai ai list
    ```
2. **Note the ID**: Locate and note down the ID of the AI you wish to instantiate.
   
3. **Create Instance**: Use the noted ID to instantiate the AI.
    ```shell
    superai ai instance instantiate -u {ID} -n {MY_AI_NAME}
    ```

4. **List Instances**: You can list all accessible AI instances or filter them.
    ```shell
    superai ai instance list  # All instances
    superai ai instance list --owned-by-me  # Only your instances
    superai ai instance list --name {MY_AI_NAME}  # Filter by name
    ```

5. **View Instance Details**: To get detailed information including checkpoints and training data.
    ```shell
    superai ai instance view {AI_INSTANCE_ID} --detailed
    ```

## Deploying an AI Instance

- **Deploy**: Use the following command to deploy an AI instance.
    ```shell
    superai ai instance deploy -i {AI_INSTANCE_ID}
    ```
- **Undeploy**: To remove a deployed instance.
    ```shell
    superai ai instance undeploy -i {AI_INSTANCE_ID}
    ```

## Training an AI Instance

1. **Label Data**: Ensure that you have enough labeled ground truth data in your application. Validate the labels via the UI.

2. **Start Training**: Use the following command to initiate training.
    ```shell
    superai ai training start -m {AI_INSTANCE_ID} -a {APP_ID}
    ```
    
3. **Monitor Training**: Keep track of training progress.
    ```shell
    superai ai training list
    ```

4. **Post-Training**: After training, a new checkpoint will be generated. Your AI instance will automatically switch to using this new checkpoint.