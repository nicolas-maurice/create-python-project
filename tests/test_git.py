"""
    tests.test_git
    ~~~~~~~~~~~~~~

    Test Git repository functions

    :copyright: Copyright 2017 by Nicolas Maurice, see AUTHORS.rst for more details.
    :license: BSD, see :ref:`license` for more details.
"""


def test_tags(repo):
    assert len(repo.get_tags()) == 11


def test_get_commits(repo):
    assert len(repo.get_commits()) == 22
    assert len(repo.get_commits('v1.0.1')) == 9
    assert len(repo.get_commits('v0.0.2')) == 17


def test_push(repo):
    repo.push()
    assert repo.git.push.call_args == (('--follow-tags',),)
    repo.push(push_tags=False)
    assert repo.git.push.call_args == ()


def test_get_scripts(repo):
    scripts = repo.get_scripts()
    assert len(scripts) > 0
