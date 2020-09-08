#!/bin/bash
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

echo "::group::Configure Git"
    git config --global user.email "github-actions[bot]@users.noreply.github.com"
    git config --global user.name "github-actions[bot]"
    git config --global user.password "$INPUT_TOKEN"
    git remote remove origin
    git remote add origin "https://github-actions[bot]:$INPUT_TOKEN@github.com/${GITHUB_REPOSITORY}.git"
echo "::endgroup::"

echo "::group::Publish Release"
    echo $INPUT_TOKEN > token
    fastrelease_release
echo "::endgroup::"

echo "::group::Bump Version"
    nbdev_bump_version
    git add settings.ini && git push
echo "::endgroup::"
