
.section .text
.align 4
.global coco

l_1:
BA param 1
l_2:
RIGHT
l_3:
AX param 0
l_4:
RIGHT
l_5:
AX param 0
l_6:
LB param 1
l_7:
XY param a 1 param b 3
l_8:
SELECT param 15
l_9:
YB param a 2 param b 1
l_10:
DOWN
l_11:
SELECT param 7

coco:
PUSH {R4,R5,R6,R7,LR}
MOV R4, SP
MOV R5, SP
SUB R4, #4
SUB SP, #512
l_12:
AB
l_13:
AX param 5
l_14:
START param 1
l_15:
XA param 2
l_16:
RB
l_17:
BX