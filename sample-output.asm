section .bss
	var2: resq 1
	var1: resq 1
	var0: resq 1

section .data
	inputBuffer db '0000000000000000000',0
	outputBuffer db '-00000000000000000000',10
	varInput2: db 'Initial value of hours: '
	varInputSize2: equ $-varInput2
	varOutput2: db 'Final value of hours: '
	varOutputSize2: equ $-varOutput2
	varInput1: db 'Initial value of secs: '
	varInputSize1: equ $-varInput1
	varOutput1: db 'Final value of secs: '
	varOutputSize1: equ $-varOutput1
	varInput0: db 'Initial value of mins: '
	varInputSize0: equ $-varInput0
	varOutput0: db 'Final value of mins: '
	varOutputSize0: equ $-varOutput0

section .text
	global _start

_start:
	; Prompt Initial value of var2
	push 1
	pop rax
	mov rdi,rax
	mov rsi,varInput2
	mov rdx,varInputSize2
	syscall
	xor rax,rax
	xor rdi,rdi
	mov rsi,inputBuffer
	push 19
	pop rdx
	syscall
	mov rcx,rax
	mov al,[rsi]
	test al,'-'
	je label1
	push 0
	jmp label2
label1:
	push 1
	dec rcx
	inc rsi
label2:
	xor rax,rax
	xor rbx,rbx
	push '0'
	pop rdi
	push 10
	pop r8
label3:
	mov bl,[rsi]
	sub bl,dil
	cmp bl,r8b
	jae label4
	mul r8
	add rax,rbx
	inc rsi
	loop label3
label4:
	pop rbx
	test rbx,rbx
	jz label5
	neg rax
label5:
	mov [var2],rax

	; Prompt Initial value of var1
	push 1
	pop rax
	mov rdi,rax
	mov rsi,varInput1
	mov rdx,varInputSize1
	syscall
	xor rax,rax
	xor rdi,rdi
	mov rsi,inputBuffer
	push 19
	pop rdx
	syscall
	mov rcx,rax
	mov al,[rsi]
	test al,'-'
	je label6
	push 0
	jmp label7
label6:
	push 1
	dec rcx
	inc rsi
label7:
	xor rax,rax
	xor rbx,rbx
	push '0'
	pop rdi
	push 10
	pop r8
label8:
	mov bl,[rsi]
	sub bl,dil
	cmp bl,r8b
	jae label9
	mul r8
	add rax,rbx
	inc rsi
	loop label8
label9:
	pop rbx
	test rbx,rbx
	jz label10
	neg rax
label10:
	mov [var1],rax

	; Prompt Initial value of var0
	push 1
	pop rax
	mov rdi,rax
	mov rsi,varInput0
	mov rdx,varInputSize0
	syscall
	xor rax,rax
	xor rdi,rdi
	mov rsi,inputBuffer
	push 19
	pop rdx
	syscall
	mov rcx,rax
	mov al,[rsi]
	test al,'-'
	je label11
	push 0
	jmp label12
label11:
	push 1
	dec rcx
	inc rsi
label12:
	xor rax,rax
	xor rbx,rbx
	push '0'
	pop rdi
	push 10
	pop r8
label13:
	mov bl,[rsi]
	sub bl,dil
	cmp bl,r8b
	jae label14
	mul r8
	add rax,rbx
	inc rsi
	loop label13
label14:
	pop rbx
	test rbx,rbx
	jz label15
	neg rax
label15:
	mov [var0],rax

	; Program code
	push 60
	push qword [var1]
	pop rax
	pop rbx
	cqo
	idiv rbx
	push rax
	push qword [var0]
	pop rax
	pop rbx
	add rax,rbx
	push rax
	pop qword [var0]
	push 60
	push 60
	push qword [var1]
	pop rax
	pop rbx
	cqo
	idiv rbx
	push rax
	pop rax
	pop rbx
	imul rbx
	push rax
	push qword [var1]
	pop rax
	pop rbx
	sub rax,rbx
	push rax
	pop qword [var1]
	push 60
	push qword [var0]
	pop rax
	pop rbx
	cqo
	idiv rbx
	push rax
	push qword [var2]
	pop rax
	pop rbx
	add rax,rbx
	push rax
	pop qword [var2]
	push 60
	push 60
	push qword [var0]
	pop rax
	pop rbx
	cqo
	idiv rbx
	push rax
	pop rax
	pop rbx
	imul rbx
	push rax
	push qword [var0]
	pop rax
	pop rbx
	sub rax,rbx
	push rax
	pop qword [var0]

	; Write final value of var2
	push 1
	pop rax
	mov rdi,rax
	mov rsi,varOutput2
	mov rdx,varOutputSize2
	syscall
	mov rax,[var2]
	test rax,rax
	js label16
	mov rsi,outputBuffer+1
	jmp label17
label16:
	mov rsi,outputBuffer
	neg rax
label17:
	push 10
	pop rbx
	xor rcx,rcx
label18:
	xor rdx,rdx
	div rbx
	push rdx
	inc rcx
	test rax,rax
	jnz label18
	push '0'
	pop rdi
	mov rdx,outputBuffer+1
label19:
	pop rax
	add rax,rdi
	mov [rdx],al
	inc rdx
	loop label19
	mov [rdx],bl
	inc rdx
	push 1
	pop rax
	mov rdi,rax
	sub rdx,rsi
	syscall

	; Write final value of var1
	push 1
	pop rax
	mov rdi,rax
	mov rsi,varOutput1
	mov rdx,varOutputSize1
	syscall
	mov rax,[var1]
	test rax,rax
	js label20
	mov rsi,outputBuffer+1
	jmp label21
label20:
	mov rsi,outputBuffer
	neg rax
label21:
	push 10
	pop rbx
	xor rcx,rcx
label22:
	xor rdx,rdx
	div rbx
	push rdx
	inc rcx
	test rax,rax
	jnz label22
	push '0'
	pop rdi
	mov rdx,outputBuffer+1
label23:
	pop rax
	add rax,rdi
	mov [rdx],al
	inc rdx
	loop label23
	mov [rdx],bl
	inc rdx
	push 1
	pop rax
	mov rdi,rax
	sub rdx,rsi
	syscall

	; Write final value of var0
	push 1
	pop rax
	mov rdi,rax
	mov rsi,varOutput0
	mov rdx,varOutputSize0
	syscall
	mov rax,[var0]
	test rax,rax
	js label24
	mov rsi,outputBuffer+1
	jmp label25
label24:
	mov rsi,outputBuffer
	neg rax
label25:
	push 10
	pop rbx
	xor rcx,rcx
label26:
	xor rdx,rdx
	div rbx
	push rdx
	inc rcx
	test rax,rax
	jnz label26
	push '0'
	pop rdi
	mov rdx,outputBuffer+1
label27:
	pop rax
	add rax,rdi
	mov [rdx],al
	inc rdx
	loop label27
	mov [rdx],bl
	inc rdx
	push 1
	pop rax
	mov rdi,rax
	sub rdx,rsi
	syscall

	; Exit
	mov rax,0x3c
	xor rdi,rdi
	syscall
