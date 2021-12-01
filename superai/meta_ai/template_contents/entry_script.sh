#!/bin/sh

if [ -z "${AWS_LAMBDA_RUNTIME_API}" ]; then
  # shellcheck disable=SC2068
  exec /usr/local/bin/aws-lambda-rie /opt/conda/envs/{{env}}/bin/python -m awslambdaric $1
else
  # shellcheck disable=SC2068
  exec /opt/conda/envs/{{env}}/bin/python -m awslambdaric $1
fi