.global _start
.align 4
_start:
mov x8, #2
mov x9, #3
mov x10, #5
mul x9, x9, x10
add x8, x8, x9
mov x9, #8
mov x10, #3
sdiv x9, x9, x10
sub x8, x8, x9
mov x0, #0
mov x16, #1
svc #0x80
