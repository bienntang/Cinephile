# Cinephile - Chatbot AI Sederhana untuk Rekomendasi Film dan Diskusi Perfilman

**Cinephile** merupakan chatbot AI sederhana yang digunakan untuk merekomendasikan film dan berdiskusi mengenai dunia perfilman.

Penggunaan nama **Cinephile** berasal dari istilah *cinephile*, yaitu seseorang yang memiliki ketertarikan dan kecintaan terhadap dunia perfilman. Konsep chatbot ini mengangkat tema tersebut dengan menghadirkan AI yang dapat membantu pengguna mencari rekomendasi film, berdiskusi mengenai film, serta mendapatkan informasi dan fakta menarik tentang dunia perfilman.

Cinephile tidak hanya berfokus pada memberikan judul film sebagai rekomendasi, tetapi juga dirancang sebagai **asisten percakapan bertema film** yang dapat digunakan untuk mengeksplorasi berbagai hal dalam dunia perfilman sesuai dengan kebutuhan dan preferensi pengguna.

Cinephile berjalan sebagai aplikasi berbasis web menggunakan **Streamlit** dan memanfaatkan **Groq API** dengan model `openai/gpt-oss-120b`.

## Fitur Cinephile

- 🎬 Rekomendasi film berdasarkan genre, mood, dan preferensi pengguna
- 💬 Diskusi mengenai film dan dunia perfilman
- 🎲 `/surprise` atau `/random` untuk mendapatkan rekomendasi film secara acak
- 🎥 `/trivia` untuk mendapatkan fakta menarik seputar perfilman
- 📚 `/watchlist` untuk melihat film yang pernah direkomendasikan selama sesi
- 📊 `/stats` untuk melihat statistik percakapan
- 🧹 `/clear` untuk menghapus percakapan dan memulai obrolan baru
- 👋 `/exit` untuk mengakhiri sesi
- ❓ `/help` untuk melihat panduan penggunaan
- 💾 Penyimpanan riwayat obrolan secara lokal
- 🔑 BYOK (Bring Your Own Key) untuk melanjutkan percakapan menggunakan API key Groq milik pengguna setelah kuota gratis sesi habis
- ⚙️ Pengaturan `Temperature` dan `Max Tokens`


---


# Cara Penggunaan Cinephile

## Prasyarat

Sebelum menjalankan Cinephile, pastikan sudah tersedia:

- **Python 3.10 atau lebih baru**
- Akun **Groq** untuk mendapatkan API key

## Langkah 1 - Clone Repository

Clone repository kemudian masuk ke folder project.

```bash
git clone https://github.com/bienntang/ChatbotAI-Cinephile.git
cd Cinephile
```

## Langkah 2 - Membuat Virtual Environment
Virtual environment bersifat opsional, tetapi disarankan agar dependencies project terpisah dari environment Python lainnya.

### Windows
```
python -m venv cinephile
cinephile\Scripts\activate
```

### Linux / MacOS
```
python -m venv cinephile
source cinephile\bin\activate
```

## Langkah 3 - Install Dependencies
Unduh seluruh library yang dibutuhkan menggunakan file `requirements.txt`.
```bash
python -m pip install -r requirements.txt
```

