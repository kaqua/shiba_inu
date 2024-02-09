## このリポジトリについて
リポジトリ名と内容は全く関係がありません

CloudFormationテンプレートからパラメータファイルを作成します。

## 作業環境
- python  
3.10
- ライブラリ  
pyyaml  
awscli

## 使い方
```
python create_cfn_parameter_file.py template/sample.yml 
パラメータファイル: sample_parameter.json
```
作成されるパラメータファイル名は、{パラメータ}_parameter.json になります。