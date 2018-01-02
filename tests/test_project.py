"""
    tests.test_project
    ~~~~~~~~~~~~~~~~~~

    Test Project manipulation functions

    :copyright: Copyright 2017 by Nicolas Maurice, see AUTHORS.rst for more details.
    :license: BSD, see :ref:`license` for more details.
"""

import os

def test_rename_project(manager, ):
    assert manager.setup_info.version.value == '0.0.0'
    assert manager.setup_info.name.value == 'Boilerplate-Python'

    manager.set_project_name('New-Package-Name')

    # Test package directory has been correctly renamed
    assert os.path.isdir('new_package_name')
    info = manager.get_info(is_filtered='new_package_name/__init__.py')[0]
    assert info.docstring.title.text == 'new_package_name'

    # Test README.rst has been modified
    assert manager.get_info(is_filtered='README.rst')[0].title.text == 'New-Package-Name'

    # Test .coveragerc has been correctly modified
    publication =  manager.get_scripts(is_filtered='.coveragerc')[0].publish()
    assert publication.split('\n')[2] == 'source = new_package_name'
    assert publication.split('\n')[10] == 'title = New-Package-Name coverage Report'

    # Test setup.py has been correctly modified
    assert manager.get_info(is_filtered='setup.py')[0].docstring.title.text == 'New-Package-Name'
    assert manager.setup_info.name.value == 'New-Package-Name'

    # Test modifications have been correctly committed
    assert not manager.is_dirty()