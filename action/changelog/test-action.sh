#!/bin/bash
cd $(dirname "$0")/../..
act -s GITHUB_TOKEN -W .github/workflows/test-action.yml workflow_dispatch
