# DOCTRINA — Batch Pilot P003–P009: Seven Published Doctoral Dissertations

**Tanggal:** 25 November 2026  
**Ruang lingkup:** 7 disertasi tambahan, di luar P002 Gutierrez (2021); objek pemeriksaan selalu **norma/konsep hukum**, bukan teori secara keseluruhan.  
**Jenis evaluasi:** telaah terbatas pada kutipan dan bagian yang dapat dibaca melalui teks PDF terbuka, dilanjutkan *auditor-proposed argument-graph testing* pada DOCTRINA v0.4.  
**Bukan:** evaluasi menyeluruh disertasi, pemeriksaan orisinalitas, pembacaan forensik seluruh halaman, audit doktrinal lengkap, atau putusan mengenai ketepatan akademik tesis penulis.

## I. Protokol, metodologi, dan batas ketertelusuran

1. Identifikasi disertasi doktoral nyata dari repositori universitas; pilih bagian yang **berobjek norma atau konsep**. Meskipun disertasi tertentu menggunakan teori atau menggabungkan metode sosio-legal, pengujian tidak menempatkan teori sebagai objek.
2. Baca abstrak serta bagian argumentatif tersedia dari teks PDF yang terindeks secara publik. Catat judul, penulis, tahun, tautan sumber asli, batas bagian yang diakses, konteks waktu/jurisdiksi.
3. Simpan **kutipan mikro** dalam `examples/dissertation_batch_003_009.json` (7–15 kata per disertasi; kurang dari 25 kata per sumber). Jangan publikasikan seluruh PDF atau paragraf panjang.
4. Rekonstruksi **tiga proposisi sebagai hipotesis auditor** (P1, P2, C1), satu keberatan serius dan satu pembelaan terkuat. Semuanya berstatus `ai_proposed`; tidak pernah disamakan dengan pendapat yang telah dikonfirmasi penulis.
5. Uji menggunakan `tests/test_pilot_batch_003_009.py` dan `scripts/run_dissertation_batch.py`: pembatasan objek, kesesuaian frase dengan **berkas kutipan mikro**, relasi graf, kemungkinan premis normatif, perbedaan atribusi, posisi keberatan, status bukti, ketergantungan bab, serta penguncian novelty.
6. Audit substantif **terpisah** mempertimbangkan keberatan dan jawaban paling masuk akal, tanpa menggunakan keluaran otomatis sebagai bukti adanya kesalahan akademik.

**Keterbatasan sumber terbesar:** PDF asli dapat dibaca lewat teks hasil ekstraksi alat web, tetapi **tidak diunduh dan di-hash di runner Python**. Screenshot PDF dari alat web dicoba, tetapi akses gambar halaman gagal pada host yang diperiksa. Oleh karena itu kode `anchor_text` hanya membuktikan kesesuaian terhadap **cuplikan yang telah dipilih auditor**, bukan keterikatan otomatis ke berkas PDF resmi, halaman cetak atau keseluruhan konteks. Semua `inspection_status` = `partial`. Tidak ada reviewer doktoral independen dalam audit ini.

## II. Tujuh disertasi dan temuan utama

| ID | Disertasi | Objek yang benar-benar diuji | Kedalaman | Tantangan terbaik untuk DOCTRINA |
|---|---|---|---|---|
| P003 | T. Liau, *Standing in Private Law* (Oxford, 2020) | KONSEP *standing* dan kaitannya dengan hak | Pendahuluan, Bab 2 dan bahasan pengecualian | Beda antara pembedaan konseptual dan keberlakuan kaidah umum |
| P004 | Laura J. Downey, *Emerging Legal Concepts ... Identity* (Edinburgh, 2017) | KONSEP identitas sebagai konsep hukum yang sedang muncul | Abstrak, Bab 5/6 | Jangan mengira deskripsi konsep berkembang sebagai tuntutan reformasi |
| P005 | Catriona A. W. McMillan, *The Human Embryo in Vitro* (Edinburgh, 2018) | KONSEP status embrio dan ketidakcocokan kategorinya | Abstrak, Bab 4 dan pembahasan berikut | Kritik *legal stasis* tidak otomatis merupakan klaim ketidakabsahan aturan |
| P006 | Sjur K. Dyrkolbotn, *On the Legitimacy of Economic Development Takings* (Durham, 2016) | NORMA/kriteria *public interest* dan ekspropriasi | Abstrak, Bab 1 hlm. 29–30 | Legitimasi normatif berbeda dari validitas hukum lintas-negara |
| P007 | David Frydrych, *The Architecture of Rights* (Oxford, 2015) | KONSEP hak, daya penegakan, hak tidak sempurna | Abstrak, Bab 6–8 terpilih | Contoh batas *imperfect right* bukan otomatis kontradiksi konsep hak |
| P008 | Carmine Conte, *Penalties Reworked* (Oxford, 2014) | NORMA aturan klausul penalti kontrak | Abstrak, Bab 1 dan pembahasan hasil | Harus mempertahankan konteks hukum 2014 ketika dibanding putusan 2015 |
| P009 | Gehan Gunatilleke, *Justifying Limitations ... under the ICCPR* (Oxford, 2020) | NORMA pembatasan kebebasan dalam Pasal 18(3)/19(3) ICCPR | Abstrak, Bab 2 hlm. 76–80 | Bedakan penghubung normatif yang **ada** dari kualitas pembenarannya |

