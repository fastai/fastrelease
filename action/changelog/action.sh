#!/bin/bash

# exit when any command fails
set -e

echo "::group::Validate Information"  
    function check_env() {
        if [ -z $(eval echo "\$$1") ]; then
            echo "Variable $1 not found.  Exiting..."
            exit 1
        fi
    }
    check_env "INPUT_TOKEN"
    echo "::add-mask::$INPUT_TOKEN"
echo "::endgroup::"

echo "::group::Update CHANGELOG.md"  
    echo $INPUT_TOKEN > token
    fastrelease_changelog
echo "::endgroup::"

echo "::group::Push Changes To Branch"
    num_issues=$(node /nissues.js)
    export BRANCH_NAME="fastrelease-action-changelog-$num_issues"
    echo "Target branch: $BRANCH_NAME"
    echo "::set-output name=branch_name::$BRANCH_NAME"
    git config --global user.email "github-actions[bot]@users.noreply.github.com"
    git config --global user.name "github-actions[bot]"
    git config --global user.password "$INPUT_TOKEN"
    git remote remove origin
    git remote add origin "https://github-actions[bot]:$INPUT_TOKEN@github.com/${GITHUB_REPOSITORY}.git"
    git checkout -B $BRANCH_NAME
    git add CHANGELOG.md
    git commit -m'Update CHANGELOG.md'
    git push -f --set-upstream origin $BRANCH_NAME
echo "::endgroup::"

echo "::group::Open Pull Request"
    node /pr.js
echo "::endgroup::"
