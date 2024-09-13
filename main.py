import os

from color_log import log
from github import Github
from github.GithubException import UnknownObjectException

logger = log(module="DEBUG")

# Get the semantic version from environment variable
semver = os.environ.get('VERSION')
if not semver:
    raise logger.error('VERSION environment variable not set')

# Get environment variables
github_token = os.environ.get('GITHUB_TOKEN')
if not github_token:
    raise ValueError('GITHUB_TOKEN environment variable not set')

github_repository = os.environ.get('GITHUB_REPOSITORY')
if not github_repository:
    raise ValueError('GITHUB_REPOSITORY environment variable not set')

# Initialize PyGithub
g = Github(github_token)
repo = g.get_repo(github_repository)

# Get the latest commit SHA
commit_sha = os.popen('git rev-parse HEAD').read().strip()

# Create a tag and release
tag_name = semver


def create_release():
    try:
        # Check if the tag already exists
        repo.get_git_ref(f"tags/{tag_name}")
        logger.warning(f"😅Tag {tag_name} already exists.")
    except UnknownObjectException:

        logger.debug(f"😔Tag {tag_name} not found.")

        # Create the release
        git_release = repo.create_git_tag_and_release(
            tag=tag_name,
            tag_message=f'Release {tag_name}',
            release_name=f'Release {tag_name}',
            release_message='Description of the release',
            object=commit_sha,
            type='commit',
            draft=False,
            prerelease=False
        )
        logger.info(f"🎉 Release created {git_release.html_url}")
        set_output("release_url", git_release.html_url)

    # Update or create the 'latest' tag
    try:
        latest_ref = repo.get_git_ref('tags/latest')
        latest_ref.edit(commit_sha, force=True)
        logger.info("😃 Updated 'latest' tag.")
    except:
        repo.create_git_ref(ref='refs/tags/latest', sha=commit_sha)
        logger.info("🎉 Release created")


def set_output(name, value):
    # Append output to the GITHUB_OUTPUT environment variable file
    output_file = os.getenv('GITHUB_OUTPUT')
    if output_file:
        with open(output_file, 'a') as file:
            file.write(f"{name}={value}\n")


if __name__ == "__main__":
    create_release()
