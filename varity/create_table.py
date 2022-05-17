import glob
import re

opt_levels = ["O0","O1","O2","O3"]
extra_options = ["","_fastmath"]
fp_instr = ["FADD",
"FADD32I",
"FCHK",
"FFMA32I",
"FFMA",
"FMNMX",
"FMUL",
"FMUL32I",
"FSEL",
"FSET",
"FSETP",
"FSWZADD",
"MUFU",
"DADD",
"DMNMX",
"DFMA",
"DMMA",
"DMUL",
"DSET",
"DSETP"]
def process_single_file(filename, instr_prefix,instr_complete):
    with open(filename) as f:
        for line in f.readlines():
            if("/*" in line and ";" in line):
                #print(line)
                instr = (re.search("\w(.*)", (re.search("\*/(.*);",line).group()))).group()
                #print(instr)
                prefix = instr.split(" ")[0]
                if prefix not in instr_prefix:
                    instr_prefix.add(prefix)
                    instr_complete.append(instr)
                    

   # print(table)
                #print(prefix)
def instruction_list_by_opt():
    for opt in opt_levels:
        for ext in extra_options:
            table = set()
            tail = opt+ext+".sass"
            name = "./**/*"+tail
            output_name = opt+ext+"_instructions.txt"
            files = glob.glob(name, recursive=True)
            for f in files:
                process_single_file(f,table,[])
            #print(output_name+"is", table)
            with open(output_name, "wt") as f:
                f.write("\n".join(list(table)))

def complete_instruction_list():
    name = "./**/*.sass"
    instr_prefix = set()
    instr_complete = []
    for f in glob.iglob(name,recursive=True):
        # print(f)
        process_single_file(f,instr_prefix, instr_complete)
    print(instr_prefix)
    with open("complete_instr_list.txt", "wt") as f:
        f.write("\n".join(instr_complete))

def type_of_operands(operand):
    if operand.startswith("!") or operand.startswith("|") or operand.startswith("-") or operand.startswith("+"):
        operand_n = operand[1:]
    else:
        operand_n = operand
    if operand_n.startswith("R"):
        return "RX"
    elif operand_n.startswith("UR"):
        return "URX"
    elif operand_n.startswith("SR"):
        return "SRX"
    elif operand_n.startswith("P"):
        return "PX"
    elif operand_n.startswith("c["):
        return "C[X][Y]"
    elif operand_n.startswith("["):
        return "MEM"
    elif re.search("^\d",operand_n) is not None:
        return "LIT"
    else: 
        print(operand,operand_n)
        return operand

def init_dict():
    d = {}
    for i in fp_instr:
        d[i] = []
    return d

def process_single_file_fp(filename,instr_pattern_dict):
    with open(filename) as f:
        for line in f.readlines():
            if("/*" in line and ";" in line):
                #print(line)
                instr = (re.search("\w(.*)", (re.search("\*/(.*);",line).group()))).group()
                #print(instr)
                inst_list = instr.split(" ")
                prefix = inst_list[0].split(".")[0]
                il = instr_pattern_dict.get(prefix)
                if il is not None:
                    inst_pattern_list = []
                    inst_pattern_list.append(inst_list[0])

                    for operand in inst_list[1:-1]:
                        inst_pattern_list.append(type_of_operands(operand))
                    inst_p = " ".join(inst_pattern_list)
                    if inst_p not in il:
                        il.append(inst_p)
                        instr_pattern_dict[prefix] = il


def fp_instruction_pattern():
    name = "./**/*.sass"
    instr_pattern_dict = init_dict()
    for f in glob.iglob(name,recursive=True):
        # print(f)
        process_single_file_fp(f, instr_pattern_dict)
    with open("inst_pattern.txt", "wt") as f:
        for k,v in instr_pattern_dict.items():
            f.write(k+"\n")
            if(v == []):
                f.write("None\n")
            else:
                for inst in v:
                    f.write(inst)
                    f.write("\n")
            f.write("\n")


if __name__ == "__main__":
    # instruction_list_by_opt()
    # complete_instruction_list()
    #table = set()
    #process_single_file("/home/xinyi/learn_sass/Varity/varity/dknuth_817421/_tests_single_/_group_1/_test_413.cu-nvcc-O1.sass",table,[])
    #print(table) 
    fp_instruction_pattern()
#print("\n")
