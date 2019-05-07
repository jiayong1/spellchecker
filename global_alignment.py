from tqdm import tqdm
score = {}
sigma = 5
score_mat_str = \
'''A  C  D  E  F  G  H  I  K  L  M  N  P  Q  R  S  T  V  W  Y
A  4  0 -2 -1 -2  0 -2 -1 -1 -1 -1 -2 -1 -1 -1  1  0  0 -3 -2
C  0  9 -3 -4 -2 -3 -3 -1 -3 -1 -1 -3 -3 -3 -3 -1 -1 -1 -2 -2
D -2 -3  6  2 -3 -1 -1 -3 -1 -4 -3  1 -1  0 -2  0 -1 -3 -4 -3
E -1 -4  2  5 -3 -2  0 -3  1 -3 -2  0 -1  2  0  0 -1 -2 -3 -2
F -2 -2 -3 -3  6 -3 -1  0 -3  0  0 -3 -4 -3 -3 -2 -2 -1  1  3
G  0 -3 -1 -2 -3  6 -2 -4 -2 -4 -3  0 -2 -2 -2  0 -2 -3 -2 -3
H -2 -3 -1  0 -1 -2  8 -3 -1 -3 -2  1 -2  0  0 -1 -2 -3 -2  2
I -1 -1 -3 -3  0 -4 -3  4 -3  2  1 -3 -3 -3 -3 -2 -1  3 -3 -1
K -1 -3 -1  1 -3 -2 -1 -3  5 -2 -1  0 -1  1  2  0 -1 -2 -3 -2
L -1 -1 -4 -3  0 -4 -3  2 -2  4  2 -3 -3 -2 -2 -2 -1  1 -2 -1
M -1 -1 -3 -2  0 -3 -2  1 -1  2  5 -2 -2  0 -1 -1 -1  1 -1 -1
N -2 -3  1  0 -3  0  1 -3  0 -3 -2  6 -2  0  0  1  0 -3 -4 -2
P -1 -3 -1 -1 -4 -2 -2 -3 -1 -3 -2 -2  7 -1 -2 -1 -1 -2 -4 -3
Q -1 -3  0  2 -3 -2  0 -3  1 -2  0  0 -1  5  1  0 -1 -2 -2 -1
R -1 -3 -2  0 -3 -2  0 -3  2 -2 -1  0 -2  1  5 -1 -1 -3 -3 -2
S  1 -1  0  0 -2  0 -1 -2  0 -2 -1  1 -1  0 -1  4  1 -2 -3 -2
T  0 -1 -1 -1 -2 -2 -2 -1 -1 -1 -1  0 -1 -1 -1  1  5  0 -2 -2
V  0 -1 -3 -2 -1 -3 -3  3 -2  1  1 -3 -2 -2 -3 -2  0  4 -3 -1
W -3 -2 -4 -3  1 -2 -2 -3 -3 -2 -1 -4 -4 -2 -3 -3 -2 -3 11  2
Y -2 -2 -3 -2  3 -3  2 -1 -2 -1 -1 -2 -3 -1 -2 -2 -2 -1  2  7'''

score_mat_lst = score_mat_str.split('\n')

first = True
for row in score_mat_lst:
    if first:
        first = False
        keys = row.split()
    else:
        r = row.split()
        left = r[0]
        for i, entry in enumerate(r[1:]):
            score[left,keys[i]] = int(entry)

# with open('data.txt', 'r') as data:
with open('rosalind_ba5e.txt', 'r') as data:
    s = data.readlines()

a, b = s[0].strip(), s[1].strip()
len_a, len_b = len(a), len(b)

pool = {}
pool[0, 0] = (0, (-1, -1))

for i in range(1, len_a+1):
    pool[i, 0] = (-sigma*i, (i-1, 0))

for i in range(1, len_b+1):
    pool[0, i] = (-sigma*i, (0, i-1))


for idx_a in tqdm(range(1, len_a+1)):
    for idx_b in range(1, len_b+1):
        candidates = []
        candidates.append((pool[idx_a-1, idx_b][0] - sigma, (idx_a-1, idx_b)))
        candidates.append((pool[idx_a, idx_b-1][0] - sigma, (idx_a, idx_b-1)))
        candidates.append((pool[idx_a-1, idx_b-1][0] + score[a[idx_a-1], b[idx_b-1]], (idx_a-1, idx_b-1)))                
        pool[idx_a, idx_b] = max(candidates, key=lambda x : x[0])



# def dp(idx_a, idx_b):
#     if idx_a > len_a or idx_b > len_b:
#         print('Error! String Index Out of Range!')
#         exit()
#     else:
#         if (idx_a, idx_b) in pool.keys():
#             return pool[idx_a, idx_b]
#         else:
#             if idx_a > 0 and idx_b == 0:
#                 pool[idx_a, idx_b] = (dp(idx_a-1, idx_b)[0] - sigma, (idx_a-1, idx_b))
#                 return pool[idx_a, idx_b]
#             elif idx_a == 0 and idx_b > 0:
#                 pool[idx_a, idx_b] = (dp(idx_a, idx_b-1)[0] - sigma, (idx_a, idx_b-1))
#                 return pool[idx_a, idx_b]       
#             else:
#                 candidates = []
#                 candidates.append((dp(idx_a-1, idx_b)[0] - sigma, (idx_a-1, idx_b)))
#                 candidates.append((dp(idx_a, idx_b-1)[0] - sigma, (idx_a, idx_b-1)))
#                 candidates.append((dp(idx_a-1, idx_b-1)[0] + score[a[idx_a-1], b[idx_b-1]], (idx_a-1, idx_b-1)))                
#                 pool[idx_a, idx_b] = max(candidates, key=lambda x : x[0])
#                 return pool[idx_a, idx_b]  

def backtrace():
    l_a, l_b = list(a), list(b)
    end = (len_a, len_b)
    act_a = []
    act_b = []

    now = end
    while True:
        pre = pool[now][1]
        if pre[0] < 0:
            break
        if pre[0] == now[0]:
            act_a.append('-')
        else:
            act_a.append(l_a.pop())
        if pre[1] == now[1]:
            act_b.append('-')
        else:
            act_b.append(l_b.pop()) 
        now = pre 

    return str(pool[end][0]), ''.join(reversed(act_a)), ''.join(reversed(act_b))     


# result = dp(len_a, len_b)
dist, act_a, act_b = backtrace()
# print(dist)
# print(act_a)
# print(act_b)

with open('result.txt', 'w') as result:
    result.writelines([dist, '\n', act_a, '\n', act_b])


print('Success!')
