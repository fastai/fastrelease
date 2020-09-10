const { Octokit } = require("@octokit/rest");
const octokit = new Octokit({
    auth: `${process.env.INPUT_TOKEN}`,
  });

github_repo = process.env.GITHUB_REPOSITORY.split('/');
octokit.issues.listForRepo({
    owner: `${github_repo[0]}`,
    repo: `${github_repo[1]}`,
    state: 'all',
}).then(response => console.log(response.data[0].number))
