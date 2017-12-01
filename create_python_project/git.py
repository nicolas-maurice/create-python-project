"""
    create_python_project.git
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Implements functions to enable automatic manipulations of a project as a git repository

    :copyright: (c) 2017 by Nicolas Maurice.
    :license: BSD, see LICENSE.rst for more details.
"""

from git import Repo


class RepositoryManager(Repo):
    """Implements functions to automatically manipulate the project has a git repository"""

    def get_tags(self):
        """Return ordered list of tags of the project ordered from most recent to oldest"""
        return sorted(self.tags, key=lambda tag: tag.commit.committed_datetime, reverse=True)

    def get_scripts(self, tree=None):
        """Explore the git repository tree in order to list all scripts that are tracked by git

        :param tree: Repository tree
        :type tree: Tree

        :return: List of scripts paths
        """
        tree = tree or self.tree()

        scripts = []
        # Get scripts at the tree level
        for blob in tree.blobs:
            scripts.append(blob)

        # Get scripts from sub trees
        for sub_tree in tree.trees:
            scripts += self.get_scripts(sub_tree)

        return scripts

    def get_commits(self, from_rev=None):
        """A list of commits from a given revision

        :param from_tag: Optional revision from which to retrieve commits (usually a tag name or a commit hash)
        :type from_tag: str

        Usually you need to retrieve all commits from a given tag or a given commit

            from create_python_project.git import RepositoryManager
            repo = RepositoryManager(path)
            repo.get_commits('v0.1.1')
            repo.get_commits('715dfb6a60eb69aea9b7d32411e445efaa6389b1')
        """
        rev = '...{from_rev}'.format(from_rev=from_rev) if from_rev else None
        return list(self.iter_commits(rev))

    def push(self, push_tags=True):
        """Push project

        :param push_tags: Optional boolean indicating whether or not to push tags
        :type push_tags: bool
        """
        extra_args = ['--follow-tags'] if push_tags else []
        self.git.push(*extra_args)
