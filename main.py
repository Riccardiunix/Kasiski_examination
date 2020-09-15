import sys
import math
import numpy
import time

def factorization(n):
    if len(dp[n]) == 0:
        for i in range(int(round(math.sqrt(n))), 0, -1):
            if n % i == 0:
                dp[n][i] = 0
                dp[n][n//i] = 0
                for j in factorization(i):
                    dp[n][j] = 0
                    dp[n][n//j] = 0
                if i != n//i:
                    for j in factorization(n//i):
                        dp[n][j] = 0
                        dp[n][n//j] = 0
    return dp[n]

start = time.time()
if __name__ == "__main__":
    text = open("text.txt", "r").read().lower().replace('\n', '')
    text_val = []
    text_ok = ""
    comb = {}
    
    for i in range(len(text)):
        if ord(text[i]) > 96 and ord(text[i]) < 123:
            text_val.append(ord(text[i]) - 97)
            text_ok += text[i]
    
    print("Finding pattern and calculating distance... ")
    a = [0] * (len(text_ok))
    m = 0
    for i in range(len(text_ok) - 1):
        pat = text_ok[i]
        for j in range(i+1, 1 + (len(text_ok) + i) // 2):
            pat += text_ok[j]
            if not pat in comb:
                comb[pat] = [i]
            else:
                arr = comb[pat]
                for l in arr:
                    a[i - l] += 1
                m = max(m, i - arr[0])
                comb[pat].append(i)
    del comb
    a = a[:(m + 1)]
    
    print("Calculating key length... ")
    dp = [{}, {}]
    b = [0] * (m + 1)
    for i in range(2, m+1):
        dp.append({})
        if a[i] > 0:
            for j in factorization(i).keys():
                b[j] -= a[i]
    del dp
    
    fact = [1]
    if m <= 492:
        for i in numpy.argsort(b[1:])[:min(m, 9)]:
            fact.append(i)
    else:
        for i in range(min(m, 9)):
            mi = b[2]
            miI = 2
            for j in range(3, m+1):
                if mi > b[j]:
                    mi = b[j]
                    miI = j
            b[miI] = 0
            fact.append(miI)
    
    eng = [8.167, 1.492, 2.782, 4.253, 12.702, 2.228, 2.015, 6.094, 6.966, 0.153, 0.772, 4.025, 2.406, 6.749, 7.507, 1.929, 0.095, 5.987, 6.327, 9.056, 2.758, 0.978, 2.360, 0.15, 1.974, 0.074]
    ita = [11.293, 0.911, 4.822, 3.724, 12.044, 1.115, 1.742, 1.465, 9.752, 0.002, 0.00001, 5.644, 2.544, 7.087, 9.624, 2.918, 0.795, 6.555, 5.506, 5.973, 3.581, 2.220, 0.001, 0.006, 0.001, 0.675]
    perc = ita

    for lung in fact:
        #Popolo array
        freq = []
        som = [0] * lung
        
        #Calcolo della freqenza dei caratteri nella sotto sequenza --O(n)
        for i in range(len(text_val)):
            if i < lung:
                freq.append([0] * 26)
            som[i % lung] += 1
            freq[i % lung][text_val[i]] += 1
        
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
        solved = [""] * len(text)
        for i in range(len(text)):
            solved[i] = text[i]
            if ord(text[i]) > 96 and ord(text[i]) < 123: 
                solved[i] = chr(97 + (text_val[j] - key_val[j % lung]) % 26)
                j += 1
        print(''.join(solved) + "\n")
    print(time.time() - start)
            
