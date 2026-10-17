# DevSecOps Pertemuan 5 — Manajemen Inventori Sederhana

## 1. Nama Aplikasi & Fungsinya
**Manajemen Inventori Sederhana** adalah aplikasi command-line berbasis Python
yang mendemonstrasikan pengelolaan stok barang: menambah barang, mengurangi
stok, memvalidasi input, dan menghasilkan ringkasan laporan (total nilai
inventori, barang dengan stok menipis, dsb).

## 2. Bahasa / Framework
- **Bahasa:** Python 3.11
- **Testing:** pytest + pytest-cov
- Tidak menggunakan framework web (murni Python standard library untuk logika
  inti), sehingga mudah dijalankan tanpa dependency berat.

## 3. Cara Menjalankan Aplikasi
```bash
# 1. Install dependency
pip install -r requirements.txt

# 2. Jalankan aplikasi (demo)
python -m app.main

# 3. Jalankan unit test
pytest --cov=app --cov-report=xml:coverage.xml
```

## 4. Overview Pipeline CI/CD
Pipeline didefinisikan di `.github/workflows/devsecops.yml` menggunakan GitHub
Actions, dengan 2 job terpisah yang berjalan di runner `ubuntu-latest`:

1. **`build`** — checkout kode, install dependency, menjalankan unit test
   (`pytest`) beserta coverage report.
2. **`sast-scan`** (bergantung pada `build` via `needs: build`) — menjalankan
   analisis SAST menggunakan **SonarCloud** (`SonarSource/sonarcloud-github-action`),
   lalu memeriksa **Quality Gate** (`SonarSource/sonarqube-quality-gate-action`)
   sebagai pipeline blocker otomatis — pipeline akan gagal jika kode tidak
   memenuhi standar kualitas/keamanan yang ditentukan SonarCloud (Sonar Way).

Workflow terpicu otomatis setiap ada **push ke branch `main`** dan setiap ada
**pull request ke branch `main`**.

### Konfigurasi terkait
- `sonar-project.properties` — konfigurasi project untuk analisis SonarCloud
  (project key, organization, path source & test).
- GitHub Secrets yang dibutuhkan: `SONAR_TOKEN` (token dari SonarCloud,
  disimpan di Settings → Secrets and variables → Actions).
