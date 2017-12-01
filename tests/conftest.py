"""
    tests.conftest
    ~~~~~~~~~~~~~~

    :copyright: (c) 2015 by the Flask Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""
import os

import pytest
from git import Git

from create_python_project.git import RepositoryManager

DIR_NAME = os.path.dirname(__file__)
TEST_REPO = os.path.join(DIR_NAME, 'repo')


@pytest.fixture(scope='function')
def repo(monkeypatch, mocker):
    _repo = RepositoryManager(path=TEST_REPO)

    # Monkey patch and Mock _repo.git.push function so we do not need to effectively push to remotes during tests.
    # We cannot monkey patch the git.push function due to GitPython implementation of Git class with __slots__
    # (c.f. https://github.com/gitpython-developers/GitPython/blob/master/git/cmd.py)
    # So we need to monkey path the full _repo.git attribute
    class MockGit(Git):
        def push(self, *args, **kwargs):
            pass

    monkeypatch.setattr(_repo, 'git', value=MockGit(_repo.working_dir))
    mocker.patch.object(_repo.git, 'push')

    # Keep track of initial repository state (remotes, tags, commits)
    # so we can roll back all modifications at the end of tests
    initial_remotes = _repo.remotes
    initial_tags = _repo.tags
    initial_head_commit = _repo.head.commit

    yield _repo

    # Roll back manipulations (new remotes, tags, commits) performed during tests
    _repo.head.reset(initial_head_commit, working_tree=True)
    _repo.delete_tag(*[tag for tag in _repo.tags if tag not in initial_tags])
    for remote in _repo.remotes:
        if remote not in initial_remotes:
            _repo.delete_remote(remote)
