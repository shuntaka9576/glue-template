import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';

type Props = {} & cdk.StackProps;

const GLUE_SCRIPT_LOCATION = 'glue/scripts';

export class DataPlatFormStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: Props) {
    super(scope, id, props);

    const ioBucket = new cdk.aws_s3.Bucket(this, 'IoBucket', {
      bucketName: `io-${this.region}-${this.account}`,
      blockPublicAccess: cdk.aws_s3.BlockPublicAccess.BLOCK_ALL,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      autoDeleteObjects: true,
    });

    const glueSystemBucket = new cdk.aws_s3.Bucket(this, 'guleBucket', {
      bucketName: `glue-system-${this.region}-${this.account}`,
      blockPublicAccess: cdk.aws_s3.BlockPublicAccess.BLOCK_ALL,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      autoDeleteObjects: true,
    });

    new cdk.aws_s3_deployment.BucketDeployment(this, 'GlueScriptDeploy', {
      sources: [cdk.aws_s3_deployment.Source.asset('../src-glue/src')],
      destinationBucket: glueSystemBucket,
      destinationKeyPrefix: GLUE_SCRIPT_LOCATION,
    });

    const glueJobRole = new cdk.aws_iam.Role(this, 'GlueJobRole', {
      assumedBy: new cdk.aws_iam.CompositePrincipal(
        new cdk.aws_iam.ServicePrincipal('glue.amazonaws.com')
      ),
      managedPolicies: [
        cdk.aws_iam.ManagedPolicy.fromAwsManagedPolicyName(
          'service-role/AWSGlueServiceRole'
        ),
      ],
      inlinePolicies: {
        inlinePolicies: cdk.aws_iam.PolicyDocument.fromJson({
          Version: '2012-10-17',
          Statement: [
            {
              Effect: 'Allow',
              Action: ['s3:ListBucket'],
              Resource: [`arn:aws:s3:::${glueSystemBucket.bucketName}`],
            },
            {
              Effect: 'Allow',
              Action: 's3:*Object',
              Resource: [`arn:aws:s3:::${glueSystemBucket.bucketName}/*`],
            },
            {
              Effect: 'Allow',
              Action: ['s3:ListBucket'],
              Resource: [`arn:aws:s3:::${ioBucket.bucketName}`],
            },
            {
              Effect: 'Allow',
              Action: 's3:*Object',
              Resource: [`arn:aws:s3:::${ioBucket.bucketName}/*`],
            },
          ],
        }),
      },
    });

    const jobNames = ['convert-fruits-job'];

    jobNames.map((jobName) => {
      const script_name = jobName.replace(/-/g, '_');

      new cdk.aws_glue.CfnJob(this, `${jobName}`, {
        name: `${jobName}`,
        command: {
          name: 'glueetl',
          pythonVersion: '3',
          scriptLocation: `s3://${glueSystemBucket.bucketName}/${GLUE_SCRIPT_LOCATION}/${script_name}.py`,
        },
        role: glueJobRole.roleArn,
        numberOfWorkers: 2,
        glueVersion: '4.0',
        workerType: 'G.1X',
        defaultArguments: {
          '--enable-glue-datacatalog': 'TRUE',
          '--enable-metrics': 'TRUE',
          '--enable-spark-ui': 'TRUE',
          '--enable-job-insights': 'FALSE',
          '--enable-continuous-cloudwatch-log': 'TRUE',
          '--job-language': 'python',
          '--job-bookmark-option': 'job-bookmark-disable',
          '--TempDir': `s3://${glueSystemBucket.bucketName}/glue/temporary/`,
          '--spark-event-logs-path': `s3://${glueSystemBucket.bucketName}/glue/sparkHistoryLogs/`,
          '--IO_S3_BUCKET': ioBucket.bucketName,
        },
      });
    });
  }
}
