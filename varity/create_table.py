import glob
import re

opt_levels = ["O0","O1","O2","O3"]
extra_options = ["","_fastmath"]
def process_single_file(filename, table):
    with open(filename) as f:
        for line in f.readlines():
            if("/*" in line and ";" in line):
                #print(line)
                instr = (re.search("\w(.*)", (re.search("\*/(.*);",line).group()))).group()
                #print(instr)
                prefix = instr.split(" ")[0]
                table.add(prefix)
   # print(table)
                #print(prefix)
def get_sass():
    for opt in opt_levels:
        for ext in extra_options:
            table = set()
            tail = opt+ext+".sass"
            name = "./**/*"+tail
            output_name = opt+ext+"_instructions.txt"
            files = glob.glob(name, recursive=True)
            for f in files:
                process_single_file(f,table)
            #print(output_name+"is", table)
            with open(output_name, "wt") as f:
                f.write("\n".join(list(table)))
if __name__ == "__main__":
    get_sass()
    # process_single_file("./dknuth_733807/_tests_single_/_group_1/_test_7.cu-nvcc-O2_fastmath.sass",set()) 
print("\n")
