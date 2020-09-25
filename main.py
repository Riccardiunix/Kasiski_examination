import math
import numpy
import time
import argparse

def factorization(n):
    if not n in dp:
        dp[n] = {}
        dp[n][n] = 0
        for i in range(int(round(math.sqrt(n))), 1, -1):
            if n % i == 0:
                dp[n][i] = 0
                for j in factorization(i):
                    dp[n][j] = 0
                    dp[n][n//j] = 0
                if i != n//i:
                    dp[n][n//i] = 0
                    for j in factorization(n//i):
                        dp[n][j] = 0
                        dp[n][n//j] = 0
    return dp[n].keys()

start = time.time()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type=str, help="the input file")
    parser.add_argument('-o', type=str, default="", help="the output file")
    parser.add_argument('-l', type=int, default=0, help="the letter frequency to use for the frequency analysis.\n0: italian; 1: english")
    args = parser.parse_args()
    
    text = open(args.i, "r").read().lower().replace('\n', '')
    text_ok = ""
    allComb = {}
    comb = {}
    
    for char in text:
        val = ord(char)
        if val > 96 and val < 123:
            text_ok += char
    
    print("Finding pattern and calculating distance... ")
    dim = len(text_ok)
    a = {}
    m = 0
    for i in range(dim-1):
        pat = text_ok[i]
        for j in range(i+1, min(dim, (dim//2)+i+1)):
            pat += text_ok[j]
            if pat in comb:
                for l in comb[pat]:
                    diff = i - l
                    if diff in a:
                        a[diff] += 1
                    else:
                        a[diff] = 1
                m = max(m, i - comb[pat][0])
                comb[pat].append(i)
            elif pat in allComb:
                comb[pat] = [allComb[pat], i]
                del allComb[pat]
            else:
                allComb[pat] = i
    del comb
    del allComb
    
    print("Calculating key length... ")
    dp = {}
    b = [0] * (m + 1)
    for i in a.keys():
        for j in factorization(i):
            b[j] -= a[i]
    del dp
    
    fact = []
    if m <= 1019:
        fact = numpy.argsort(b[2:])[:min(m, 10)]
        for i in range(min(m, 10)):
            fact[i] = fact[i] + 2  
    else:
        for i in range(10):
            mi = b[2]
            miI = 2
            for j in range(3, m+1):
                if mi > b[j]:
                    mi = b[j]
                    miI = j
            b[miI] = 0
            fact.append(miI)
    
    perc = [11.293, 0.911, 4.822, 3.724, 12.044, 1.115, 1.742, 1.465, 9.752, 0.002, 0.00001, 5.644, 2.544, 7.087, 9.624, 2.918, 0.795, 6.555, 5.506, 5.973, 3.581, 2.220, 0.001, 0.006, 0.001, 0.675]
    if args.l == 1:
        perc = [8.167, 1.492, 2.782, 4.253, 12.702, 2.228, 2.015, 6.094, 6.966, 0.153, 0.772, 4.025, 2.406, 6.749, 7.507, 1.929, 0.095, 5.987, 6.327, 9.056, 2.758, 0.978, 2.360, 0.15, 1.974, 0.074]
    
    if args.o != '':
        out = open(args.o, 'w')
    
    for lung in fact:
        #Popolo array
        freq = []
        som = [0] * lung
        
        #Calcolo della freqenza dei caratteri nella sotto sequenza --O(n)
        for i in range(len(text_ok)):
            if i < lung:
                freq.append([0] * 26)
            som[i % lung] += 1
            freq[i % lung][ord(text_ok[i])-97] += 1
        
        key = ""
        key_val = []
        for i in range(lung):
            tot = [0] * 26
            for j in range(26):
                for k in range(26):
                    tot[j] += abs(freq[i][(j + k) % 26] - perc[k])
            mi = tot[0]
            ind = 0
            for j in range(1, 26):
                if tot[j] < mi:
                    mi = tot[j]
                    ind = j
            key += chr(ind + 97)
            key_val.append(ind)
            
        print("\t%s\t%d" % (key, lung))
        j = 0
        solved = []
        for i in range(len(text)):
            if ord(text[i]) > 96 and ord(text[i]) < 123: 
                solved.append(chr(97 + (ord(text_ok[j]) - key_val[j % lung] - 97) % 26))
                j += 1
            else:
                solved.append(text[i])
                
        if args.o != '':
            out.write("\t%s\t%d\n" % (key, lung) + ''.join(solved) + "\n\n")
        print(''.join(solved) + "\n")
    print(time.time() - start)
            
