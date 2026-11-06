import os, re, collections
kok = r'C:\veri\Celeb-DF-v2'
liste = []
for satir in open(os.path.join(kok, 'List_of_testing_videos.txt')):
    p = satir.split()
    if len(p) == 2:
        liste.append((p[0], p[1]))
test = set(y for e, y in liste)
print('etiket x klasor:', dict(collections.Counter((e, y.split('/')[0]) for e, y in liste)))
tum = []
for k in ['Celeb-real', 'Celeb-synthesis', 'YouTube-real']:
    for f in os.listdir(os.path.join(kok, k)):
        tum.append(k + '/' + f)
print('toplam', len(tum), '| test listesi', len(test), '| listede olup diskte olmayan', len(test - set(tum)))
def kimlik(y):
    return set(re.findall(r'id\d+', y.split('/')[1]))
tk, ek = set(), set()
for y in tum:
    (tk if y in test else ek).update(kimlik(y))
print('test kimlik', len(tk), '| egitim kimlik', len(ek), '| ORTAK kimlik', len(tk & ek))
print('kimligi okunamayan dosya (YouTube)', sum(1 for y in tum if not kimlik(y)))
