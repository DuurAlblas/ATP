
.section .text
.align 4
.global coco

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
B l_18
l_4:
LDR R0, [R4]
SUB R0, #1
STR R0, [R4]
l_5:
BL f_1
l_6:
POP {PC}
l_7:
f_1:
PUSH {LR}
l_8:
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
BEQ l_9
BNE l_10
l_9:
B l_19
l_10:
LDR R0, [R4]
SUB R0, #1
STR R0, [R4]
l_11:
BL f_2
l_12:
POP {PC}

coco:
PUSH {R4,R5,R6,R7,LR}
MOV R4, SP
MOV R5, SP
SUB R4, #4
SUB SP, #256
l_13:
MOV R0, #8
STR R0, [R4]
l_14:
SUB R4, #4
l_15:
MOV R0, #0
STR R0, [R4]
l_16:
ADD R4, #4
l_17:
BL f_2
l_18:
LDR R0, [R4]
ADD R0, #1
STR R0, [R4]
l_19:
LDR R0, [R4]
BL print
l_20:
MOV SP, R5
POP {R4,R5,R6,R7,PC}