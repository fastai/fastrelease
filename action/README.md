This Action performs the following steps:

1.  Generates a new tag based on the version number in `settings.ini` file in the root of your repo.
2.  Uploads this tagged release to GitHub.
3.  Bumps the version number in `settings.ini` and commits that to GitHub.

You usually want to use this Action with the [fastai/fastrelease/action/changelog](https://github.com/fastai/fastrelease/tree/changelog-instructions/action/changelog) action such that when an appropriate pull request gets merged a release is automatically generated.

You can use this action as follows:

```yaml
name: test-publish
on: workflow_dispatch #TODO see event after automated pull request is merged and change this
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - uses: actions/setup-python@v2
      with:
        python-version: '3.7'
        architecture: 'x64'
    - uses: fastai/fastrelease/action/publish@master
      with:
        token: ${{ secrets.GITHUB_TOKEN }}
```
