
.section .text
.align 4
.global coco


coco:
PUSH {R4,R5,R6,R7,LR}
MOV R4, SP
MOV R5, SP
SUB R4, #4
SUB SP, #256
l_1:
MOV R2, #1
MOV R3, #4
MUL R2, R2, R3
SUB R2, R5, R2
STR R0, [R2]
l_2:
MOV R2, #2
MOV R3, #4
MUL R2, R2, R3
SUB R2, R5, R2
STR R1, [R2]
l_3:
LDR R0, [R4]
BL print
l_4:
SUB R4, #4
l_5:
LDR R0, [R4]
BL print
l_6:
LDR R0, [R4]
MOV SP, R5
POP {R4,R5,R6,R7,PC}