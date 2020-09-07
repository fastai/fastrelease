# fastrelease
> Auto-generated tagged releases, and release notes (from GitHub issues).


`fastrelease` provides two commands that you can run from your shell:

- `nbdev_changelog`: creates a CHANGELOG.md file from closed and labeled GitHub issues
- `nbdev_tag_release`: tags and creates a release in GitHub for the current version.

## Install

`fastrelease` has no prerequisites and will run on Python 3.4 or later. You can install from pip:

`pip install fastrelease`

...or conda:

`conda install -c fastai fastrelease`

## How to use

### Set up

First, create a `settings.ini` file with the following contents (replacing the values as described below):

```
[DEFAULT]
lib_name = fastrelease
user = fastai
version = 0.0.1
```

Set `lib_name` to the name of GitHub repo, `user` to the owner of that repo, and `version` to the version number of your library. (Note that if you use [nbdev](https://nbdev.fast.ai) then you'll already have this information, so you don't need to do anything further to set it up.)

You'll need to get a GitHub [personal access token](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token) if you haven't already. To do so, [click here](https://github.com/settings/tokens/new) and enter "fastrelease" in the "Note" section, and click the `repo` checkbox.

Then click "Generate Token" at the bottom of the screen, and copy the token (the long string of letters and numbers shown). You can easily do that by clicking the little clipboard icon next to the token.

<img alt="Copying your token" width="743" caption="Copying your token" src="https://docs.fast.ai/images/att_00001.png">

Paste that token into a file called `token` into the root of your repo. You can run the following in your terminal (`cd` to the root of your repo first) to create that file:

    echo XXX > token

Replace *XXX* above with the token you copied. Also, ensure that this file isn't added to git, by running this in your terminal:

    echo token >> .gitignore

### Creating release notes

Now you're ready to create your release notes. These are created in a file called `CHANGELOG.md`.

All issues with the label **bug**, **enhancement**, or **breaking** that have been closed in your repo since your last release will be added to the top of this file. If you haven't made any releases before, then all issues with those labels will be included.

Therefore, before you create or update `CHANGELOG.md`, go to your GitHub issues page, remove `is:open` from the filter, and label any issues you want included with one of the labels above. When you've done that, you can create or update your release notes by running in your terminal:

    fastrelease_changelog

The titles and bodies of each issue will be added. Open `CHANGELOG.md` in your editor and make any edits that you want, and then commit the file to your repo (remember to `git add` it!)

### Tagging a release

It's important that you now tag a release. This will create a tag in GitHub with your current version number in `settings.ini`, and will then make it into a release:

    fastrelease_release

After you run this, be sure to increment your version number in `settings.ini`. You can either edit it manually, or if you use nbdev it can be done for you by running:

    nbdev_bump_version
