import re


class ScalaParse:

    def __init__(self, filename):
        self.filename = filename

    def read_file(self):
        with open('scalacode.scala') as myfile:
            data = myfile.readable()
        print(data)


methodLogic = """object FilterOnList {

  def filterOnList(df: DataFrame, targetCol: String, values: List[Int]): DataFrame = {
    filterFunct(df, targetCol, values)
  }
  def filterFunct(df: DataFrame, targetCol: String, values: List[Int]): DataFrame = {
    df.where(!col(targetCol).isin(values: _*))
  }
}
"""
methodLogic2 = "def filterOnList(df: DataFrame, targetCol:String, values: List[Int]): DataFrame = {"

pattern = r"def (\w+)\((.*)\): (\w+)"
searched = re.search(pattern, methodLogic2)

# all_searched = re.findall(pattern, methodLogic2, re.MULTILINE)
#
# print(all_searched)
ptrn = re.compile("def (\w+)\((.*)\): (\w+)", re.MULTILINE)
ptrn2 = ptrn.finditer(methodLogic)
# print(ptrn2)

for k in ptrn2:
    print(k.group())

print(searched.group())

raw_res = searched.group()
first, *middle, last = raw_res.split()
returnType = last
print(returnType)

funcName = r"def (\w+)"
funcNameFind = re.search(funcName, raw_res)
funNameRaw = funcNameFind.group()
# print(funNameRaw)
cleanFuncName = funNameRaw.replace("def ", "")
print(cleanFuncName)


retrieveParams = r"\((.*)\)"
retrieveParamsFind = re.search(retrieveParams, raw_res)
retrieveParamsRaw = retrieveParamsFind.group()
retrieveParamsClean = retrieveParamsRaw[1:-1]
sepByComma = [e.strip() for e in retrieveParamsClean.split(',')]

dictByComma = dict(item.split(":") for item in retrieveParamsClean.split(","))
# print(dictByComma)

for k, v in dictByComma.items():
    dictByComma[k] = v.lstrip()
    new_dict = {k.lstrip(): v for k, v in dictByComma.items()}
# print(dictByComma)

# new_dict = {k.lstrip(): v for k, v in dictByComma.items()}
print(new_dict)

all_params = []

for i in sepByComma:
    sepBySemiColon = [p.strip() for p in i.split(':')]
    all_params.append(sepBySemiColon)


