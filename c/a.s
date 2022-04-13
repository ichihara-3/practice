	.section	__TEXT,__text,regular,pure_instructions
	.build_version macos, 12, 0	sdk_version 12, 3
	.globl	_AddNum                         ## -- Begin function AddNum
	.p2align	4, 0x90
_AddNum:                                ## @AddNum
## %bb.0:
	pushq	%rbp
	movq	%rsp, %rbp
	movl	%edi, -4(%rbp)
	movl	%esi, -8(%rbp)
	movl	$10, -12(%rbp)
	movl	-4(%rbp), %eax
	addl	-8(%rbp), %eax
	addl	-12(%rbp), %eax
	popq	%rbp
	retq
                                        ## -- End function
	.globl	_MyFunc                         ## -- Begin function MyFunc
	.p2align	4, 0x90
_MyFunc:                                ## @MyFunc
## %bb.0:
	pushq	%rbp
	movq	%rsp, %rbp
	movl	$10, %edi
	movl	$20, %esi
	callq	_AddNum
	popq	%rbp
	retq
                                        ## -- End function
.subsections_via_symbols
