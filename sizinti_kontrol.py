import csv, collections
rows = list(csv.DictReader(open(r'C:\veri\ff_bolme.csv', encoding='utf-8')))
grup_split = collections.defaultdict(set)
kimlik_grup = collections.defaultdict(set)
for r in rows:
    grup_split[r['grup']].add(r['split'])
    for kid in r['video'].replace('.mp4', '').split('_'):
        kimlik_grup[kid].add(r['grup'])
print('satir:', len(rows), '| grup:', len(grup_split))
print("birden fazla split'te olan grup:", sum(len(s) > 1 for s in grup_split.values()))
print('birden fazla grupta gecen kimlik:', sum(len(g) > 1 for g in kimlik_grup.values()))
print('split dagilimi (grup):', collections.Counter(next(iter(s)) for s in grup_split.values()))
