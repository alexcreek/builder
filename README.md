# Builder

Builder's purpose in life is to run scripts in response to webhooks from Github repos.  It's running in a k8s cluster building and publishing docker images to a local registry.

Builder takes it's instructions from a config file in your repo named `Builderfile`.  There's only one setting you need to define; `build`:

```
build: ./build-script
```

Your project's webhooks needs to be configured to send push events to the address where Builders running.  You should REALLY consider configuring the shared secret too.

That's it.  Super simple and half the time it almost works.
