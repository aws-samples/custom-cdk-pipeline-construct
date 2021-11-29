# Custom CDK Pipeline Construct

This project has the objective of teaching you how to build a Custom CDK Pipeline, but mainly teach you how to build
your own Custom CDK Constructs. You'll additionally learn how to implement unit tests for your Construct, and even
insert those tests in your deployment pipeline. 


## Concepts and services you should be familiar with

Before you can dive into this project, you should be familiar with a few concepts and AWS Services:
- [DevOps](https://aws.amazon.com/devops/what-is-devops/)
- [Infrastructure as Code](https://d1.awsstatic.com/whitepapers/DevOps/infrastructure-as-code.pdf?did=wp_card&trk=wp_card)
- [CI/CD](https://en.wikipedia.org/wiki/CI/CD)
  - [Building a complete CI/CD Pipeline in AWS](https://aws.amazon.com/blogs/devops/complete-ci-cd-with-aws-codecommit-aws-codebuild-aws-codedeploy-and-aws-codepipeline/)
- [Tests](https://martinfowler.com/articles/practical-test-pyramid.html) (more specifically [Unit Tests](https://martinfowler.com/articles/practical-test-pyramid.html#UnitTests))
- [Python](https://www.python.org/)
  - [unittest library](https://docs.python.org/3/library/unittest.html)
- [AWS Cloud Development Kit (CDK)](https://aws.amazon.com/cdk/)
- [AWS CloudFormation](https://aws.amazon.com/cloudformation/)
- [AWS CodePipeline](https://aws.amazon.com/codepipeline/)
- [AWS CodeBuild](https://aws.amazon.com/codebuild/)
- [AWS CodeCommit](https://aws.amazon.com/codecommit/)
- [Amazon API Gateway](https://aws.amazon.com/api-gateway/)
- [AWS Lambda](https://aws.amazon.com/lambda/)


## Architecture

When you deploy this application, you'll have a few new resources created. Here are the most important ones:
- A `master` pipeline in CodePipeline, alongside 2 CodeBuild projects
- A `develop` pipeline in CodePipeline, alongside 2 CodeBuild projects
- An API Gateway
- A 'Hello World' Lambda Function

The API Gateway and Lambda Function are part of the Application Construct. You can change everything inside here to
exactly represent the resources needed for your application.

The `master` and `develop` pipelines are part of the Pipeline Construct. If you need specific deployment steps,
additional stages, etc., you should implement your changes here.

Finally, we orchestrate the creation of our application and our pipeline in the Custom Pipeline Stack. Here's where we
reference our Git repository (in this case, CodeCommit). You should change this information so your pipelines can point
to your repository. In case you want to use GitHub as your source repository, you can check [this documentation](https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_codepipeline_actions/GitHubSourceAction.html)
or follow [this example](https://docs.aws.amazon.com/cdk/latest/guide/cdk_pipeline.html#cdk_pipeline_define).

In order to have totally separate deployments, we're going to have 2 separate stacks, one for the production environment
(`master` branch), and another one for the development environment (`develop` branch). This way, if you perform changes
to the `develop` branch, only the development pipeline is going to be triggered, and therefore, only the development
environment is going to be affected.
It's nice to say that this separation could also have been implemented in a few different ways, like with [Nested
Stacks](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-nested-stacks.html),
with another centralized Construct, etc., the final solution would be the same. 


## What is AWS CDK?

Quoting the AWS CDK service page:

>The AWS Cloud Development Kit (AWS CDK) is an open source software development framework to define your cloud
application resources using familiar programming languages.

What happens "under the hood" when you deploy an AWS CDK Stack is a conversion of everything that you wrote in your
chosen language to a CloudFormation template, and then AWS CDK automatically runs that template in CloudFormation for
you.  

To see more on how AWS CDK has introduced us the concept of 'Infrastructure is Code' instead of the usual
'Infrastructure as Code', check the AWS CDK [developer guide](https://docs.aws.amazon.com/cdk/latest/guide/home.html),
and also check its [API reference](https://docs.aws.amazon.com/cdk/api/latest/docs/aws-construct-library.html).

Additionally, it's highly recommended that you check out the [AWS CDK Workshop](https://cdkworkshop.com/). There, you're
going to learn how to use AWS CDK to build your own stacks, and even begin to learn the concept of Constructs.


## Installation and Deployment

If you checked out the AWS CDK Workshop mentioned in the previous topic, you've probably already done this. But in case
you didn't, this is how you install AWS CDK:

1. First, check out the pre-requisites page in the [Developer Guide](https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html#getting_started_prerequisites).

2. Then, run the following command to install the AWS CDK Toolkit:
    ```
    $ npm install -g aws-cdk
    ```

3. Check if the AWS CDK Toolkit was installed successfully:
    ```
    $ cdk --version
    1.21.1 (build 842cc5f)
    ```

4. Before you run this project, you need to bootstrap AWS CDK to create the needed resources for the toolkit’s operation
in you AWS Account. So run the command below:
    ```
    $ cdk bootstrap
    ```

5. Go to the AWS CodeCommit dashboard in your AWS account and create a repository (if you want, use the name
`custom-cdk-pipeline-construct` to skip step 8).

6. Clone the AWS CodeCommit repository you've just created to your local machine.

7. Download this GitHub repository's code and unzip all its content inside your AWS CodeCommit repo's local folder.

8. If you didn't use `custom-cdk-pipeline-construct` for your repo's name, open the
`cdk_pipeline_artifact/custom_pipeline_stack.py` file and change the repository name according to the one you created in 
your account:
    ```
    app_repository = codecommit.Repository.from_repository_name(self, 'CodeCommitRepo', '<YOUR_REPO_NAME_HERE>')
    ```

9. Commit and push everything to your AWS CodeCommit repository.

10. Finally, deploy the project:
    ```
    $ cdk deploy --all
    ```
   If we only had 1 stack to be created, we could simply run `cdk deploy`. However, in this case we have 2 stacks, so we
   need to specify `--all` to deploy all existing stacks. We could also deploy only 1 of our stacks if desired, running
   `cdk deploy <stack-name>`.


## What is a Construct?

Quoting the [AWS CDK Developer Guide](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html):

>Constructs are the basic building blocks of AWS CDK apps. A construct represents a "cloud component" and encapsulates
everything AWS CloudFormation needs to create the component.
>
>A construct can represent a single resource, such as an Amazon Simple Storage Service (Amazon S3) bucket, or it can 
represent a higher-level component consisting of multiple AWS resources. Examples of such components include a worker 
queue with its associated compute capacity, a cron job with monitoring resources and a dashboard, or even an entire app 
spanning multiple AWS accounts and regions.
>
>The AWS CDK includes the AWS Construct Library, which contains constructs representing AWS resources.
>
>This library includes constructs that represent all the resources available on AWS. For example, the s3.Bucket class 
represents an Amazon S3 bucket, and the dynamodb.Table class represents an Amazon DynamoDB table.

To keep diving inside this project, you should also be familiar with the different Construct levels. So let's continue
reading the API Reference:

>There are three different levels of constructs in this library, beginning with low-level constructs, which we call CFN 
Resources (or L1, short for "level 1") or Cfn (short for CloudFormation) resources. These constructs directly represent 
all resources available in AWS CloudFormation. CFN Resources are periodically generated from the AWS CloudFormation 
Resource Specification. They are named CfnXyz, where Xyz is name of the resource. For example, CfnBucket represents the 
AWS::S3::Bucket AWS CloudFormation resource. When you use Cfn resources, you must explicitly configure all resource 
properties, which requires a complete understanding of the details of the underlying AWS CloudFormation resource model.
>
>The next level of constructs, L2, also represent AWS resources, but with a higher-level, intent-based API. They provide 
similar functionality, but provide the defaults, boilerplate, and glue logic you'd be writing yourself with a CFN 
Resource construct. AWS constructs offer convenient defaults and reduce the need to know all the details about the AWS 
resources they represent, while providing convenience methods that make it simpler to work with the resource. For 
example, the s3.Bucket class represents an Amazon S3 bucket with additional properties and methods, such as 
bucket.addLifeCycleRule(), which adds a lifecycle rule to the bucket.
>
>Finally, the AWS Construct Library includes even higher-level constructs, L3, which we call patterns. These constructs 
are designed to help you complete common tasks in AWS, often involving multiple kinds of resources. For example, the 
aws-ecs-patterns.ApplicationLoadBalancedFargateService construct represents an architecture that includes an AWS Fargate
container cluster employing an Application Load Balancer (ALB). The aws-apigateway.LambdaRestApi construct represents an
Amazon API Gateway API that's backed by an AWS Lambda function.

In this project, you'll see that 2 L3 Constructs were built, the `ApplicationConstruct` and the `CustomPipeline`. Within
those, we've used 2 L3 constructs provided by AWS:
- `aws_solutions_constructs.aws_apigateway_lambda.ApiGatewayToLambda`: This Construct builds an Amazon API Gateway, with
an endpoint directed to an AWS Lambda Function, while enabling the CloudWatch logs and X-Ray tracing for both API
Gateway and Lambda. Check out the [library's documentation](https://docs.aws.amazon.com/solutions/latest/constructs/aws-apigateway-lambda.html).
- `aws_cdk.pipelines.CdkPipeline`: This Construct creates a pipeline in AWS CodePipeline to deploy AWS CDK applications.
One interesting feature of this library is that is has a `SelfMutate` step in the end of the pipeline, that deploys your
AWS CDK application and mutates the pipeline itself in case there were changes made to the it. Check out its
[documentation](https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.pipelines/CdkPipeline.html).


## How to build a custom Construct

Creating a custom Construct it a lot easier than you might think. Simply create a new class, and use the
`aws_cdk.core.Construct` as its parent. That's it! See the `ApplicationConstruct` example:
```
class ApplicationConstruct(core.Construct):
    # ...
```

After you do this, you can start implementing anything you want inside your Construct. In our `ApplicationConstruct`
example, we implemented 2 possibilities, the creation of the API Gateway with IAM Authorization or with no
authorization at all. This is not a trivial thing to do inside the `aws_solutions_constructs.aws_apigateway_lambda.ApiGatewayToLambda`
library, so we simplified this by creating our Construct and just receiving an `use_iam_authorization` parameter that,
under the hood, will do the configurations needed for each API Gateway authorization type. 

Right here we've created an L3 Construct, that uses another L3 Construct internally.

Now, imagine you have a bigger and more complex application, like an ELB in front of an ECS cluster that connects to a
DynamoDB table and saves files to an S3 bucket, and all of that behind a CloudFront distribution with a Route 53 domain.
You could implement all that infrastructure inside your own Construct, and even if you needed several different
environments, you could simply instantiate your Construct several times, and all your infrastructure would be ready for
all your environments.

That's exactly what we do with our `CustomPipeline` Construct! We created a tool that manages several resources, but can
be quickly and easily replicated. So let's check how we've done that. 


## Building a Custom CDK Pipeline with Constructs

Here, we've followed the same pattern we did in our `ApplicationConstruct`:
```
class CustomPipeline(core.Construct):
    # ...
```

In order to build a pipeline in AWS CodePipeline, we must create several stages:
1. Reference our source Git repository in CodeCommit
2. Run our unit tests and build our CDK Application
3. Deploy the application and redeploy the pipeline itself in case anything changed

To achieve that, we've created several resources. So let's begin with our first stage.

#### Referencing our source repository

Here we created a `source_artifact` (`aws_cdk.aws_codepipeline.Artifact`) to store all our repositories files during the
deployment. After that, we created a `source_action` (`aws_cdk.aws_codepipeline_actions.CodeCommitSourceAction`) using
the repository and branch provided to us, and referencing the `source_artifact` we've just created.

#### Building and running tests

To satisfy the second stage, we've built a `cloud_assembly_artifact` (`aws_cdk.aws_codepipeline.Artifact`) to store the
CloudFormation file that is going to be generated here and deployed in our third stage. Then, we created the
`synth_action` (`aws_cdk.pipelines.SimpleSynthAction`), which creates a CodeBuild project. The project has an
`install_command` step, where we can install any libraries needed for the `test_commands` and `synth_command` steps.
Next, the project runs the `test_commands` step, which will execute any tests implemented (we'll explain more about that
in the [Testing your custom Construct](#Testing your custom Construct) section of this document). And finally, in the
`synth_command` step it builds our application, which is nothing more than running `npx cdk synth` to create the
CloudFormation template that will represent the infrastructure of our application.

#### Deploying our application

Lastly, to satisfy the final stage, we created the `cdk_pipeline` (`aws_cdk.pipelines.CdkPipeline`), that will actually
create the pipeline in CodePipeline, and reference the 2 stages created previously. As we're creating our pipeline using
the `CdkPipeline`, in the end of it we're going to additionally have the `SelfMutate` stage, mentioned in the end of the
[What is a Construct?](#What is a Construct?) section of this document. The `SelfMutate` stage redeploys the AWS
CloudFormation template that deployed all this infrastructure. Therefore, the AWS CodeBuild project that will do this
needs the correct AWS CloudFormation permissions. To do so, this library uses prerelease features of the AWS CDK
framework, which can be enabled by adding the following code to the `cdk.json` of your project:

    ```
    {
      // ...
      "context": {
        "@aws-cdk/core:newStyleStackSynthesis": true
      }
    }
    ```

If you don't do this procedure, the AWS CodeBuild project will not have the correct permissions in its AWS IAM Role, and
will always fail in the `SelfMutate` step. You can see more information regarding the `CdkPipeline` library in
[this documentation](https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.pipelines/README.html).

Finally, in the creation of the `CdkPipeline`, we also reference the created `cloud_assembly_artifact`, so during the
`SelfMutate` stage it can get the CloudFormation template generated in the Build stage and deploy it.

With all that said, this might seem like a lot, and that's exactly why we created this Construct. So in the future,
instead of copying and pasting almost 30 lines of code, you can simply instantiate a `CustomPipeline` object, and you'll
have a totally working pipeline for the desired repository and branch.


## Testing your custom Construct

Tests are an important part of software development and CI/CD, so let's focus right now on how to implement unit tests
for our CDK Pipeline `CustomPipeline` Construct.

For our pipeline to be created successfully, all of the components mentioned in the [Building a Custom CDK Pipeline with
Constructs](#Building a Custom CDK Pipeline with Constructs) section of this document must be created. Therefore, those
are exactly the points we need to test: if every component was created the way they should be.

In unit tests we only test our code, we shouldn't test external libraries, so we need to mock every component from the
`aws_cdk` library and any other external library we use. That's why if you check the
`test_custom_cdk_pipeline.TestPipelineConstruct.test_should_break_if_source_action_not_created_properly` for example,
you'll see that the artifacts, repository and even the source action are mocked.

Now let's begin understanding the unit tests implementation for our Construct. There's 3 necessary things for us to
test:
- The `source_action`, that'll fetch our code from the CodeCommit repository
- The `simple_synth_action`, that'll build our CDK application and generate the CloudFormation template
- The `cdk_pipeline`, that'll create our pipeline in CodePipeline and add the `SelfMutate` step in the end of it to
deploy our app and update itself

We need to make sure that all of these components are created only once and with the correct parameters.

### Source Action

So let's start with the `source_action`. As previously mentioned, we mocked the artifacts, repository and even the
source action. 

#### Using `mock.MagicMock.side_effect`

An interesting and necessary approach we took here is the `mock.MagicMock.side_effect`. As we created 2
artifacts (`aws_cdk.aws_codepipeline.Artifact`), we need to make sure that each one of them is passed correctly in the
source action creation. So when we assign a list composed by the mocked artifacts, in their respective order, to the
`side_effect` property of the mocked `Artifact` (`aws_cdk.aws_codepipeline.Artifact`), we're inferring that whenever an
`Artifact` is created, its value will be retrieved from this list. Check out the [unittest.mock documentation](https://docs.python.org/3/library/unittest.mock.html#quick-guide)
for more details on the `side_effect` feature.

#### Why shouldn't we mock the `aws_cdk.core.Stack`?

Now there's an important thing we have to talk about. As we've said before, in unit tests we only test our code, we
shouldn't test external libraries. However, when testing Constructs we need to create an actual `Stack`
(`aws_cdk.core.Stack`) in order for it to work. If we try to mock the `Stack` object as well, the Construct creation
will fail due to how the CDK code architecture works, and none of our tests will run. For more information regarding
testing Constructs, check out [this section of the Developer Guide](https://docs.aws.amazon.com/cdk/latest/guide/testing.html).

#### Invoking the actual code

After creating the `Stack`, we need to instantiate our actual `CustomPipeline` Construct to check if the expected values
in our tests comply with what's implemented. Here's where we need the `Stack` we created, to pass as an argument when
instantiating our Construct.

#### Testing the Source Action

With all these things in mind, let's finally test the `source_action_mock`. Here we'll have to test if it was called
only once and if we're passing the expected parameters to it. To satisfy this, we'll use the
`mock.MagicMock.assert_called_once_with` method, giving the parameters we expect to have been passed during the
execution:
- action_name: can be any desired name
- repository: the mocked `repository` we created
- branch: the branch name for our test, which can also be any desired name
- output: the mocked `source_artifact` we created

To read more about the `assert_called_once_with`, check out the [unittest.mock documentation](https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock.assert_called_once_with).


### Simple Synth Action

To test the `simple_synth_action` we're going to implement some similar snippets we did in the [Source Action](#Source Action)
section, like mocking the artifacts and repository, using the `side_effect` property for the artifacts, creating the
`Stack` and invoking the actual code. The main difference is that we'll be testing the `simple_synth_action_mock`.

Again, we'll use the `assert_called_once_with`, but here we'll use the needed parameters for the
`simple_synth_action_mock`:
- action_name: can be any desired name
- source_artifact: the mocked `source_artifact` we created
- cloud_assembly_artifact: the `cloud_assembly_artifact` we created
- test_commands: the commands that will run our tests. Check the [Running our unit tests](#Running our unit tests)
section of this document for more information.
- install_command: the command to install all necessary programs and libraries for our build process to work
- synth_command: the command that will synthesise our CloudFormation template 


### CDK Pipeline

Finally, to test the `cdk_pipeline_mock` we'll also need similar snippets we implemented before, as mentioned in the
beginning of the [Simple Synth Action](#Simple Synth Action) section. However, here we'll need to use another feature
from the unittest lib.

#### Using `mock.MagicMock.return_value`

In the `cdk_pipeline_mock` we'll need to pass as a parameter the object returned by the mocked `source_action`. To
achieve this, we'll use the `return_value` property of our `source_action_mock` and assign the
`source_action_value_mock` to it. This way, when our actual code tries to get the value of `source_action_mock`, it will
receive the assigned mocked value.

We'll also need to do the same thing with the `simple_synth_action_mock`.

#### Testing the CDK Pipeline

Finally, let's test the `cdk_pipeline_mock`. Here we'll use the `assert_called_once_with` again, but with the needed
parameters for the `cdk_pipeline_mock`:
- scope: the `custom_pipeline` we created
- construct_id: the test construct id, which can be any desired name
- pipeline_name: the test pipeline name, which can be any desired name
- cloud_assembly_artifact: the `cloud_assembly_artifact_mock` we created
- source_action: the `source_action_value_mock` we created
- synth_action: the `simple_synth_action_value_mock` we created

### Running our unit tests

When using the `unittest` library, you can simply run your tests with the following command:
```
$ python -m unittest
```

The library will automatically locate the implemented tests inside the project and run them.

When running your tests, if you get a message similar with the one below, all your tests were successful:
```
.....
----------------------------------------------------------------------
Ran 5 tests in 0.018s

OK
```

However, if the message is similar to the one below, one or more of your tests have failed:
```
....F
======================================================================
FAIL: test_should_break_if_synth_action_not_created_properly (tests.unit.test_custom_cdk_pipeline.TestPipelineConstruct)
----------------------------------------------------------------------
Traceback (most recent call last):
  ...
AssertionError: expected call not found.
Expected: SimpleSynthAction(action_name='Cdk_Build', source_artifact=<MagicMock id='4368728976'>, cloud_assembly_artifact=<MagicMock id='4430777872'>, test_commands=['python -m unittest'], install_command='npm install -g aws-cdk && python -m pip install -r requirements.txt', synth_command='npx cdk synth')
Actual: SimpleSynthAction(action_name='Cdk_Build', source_artifact=<MagicMock id='4368728976'>, cloud_assembly_artifact=<MagicMock id='4430777872'>, test_commands=['python -m unittest'], install_command='npm install -g aws-cdk && python -m pip install -r requirements.txt', synth_command='npx cdk diff')

----------------------------------------------------------------------
Ran 5 tests in 0.022s

FAILED (failures=1)
```

In the message above, you can see the reason of why this specific test failed. You will receive similar messages for
each failed test. If the tests fail during the build stage of our pipeline, the whole pipeline deployment will
automatically fail as well.

When building the `synth_action` for our pipeline, we can specify the `test_commands`, just like we mentioned in the
[Building a Custom CDK Pipeline with Constructs](#Building a Custom CDK Pipeline with Constructs) section of this
document. That's where you should insert the `python -m unittest` command to test your application during the build
stage. 


## Summary

We've finally reached the end of our project. Here, we've shown you how to build a custom Construct from scratch, how to
build your own CDK Pipeline Construct, how to implement unit tests for it and how to insert those tests in your
pipeline. We thoroughly went step by step into each of these phases, showing why each piece of code was implemented, and
how you could replicate it to create your own custom Construct.

I hope this artifact was helpful and that you've learned something new!

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.
