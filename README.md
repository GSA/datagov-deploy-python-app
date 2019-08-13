[![CircleCI](https://circleci.com/gh/GSA/datagov-deploy-python-app.svg?style=svg)](https://circleci.com/gh/GSA/datagov-deploy-python-app)

# datagov-deploy-python-app

Deploys a Python based application in [12 factor](https://12factor.net/)
fashion.

- Creates a system user to own the application.
- Each deployment is isolated in its own directory with its own virtualenv.
- Makes secrets available in `$APP_DEPLOYMENT_DIR/secrets/env`.
- Application configuration and installation is done first, before linking
  (making the deployment active).
- Old deployments are removed.
- (Optionally) installs a supervisor configuration.
- (Optionally) installs a crontab.

This role is influenced by [Ansistrano](https://github.com/ansistrano/deploy).


## Usage

### Dependencies

Include these roles in your requirements.yml.

- [avanov.pyenv](https://github.com/avanov/ansible-galaxy-pyenv)

Use the role in your playbook:

```yaml
---
- name: install a python app
  roles:
    - role: gsa.datagov-deploy-python-app
      vars:
        python_app_user: myapp
```


### Variables


#### `python_app_user` string required

The OS user to create and install the app under. This is also used as the
application name.

#### `python_app_git_repo` string required

The git URL to your app repository.


#### `python_app_version` string (default: master)

The tag, branch, or commit to clone your application from.


#### `python_app_deploy_version` string

The string to use for the deployment version. This is usually a timestamp so
each deployment is uniq. It's important that deploy versions sort
chronologically so that cleanup removes the oldest deploys by sorting by the
deployment version.


#### `python_app_home` string (default: /home/{{ python_app_user }})

Directory to create for the Python app user's home directory. This is where
application deployments will be installed.


#### `python_app_python_version` string  (default: "3.6.8")

The version of Python to install.


#### `python_app_requirements_txt` string (default: requirements.txt)

The relative path to your requirements.txt from your application source.


#### `python_app_deployments_to_retain` number (default: 1)

The number of previous deployments to retain. Set to 0 to retain all old
deployments.


#### `python_app_os_packages` list (default: [])

List of OS packages that are needed by your application.


#### `python_app_supervisor_conf` string

Path to your supervisor configuration. This should probably be prefixed with
your playbook directory, e.g. `{{ playbook_dir }}/files/supervisor.conf`.


#### `python_app_supervisor_programs` list (default: [])

List of supervisor programs to restart after a deployment.


## Development

### Requirements

- [Docker](https://www.docker.com/get-started)
- [Pipenv](https://pipenv.readthedocs.io/en/latest/)


### Setup

Pipenv creates a virtualenv for you and installs the python dependencies.

    $ pipenv install --dev

Then you can run commands with pipenv.

    $ pipenv run molecule converge

Or, you can activate the virtualenv in your shell so you don't have to run pipenv
all the time.

    $ pipenv shell


### Run the tests

Run the tests with [molecule](https://molecule.readthedocs.io/en/latest/).

    $ pipenv run molecule test --all

If you're new to molecule, see our
[wiki](https://github.com/GSA/datagov-deploy/wiki/Developing-Ansible-roles-with-Molecule)
for a quick primer.


## Contributing

See [CONTRIBUTING](CONTRIBUTING.md) for additional information.


## Public domain

This project is in the worldwide [public domain](LICENSE.md). As stated in [CONTRIBUTING](CONTRIBUTING.md):

> This project is in the public domain within the United States, and copyright and related rights in the work worldwide are waived through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).
>
> All contributions to this project will be released under the CC0 dedication. By submitting a pull request, you are agreeing to comply with this waiver of copyright interest.
