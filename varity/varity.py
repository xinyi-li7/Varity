import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'common')))

# Varity modules
import gen_program
import cfg
import run
import type_checking
import dump

# Python modules
import subprocess
import socket
import multiprocessing as mp
import argparse

def writeProgramCode(fileName):
    # Write C code
    p = gen_program.Program()
    (code, allTypes) = p.printCode()
    c_fileName = fileName + ".c"
    #writeInputFile(c_fileName, allTypes)
    writeInputFile(fileName, allTypes)
    f = open(c_fileName, "w")
    f.write(code)
    f.close()

    # Write CUDA code
    (code, allTypes) = p.printCode("NVIDIA")
    cuda_fileName = fileName + ".cu"
    #writeInputFile(cuda_fileName, allTypes)
    f = open(cuda_fileName, "w")
    f.write(code)
    f.close()

    # Write HIP code
    (code, allTypes) = p.printCode("AMD")
    cuda_fileName = fileName + ".hip"
    #writeInputFile(cuda_fileName, allTypes)
    f = open(cuda_fileName, "w")
    f.write(code)
    f.close()

def writeInputFile(fileName, allTypes):
    f = open(fileName+".input", "w")
    f.write(type_checking.getTypeString()+",")
    f.write(allTypes+"\n")
    f.close()

def isCUDACompiler(compiler_name):
    return "nvcc" in compiler_name

def getExtraOptimization(compiler_name, e: int):
    ret = ""
    if "clang" in compiler_name:
        if e == 1:
            ret = "-ffp-contract=off"
        ret = ret + " -std=c99"
    elif "gcc" in compiler_name:
        if e == 1:
            ret = "-ffp-contract=off"
        ret = ret + " -std=c99"
    elif "pgi" in compiler_name:
        if e == 1:
            ret = "-nofma"
        ret = ret + " -c99"
    #elif "nvcc" in compiler_name:
    #    if e == 1:
    #        ret = "--fmad=false"
    #    ret = ret + " -arch=sm_86"
    elif "nvcc" in compiler_name:
        if e == 1:
            ret = "--use_fast_math"
        ret = ret + " -arch=sm_86"
    elif "xlc" in compiler_name:
        if e == 1:
            ret = "-qfloat=nomaf"

    return ret

def compileCode(config):
    (compiler_name, compiler_path, op_level, other_op, dirName, fileName) = config
    try:
        pwd = os.getcwd()
        os.chdir(dirName)
        libs = " -lm "
        more_ops = getExtraOptimization(compiler_name, other_op)
        extra_name = ""
        #if other_op == 1:
        #    extra_name = "_nofma"
        if other_op == 1:
            extra_name = "_fastmath"
        compilation_arguments = [compiler_path, op_level, more_ops, libs, "-o", fileName+"-"+compiler_name+op_level+extra_name+".exe", fileName]
        cmd = " ".join(compilation_arguments)
        #cmd = compiler_path + " " + op_level + " " + more_ops + " " + libs + " -o " + fileName + "-" + compiler_name + op_level + extra_name + ".exe " + fileName
        #if isCUDACompiler(compiler_name):
        #    cmd = cmd+"u"

        out = subprocess.check_output(cmd, shell=True)
        os.chdir(pwd)
    except subprocess.CalledProcessError as outexc:                                                                                                   
        print("Error at compile time:", outexc.returncode, outexc.output)
        print("FAILED: ", cmd)

def generateTests():
    dir = getTargetDirectory()
    print("Generating {} groups, {} tests... ".format(cfg.NUM_GROUPS, cfg.TESTS_PER_GROUP))
    fileNameList = []
    for g in range(cfg.NUM_GROUPS):
        # Create directory
        p = dir + "/" + cfg.TESTS_DIR + "/_group_" + str(g+1)
        try:
            os.makedirs(p)
        except FileExistsError:
            pass # directory already exists
        
        # Write the program source code
        for t in range(cfg.TESTS_PER_GROUP): 
            #fileName = p + "/_test_" + str(t+1) + ".cu"
            fileName = p + "/_test_" + str(t+1) 
            fileNameList.append(fileName)

    cpuCount = mp.cpu_count()
    for i in range(0, len(fileNameList), cpuCount):
        workLoad = fileNameList[i:i+cpuCount]
        with mp.Pool(cpuCount) as myPool:
            myPool.map(writeProgramCode, workLoad)
            #writeProgramCode(fileName)
    print("done!")
    return dir

def compileTests(path):
    print("Compiling tests...")
    print("Total tests to compile: ", cfg.NUM_GROUPS*cfg.TESTS_PER_GROUP)

    compileConfigList = []
    for g in range(cfg.NUM_GROUPS):
        p = path + "/" + cfg.TESTS_DIR + "/_group_" + str(g+1)
        for t in range(cfg.TESTS_PER_GROUP):
            fileName = "_test_" + str(t+1) + ".cu"
            for c in cfg.COMPILERS:
                compiler_name = c[0]
                compiler_path = c[1]
                for opts in cfg.OPT_LEVELS:
                    (op, other_op) = opts
                    config = (compiler_name, compiler_path, op, other_op, p, fileName)
                    compileConfigList.append(config)

    cpuCount = mp.cpu_count()
    for i in range(0, len(compileConfigList), cpuCount):
        print("\r--> Compiling test: {}".format(int(i/cpuCount)+1), end='')
        sys.stdout.flush()
        workLoad = compileConfigList[i:i+cpuCount]
        with mp.Pool(cpuCount) as myPool:
            myPool.map(compileCode, workLoad)

    print("")

def dirName():
    return socket.gethostname()+"_"+str(os.getpid())

def getTargetDirectory():
    p = dirName()
    print("Creating dir:", p)
    try:
        os.mkdir(p)
    except OSError:
        print ("Creation of the directory %s failed" % p)
        exit()
    return p

def runTests(dir):
    #p = getTargetDirectory()
    #cfg.TESTS_DIR = p + "/" + cfg.TESTS_DIR
    #p = dir
    run.run(dir)

def dumpSASS(dir):
    dump.dump(dir)
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--generate", help="generate programs",action="store_true")
    parser.add_argument("-c", "--compile", type=str, help="compile programs in dir: COMPILE")
    parser.add_argument("-r", "--run",nargs=1, type=str, help="run programs in dir: RUN, need one argument after run to specify the device as host, AMD or NVIDIA")
    parser.add_argument("-d","--dump",type=str,help="dump the SASS codes for each file")
    args = parser.parse_args()
    
#    if len(sys.argv) == 1:
#        dir = generateTests()
#        compileTests(dir)
#        runTests(dir)
#    else:
    if args.generate:
        generateTests()
    if args.compile:
        compileTests(args.compile)
    if args.run:
        device = args.run[0].lower()
    if device == "host":
        print("Running on the host device. To run on other devices, specify --run 'device_name'")
        # runHost()
        # runTests(args.run)
        generateTests()
    elif device == "amd":
        # runAMD()
        runTests(args.run)
    elif device == "nvidia":
        # runNVIDIA()
        runTests(args.run)
    else:
        print("Invalid device argument. Please use 'host', 'AMD', or 'NVIDIA'.")
    if args.dump:
        dumpSASS(args.dump)
if __name__ == '__main__':
    main()
