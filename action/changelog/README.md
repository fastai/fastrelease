This Action assists you in drafting a Changelog by pulling your Issues and PRs since your last release via the GitHub API.

PRs and Issues are filtered by user specified labels, and relevant information is either appended to or creates a `CHANGELOG.md` file at the root of your repository.  These changes to CHANGELOG.md are then submitted as a pull request for your review.

You can use this Action like so:

```yml
name: generate-changelog
on: workflow_dispatch
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v1
    - name: Test Action
      uses: fastai/fastrelease/changelog@master
      with:
        TOKEN: ${{ secrets.GITHUB_TOKEN }}
```
