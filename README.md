# Pure-HTML
Make HTML pure by removing annoying tags and classes for better processing and reading

## Build and upload
    
```sh
python -m build
twine upload --repository testpypi dist/*
```

## Install

```sh
# pip install --index-url https://test.pypi.org/simple/ --no-deps pure-html
pip install --upgrade pure-html
```