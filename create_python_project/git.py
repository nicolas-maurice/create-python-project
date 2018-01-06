"""
    create_python_project.git
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Implements functions to enable automatic manipulations of a project as a git repository

    :copyright: Copyright 2017 by Nicolas Maurice, see AUTHORS.rst for more details.
    :license: BSD, see :ref:`license` for more details.
"""

from functools import partial

from git import Repo

from .utils import is_matching


class RepositoryManager(Repo):
    """Implements functions to automatically manipulate the project has a git repository"""

    def apply_func(self, func, *args, is_filtered=None, tree=None, **kwargs):
        tree = tree or self.tree()

        if isinstance(is_filtered, str):
            is_filtered = [is_filtered]

        if isinstance(is_filtered, list):
            is_filtered = partial(is_matching, is_filtered)

        for blob in tree.blobs:
            if not callable(is_filtered) or is_filtered(blob):
                func(blob,
                     *[arg(blob) if callable(arg) else arg for arg in args],
                     **{kw: arg(blob) if callable(arg) else arg for kw, arg in kwargs.items()})

        for sub_tree in tree.trees:
            self.apply_func(func, is_filtered=is_filtered, tree=sub_tree, *args, **kwargs)

    def commit(self, *args, **kwargs):
        if self.is_dirty():
            self.git.commit(*args, **kwargs)

    def get_tags(self):
        """Return ordered list of tags of the project ordered from most recent to oldest"""
        return sorted(self.tags, key=lambda tag: tag.commit.committed_datetime, reverse=True)

    def get_blobs(self, is_filtered=None):
        """Explore the git repository tree in order to list all scripts that are tracked by git

        :param tree: Repository tree
        :type tree: Tree

        :return: List of scripts paths
        """

        blobs = []
        self.apply_func(lambda blob: blobs.append(blob), is_filtered=is_filtered)

        return blobs

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

    def mv(self, old_path, new_path):
        """Rename"""
        self.git.mv(old_path, new_path)
        self.git.commit(old_path, new_path, '-m', 'rename folder {0} to {1}'.format(old_path, new_path))
