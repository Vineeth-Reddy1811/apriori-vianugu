import itertools

# prompt to enter support values in percent

# min_sup = int(input("Please enter support value in %: ")) /10
min_sup = 2
confidence = 66

# Compute candidate 1-itemset
C1 = {}
# total number of transactions contained in the file
transactions = 0
D = []
T = []

# Reading and handling CSV dataset file.
with open("1000-out1.csv", "r") as f:
    for line in f:
        T = []
        transactions += 1
        for word in line.split():
            T.append(word)
            if word not in C1.keys():
                C1[word] = 1
            else:
                count = C1[word]
                C1[word] = count + 1
        D.append(T)

# Compute frequent 1-itemset
L1 = []
for key in C1:
    if (100 * C1[key] / transactions) >= min_sup:
        list = []
        list.append(key)
        L1.append(list)


# apriori_gen function

def apriori_gen(Lk_1, k):
    length = k
    Ck = []
    for l1 in Lk_1:
        for l2 in Lk_1:
            count = 0
            c = []
            if l1 != l2:
                while count < length - 1:
                    if l1[count] != l2[count]:
                        break
                    else:
                        count += 1
                else:
                    if l1[length - 1] < l2[length - 1]:
                        for item in l1:
                            c.append(item)      #joining
                        c.append(l2[length - 1])
                        if not has_infrequent_subset(c, Lk_1, k):
                            Ck.append(c)
                            c = []
    return Ck


def findsubsets(S, m):
    return set(itertools.combinations(S, m))



def has_infrequent_subset(c, Lk_1, k):
    list = []
    list = findsubsets(c, k)
    for item in list:
        s = []
        for l in item:
            s.append(l)
        s.sort()
        if s not in Lk_1:
            return True
    return False


def frequent_itemsets():
    k = 2
    Lk_1 = []
    Lk = []
    L = []

    for item in L1:
        Lk_1.append(item)
    while Lk_1 != []:
        Ck = []
        Lk = []
        Ck = apriori_gen(Lk_1, k - 1)
        for c in Ck:
            count = 0
            transactions = 0
            s = set(c)
            for T in D:
                transactions += 1
                t = set(T)
                if s.issubset(t) == True:
                    count += 1
            if (100 * count / transactions) >= min_sup:
                c.sort()
                Lk.append(c)
        Lk_1 = []
        for l in Lk:
            Lk_1.append(l)
        k += 1
        if Lk != []:
            L.append(Lk)

    return L


def generate_association_rules():
    s = []
    r = []
    length = 0
    count = 1
    inc1 = 0
    inc2 = 0
    num = 1
    m = []
    L = frequent_itemsets()
    for list in L:
        for l in list:
            length = len(l)
            count = 1
            while count < length:
                s = []
                r = findsubsets(l, count)
                count += 1
                for item in r:
                    inc1 = 0
                    inc2 = 0
                    s = []
                    m = []
                    for i in item:
                        s.append(i)
                    for T in D:
                        if set(s).issubset(set(T)) == True:
                            inc1 += 1
                        if set(l).issubset(set(T)) == True:
                            inc2 += 1
                    if 100 * inc2 / inc1 >= confidence:
                        for index in l:
                            if index not in s:
                                m.append(index)
                        print("%s" % (s))
                        num += 1

generate_association_rules()
print("--------------------------------------------------------")