const { Octokit } = require("@octokit/rest");
const octokit = new Octokit({
    auth: `${process.env.INPUT_TOKEN}`,
  });

github_repo = process.env.GITHUB_REPOSITORY.split('/');

octokit.pulls.create({
    owner: `${github_repo[0]}`,
    repo: `${github_repo[1]}`,
    title: '[bot] Update CHANGELOG.md',
    head: 'fastrelease-action-changelog',
    base: 'master',
    body: "This is an automated PR with an update to CHANGELOG.md.  Please edit this file as desired before merging."
})
