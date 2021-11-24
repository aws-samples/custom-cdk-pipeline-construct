from aws_cdk import (
    aws_codecommit as codecommit,
    core
)
from pipeline_construct import CustomPipeline
from application_construct import ApplicationConstruct


class CustomPipelineStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, branch: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ApplicationConstruct(self, "{}-app-stack".format(branch))

        app_repository = codecommit.Repository.from_repository_name(self, 'CodeCommitRepo', 'cdk-pipeline-artifact')
        CustomPipeline(self, 'custom-{}-pipeline'.format(branch), branch=branch, repository=app_repository)
