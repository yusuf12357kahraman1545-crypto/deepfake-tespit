import os, csv, cv2
import numpy as np

KOK = r'C:\veri\ff'
CIKIS = r'C:\veri\islenmis'
MODEL = r'C:\veri\face_detection_yunet_2023mar.onnx'
MARJ, BOYUT, KARE = 1.3, 224, 10
YOL = {'gercek': ('original_sequences', 'youtube', 'real'),
       'sahte': ('manipulated_sequences', 'Deepfakes', 'fake')}

detector = cv2.FaceDetectorYN.create(MODEL, "", (320, 320), 0.8, 0.3, 5000)
rows = list(csv.DictReader(open(r'C:\veri\ff_bolme.csv', encoding='utf-8')))

for j, r in enumerate(rows, 1):
    ana, alt, etiket = YOL[r['etiket']]
    ad = r['video']
    p23 = os.path.join(KOK, ana, alt, 'c23', 'videos', ad)
    p40 = os.path.join(KOK, ana, alt, 'c40', 'videos', ad)
    if not (os.path.exists(p23) and os.path.exists(p40)):
        print('EKSIK:', ad); continue
    cap23, cap40 = cv2.VideoCapture(p23), cv2.VideoCapture(p40)
    n = int(cap23.get(cv2.CAP_PROP_FRAME_COUNT))
    if n <= 0:
        cap23.release(); cap40.release(); continue
    hedef = set(np.linspace(0, n - 1, KARE, dtype=int).tolist())
    i, kayit = 0, 0
    while i <= max(hedef):
        ok1, f23 = cap23.read()
        ok2, f40 = cap40.read()
        if not (ok1 and ok2):
            break
        if i in hedef:
            h, w = f23.shape[:2]
            detector.setInputSize((w, h))
            _, faces = detector.detect(f23)
            if faces is not None and len(faces) > 0:
                x, y, fw, fh = max(faces, key=lambda f: f[14])[:4]
                cx, cy = x + fw / 2, y + fh / 2
                s = max(fw, fh) * MARJ
                x0, y0 = int(max(cx - s / 2, 0)), int(max(cy - s / 2, 0))
                x1, y1 = int(min(cx + s / 2, w)), int(min(cy + s / 2, h))
                a, b = f23[y0:y1, x0:x1], f40[y0:y1, x0:x1]
                if a.size > 0 and b.size > 0:
                    for comp, img in (('c23', a), ('c40', b)):
                        kl = os.path.join(CIKIS, r['split'], comp, etiket)
                        os.makedirs(kl, exist_ok=True)
                        cv2.imwrite(os.path.join(kl, f"{ad[:-4]}_{i:04d}.png"), cv2.resize(img, (BOYUT, BOYUT)))
                    kayit += 1
        i += 1
    cap23.release(); cap40.release()
    if kayit < KARE:
        print(f"UYARI: {ad} icin sadece {kayit} kare kaydedildi")
    if j % 20 == 0:
        print(f"{j}/{len(rows)} video islendi")
print("On isleme bitti!")
