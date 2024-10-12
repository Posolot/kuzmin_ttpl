%macro pushd 0
   push rax
   push rbx
   push rcx
   push rdx
%endmacro

%macro popd 0
   pop rdx
   pop rcx
   pop rbx
   pop rax
%endmacro

%macro print 2
   pushd
   mov rax, 1
   mov rdi, 1
   mov rsi, %1
   mov rdx, %2
   syscall
   popd
%endmacro

%macro dprint 0
   pushd
   xor rbx, rbx
   mov rcx, 10
   %%divide:
       xor rdx, rdx
       div rcx
       print value, 1

       push rdx
       inc rbx
       test rax, rax
       jnz %%divide

   %%digit:
       pop rax
       add rax, '0'
       mov [value], rax
       print value, 1
       dec rbx
       jnz %%digit
   popd
%endmacro

%macro print_number 1
   push rax
   push rbx
   push rcx
   push rdx

   mov rax, %1

   mov rdi, 1
   mov rsi, rax
   mov rdx, 10
   mov rax, 1
   syscall

   pop rdx
   pop rcx
   pop rbx
   pop rax
%endmacro

section .data
    input_number dq 130
    value dq 0
    newline db 0xA, 0xD
    nlen equ $ - newline
    completed_msg db 'approximate root of a number', 0xA, 0xD
    len equ $ - completed_msg

section .bss
    temp1 resq 1
    temp2 resq 1

section .text
    global _start

_start:
    mov rax, [input_number]
    shr rax, 1
    mov [temp1], rax

    mov rax, [input_number]
    mov rbx, [temp1]
    xor rdx, rdx
    div rbx
    add rax, [temp1]
    shr rax, 1
    mov [temp2], rax

while_loop:
    mov rax, [temp1]
    sub rax, [temp2]
    cmp rax, 1
    jl end_while

    mov rax, [temp2]
    mov [temp1], rax

    mov rax, [input_number]
    mov rbx, [temp1]
    xor rdx, rdx
    div rbx
    add rax, [temp1]
    shr rax, 1
    mov [temp2], rax

    jmp while_loop

end_while:
    mov rax, [temp2]
    dprint
    print newline, nlen
    print completed_msg, len
    mov rax, 60
    xor rdi, rdi
    syscall
