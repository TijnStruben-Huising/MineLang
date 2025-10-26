import sys,os
false = False
true = True
path = sys.argv[1]
output_path = path + ".s"
final_output = sys.argv[2]

code = ""
with open(path) as file:
    code = file.read()

alpha = {x for x in "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"}
num = {x for x in "1234567890"}
extra = {x for x in ".+-"}


lexed = []
acc = ""
for x in code:
    if not (x in alpha or x in num or x in extra):
        if acc != "":
            lexed.append(acc)
            acc = ""
    else:
        acc += x
if acc != "":
    lexed.append(acc)
#print(lexed)
op = []
read_children = 0
children_acc = []
temp_val = ""
for x in lexed:
    if read_children > 0:
        children_acc.append(x)
        read_children -= 1
        if read_children == 0:
            read_children = 0
            op.append((temp_val,children_acc))

    elif x.isdecimal():
        op.append(("LABEL",[int(x)]))
    elif x in {"READ","WRITE","SYSCALL","PLACE","FLAG"}:
        op.append((x,[]))
    elif x == "GOTO":
        temp_val = x
        children_acc = []
        read_children = 1
    elif x == "DO":
        temp_val = x
        children_acc = []
        read_children = 9    
    elif x == "MOV":
        temp_val = x
        children_acc = []
        read_children = 2 
    else: 
        pass

#print(op)


def label_of_int(i):
    return "_label_"+str(i)

compiled = []

for x in op:
    (val,extra) = x
    if val == "GOTO":
        compiled.append("   jmp "+label_of_int(extra[0]))
    elif val == "MOV":
        mv1 = extra[0]
        mv2 = extra[1]
        if mv1 == "+":
            compiled.append("   inc %rax")
        if mv1 == "-":
            compiled.append("   dec %rax")
        if mv2 == "+":
            compiled.append("   inc %rbx")
        if mv2 == "-":
            compiled.append("   dec %rbx")
    elif val == "LABEL":
        compiled.append("   "+label_of_int(extra[0])+":")
    elif val == "DO":
        compiled.append("   push %rax")
        compiled.append("   push %rbx")

        compiled.append("   mov %rax, %rdi")
        compiled.append("   mov %rbx, %rsi")

        compiled.append("   call TEST")

        compiled.append("   mov %rax, %rcx")
        compiled.append("   pop %rbx")
        compiled.append("   pop %rax")

        for x in range(9):
            compiled.append("   mov $"+str(x)+", %rdx")

            compiled.append("   cmp %rcx, %rdx")
            compiled.append("   je "+label_of_int(extra[x]))

    elif val == "READ":
        compiled.append("   push %rax")
        compiled.append("   push %rbx")

        compiled.append("   mov %rax, %rdi")
        compiled.append("   mov %rbx, %rsi")

        compiled.append("   call READ")

        compiled.append("   pop %rbx")
        compiled.append("   pop %rax")
    elif val == "WRITE":
        compiled.append("   push %rax")
        compiled.append("   push %rbx")

        compiled.append("   mov %rax, %rdi")
        compiled.append("   mov %rbx, %rsi")

        compiled.append("   call WRITE")

        compiled.append("   pop %rbx")
        compiled.append("   pop %rax")
    elif val == "PLACE":
        compiled.append("   push %rax")
        compiled.append("   push %rbx")

        compiled.append("   mov %rax, %rdi")
        compiled.append("   mov %rbx, %rsi")

        compiled.append("   call PLACE")

        compiled.append("   pop %rbx")
        compiled.append("   pop %rax")
    elif val == "FLAG":
        compiled.append("   push %rax")
        compiled.append("   push %rbx")

        compiled.append("   mov %rax, %rdi")
        compiled.append("   mov %rbx, %rsi")

        compiled.append("   call FLAG")

        compiled.append("   pop %rbx")
        compiled.append("   pop %rax")
    elif val == "SYSCALL":
        compiled.append("   push %rax")
        compiled.append("   push %rbx")

        compiled.append("   mov %rax, %rdi")
        compiled.append("   mov %rbx, %rsi")

        compiled.append("   call SYSCALL")

        compiled.append("   pop %rbx")
        compiled.append("   pop %rax")
compiled = """
    .global main

    .text

main:
    call startup
    mov $0, %rax
    mov $0, %rbx

""" + "\n".join(compiled) + """

mov $60, %rax
mov $0, %rdi
    syscall

"""

with open(output_path,"w") as file:
    file.write(compiled)

os.system("gcc " + output_path +" lib.c -o " + final_output)