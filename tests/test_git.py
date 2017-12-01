"""
    tests.test_git
    ~~~~~~~~~~~~~~

    Test Git repository functions

    :copyright: (c) 2015 by the Flask Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""


def test_tags(repo):
    assert [tag_ref.tag.tag for tag_ref in repo.get_tags()] == ['v0.2.0', 'v0.1.1', 'v0.1.0', 'v0.0.0']
    repo.create_tag('v0.3.0', message='Release v0.3.0')
    assert [tag_ref.tag.tag for tag_ref in repo.get_tags()] == ['v0.3.0', 'v0.2.0', 'v0.1.1', 'v0.1.0', 'v0.0.0']


def test_get_commits(repo):
    assert len(repo.get_commits()) == 54
    assert len(repo.get_commits('715dfb6a60eb69aea9b7d32411e445efaa6389b')) == 2
    assert len(repo.get_commits('v0.1.1')) == 20


def test_push(repo):
    repo.push()
    assert repo.git.push.call_args == (('--follow-tags',),)
    repo.push(push_tags=False)
    assert repo.git.push.call_args == ()


def test_get_scripts(repo):
    scripts = repo.get_scripts()
    assert len(scripts) > 0
