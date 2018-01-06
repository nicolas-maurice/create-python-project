"""
    create_python_project.cli.info
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Implement command line interface for Create-Python-Project

    :copyright: Copyright 2017 by Nicolas Maurice, see AUTHORS.rst for more details.
    :license: BSD, see :ref:`license` for more details.
"""

import click

from .project import ProjectManager


@click.command()
@click.option('--boilerplate', '-b',
              type=str,
              help='Git URL of the repository to clone a project from')
@click.option('--git-url', '-u', 'url',
              type=str,
              help='Git URL of your project')
@click.option('--upstream-name', 'upstream_name',
              type=str,
              help='Name of the upstream to rename the origin remote to',
              default='boilerplate')
@click.option('--author-name', '-a',
              type=str,
              help='Author of the project')
@click.option('--author-email', '-e',
              type=str,
              help='Author\'s email of the project')
@click.argument('project_name',
                type=str,
                required=True)
def create_python_project(boilerplate, url, upstream_name,
                          author_name, author_email,
                          project_name):
    """Creates a new project"""

    click.echo('Creating new project...')

    # Clone boilerplate
    click.echo('Cloning project from {url}'.format(url=boilerplate))
    manager = ProjectManager.clone_from(url=boilerplate, to_path=project_name)

    # Set project origins
    click.echo('Set project origin remote to {url}'.format(url=url))
    manager.set_project_origin(upstream_name, url)
    click.echo('Remote {remote} has been set'.format(remote=boilerplate))

    # Rename project
    new_name = manager.set_project_name(project_name)
    click.echo('Project name has been set to {name}'.format(name=new_name))

    # Rename author
    if author_name is not None:  # pragma: no branch
        manager.set_project_author(author_name=author_name)
        click.echo('Project author\'s name has been set to {name}'.format(name=author_name))

    if author_email is not None:  # pragma: no branch
        manager.set_project_author(author_email=author_email)
        click.echo('Project author\'s email has been set to {email}'.format(email=author_email))

    click.echo('Project successfully created!! Happy coding! :-)')