ASM = {
    "C_ARITHMETIC": {
        "binary":   ["@SP", "AM=M-1", "D=M", "A=A-1"],
        "unary":    ["@SP", "A=M-1"],
        "logic": [
            "@SP", "AM=M-1", "D=M", "A=A-1", "D=M-D", "M=-1", "@SKIP_%%COUNT%%",
            "D;%%COND%%", "@SP", "A=M-1", "M=0", "(SKIP_%%COUNT%%)"
        ],
        "add":  "D+M",
        "sub":  "M-D",
        "and":  "D&M",
        "or":   "D|M",
        "not":  "!M",
        "neg":  "-M"
    },

    "C_PUSH": {
        "end":      ["@SP", "M=M+1", "A=M-1", "M=D"],
        "indirect": ["@%%CONST%%", "D=A", "@%%SEG%%", "A=D+M", "D=M"],
        "direct":   ["@%%ADDR%%", "D=M"],
        "constant": ["@%%CONST%%", "D=A"]
    },
    
    "C_POP": {
        "indirect": [
            "@%%CONST%%", "D=A", "@%%SEG%%", "D=D+M", "@R13", "M=D", "@SP",
            "AM=M-1", "D=M", "@R13", "A=M", "M=D"
        ],
        "direct": ["@SP", "AM=M-1", "D=M", "@%%ADDR%%", "M=D"]
    },

    "C_IF": ["@SP", "AM=M-1", "D=M", "@%%IF%%", "D;JNE"],

    "C_CALL": [
        "@%%FNAME%%$ret_%%CNT%%", "D=A", "@SP", "M=M+1", "A=M-1", "M=D", "@LCL", "D=M", "@SP", "M=M+1", "A=M-1", "M=D",
        "@ARG", "D=M", "@SP", "M=M+1", "A=M-1", "M=D", "@THIS", "D=M", "@SP", "M=M+1", "A=M-1", "M=D",
        "@THAT", "D=M", "@SP", "M=M+1", "A=M-1", "M=D", "@%%NARG%%", "D=A", "@5", "D=D+A", "@SP", "D=M-D",
        "@ARG", "M=D", "@SP", "D=M", "@LCL", "M=D", "@%%FNAME%%", "0;JMP", "(%%FNAME%%$ret_%%CNT%%)"
    ],

    "C_FUNCTION": ["(%%FNAME%%)", "@%%NLCL%%", "D=A", "@NoArg_%%CNT%%", "D;JEQ", "(InitLoop_%%CNT%%)", "@SP", "M=M+1", "A=M-1", "M=0", "@InitLoop_%%CNT%%", "D=D-1;JGT", "(NoArg_%%CNT%%)"],

    "C_RETURN": [
        "@LCL", "D=M", "@R13", "M=D", "@5", "A=D-A", "D=M", "@R14", "M=D", "@SP", "A=M-1", "D=M", "@ARG", "A=M", "M=D",
        "@ARG", "D=M", "@SP", "M=D+1", "@R13", "M=M-1", "A=M", "D=M", "@THAT", "M=D", "@R13", "M=M-1", "A=M", "D=M",
        "@THIS", "M=D", "@R13", "M=M-1", "A=M", "D=M", "@ARG", "M=D", "@R13", "M=M-1", "A=M", "D=M", "@LCL", "M=D",
        "@R14", "A=M", "0;JMP"
    ],

    "INIT_SP": ["\t@256", "D=A", "@SP", "M=D"],

    "HALT": ["(END)", "@END", "0;JMP"]
}
