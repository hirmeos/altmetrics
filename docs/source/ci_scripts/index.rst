CI Scripts
==========

Our CI scripts are executed by the Gitlab CI machine, based on a yaml file. The
process is split into stages, each of which can be configured to run under
certain conditions - for example, whenever code is pushed to Gitlab the
'version', 'test' and 'flake' stages will run; however, the 'docker' and 'helm'
stages of the CI will only run when a new tag is pushed to Gitlab (representing
a new release).


Stages of the CI scripts
------------------------
The stages of our CI scripts vary, depending on the application, but generally
are as follows:

version
~~~~~~~
  - Pull the release version of the software that has been pushed to Gitlab
    (based on tags).
  - Instantiate any variables used in subsequent steps (e.g. postgres machine
    for testing).

test
~~~~
  - Using tox, set the virtual environment(s) needed for testing.
  - Execute all test scripts.

k8s-scripts
~~~~~~~~~~~
  - Clone our kubernetes folder from Gitlab.
  - contains our code for creating helm charts.

docker
~~~~~~
  - Build the docker image of of the software to be deployed.
  - Push the image to our container repository.

helm
~~~~
  - Build a helm chart for deploying the latest application.
  - Push the helm chart to an Amazon S3 bucket.
  - Update the kubernetes repository with the latest helm chart version.

flake
~~~~~
  - Run flake8 to to highlight any deviations from our style guidelines.


The only stage that is allowed to fail is the flake8 stage, since it is not
crucial for the application to run.
