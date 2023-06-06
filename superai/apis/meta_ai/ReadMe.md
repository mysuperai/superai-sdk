# Meta-AI API setup

This module contains the implementation of communicating with the meta-ai repository.

# Requirements

- Python
- pip install `astor` for patching the schema

## Changes in schema

If the meta-ai repository is updated with a new schema element, we would have to update the
file [meta_ai_graphql_schema.py](./meta_ai_graphql_schema.py). The way to do this is using the [Makefile](./Makefile).

### Steps to update the schema

1. You can update the schema from dev using the following command
    ```bash
    cd superai/apis/meta_ai
    make schema
    ```
2. The Makefile requires a `.makerc` file in the meta_ai folder. There is a template called `.makerc.template`. Just
   remove the `.template` suffix and fill in the correct values.
The contents of this file are
   ```bash
   export HASURA_ADMIN_SECRET=<secret-key>
   export HASURA_ENDPOINT=https://metaai-dev.super.ai/v1/graphql
   ```
   You can obtain the `<secret-key>` from 1password under the key **_Hasura dev access key_**
3. If you want to reflect your local development changes (in case the branch is not merged to dev), change the `HASURA_ENDPOINT` above to where hasura is running. For eg.
   ```bash
   export HASURA_ENDPOINT=http://localhost:62250/v1/graphql
   ```