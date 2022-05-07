import glob

instr_type =["FADD",
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
"HADD2",
"HADD2_32I",
"HFMA2",
"HFMA2_32I",
"HMMA",
"HMNMX2",
"HMUL2",
"HMUL2_32I",
"HSET2",
"HSETP2",
"DADD",
"DFMA",
"DMMA",
"DMUL",
"DSETP",
"BMMA",
"BMSK",
"BREV",
"FLO",
"IABS",
"IADD",
"IADD3",
"IADD32I",
"IDP",
"IDP4A",
"IMAD",
"IMMA",
"IMNMX",
"IMUL",
"IMUL32I",
"ISCADD",
"ISCADD32I",
"ISETP",
"LEA",
"LOP",
"LOP3",
"LOP32I",
"POPC",
"SHF",
"SHL",
"SHR",
"VABSDIFF",
"VABSDIFF4",
"F2F",
"F2I",
"I2F",
"I2I",
"I2IP",
"I2FP",
"F2IP",
"FRND",
"MOV",
"MOV32I",
"MOVM",
"PRMT",
"SEL",
"SGXT",
"SHFL",
"PLOP3",
"PSETP",
"P2R",
"R2P",
"LD",
"LDC",
"LDG",
"LDGDEPBAR",
"LDGSTS",
"LDL",
"LDS",
"LDSM",
"ST",
"STG",
"STL",
"STS",
"MATCH",
"QSPC",
"ATOM",
"ATOMS",
"ATOMG",
"RED",
"CCTL",
"CCTLL",
"ERRBAR",
"MEMBAR",
"CCTLT",
"R2UR",
"REDUX",
"S2UR",
"UBMSK",
"UBREV",
"UCLEA",
"UF2FP",
"UFLO",
"UIADD3",
"UIADD3.64",
"UIMAD",
"UISETP",
"ULDC",
"ULEA",
"ULOP",
"ULOP3",
"ULOP32I",
"UMOV",
"UP2UR",
"UPLOP3",
"UPOPC",
"UPRMT",
"UPSETP",
"UR2UP",
"USEL",
"USGXT",
"USHF",
"USHL",
"USHR",
"VOTEU",
"TEX",
"TLD",
"TLD4",
"TMML",
"TXD",
"TXQ",
"SUATOM",
"SULD",
"SUQUERY",
"SURED",
"SUST",
"BMOV",
"BPT",
"BRA",
"BREAK",
"BRX",
"BRXU",
"BSSY",
"BSYNC",
"CALL",
"EXIT",
"JMP",
"JMX",
"JMXU",
"KILL",
"NANOSLEEP",
"RET",
"RPCMOV",
"RTT",
"WARPSYNC",
"YIELD",
"B2R",
"BAR",
"CS2R",
"DEPBAR",
"GETLMEMBASE",
"LEPC",
"NOP",
"PMTRIG",
"R2B",
"S2R",
"SETCTAID",
"SETLMEMBASE",
"VOTE"]

def init_dict():
    d = {}
    for i in instr_type:
        d[i] = []
    return d

def write_to_doc(filename,d):
    classify_doc = filename.split(".")[0]+"_classify.txt"
    with open(classify_doc, "w") as f:
        for k,v in d.items():
            f.write(k+"\n")
            if(v == []):
                f.write("None\n")
            else:
                for inst in v:
                    f.write(inst)
            f.write("\n\n")
            


def process_single_file(filename,d):
    other_type = []
    with open(filename) as f:
        for line in f.readlines():
            inst_T = line.split(".")[0]
            inst_T = inst_T.split("\n")[0]
            inst_T = inst_T.split(";")[0]
            #print(inst_T,d.get(inst_T) is None)
            if(d.get(inst_T) is None):
                #print("none")
                other_type.append(line)
            else:
                d[inst_T].append(line)
                #print(d[inst_T])
        write_to_doc(filename, d)
    #print(d)


if __name__ == "__main__":
    for file in glob.glob("*.txt"):
        d = init_dict()
        #print(d)
        process_single_file(file,d)

