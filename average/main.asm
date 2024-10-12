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

%macro fdev 2
    pushd
    mov rax, %1
    mov rbx, %2
    mov rdi, result
    mov ebp, 10
    xor rcx, rcx
    xor rdx, rdx

convert_to_string:
    xor rdx, rdx
    div rbx
    add rdx, '0'
    mov [result + rcx], rdx
    inc rcx
    test rax, rax
    jnz convert_to_string

    mov byte [result + rcx], 0
    mov rax, rcx
    print result, rax
    popd
%endmacro

section .text
global _start

_start:
    mov rbx, 0
    xor rax, rax
    xor rcx, rcx

sum_arrays:
    add rax, x[rbx]
    add rcx, y[rbx]
    inc rbx
    cmp rbx, lenx / 4
    jl sum_arrays

    sub rax, rcx

    test rax, rax
    jns no_negative
    mov byte [result], '-'
    print result, 1
    neg rax

no_negative:
    mov rbx, lenx / 4
    xor rdx, rdx
    div rbx
    mov [ans], rax
    mov rax, [ans]
    fdev rax, 10
    print newline, 2
    mov rax, 60
    xor rdi, rdi
    syscall

section .data
    x dd 5, 3, 2, 6, 1, 7, 4
    lenx equ $ - x
    y dd 0, 10, 1, 9, 2, 8, 5
    leny equ $ - y
    newline db 0xA, 0xD

section .bss
    result resb 32
    ans resb 8

