# pasa
意味役割付与システムASAのPython移植版

オリジナル: https://github.com/Takeuchi-Lab-LM/scala_asa3


## 実行に必要な環境

- python 3.6+
- mecab
- cabocha
- cabochaのpythonバインディング: https://github.com/taku910/cabocha/tree/master/python/
  - インストール方法  
    <pre>
    pip install git+https://github.com/taku910/cabocha.git#subdirectory=python
    </pre>  
    または  
    <pre>
    curl -OL https://github.com/taku910/cabocha/archive/master.zip
    unzip master.zip  
    cd cabocha-master  
    pip install python/  
    </pre>
  
