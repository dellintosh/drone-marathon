This plugin can be used to deploy applications to a [Marathon](https://mesosphere.github.io/marathon/) server.

# Marathon File

In addition to the `.drone.yml` file you will need to create a `marathon.json` file that contains the Marathon configuration.  Please see [here](https://github.com/mesosphere/marathon/tree/master/examples) for examples. Values can also be substituted from the `.drone.yml` using the following format:

In the `.drone.yml` file (can use any values - either hard-coded or from the environment):

```yaml
publish:
  marathon:
    image: e20co/drone-marathon:0.5
    values:
      BRANCH_NAME: $$BRANCH  # Where $$BRANCH = "mybranch"
```

In the `marathon.json` file (please note the `<<` and `>>` around the `BRANCH_NAME` key):

```js
{
  "id": "/my-application/branch-<<BRANCH_NAME>>",
  ...
}
```

Will result in:

```js
{
  "id": "/my-application/branch-mybranch",
  ...
}
```

Example Configuration

```yaml
publish:
  marathon:
    image: e20co/drone-marathon:0.5
    server: http://marathon.mesos:8080
```

Example Configuration using `trigger_restart` and `values` to override values within the `marathon.json` file.

```yaml
publish:
  marathon:
    image: e20co/drone-marathon:0.5
    server: http://marathon.mesos:8080
    trigger_restart: true
    values:
      BRANCH_NAME: $$BRANCH
      TAG_NAME: $$TAG
      SOME_OTHER_VALUE: foobar
```

```js
{
  "id": "/demo-application/<<BRANCH_NAME>>/<<SOME_OTHER_VALUE>>",
  "instances": 1,
  "cpus": 0.2,
  "mem": 256,
  "container": {
    "type": "docker",
    "docker": {
      "image": "nginx:<<TAG_NAME>>",
      "network": "BRIDGE",
      "portMappings": [
        {
          "containerPort": 80,
          "hostPort": 0,
          "protocol": "tcp"
        }
      ]
    }
  },
  "healthChecks": [
    {
      "gracePeriodSeconds": 120,
      "intervalSeconds": 30,
      "maxConsecutiveFailures": 3,
      "path": "/",
      "portIndex": 0,
      "protocol": "HTTP",
      "timeoutSeconds": 5
    }
  ]
}
```

# Parameter Reference

`server`

The Marathon server URL. defaults to `http://marathon.mesos:8080`

`marathonfile`

The Marathon configuration file. defaults to `marathon.json`.

`trigger_restart`

Force a restart of the application. defaults to `false`.

`values`

Map of values to replace in the `marathonfile`, above.  Optional.
