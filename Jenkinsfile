#!/usr/bin/env groovy

library identifier: 'superai-sdk-automation@main', retriever: modernSCM(
    [$class       : 'GitSCMSource',
     remote       : 'https://github.com/mysuperai/superai-sdk-automation.git',
     credentialsId: 'sueprai-ci-github-token'])

buildPipeline(this, [name: "superai-sdk"])