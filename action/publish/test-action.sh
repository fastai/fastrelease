#!/bin/bash
cd $(dirname "$0")/../..
act -P ubuntu-latest=nektos/act-environments-ubuntu:18.04 -s GITHUB_TOKEN -W .github/workflows/test-publish.yml workflow_dispatch
