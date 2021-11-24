#!/usr/bin/env python3

from aws_cdk import core

from cdk_pipeline_artifact.custom_pipeline_stack import CustomPipelineStack


app = core.App()
CustomPipelineStack(app, "master-pipeline-stack", "master")
CustomPipelineStack(app, "develop-pipeline-stack", "develop")

app.synth()
