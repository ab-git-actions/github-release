import os
import json
from github import Github

# # Load GitVersion output
# with open('gitversion.json', 'r') as f:
#     version_info = json.load(f)
#
# semver = version_info['SemVer']

# # Get environment variables
# github_token = os.environ.get('GITHUB_TOKEN')
# if not github_token:
#     raise ValueError('GITHUB_TOKEN environment variable not set')
#
# github_repository = os.environ.get('GITHUB_REPOSITORY')
# if not github_repository:
#     raise ValueError('GITHUB_REPOSITORY environment variable not set')

# Get the semantic version from environment variable
semver = os.environ.get('VERSION')
if not semver:
    raise ValueError('VERSION environment variable not set')

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
try:
    # Check if the tag already exists
    repo.get_git_ref(f"tags/{tag_name}")
    print(f"Tag {tag_name} already exists.")
except UnknownObjectException:
    print(f"Tag {tag_name} not found.")

    # Create the release
    repo.create_git_tag_and_release(
        tag=tag_name,
        tag_message=f'Release {tag_name}',
        release_name=f'Release {tag_name}',
        release_message='Description of the release',
        object=commit_sha,
        type='commit',
        draft=False,
        prerelease=False
    )
    print(f"Created tag and release {tag_name}")

# Update or create the 'latest' tag
try:
    latest_ref = repo.get_git_ref('tags/latest')
    latest_ref.edit(commit_sha, force=True)
    print("Updated 'latest' tag.")
except:
    repo.create_git_ref(ref='refs/tags/latest', sha=commit_sha)
    print("Created 'latest' tag.")

# import os
# import json
# import subprocess
# from github import Github
#
# # Get the semantic version from gitversion
# result = subprocess.run(['gitversion', '/output', 'json'], capture_output=True, text=True)
# if result.returncode != 0:
#     raise Exception(f"GitVersion failed: {result.stderr}")
# gitversion_output = result.stdout
#
# # Parse the JSON output
# version_info = json.loads(gitversion_output)
# semver = version_info['SemVer']
#
# # Use PyGithub to create a tag
# github_token = os.environ.get('GITHUB_TOKEN')
# if not github_token:
#     raise ValueError('GITHUB_TOKEN environment variable not set')
#
# g = Github(github_token)
# repo = g.get_repo('yourusername/yourrepository')
#
# # Get the latest commit SHA
# commit_sha = repo.get_commits()[0].sha
#
# # Create a tag and release
# tag_name = semver
# repo.create_git_tag_and_release(
#     tag=tag_name,
#     tag_message=f'Release {tag_name}',
#     release_name=f'Release {tag_name}',
#     release_message='Description of the release',
#     object=commit_sha,
#     type='commit',
#     draft=False,
#     prerelease=False
# )
#
# # Update or create the 'latest' tag
# try:
#     latest_ref = repo.get_git_ref('tags/latest')
#     latest_ref.edit(commit_sha)
# except Exception:
#     repo.create_git_ref(ref='refs/tags/latest', sha=commit_sha)
