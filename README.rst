drone-marathon
==============

Deploys to a Marathon cluster

This module takes MASSIVE inspiration from https://github.com/drone-plugins/drone-marathon,
but this one is:

- Written in Python (since that's what our team knows better than Go)
- Available for Drone.io v0.4 (the official one is still in-development for v0.5)

Overview
--------

Run the plugin directly after installing requirements:

.. code-block:: bash

    python plugin/main.py <<EOF
    {
        "repo" : {
            "owner": "foo",
            "name": "bar",
            "full_name": "foo/bar"
        },
        "system": {
            "link_url": "http://drone.mycompany.com"
        },
        "build" : {
            "number": 22,
            "status": "success",
            "started_at": 1421029603,
            "finished_at": 1421029813,
            "commit": "9f2849d5",
            "branch": "master",
            "message": "Update the Readme",
            "author": "johnsmith",
            "author_email": "john.smith@gmail.com"
        },
        "vargs": {
            "server": "http://marathon.example.com:8080",
            "id": "myapp",
            "instances": 1,
            "cpus": 0.25,
            "mem": 64,
            "docker_image": mycompany/someapp,
            ...
        }
    }
    EOF

Docker
------

Alternatively, run the plugin directly from a built Docker image:

.. code-block:: bash

    docker run -i expansioncap/drone-marathon <<EOF
    {
        "repo" : {
            "owner": "foo",
            "name": "bar",
            "full_name": "foo/bar"
        },
        "system": {
            "link_url": "http://drone.mycompany.com"
        },
        "build" : {
            "number": 22,
            "status": "success",
            "started_at": 1421029603,
            "finished_at": 1421029813,
            "commit": "9f2849d5",
            "branch": "master",
            "message": "Update the Readme",
            "author": "johnsmith",
            "author_email": "john.smith@gmail.com"
        },
        "vargs": {
            "room_auth_token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            "room_id_or_name": 1234567,
            "message_notify": true
        }
    }
    EOF


License
-------

drone-marathon is licensed under the Apache License. A copy is included
in this repository.
