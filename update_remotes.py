from pathlib import Path

from git import Repo
from git.exc import InvalidGitRepositoryError

# old, new = Path("./remotes.txt").read_text().split("\n\n")
old, new = Path("./work-remotes.txt").read_text().split("\n\n")


remote_map = {o: n for o, n in zip(old.split("\n"), new.split("\n")[1:])}

print(remote_map)

for project in Path("..").iterdir():
    if not project.is_dir():
        continue
    print(project)

    try:
        r = Repo(str(project))
    except InvalidGitRepositoryError:
        print(f"{project} is not a git repo")
        continue

    try:
        old_url = r.remote().url
    except ValueError:
        print(f"{project} has no remote")
        continue

    if old_url in remote_map.keys():

        new_remote = remote_map[old_url]

        print(f"Changine remote {old_url} to {new_remote}")

        r.delete_remote("origin")

        r.create_remote("origin", new_remote)
    else:
        print(f"did not find {old_url} in remote map")
