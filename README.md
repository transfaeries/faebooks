# faebot
A general use ML bot for twitter,discord, signal, etc.

Deployment Workflow:

from repository home
```bash
docker build -t codefaeries/faebooks --file faebooks/Dockerfile .
```

from faebooks
```bash
fly deploy --image codefaeries/faebooks:latest --local-only --strategy immediate
```
