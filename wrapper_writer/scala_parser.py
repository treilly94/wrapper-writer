import re
import yaml
import os


class ScalaParse:

    def __init__(self, filename, config_name, append_config=False):
        self.filename = filename
        self.config_filename = config_name
        self.if_config_exists = append_config

    def read_file(self):
        try:
            with open(self.filename) as logic_file:
                data = logic_file.read()
            return data
        except IOError as e:
            print("I/O error({0}): {1}".format(e.errno, e.strerror))

    def prepare_files(self):
        print("Checking if file exists ...")
        if os.path.exists(self.config_filename):
            os.remove(self.config_filename)
        else:
            print("The config file does not exists")

    def find_method_regex(self):
        retrieve_data = self.read_file()
        if not self.if_config_exists:
            self.prepare_files()
        ptrn = re.compile("def (\w+)\((.*)\): (\w+)", re.MULTILINE)
        try:
            ptrn2 = ptrn.finditer(retrieve_data)
        except:
            print("Nothing In There")
        print(ptrn2)
        return ptrn2

    def multi_process(self):
        all_found = self.find_method_regex()
        matches = tuple(all_found)
        if not matches:
            raise Exception("No Methods Found")
        for i in matches:
            ig = i.group()
            # print("Task")
            # print(ig)
            return_type = self.extract_return_type(ig)
            method_name = self.extract_method_name(ig)
            params = self.extract_params(ig)
            data ={"methods": {method_name: {"params": params, "return_type": return_type}}}
            print(self.if_config_exists)
            with open(self.config_filename, 'a') as yaml_file:
                yaml.dump(data, yaml_file, default_flow_style=False)

    @staticmethod
    def extract_return_type(raw_res):
        first, *middle, last = raw_res.split()
        return_type = last
        return return_type

    @staticmethod
    def extract_method_name(raw_res):
        func_name = r"def (\w+)"
        func_name_find = re.search(func_name, raw_res)
        fun_name_raw = func_name_find.group()
        clean_func_name = fun_name_raw.replace("def ", "")
        return clean_func_name

    @staticmethod
    def extract_params(raw_res):
        retrieve_params = r"\((.*)\)"
        retrieve_params_find = re.search(retrieve_params, raw_res)
        retrieve_params_raw = retrieve_params_find.group()
        retrieve_params_clean = retrieve_params_raw[1:-1]
        dict_by_comma = dict(item.split(":") for item in retrieve_params_clean.split(","))
        for k, v in dict_by_comma.items():
            dict_by_comma[k] = v.lstrip()
            new_dict = {k.lstrip(): v for k, v in dict_by_comma.items()}
        return new_dict


if __name__ == '__main__':
    x = ScalaParse("scalacode.scala", "config_eres.yml")
    x.multi_process()


# methodLogic = """object FilterOnList {
#
#   def filterOnList(df: DataFrame, targetCol: String, values: List[Int]): DataFrame = {
#     filterFunct(df, targetCol, values)
#   }
#   def filterFunct(df: DataFrame, targetCol: String, values: List[Int]): DataFrame = {
#     df.where(!col(targetCol).isin(values: _*))
#   }
# }
# """
# methodLogic2 = "def filterOnList(df: DataFrame, targetCol:String, values: List[Int]): DataFrame = {"
#
# pattern = r"def (\w+)\((.*)\): (\w+)"
# searched = re.search(pattern, methodLogic2)
#
# # all_searched = re.findall(pattern, methodLogic2, re.MULTILINE)
# #
# # print(all_searched)
# ptrn = re.compile("def (\w+)\((.*)\): (\w+)", re.MULTILINE)
# ptrn2 = ptrn.finditer(methodLogic)
# # print(ptrn2)
#
# for k in ptrn2:
#     print(k.group())
#
# print(searched.group())
#
# raw_res = searched.group()
# first, *middle, last = raw_res.split()
# returnType = last
# print(returnType)
#
# funcName = r"def (\w+)"
# funcNameFind = re.search(funcName, raw_res)
# funNameRaw = funcNameFind.group()
# # print(funNameRaw)
# cleanFuncName = funNameRaw.replace("def ", "")
# print(cleanFuncName)
#
#
# retrieveParams = r"\((.*)\)"
# retrieveParamsFind = re.search(retrieveParams, raw_res)
# retrieveParamsRaw = retrieveParamsFind.group()
# retrieveParamsClean = retrieveParamsRaw[1:-1]
# sepByComma = [e.strip() for e in retrieveParamsClean.split(',')]
#
# dictByComma = dict(item.split(":") for item in retrieveParamsClean.split(","))
# # print(dictByComma)
#
# for k, v in dictByComma.items():
#     dictByComma[k] = v.lstrip()
#     new_dict = {k.lstrip(): v for k, v in dictByComma.items()}
# # print(dictByComma)
#
# # new_dict = {k.lstrip(): v for k, v in dictByComma.items()}
# print(new_dict)
#
# all_params = []
#
# for i in sepByComma:
#     sepBySemiColon = [p.strip() for p in i.split(':')]
#     all_params.append(sepBySemiColon)
#
#
