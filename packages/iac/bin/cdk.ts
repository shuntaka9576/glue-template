#!/usr/bin/env node
import * as cdk from 'aws-cdk-lib';
import { DataPlatFormStack } from '../lib/data-platform-stack';

const app = new cdk.App();

new DataPlatFormStack(app, `data-platform-stack`);