### P003 — *Standing* bukan otomatis *claim-right*

**Sumber:** T. Liau, *Standing in Private Law*, Oxford DPhil 2020; pendahuluan hlm. cetak 5–7, Bab 2, pembahasan pengecualian dalam hukum *tort*. [Rekaman resmi dan PDF](https://ora.ox.ac.uk/objects/uuid:f2acd5c9-7173-43a3-bd86-3b1019409d1b).

**Rekonstruksi sementara:** penulis membedakan kedudukan menggugat (sebagai kekuasaan menuntut) dari hak substantif; lalu berpendapat suatu kaidah umum memungkinkan pemegang hak primer menuntut pemenuhannya. Bagian berikut juga menyebut pengecualian.

**Kritik terbatas:** pembedaan *standing* dan *right* sebagai dua kategori tidak, tanpa premis doktrinal tambahan, membuktikan kaidah **eksklusivitas pemegang hak** pada semua cabang hukum privat.

**Pembelaan terkuat:** penulis justru memisahkan argumen konseptual dan pemeriksaan doktrinal, serta membahas pengecualian. DOCTRINA harus memeriksa argumentasi pelengkap tersebut sebelum memberi label lompatan inferensi.

**Kebutuhan pengembangan:** *concept → doctrine transition examiner*, pemeriksaan pengecualian dan aturan generalisasi.

### P004 — Identitas sebagai konsep hukum yang *sedang muncul*

**Sumber:** Laura J. Downey, *Emerging Legal Concepts at the Nexus of Law, Technology and Society: A Case Study in Identity*, Edinburgh PhD 2017; abstrak dan sekitar Bab 5, PDF dekat halaman 124; penerapan dalam Bab 6. [Teks PDF resmi](https://era.ed.ac.uk/bitstream/handle/1842/25946/Downey2017.pdf?isAllowed=y&sequence=1).

**Rekonstruksi sementara:** identitas dipakai dengan makna majemuk dan semakin penting dalam pembicaraan tentang perkembangan teknologi reproduksi dan regulasinya. Konsep dapat *berpotensi* muncul secara hukum sekalipun belum ada pengakuan resmi yang tegas.

**Kritik terbatas:** bagaimana membuktikan tingkat kemunculan **secara yuridis**, bukan hanya frekuensi pemakaian dalam diskursus publik? Parameter sebaiknya meliputi penggunaan di putusan, instrumen hukum, aktor hukum dan batas pengakuan.

**Pembelaan terkuat:** penulis secara eksplisit tidak menjadikan tuntutan intervensi normatif sebagai tujuan utama, dan telah membangun kerangka faktor kemunculan konsep. Jika DOCTRINA menyimpulkan bahwa disertasi gagal karena tidak menawarkan reformasi aturan, itu **false positive metodologis**.

**Kebutuhan pengembangan:** *non-prescriptive conceptual research protection*; pemisahan klaim deskriptif konseptual dari rekomendasi normatif.

### P005 — Embrio sebagai entitas prosesual dalam *legal stasis*

**Sumber:** Catriona A. W. McMillan, *The Human Embryo in Vitro: A Processual Entity in Legal Stasis*, Edinburgh PhD 2018; abstrak, Bab 4 hlm. cetak 148–149, dan bahasan lanjut mengenai status hukum embrio. [Teks PDF resmi](https://era.ed.ac.uk/server/api/core/bitstreams/2e0c8ff5-f9a8-4939-bf8e-4e79ac078f07/content).

**Rekonstruksi sementara:** kategorisasi embrio dalam rezim Human Fertilisation and Embryology Act 1990 (beserta perubahan) dikritik karena sifat embrio sebagai proses tidak mudah dipadatkan dalam satu kategori statis. Penulis mendiagnosis *legal gap* dan mempertimbangkan kemungkinan pembingkaian konseptual yang lebih tepat.

**Kritik terbatas:** adanya perbedaan antara ontologi biologis dan kategori hukum tidak dengan sendirinya menjadikan kategori tersebut tidak sah. Hukum dapat memakai fiksi atau garis batas institusional secara sah jika tujuan dan konsekuensinya dijustifikasi.

**Pembelaan terkuat:** penulis tidak mengatakan peraturan harus mereproduksi semua perubahan biologis; ia juga membedakan kemungkinan perbaikan dari kewajiban reformasi tunggal. Audit yang menyamakan kritik ini dengan kewajiban membuat norma baru akan mengubah maksud tesis.

**Kebutuhan pengembangan:** pemisahan *descriptive mismatch*, *conceptual critique*, dan *prescriptive conclusion* serta pembacaan kalimat berkualifikasi.

### P006 — Pengambilalihan tanah untuk pembangunan ekonomi

**Sumber:** Sjur Kristoffer Dyrkolbotn, *On the Legitimacy of Economic Development Takings*, Durham PhD 2016; khususnya Bab 1, hlm. cetak 29–30, dan abstrak. [PDF dan metadata Durham](https://etheses.dur.ac.uk/11559/).

**Rekonstruksi sementara:** berbagai sistem hukum memakai istilah *public use*, *public purpose* dan *public interest* dengan relasi yang tidak selalu sama. Penulis mengusulkan bahwa selain manfaat publik, legitimasi pengambilalihan seharusnya memperhatikan pengambilan keputusan yang adil serta partisipasi pihak yang terdampak.

**Kritik terbatas:** agar dapat dipakai sebagai kriteria **validitas positif**, standar partisipasi memerlukan dasar hukum yang berbeda pada tiap yurisdiksi. Akan salah jika norma legitimasi yang dipertahankan penulis otomatis ditampilkan sebagai bunyi undang-undang yang berlaku di semua negara.

**Pembelaan terkuat:** penulis secara eksplisit mengingatkan bahwa istilah-istilah tersebut terikat konteks masing-masing yurisdiksi dan mengajukan partisipasi sebagai **argumen legitimasi normatif**. DOCTRINA tidak berhak menyamakan perbedaan normatif-yuridis dengan kekeliruan.

**Kebutuhan pengembangan:** *validity/legitimacy separation*, *jurisdiction-aware interpretive scope*, dan jembatan norma–konsep.

### P007 — Hak yang tidak sepenuhnya dapat dipaksakan

**Sumber:** David Frydrych, *The Architecture of Rights*, Oxford DPhil 2015; abstrak serta Bab 6–8 mengenai penegakan, invokasi, dan hak yang tidak sempurna. [Teks PDF Oxford](https://ora.ox.ac.uk/objects/uuid:8a0f3763-e786-42d6-bd62-b9eee7ad36c7/files/m1068f2591c1de8c3279d4ff2dc0eef51).

**Rekonstruksi sementara:** hak tidak identik dengan satu bentuk kekuasaan hukum untuk memaksakan pelaksanaannya. Tesis mempertimbangkan hak yang tidak dapat ditegakkan sebagai kasus kurang sempurna, serta mekanisme klaim melalui kebebasan hukum, di luar tindakan memaksa pengadilan.

**Kritik terbatas:** jika penegakan tidak merupakan kondisi yang selalu diperlukan, kriteria pembatas tetap harus ditetapkan agar konsep hak tidak mencakup setiap harapan atau klaim moral tanpa status yuridis yang jelas.

**Pembelaan terkuat:** naskah membicarakan jenis hak yang tidak sempurna dan cara invokasi hak; perbedaan antara kasus utama dan kasus batas tidak otomatis merupakan kontradiksi.

**Kebutuhan pengembangan:** *concept boundary / central case / imperfect instance* review tanpa mengubah penelitian konsep hak menjadi pengujian kebenaran seluruh teori filsafat hak.

### P008 — Peraturan klausul penalti dalam hukum kontrak

**Sumber:** Carmine Conte, *Penalties Reworked: The Rule Against Penalties Restated, Justified and Refined*, Oxford DPhil 2014; abstrak dan Bab 1, serta uraian mengenai akibat klausul penalti. [Teks PDF Oxford](https://ora.ox.ac.uk/objects/uuid:4bdd452a-08cf-42cd-a1eb-8b3be516c4f5/files/m30446e13be8e7ecb15fbed291e57a701).

**Rekonstruksi sementara:** penulis berupaya merumuskan ulang doktrin penalti kontraktual dengan menekankan beban berlebihan relatif pada fungsi sah klausul, termasuk tesis mengenai akibat ketidakberlakuan yang sebagian.

**Kritik terbatas:** analisis interpretatif harus diuji dengan bahan hukum **yang tersedia pada 2014**. Putusan UK Supreme Court *Cavendish/ParkingEye* [2015] UKSC 67 penting ketika mencari relevansi sekarang, tetapi bukan bahan yang pantas diwajibkan hadir di disertasi tahun sebelumnya. [Sumber putusan kemudian, 4 November 2015](https://www.bailii.org/uk/cases/UKSC/2015/67.html).

**Pembelaan terkuat:** naskah sendiri menjelaskan pemilihan hukum Inggris dan Australia, fase pemeriksaan putusan, serta perbedaan antara perumusan ulang, justifikasi dan penghalusan kaidah. Kode yang mengabaikan waktu bisa salah menilai disertasi hanya karena hukum berkembang setelah kelulusannya.

**Kebutuhan pengembangan:** model versi hukum dan pemisahan *historical assessment* dari *present-law applicability*.

### P009 — Pembatasan dua kebebasan menurut ICCPR

**Sumber:** Gehan Gunatilleke, *Justifying Limitations on the Freedom to Manifest Religion or Belief and the Freedom of Expression under the ICCPR*, Oxford DPhil 2020; abstrak dan Bab 2, terutama hlm. cetak 76–80. [PDF Oxford](https://ora.ox.ac.uk/objects/uuid:95bc481e-8175-44f2-9498-7fc8b5958883/download_file?safe_filename=Gehan_Gunatilleke_DPhil_Thesis.pdf&type_of_work=Thesis).

**Rekonstruksi sementara:** penulis menguji pembenaran pembatasan kebebasan menurut ICCPR Pasal 18(3) dan 19(3), serta membela pendekatan yang mensyaratkan alasan publik dan dasar kewajiban keadilan bagi individu yang dibatasi.

**Kritik terbatas:** perlu dijelaskan kapan suatu pendekatan kewajiban merupakan interpretasi yang dapat ditampung dalam objek dan tujuan ICCPR, dan kapan ia menjadi **standar normatif tambahan** yang tidak disebutkan secara eksplisit oleh naskah perjanjian. Perbedaan ini tidak dapat diselesaikan oleh pemeriksaan kata kunci atau nilai Boolean `normative_bridge`.

**Pembelaan terkuat:** penulis secara eksplisit mengembangkan alasan konseptual, normatif dan politis, serta memeriksa sejarah penyusunan dan praktik komite HAM. Tuduhan `IA-06` yang menyatakan tidak ada alasan normatif hanya karena anotator lupa mencatat premis akan menjadi diagnosis keliru.

**Kebutuhan pengembangan:** kualitas alasan jembatan normatif, bukan sekadar keberadaannya; pemisahan tekstual ICCPR dari argumentasi normatif peneliti.

## III. Hasil eksekusi DOCTRINA v0.4

**Reproduksi:** `examples/dissertation_batch_003_009.json`; `tests/test_pilot_batch_003_009.py`; `scripts/run_dissertation_batch.py`. Semua berada dalam [repository DOCTRINA](https://github.com/AzrielChoerulHakim/DOCTRINA_dissertation-legal-norcon). Pengujian dijalankan pada GitHub Actions.

| Indikator | Hasil teramati | Interpretasi yang sah |
|---|---:|---|
| Sumber disertasi berbeda | 7 | Korporasi data pilot baru dengan 4 KONSEP + 3 NORMA |
| Unit test keseluruhan | 55/55 lulus | Perilaku kode atas fixture yang tersedia memenuhi ekspektasi |
| Tes baru batch ini | 13/13 lulus | Ketujuh objek diterima dan kontrol negatif berhasil |
| Kasus dengan kritik yang terbukti secara substantif oleh mesin | **0** | Mesin tidak menghasilkan putusan akademik atas teks penuh |
| Kasus dengan keluaran `STRUCTURAL_REVIEW_WITH_LIMITATIONS` | 7/7 | Semua memiliki keterbatasan sumber atau keberatan terbuka |
| Kasus dengan `OPEN_SERIOUS_OBJECTION` | 7/7 | Keberatan direkam sebagai usulan, bukan disimpulkan salah |
| Kasus norma dengan sumber bertanda belum diperiksa penuh | 3/3 | Menjaga kehati-hatian terhadap teks hukum |
| Kasus dengan keputusan novelty prematur | 0 | Final originality tetap terkunci |
| Teks PDF asli yang diverifikasi secara hash dalam runtime | **0/7** | Kegagalan infrastruktur sumber yang harus diperbaiki |
| Rekonstruksi yang disetujui penulis asli | **0/7** | Tidak ada dasar klaim kesetiaan semantik final |
| Penilai akademik independen | **0** | Precision, recall dan false-positive rate substantif **belum dapat dihitung** |

**Hasil 0 *critical machine findings* tidak membuktikan ketujuh disertasi bebas kesalahan.** Graf hanya menguji struktur argumen yang sudah dipilih dan direkonstruksi oleh auditor. Bila premis normatif pada P009 dihilangkan secara sengaja dalam kontrol negatif, `IA-06` muncul sekalipun naskah asli memuat pembenaran normatif. Ini menunjukkan risiko penting: **ketepatan masukan dan atribusi sama mendasarnya dengan pemeriksaan logika.**

## IV. Taksonomi kegagalan yang ditemukan

| Kode risiko yang diusulkan | Kasus pemicu | Pola risiko | Mekanisme koreksi |
|---|---|---|---|
| R-01 SOURCE ANCHOR GAP | Semua | Teks mikro buatan auditor sama dengan dirinya sendiri, tetapi belum dibandingkan byte-per-byte dengan PDF asli | Verifikasi otomatis halaman, kutipan, hash berkas dan keterbatasan ekstraksi |
| R-02 RECONSTRUCTION LEAKAGE | P009 | Hilangnya premis saat anotasi dapat menciptakan `IA-06` palsu | Dua tahap rekonstruksi + approval peneliti + pengujian pembelaan terkuat |
| R-03 OVERPRESCRIPTION | P004, P005 | Kritik/deskripsi konsep dipaksa menjadi rekomendasi reformasi | Klasifikasi *critical/descriptive/conditional* dan larangan wajib preskripsi |
| R-04 LEGITIMACY/VALIDITY COLLAPSE | P006 | Standar legitimasi diperlakukan sebagai hukum positif otomatis | Pembatas yurisdiksi dan pemeriksaan sumber kaidah |
| R-05 CONCEPT/DOCTRINE TRANSITION | P003, P007 | Pembedaan konseptual langsung diubah menjadi generalisasi doktrinal | Uji langkah interpretatif dan pengecualian |
| R-06 TIME-TRAVEL ERROR | P008 | Putusan setelah disertasi dipakai untuk menilai argumen historis | Mesin waktu dan status berlaku pada tanggal penelitian |
| R-07 BRIDGE BOOLEAN FALLACY | P006, P009 | `normative_bridge=true` dianggap membuktikan kualitas alasan | Review kecukupan inferensi, bukti dan sanggahan |
| R-08 SYNTHETIC-CHAPTER BIAS | Semua | ID CH1/CH2 dalam fixture disalahpahami sebagai label bab penulis | Hubungkan graf langsung dengan heading asli, bukan placeholder |
| R-09 NOVELTY PREMATURE | Semua | Sistem menginferensi orisinalitas dari keunikan redaksi | Pertahankan pengunci tiga kategori sampai final dissertation gate |

## V. Keputusan metodologis setelah batch

1. **Tidak ada dasar untuk mengklaim peningkatan akurasi akademik sebesar angka tertentu.** Pilot teknis belum mempunyai standar pembanding ahli.
2. **Fondasi norm/concept dan pengunci novelty sudah berfungsi** pada data berstruktur, sehingga prioritas baru bukan membuat kategori novelty tambahan.
3. **Kelemahan terbesar adalah original-source grounding**: pemeriksaan terhadap sumber penuh, status normatif dan konteks pernyataan belum ditutup secara teknis.
4. **Kelemahan kedua adalah fidelity**: setiap kesimpulan AI harus dapat ditelusuri ke teks asli dan mendapat kesempatan untuk dibantah sebagai salah rekonstruksi.
5. **Mesin argumentasi semantik** baru boleh dinilai setelah dua kelemahan di atas diatasi; selama ini ia hanya pemeriksa graf dan protokol evaluasi manusia.
6. **Audit novelty normative / interpretative / conceptual tetap terakhir**. Tidak ada audit orisinalitas ketujuh disertasi pada batch ini.

## VI. Integritas dan hak akses

Tidak ada naskah disertasi publik yang direproduksi penuh ke GitHub. Cuplikan frase singkat disimpan semata untuk fixture pengujian. Kutipan dalam pengujian tidak boleh ditafsirkan sebagai verifikasi otomatis sumber primer atau pengganti pembacaan penuh. Semua temuan terhadap penulis asli diberi status *review question* dan selalu disertai *strongest plausible reply*.

**Rencana aksi setelah evaluasi** tersedia di `docs/RFC-010-POST-BATCH-DEVELOPMENT-PLAN.md`.
