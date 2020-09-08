#!/bin/bash
cd $(dirname "$0")/../..
act -s GITHUB_TOKEN -W .github/workflows/test-changelog.yml workflow_dispatch
