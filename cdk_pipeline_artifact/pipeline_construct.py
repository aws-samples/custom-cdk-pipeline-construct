from aws_cdk import (
    aws_codecommit as codecommit,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions,
    pipelines,
    core
)


class CustomPipeline(core.Construct):

    """
        Just for test reasons, the 'id' represents the environment/branch the user is creating the pipeline: master,
        develop, staging, etc.
    """
    def __init__(self, scope: core.Construct, construct_id: str, branch: str, repository: codecommit.IRepository):
        super().__init__(scope, construct_id)

        source_artifact = codepipeline.Artifact()
        cloud_assembly_artifact = codepipeline.Artifact()

        source_action = codepipeline_actions.CodeCommitSourceAction(
            action_name='CodeCommit_Source',
            repository=repository,
            branch=branch,
            output=source_artifact
        )

        synth_action = pipelines.SimpleSynthAction(
            action_name='Cdk_Build',
            source_artifact=source_artifact,
            cloud_assembly_artifact=cloud_assembly_artifact,
            test_commands=['python -m unittest'],
            install_command='npm install -g aws-cdk && python -m pip install -r requirements.txt',
            synth_command='npx cdk synth'
        )

        pipeline_name = '{}-pipeline'.format(branch)

        self.cdk_pipeline = pipelines.CdkPipeline(
            self,
            pipeline_name,
            pipeline_name=pipeline_name,
            cloud_assembly_artifact=cloud_assembly_artifact,
            source_action=source_action,
            synth_action=synth_action
        )
