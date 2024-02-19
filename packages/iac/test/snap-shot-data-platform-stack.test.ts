import * as cdk from 'aws-cdk-lib';
import { Template } from 'aws-cdk-lib/assertions';
import { DataPlatFormStack } from '../lib/data-platform-stack';

test('snapshot test', () => {
  const app = new cdk.App();
  const stack = new DataPlatFormStack(app, 'data-platform-stack');
  const template = Template.fromStack(stack).toJSON();

  template.Resources.GlueScriptDeployCustomResourceFD1DDCB8.Properties.SourceObjectKeys =
    null;

  expect(template).toMatchSnapshot();
});
