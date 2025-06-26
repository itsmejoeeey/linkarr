## Developing

#### Run code formatting

From inside your virtual env:

```
pip install -r requirements.dev.txt
black src
```

### Testing

From inside your virtual env:

```
cd src
python -m unittest discover ../test
```