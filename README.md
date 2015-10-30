# Exhacktion

Exhacktion is just what you need. It allows you to use libraries as if they
used granular exception classes, even when they don't. That is, as long as they
do export the granularity in a way, be it through `e.errno` or `e.message`.

## Example: Python 2 and EnvironmentError

Consider the following:

```
try:
    os.chown("README.md", 100, 100)
except EnvironmentError as e:
    if e.errno == errno.ENOENT:
        pass
    else:
        raise
```

Would it not just be way nicer to say

```
try:
    os.chown("README.md", 100, 100)
except FileNotFoundError:
    pass
```

Yes it would! And Exhaction is what'll make that happen for you. Of course,
Python 3 already has that built-in, just for you. But it makes a nice use case.
