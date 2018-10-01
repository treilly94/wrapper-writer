import re


class ScalaParse:

    def __init__(self, filename):
        self.filename = filename

    def read_file(self):
        with open(self.filename) as myfile:
            data = myfile.read()
        return data

    def find_method_regex(self):
        retrieve_data = self.read_file()
        ptrn = re.compile("def (\w+)\((.*)\): (\w+)", re.MULTILINE)
        ptrn2 = ptrn.finditer(retrieve_data)
        # print(type(ptrn2))
        # for k in ptrn2:
        #     print(k.group())
        return ptrn2

    breakDown= []
    def multi_process(self):
        allfound = self.find_method_regex()
        for i in allfound:
            ig = i.group()
            extract_return_type = self.string_manipulation(ig)
            print(extract_return_type)
            extract_name = self.extract_item(ig)
            print(extract_name)
            # breadDown.append[extract_name, extract_return_type]

    def string_manipulation(self, raw_res):
        first, *middle, last = raw_res.split()
        returnType = last
        return returnType

    def extract_item(self, raw_res):
        funcName = r"def (\w+)"
        funcNameFind = re.search(funcName, raw_res)
        funNameRaw = funcNameFind.group()
        cleanFuncName = funNameRaw.replace("def ", "")
        return cleanFuncName




if __name__ == '__main__':
    x = ScalaParse("scalacode.scala")
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
