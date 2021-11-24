import json
import unittest
import mock
from mock import patch
from aws_cdk import core

import sys
sys.path.insert(1, '../..')

from cdk_pipeline_artifact import pipeline_construct


class TestCDKJson(unittest.TestCase):

    def test_should_break_if_new_style_stack_synthesis_is_not_configured(self):
        with open("cdk.json", "r") as cdk_json_file:
            cdk_json_content = json.loads(cdk_json_file.read())
            self.assertTrue("@aws-cdk/core:newStyleStackSynthesis" in cdk_json_content.get("context", {}))

    def test_should_break_if_new_style_stack_synthesis_is_false(self):
        with open("cdk.json", "r") as cdk_json_file:
            cdk_json_content = json.loads(cdk_json_file.read())
            context = cdk_json_content.get("context", {})
            self.assertTrue(context.get("@aws-cdk/core:newStyleStackSynthesis", False) is True)


class TestPipelineConstruct(unittest.TestCase):

    @patch('pipeline_construct.codepipeline.Artifact')
    @patch('pipeline_construct.pipelines.CdkPipeline')
    @patch('pipeline_construct.pipelines.SimpleSynthAction')
    @patch('pipeline_construct.codepipeline_actions.CodeCommitSourceAction')
    def test_should_break_if_source_action_not_created_properly(
            self, source_action_mock, simple_synth_action_mock, cdk_pipeline_mock, artifact_mock):
        source_artifact_mock = mock.MagicMock()
        cloud_assembly_artifact_mock = mock.MagicMock()
        artifact_mock.side_effect = [source_artifact_mock, cloud_assembly_artifact_mock]
        repository_mock = mock.MagicMock()
        branch = 'test'

        stack = core.Stack()
        pipeline_construct.CustomPipeline(stack, 'test-pipeline', branch=branch, repository=repository_mock)

        source_action_mock.assert_called_once_with(
            action_name='CodeCommit_Source',
            repository=repository_mock,
            branch=branch,
            output=source_artifact_mock
        )

    @patch('pipeline_construct.codepipeline.Artifact')
    @patch('pipeline_construct.pipelines.CdkPipeline')
    @patch('pipeline_construct.pipelines.SimpleSynthAction')
    @patch('pipeline_construct.codepipeline_actions.CodeCommitSourceAction')
    def test_should_break_if_synth_action_not_created_properly(
            self, source_action_mock, simple_synth_action_mock, cdk_pipeline_mock, artifact_mock):
        source_artifact_mock = mock.MagicMock()
        cloud_assembly_artifact_mock = mock.MagicMock()
        artifact_mock.side_effect = [source_artifact_mock, cloud_assembly_artifact_mock]
        repository_mock = mock.MagicMock()

        stack = core.Stack()
        pipeline_construct.CustomPipeline(stack, 'test-pipeline', branch='test', repository=repository_mock)

        simple_synth_action_mock.assert_called_once_with(
            action_name='Cdk_Build',
            source_artifact=source_artifact_mock,
            cloud_assembly_artifact=cloud_assembly_artifact_mock,
            test_commands=['python -m unittest'],
            install_command='npm install -g aws-cdk && python -m pip install -r requirements.txt',
            synth_command='npx cdk synth'
        )

    @patch('pipeline_construct.codepipeline.Artifact')
    @patch('pipeline_construct.pipelines.CdkPipeline')
    @patch('pipeline_construct.pipelines.SimpleSynthAction')
    @patch('pipeline_construct.codepipeline_actions.CodeCommitSourceAction')
    def test_should_break_if_cdk_pipeline_not_created_properly(
            self, source_action_mock, simple_synth_action_mock, cdk_pipeline_mock, artifact_mock):
        source_action_value_mock = mock.MagicMock()
        source_action_mock.return_value = source_action_value_mock
        simple_synth_action_value_mock = mock.MagicMock()
        simple_synth_action_mock.return_value = simple_synth_action_value_mock

        source_artifact_mock = mock.MagicMock()
        cloud_assembly_artifact_mock = mock.MagicMock()
        artifact_mock.side_effect = [source_artifact_mock, cloud_assembly_artifact_mock]
        repository_mock = mock.MagicMock()

        stack = core.Stack()
        branch = 'test'
        custom_pipeline = pipeline_construct.CustomPipeline(stack, '{}-pipeline', branch=branch, repository=repository_mock)

        pipeline_name = '{}-pipeline'.format(branch)
        cdk_pipeline_mock.assert_called_once_with(
            custom_pipeline,
            pipeline_name,
            pipeline_name=pipeline_name,
            cloud_assembly_artifact=cloud_assembly_artifact_mock,
            source_action=source_action_value_mock,
            synth_action=simple_synth_action_value_mock
        )
