import os

kok = r'C:\veri\ff'
orig_c23 = set(os.listdir(os.path.join(kok, r'original_sequences\youtube\c23\videos')))
orig_c40 = set(os.listdir(os.path.join(kok, r'original_sequences\youtube\c40\videos')))
df_c23 = set(os.listdir(os.path.join(kok, r'manipulated_sequences\Deepfakes\c23\videos')))
df_c40 = set(os.listdir(os.path.join(kok, r'manipulated_sequences\Deepfakes\c40\videos')))

print('c23 == c40 (original):', orig_c23 == orig_c40)
print('c23 == c40 (Deepfakes):', df_c23 == df_c40)

orig_ids = {f.split('.')[0] for f in orig_c23}
df_pairs = [tuple(f.split('.')[0].split('_')) for f in df_c23]
df_ids = {i for p in df_pairs for i in p}

print('Original kimlik sayisi:', len(orig_ids))
print('Deepfakes icindeki kimlik sayisi:', len(df_ids))
print('Original ve Deepfakes kimlikleri birebir ayni mi?:', orig_ids == df_ids)

# Bagli bilesen (grup) sayisi
adj = {i: set() for i in orig_ids | df_ids}
for a, b in df_pairs:
    adj[a].add(b)
    adj[b].add(a)

visited = set()
gruplar = []
for i in adj:
    if i not in visited:
        comp = []
        q = [i]
        visited.add(i)
        while q:
            curr = q.pop()
            comp.append(curr)
            for nxt in adj[curr]:
                if nxt not in visited:
                    visited.add(nxt)
                    q.append(nxt)
        gruplar.append(comp)

print('Toplam bagimsiz grup sayisi:', len(gruplar))
print('Grup boyut dagilimi (kac kimlik var):', {k: sum(1 for g in gruplar if len(g)==k) for k in set(len(g) for g in gruplar)})
