# coding: UTF-8
import sys

N = 65      #セルの最大個数
R = 8       #ルール表の大きさ
MAXT = 50   #繰り返しの回数

def setrule(rule,ruleno):
    for i in range(0,R):
        rule[i] = ruleno % 2
        ruleno = ruleno // 2
    for i in range(R - 1,-1,-1):
        print(rule[i])

def initca(ca):
    line = input("caの初期値を入力して下さい:")
    print()
    for no in range(len(line)):
        ca[no] = int(line[no])

def putca(ca):
    for no in range(N - 1,-1,-1):
        print("{:1d}".format(ca[no]), end="")
    print()

def nextt(ca,rule):
    nextca = [0 for i in range(N)]
    for i in range(1,N - 1):
        nextca[i] = rule[ca[i + 1] * 4 + ca[i] * 2 + ca[i-1]]
    for i in range(N):
        ca[i] = nextca[i]

rule = [0 for i in range(R)]
ruleno = int(input("ルール番号を入力して下さい:"))
print()

if ruleno < 0 or ruleno > 255:
        print("ルール番号が正しくありません(", ruleno,")")
        sys.exit()

setrule(rule,ruleno)        #

ca = [0 for i in range(N)]  #
initca(ca)
putca(ca)

for t in range(MAXT):
    nextt(ca, rule)
    putca(ca)
