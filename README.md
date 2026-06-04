# Med Sea temperature – automatikus napi letöltés

Ez a repo minden nap automatikusan letölti a Földközi-tenger felszíni
hőmérséklet (`thetao`) napi átlagát a Copernicus Marine szolgáltatásból,
és a `data/` mappába commitolja `med_sst_ÉÉÉÉ-HH-NN.nc` néven. Ezután a
nyers adatból egy színes térkép-PNG is készül a `maps/` mappába
(`med_sst_ÉÉÉÉ-HH-NN.png`).

A futtatás **GitHub Actions**-ön történik (nem a saját gépeden), naponta egyszer.

## Adat

- **Dataset:** `cmems_mod_med_phy-tem_anfc_4.2km_P1D-m`
- **Változó:** `thetao` (tengervíz-hőmérséklet)
- **Terület:** teljes Mediterráneum (lon −17.29…36.29, lat 30.19…45.98)
- **Mélység:** ~1.02 m (felszín)
- **Időbeli felbontás:** napi átlag, mindig az aktuális (UTC) nap

## Egyszeri beállítás

### 1. Copernicus fiók titkok megadása

A GitHub repo **Settings → Secrets and variables → Actions → New repository secret**
alatt vedd fel a Copernicus Marine bejelentkezési adataidat:

| Secret neve | Érték |
|-------------|-------|
| `CM_USER`   | a Copernicus Marine felhasználóneved |
| `CM_PASS`   | a Copernicus Marine jelszavad |

Regisztráció: https://data.marine.copernicus.eu/register

### 2. Írási jog a workflow-nak

A **Settings → Actions → General → Workflow permissions** alatt legyen
bekapcsolva a **„Read and write permissions"** (hogy a futtató vissza tudjon
commitolni). A workflow `permissions: contents: write` sora ezt használja.

Ezután semmi teendő – a workflow magától fut naponta.

## Ütemezés

Naponta **13:00 UTC**-kor fut.

> ⚠️ **Nyári/téli időszámítás:** a GitHub cron mindig UTC-ben jár, nincs
> időzóna-támogatás. 13:00 UTC = **14:00 CET** (télen) és **15:00 CEST**
> (nyáron). Ha pontosan 15:00 helyi időt akarsz egész évben, az nem
> oldható meg egyetlen cron-nal; lásd lent.

### Kézi indítás / korábbi nap letöltése

A **Actions → Download Med Sea temperature → Run workflow** gombbal kézzel is
indítható. Megadható egy konkrét nap (`YYYY-MM-DD`); üresen hagyva a mai napot
tölti.

## Hasznos tudni

- **Repo mérete:** minden nap ~1–3 MB-os NetCDF fájl keletkezik, így évente
  nagyjából 0.5–1 GB-tal nő a repo. Ha hosszú távon ez sok lenne, válts
  artifact-ra vagy GitHub Releases-re, illetve Git LFS-re.
- **Hiányzó nap:** ha egy adott napra még nem publikus az adat, a futás
  hibával leáll (ez látszik az Actions fülön). Újrafuttatható később kézzel.
