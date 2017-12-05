"""
    tests.conftest
    ~~~~~~~~~~~~~~

    :copyright: (c) 2017 by Nicolas Maurice, see AUTHORS.rst for more details.
    :license: BSD, see :ref:`license` for more details.
"""

import logging
import os
import shutil

import pytest
import semver
from git import Git

from create_python_project import RepositoryManager

DIR_NAME = os.path.dirname(__file__)
TEST_REPO = os.path.join(DIR_NAME, 'repo')


@pytest.fixture(scope='function')
def repo_path():
    # Set Directory to test repository to ensure consistency in tests
    initial_dir = os.getcwd()
    os.chdir(TEST_REPO)

    yield TEST_REPO

    os.chdir(initial_dir)


@pytest.fixture(scope='function')
def repo(monkeypatch, mocker, repo_path, caplog):
    with caplog.at_level(logging.ERROR):  # Set log level to avoid to overcharge logs with GitPython logs
        # Initialize repository for testing
        _repo = RepositoryManager.init(path=repo_path)

        # Monkey patch and Mock _repo.git.push function so we do not need to effectively push to remotes during tests.
        # We cannot monkey patch the git.push function due to GitPython implementation of Git class with __slots__
        # (c.f. https://github.com/gitpython-developers/GitPython/blob/master/git/cmd.py)
        # So we need to monkey path the full _repo.git attribute
        class MockGit(Git):
            def push(self, *args, **kwargs):
                pass

        monkeypatch.setattr(_repo, 'git', value=MockGit(_repo.working_dir))
        mocker.patch.object(_repo.git, 'push')

        # Add files, commits and tags to the repository
        version = '0.0.0'
        for i, file in enumerate(_repo.untracked_files):
            _repo.git.add(file)
            _repo.git.commit(file, '-m', 'add {file}'.format(file=file))
            if i % 2 == 0:
                _repo.create_tag('v{version}'.format(version=version),
                                 message='Release v{version}'.format(version=version))
                if i > 0 and i % 8 == 0:
                    version = semver.bump_major(version)
                elif i > 0 and i % 4 == 0:
                    version = semver.bump_minor(version)
                else:
                    version = semver.bump_patch(version)

    yield _repo

    shutil.rmtree(os.path.join(repo_path, '.git'))


@pytest.fixture(scope='function')
def script_content(repo_path):
    _script_content = 'test-script-content'

    yield _script_content
