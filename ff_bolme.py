import os, csv, random, collections
kok = r'C:\veri\ff'
sahte_klasor = os.path.join(kok, r'manipulated_sequences\Deepfakes\c23\videos')
gruplar = collections.defaultdict(list)
for f in os.listdir(sahte_klasor):
    a, b = f.split('.')[0].split('_')
    gruplar[tuple(sorted((a, b)))].append(f)
anahtar = sorted(gruplar)
random.Random(42).shuffle(anahtar)
n = len(anahtar)
n_tr, n_va = round(n * 0.70), round(n * 0.15)
satirlar = []
for i, g in enumerate(anahtar):
    s = 'train' if i < n_tr else ('val' if i < n_tr + n_va else 'test')
    for kimlik in g:
        satirlar.append((s, g[0] + '_' + g[1], 'gercek', kimlik + '.mp4'))
    for f in gruplar[g]:
        satirlar.append((s, g[0] + '_' + g[1], 'sahte', f))
with open(r'C:\veri\ff_bolme.csv', 'w', newline='') as dosya:
    w = csv.writer(dosya)
    w.writerow(['split', 'grup', 'etiket', 'video'])
    w.writerows(satirlar)
print('grup sayisi', n, '| 2 sahte olmayan grup', sum(1 for g in gruplar if len(gruplar[g]) != 2))
print(dict(collections.Counter((s, e) for s, _, e, _ in satirlar)))
