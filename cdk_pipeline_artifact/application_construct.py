from aws_cdk import (
    aws_lambda as lambda_,
    aws_apigateway as api_gateway,
    core
)
from aws_solutions_constructs import aws_apigateway_lambda


class ApplicationConstruct(core.Construct):

    def __init__(self, scope: core.Construct, construct_id: str) -> None:
        super().__init__(scope, construct_id)
        self.__create_api_with_iam_authorization()

    def __create_api_with_iam_authorization(self):
        return aws_apigateway_lambda.ApiGatewayToLambda(
            self, 'ApiGatewayToLambdaFunction',
            lambda_function_props=self.__get_lambda_function_props("backend")
        )

    def __get_lambda_function_props(self, code_path):
        return {
            "runtime": lambda_.Runtime.PYTHON_3_7,
            "handler": 'index.handler',
            "code": lambda_.Code.from_asset(code_path)
        }
