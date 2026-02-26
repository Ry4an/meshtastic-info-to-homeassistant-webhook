# Meshtastic Info to Home Assistant Webhook

This is a quick script to use the [meshtastic python API](https://python.meshtastic.org/), which powers the command line tool, to pull full node info and optionally send it to a home assistant webhook for use in sensors.  This is different than using MQTT to get mesh info into home assistant which also works and is [described on the Meshtastic](website).  This could easily be turned into an integration, but a script running from a cronjob works just fine for me.

## Setup
You don't need any requirements that aren't already included in the meshstatic python package, so you can just do:

`pip3 install 'meshtastic[cli]`

and you've got everything you need installed.  Then update the `MESHTASTIC_HOST` variable in the script and optionally the `HOME_ASSISTANT_HOST` too.

## Usage

To dump the info run:

`python3 meshtastic_info_to_webhook.py`

without any arguments.  That'll get you a single json doc with (most) everything, instead of the output of `meshtastic info` which is some json mixed in with text blocks.

If you want to send it to Home Assistant you'll need to create a template that defines a webhook and one or more sensors.  Something like this in your `configurations.yaml` will get you there:

```YAML
templates:
  - triggers:
      - trigger: webhook
        webhook_id: "YOUR_SECRET_WEBHOOK_ID_GOES_HERE"
    sensor:
      - name: "Meshtastic Firmware"
        state: "{{ trigger.json.metadata.firmwareVersion }}"
```

After testing and then reloading the config, you can invoke the command like:

`env WEBHOOK_ID="YOUR_SECRET_WEBHOOK_ID_GOES_HERE" python3 meshtastic_info_to_webhook.py`

Multiple sensors can be defined and all will be updated with a single webhook POST.
