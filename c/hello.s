	.globl	_main                           ## -- Begin function main
_main:                                  ## @main
	pushq	%rbp
	movq	%rsp, %rbp
	leaq	L_.str(%rip), %rdi
	callq	_puts
	xorl	%eax, %eax
	popq	%rbp
	retq
                                        ## -- End function
L_.str:                                 ## @.str
	.asciz	"Hello, World"
