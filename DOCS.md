This plugin can be used to deploy applications to [Marathon](https://mesosphere.github.io/marathon/).

The following parameters are used to configuration the plugin's behavior:

* **url** - The URL to POST the webhook to.

The following is a sample drone-marathon configuration in your 
.drone.yml file:

```yaml
notify:
  drone-marathon:
    image: expansioncap/drone-marathon
    url: http://mockbin.org/
```