## Langkah 3 - Mengatur API Key
1. Buat dan ambil API Key Groq melalui [console.groq.com/keys](https://console.groq.com/keys).
2. Salin file `.env.example` menjadi `.env`.
   **Windows**
   ```powershell
   Copy-Item .env.example .env
   ```

   **Linux / MacOS**
   ```bash
   cp .env.example .env
   ```

3. Buka file `.env`, kemudian masukkan API Key Groq:
   ```env
   GROQ_API_KEY=isi_api_key_milikmu_di_sini
   ```

**Jangan membagikan API key atau memasukkan file `.env` ke repository publik.**

## Langkah 5 - Menjalankan Aplikasi
Jalankan aplikadi menggunakan Streamlit:

```bash
streamlit run app.py
```

Setelah dijalankan, Streamlit akan membuka browser secara otomatis pada laman:

```text
http://localhost:8501
```

Jika browser tidak terbuka otomatis, buka alamat laman tersebut secara manual melalui browser.

---

# BYOK (Bring Your Own Key)

Cinephile menyediakan kuota AI gratis sebanyak **5 panggilan API dalam satu sesi obrolan**.

Kuota digunakan untuk fitur yang membutuhkan pemanggilan AI, yaitu:

* Chat biasa
* `/surprise`
* `/random`
* `/trivia`

Ketika kuota gratis telah habis, sidebar akan menampilkan kolom untuk memasukkan **API key Groq** milik pengguna.

Masukkan API key tersebut untuk melanjutkan percakapan menggunakan akun Groq milik sendiri.

> Penggunaan API key sendiri tetap mengikuti limit dan ketentuan akun Groq. BYOK tidak berarti penggunaan API menjadi tanpa batas.

API key yang dimasukkan melalui sidebar hanya digunakan selama sesi aplikasi dan **tidak disimpan ke dalam file riwayat obrolan**.

---

# Riwayat Obrolan

Cinephile menyediakan fitur untuk menyimpan riwayat percakapan secara lokal.

Jika toggle **Simpan riwayat obrolan** diaktifkan:

* Obrolan akan otomatis disimpan setelah percakapan berlangsung.
* Riwayat disimpan di dalam folder `chat_history`.
* Judul obrolan dibuat berdasarkan pesan pengguna.
* Percakapan sebelumnya dapat dibuka kembali dengan mengeklik judul obrolan pada sidebar.
* Riwayat obrolan dapat dihapus dengan mengeklik ikon sampah (🗑️).

Untuk memulai percakapan baru, pengguna dapat menggunakan salah satu cara berikut:

* Klik **Obrolan Baru** pada sidebar.
* Ketik command `/clear`.

Memulai obrolan baru **tidak akan menghapus riwayat percakapan sebelumnya**.

Jika tidak ingin menyimpan percakapan berikutnya, matikan toggle **Simpan riwayat obrolan** pada sidebar.

---

# Command

Cinephile menyediakan beberapa command untuk membantu pengguna berinteraksi dengan chatbot.

| Command      | Fungsi                                               |
| ------------ | ---------------------------------------------------- |
| `/help`      | Menampilkan panduan penggunaan Cinephile             |
| `/clear`     | Hapus percakapan dan mulai obrolan baru              |
| `/exit`      | Mengakhiri sesi obrolan                              |
| `/stats`     | Menampilkan statistik sesi                           |
| `/surprise`  | Mendapatkan rekomendasi film secara acak             |
| `/random`    | Alias dari `/surprise`                               |
| `/trivia`    | Mendapatkan fakta menarik tentang perfilman          |
| `/watchlist` | Melihat film yang pernah direkomendasikan dalam sesi |

Command `/help`, `/clear`, `/exit`, `/stats`, dan `/watchlist` diproses secara lokal sehingga **tidak menggunakan kuota API**.

Sementara itu, command `/surprise`, `/random`, dan `/trivia` membutuhkan pemanggilan AI sehingga akan menggunakan kuota API.

---

# Contoh Cuplikan Percakapan

Berikut merupakan contoh penggunaan Cinephile dalam percakapan.

> **Screenshot percakapan dapat ditambahkan pada bagian ini.**

### Contoh Input

```text
Aku pengen film yang bikin tegang tapi nggak terlalu banyak jumpscare.
```

Cinephile akan memberikan rekomendasi film berdasarkan preferensi yang diberikan dalam percakapan.

### Contoh Command

Pengguna juga dapat menggunakan command yang tersedia, misalnya:

```text
/surprise
```

atau:

```text
/trivia
```

Command `/surprise` akan meminta AI untuk memberikan rekomendasi film secara acak, sedangkan `/trivia` digunakan untuk mendapatkan fakta menarik mengenai dunia perfilman.

---

# Penjelasan Kode

## Struktur Project

Struktur utama project Cinephile adalah sebagai berikut:

```text
Cinephile/
│
├── chat_history/
│   └── *.json
│
├── cinephile/
│   └── Virtual environment
│
├── .env
├── .env.example
├── .gitignore
├── app.py
├── requirements.txt
└── README.md
```
## `app.py`

`app.py` merupakan file utama aplikasi Cinephile. File ini menangani berbagai komponen utama aplikasi, antara lain:

* Konfigurasi Streamlit
* System prompt chatbot
* Koneksi ke Groq API
* Pengelolaan percakapan
* Streaming respons AI
* Pemrosesan command chatbot
* Pengaturan sidebar
* Pengelolaan kuota API
* Fitur BYOK
* Penyimpanan dan pemuatan riwayat obrolan
* Watchlist film
* Statistik percakapan

## `chat_history/`

Folder `chat_history/` digunakan untuk menyimpan riwayat percakapan dalam format JSON.

Setiap percakapan disimpan dalam file tersendiri yang berisi informasi seperti:

* ID obrolan
* Judul obrolan
* Waktu dibuat
* Waktu terakhir diperbarui
* Jumlah penggunaan API
* Isi pesan dalam percakapan

Penyimpanan ini memungkinkan pengguna untuk membuka kembali percakapan yang telah dilakukan sebelumnya.

## `cinephile/`

Folder `cinephile/` merupakan **virtual environment Python** yang digunakan untuk mengisolasi dependencies Cinephile dari environment Python lainnya.

Virtual environment ini digunakan secara lokal dan **tidak perlu dimasukkan ke repository Git**.

## `.env`

File `.env` digunakan untuk menyimpan API key Groq secara lokal.

Contoh isi file:

```env
GROQ_API_KEY=isi_api_key_milikmu_di_sini
```

File `.env` tidak boleh dibagikan atau dimasukkan ke repository publik karena berisi informasi sensitif.

## `.env.example`

File `.env.example` merupakan template yang menunjukkan environment variable yang dibutuhkan oleh aplikasi.

Contoh:

```env
GROQ_API_KEY=
```

File ini dapat dimasukkan ke repository karena tidak berisi API key asli.

Pengguna dapat menyalin file tersebut menjadi `.env`, kemudian mengisi API key miliknya.

## `.gitignore`

File `.gitignore` digunakan untuk menentukan file dan folder yang tidak perlu dimasukkan ke repository Git.

Pada project Cinephile, beberapa file dan folder yang diabaikan adalah:

* `.env` untuk mencegah API key dan informasi sensitif ikut masuk ke repository.
* `__pycache__/` untuk mengabaikan file cache Python.
* `.cinephile/` untuk mengabaikan virtual environment atau file environment lokal yang digunakan selama pengembangan.
* `*.pyc` untuk mengabaikan file hasil kompilasi Python.
* `.DS_Store` untuk mengabaikan file metadata yang dibuat oleh macOS.
* `chat_history/` untuk mengabaikan file riwayat percakapan yang tersimpan secara lokal.

## `requirements.txt`

File `requirements.txt` berisi daftar dependencies Python yang dibutuhkan untuk menjalankan aplikasi Cinephile.

File ini digunakan untuk membantu proses instalasi seluruh library yang diperlukan oleh aplikasi.

## `README.md`

File `README.md` merupakan dokumentasi utama project Cinephile.

Dokumentasi ini berisi informasi mengenai:

* Deskripsi aplikasi
* Instalasi
* Cara menjalankan aplikasi
* Fitur
* Command
* BYOK
* Riwayat obrolan
* Struktur project
* Penggunaan Generative AI dalam pengembangan

---

# Penggunaan Generative AI dalam Pengembangan

Dalam proses pengembangan chatbot Cinephile, **Generative AI digunakan sebagai alat bantu** dalam beberapa tahap, yaitu **brainstorming, perancangan, pengembangan, dan dokumentasi**.

Pada tahap brainstorming dan perancangan, Generative AI digunakan untuk membantu mencari serta mengembangkan ide terkait fitur dan command yang dapat digunakan pada chatbot, seperti:

* `/help`
* `/clear`
* `/exit`
* `/stats`
* `/surprise`
* `/trivia`
* `/watchlist`

Generative AI juga digunakan sebagai bantuan dalam merancang dan mengembangkan tampilan **sidebar** pada aplikasi. Bantuan tersebut mencakup penyusunan komponen antarmuka serta pengaturan fitur yang ditampilkan pada sidebar.

Selain itu, Generative AI digunakan sebagai bantuan dalam menyusun dan memperbaiki dokumentasi `README.md` agar informasi mengenai aplikasi, fitur, command, struktur project, dan cara penggunaan dapat disampaikan dengan lebih terstruktur.

Hasil dari bantuan Generative AI kemudian **disesuaikan kembali dengan kebutuhan aplikasi, diperiksa, diuji, dan diimplementasikan** ke dalam kode sesuai dengan rancangan yang dibuat.