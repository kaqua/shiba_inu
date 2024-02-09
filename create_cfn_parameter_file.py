import yaml
import sys
import os
import json

from awscli.customizations.cloudformation.yamlhelper import yaml_parse

# テンプレートの拡張子チェック
def check_template_extension(template_file):

    # 許可する拡張子
    extension_ok_list = ('.yml', '.yaml')

    # 許可する拡張子かどうか
    if template_file.endswith(extension_ok_list):
        check_result = "OK"
    else:
        check_result = "NG"

    return check_result

# パラメータをファイルに出力する
def create_parameter_list(yaml_dict, set_default):

    # パラメータ初期化
    parameter_list = []

    for key, value in yaml_dict['Parameters'].items():
        parameter = {}
        parameter["ParameterKey"] = key
        parameter["ParameterValue"] = \
            value.setdefault('Default', "") if set_default == True else ""
        parameter_list.append(parameter)

    return parameter_list

# テンプレートファイルを作成する
def create_parameter_file(template_file_name, parameter_list):

    output_pamater_file = f'{template_file_name}_parameter.json'

    # ファイル出力
    with open(output_pamater_file, mode="w") as file:
        json.dump(parameter_list, file, indent=4, ensure_ascii=False)

    print(f"パラメータファイル: {output_pamater_file}")
    return None

def main():

    args = sys.argv

    # 引数からテンプレートファイルを変数に格納
    template_file = os.path.abspath(args[1])

    # パラメータデフォルトフラグセット
    set_default = True if len(args) == 2 else False

    # テンプレートの拡張子チェック
    result = check_template_extension(template_file)
    if result == "NG":
        print("ファイルの拡張子を確認してください")
        sys.exit(1)

    try:
        with open(template_file, 'r') as file:
            # YAML文字列を解析し、順序付き辞書型のオブジェクトを返却する
            yaml_dict = yaml_parse(file.read())
    except yaml.parser.ParserError as e:
        print(e)
        print('YAML形式として解析できない文字列です。（例：キーや:が無い）')
    except yaml.scanner.ScannerError as e:
        print(e)
        print('YAML形式として読み取れない値が含まれています。（例：CFnの組み込み関数の構文誤り）')

    # パラメータリストを作成する
    parameter_list = create_parameter_list(yaml_dict, set_default)

    # テンプレート名を取得する
    template_file_name = os.path.splitext(os.path.basename(template_file))[0]

    # テンプレートファイルを作成する
    create_parameter_file(template_file_name, parameter_list)

if __name__ == '__main__':
    main()