# faebot
A conversational ML bot for mastodon, twitter, discord, signal, etc.

Deployment Workflow:

from repository home
```bash
docker build -t codefaeries/faebooks --file faebooks/Dockerfile .
```

from faebooks
```bash
fly deploy --image codefaeries/faebooks:latest --local-only --strategy immediate
```

Version log:

If we say the heroku version is v0.1.0

and that the fly version has subversions based on fly releases

this version of faebot is v0.2.15
