import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

app_user = 'app'
python_version = '2.7.15'
deployment_version = '20190308132800'


def test_hosts_file(host):
    f = host.file('/etc/hosts')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


def test_app_home(host):
    home = host.file('/home/%s' % app_user)

    assert home.exists
    assert home.is_directory
    assert home.user == app_user
    assert home.group == app_user
    assert home.mode == 0o755


def test_app_python(host):
    python = host.file(
        '/home/%s/.pyenv/versions/%s/bin/python' % (app_user, python_version))

    assert python.exists
    assert python.is_file
    assert python.user == app_user
    assert python.group == app_user
    assert python.mode == 0o755


def test_app_current_link(host):
    expected_deployment = '/home/%s/deployments/%s' \
        % (app_user, deployment_version)
    current = host.file('/home/%s/current' % app_user)

    assert current.exists
    assert current.is_symlink
    assert current.user == app_user
    assert current.group == app_user
    assert current.linked_to == expected_deployment


def test_app_src_dir(host):
    src = host.file(
        '/home/%s/deployments/%s/src' % (app_user, deployment_version))

    assert src.exists
    assert src.is_directory
    assert src.user == app_user
    assert src.group == app_user
    assert src.mode == 0o755


def test_app_src_code(host):
    app_source = host.file(
        '/home/%s/deployments/%s/src/.git' % (app_user, deployment_version))

    assert app_source.exists
    assert app_source.is_directory
    assert app_source.user == app_user
    assert app_source.group == app_user
    assert app_source.mode == 0o755


def test_app_secrets_dir(host):
    secrets = host.file(
        '/home/%s/deployments/%s/secrets' % (app_user, deployment_version))

    assert secrets.exists
    assert secrets.is_directory
    assert secrets.user == app_user
    assert secrets.group == app_user
    assert secrets.mode == 0o750


def test_app_virtualenv_dir(host):
    virtualenv = host.file(
        '/home/%s/deployments/%s/virtualenv' % (app_user, deployment_version))

    assert virtualenv.exists
    assert virtualenv.is_directory
    assert virtualenv.user == app_user
    assert virtualenv.group == app_user
    assert virtualenv.mode == 0o755


def test_app_virtualenv_python(host):
    python = host.file('/home/%s/deployments/%s/virtualenv/bin/python'
                       % (app_user, deployment_version))

    assert python.exists
    assert python.user == app_user
    assert python.group == app_user
    assert python.mode == 0o755


def test_app_os_packages(host):
    libgeos = host.package('libgeos-dev')

    assert libgeos.is_installed


def test_app_requirements(host):
    pip_packages = host.pip_package.get_packages(
        pip_path='/home/%s/deployments/%s/virtualenv/bin/pip'
        % (app_user, deployment_version))

    assert 'OWSLib' in pip_packages
