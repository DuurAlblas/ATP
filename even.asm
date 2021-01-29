
.section .text
.align 4
.global even

l_1:
f_2:
PUSH {LR}
l_2:
MOV R0, #1
MOV R3, #4
MUL R0, R0, R3
SUB R0, R5, R0
MOV R1, #2
MOV R3, #4
MUL R1, R1, R3
SUB R1, R5, R1
LDR R0, [R0]
LDR R1, [R1]
CMP R0, R1
BEQ l_3
BNE l_4
l_3:
B l_5
l_4:
B l_7
l_5:
LDR R0, [R4]
ADD R0, #1
STR R0, [R4]
l_6:
B l_9
l_7:
LDR R0, [R4]
SUB R0, #1
STR R0, [R4]
l_8:
BL f_1
l_9:
POP {PC}
l_10:
f_1:
PUSH {LR}
l_11:
MOV R0, #1
MOV R3, #4
MUL R0, R0, R3
SUB R0, R5, R0
MOV R1, #2
MOV R3, #4
MUL R1, R1, R3
SUB R1, R5, R1
LDR R0, [R0]
LDR R1, [R1]
CMP R0, R1
BEQ l_12
BNE l_13
l_12:
B l_15
l_13:
LDR R0, [R4]
SUB R0, #1
STR R0, [R4]
l_14:
BL f_2
l_15:
POP {PC}

even:
PUSH {R4,R5,R6,R7,LR}
MOV R4, SP
MOV R5, SP
SUB R4, #4
SUB SP, #256
l_16:
MOV R2, #1
MOV R3, #4
MUL R2, R2, R3
SUB R2, R5, R2
STR R0, [R2]
l_17:
SUB R4, #4
l_18:
MOV R0, #0
STR R0, [R4]
l_19:
ADD R4, #4
l_20:
BL f_2
l_21:
LDR R0, [R4]
BL print
l_22:
LDR R0, [R4]
MOV SP, R5
POP {R4,R5,R6,R7,PC}