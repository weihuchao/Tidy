## 初始化环境

```bash
pyenv virtualenv tidy
pyenv activate tidy

pip install ipython
pip install mutagen
pip install ebooklib beautifulsoup4

pip install opencc
```

```bash
pip freeze > requirements.txt
pip install -r requirements.txt
```