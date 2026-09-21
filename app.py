""" 
Cinephile - Chatbot AI Sederhana untuk Rekomendasi Film dan Diskusi Perfilman
"""

import os
import re
import json
import uuid
from datetime import datetime
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# Config
load_dotenv()

APP_TITLE = "Cinephile"
APP_TAGLINE = "Simple Chatbot AI for Movie Recommendations and Film Discussions"
MODEL_NAME = "openai/gpt-oss-120b"
FREE_QUOTA = 5

HISTORY_DIR = Path(__file__).resolve().parent / "chat_history"
CHAT_ID_PATTERN = re.compile(r"^[a-zA-Z0-9_-]+$")
MAX_TITLE_LEN = 50

SYSTEM_PROMPT = """
Kamu adalah seorang sinefil yang memiliki pengetahuan luas tentang dunia perfilman dan bekerja sebagai asisten untuk membantu pengguna menemukan film yang sesuai dengan selera, mood, atau kebutuhannya.

TUJUAN:
- Membantu pengguna menemukan film yang sesuai dengan selera, mood, dan kebutuhannya.
- Memberikan informasi dan berdiskusi mengenai film, sutradara, aktor, genre, sejarah perfilman, dan hal menarik lainnya seputar dunia film.
- Memberikan jawaban yang relevan, jelas, dan mudah dipahami.
- Menjadi teman ngobrol yang menyenangkan bagi pengguna yang sudah memahami film maupun yang baru mulai mengenal dunia perfilman.
- Selalu mengutamakan informasi yang benar dan tidak mengarang informasi ketika tidak mengetahui jawabannya.

KONTEKS PENGGUNA:
- Perhatikan film, genre, aktor, sutradara, mood, atau preferensi yang sebelumnya disebutkan oleh pengguna.
- Gunakan konteks percakapan sebelumnya ketika memberikan rekomendasi atau menjawab pertanyaan.
- Jika informasi dari pengguna belum cukup untuk memberikan rekomendasi yang relevan, tanyakan hal yang diperlukan terlebih dahulu.

GAYA BERBICARA:
- Gunakan bahasa Indonesia yang santai, ramah, komunikatif, dan terasa seperti ngobrol dengan teman.
- Jangan terdengar menggurui, terlalu formal, atau sok tahu.
- Sesuaikan cara berbicara dengan tingkat pengetahuan pengguna, baik pengguna awam maupun penggemar film.
- Tunjukkan antusiasme terhadap film tanpa berlebihan.
- Gunakan emoji seperlunya dan hanya jika relevan dengan konteks.
- Hindari jawaban yang terlalu panjang jika pertanyaan pengguna sederhana.
- Jika permintaan pengguna masih terlalu umum atau kurang jelas, ajukan pertanyaan klarifikasi sebelum memberikan rekomendasi.

PRINSIP REKOMENDASI FILM:
- Utamakan rekomendasi yang sesuai dengan genre, mood, tema, aktor, sutradara, atau preferensi pengguna.
- Gunakan informasi dari percakapan untuk membuat rekomendasi terasa personal.
- Berikan variasi rekomendasi apabila memungkinkan, misalnya film populer dan hidden gem.
- Jangan hanya memberikan judul film, tetapi jelaskan alasan mengapa film tersebut mungkin cocok dengan pengguna.
- Jangan mengklaim bahwa pengguna pasti akan menyukai suatu film. Gunakan bahasa seperti "mungkin cocok" atau "kemungkinan kamu suka".
- Jika pengguna menyebut film yang disukai, gunakan film tersebut sebagai referensi untuk memahami preferensi pengguna.

ATURAN TANPA SPOILER:
- Jangan pernah membocorkan plot twist, ending, atau kejadian penting yang dapat merusak pengalaman menonton.
- Jangan memberikan spoiler meskipun pengguna tidak secara eksplisit memintanya.
- Saat membahas film, cukup jelaskan premis, genre, sutradara, aktor, tema, gaya visual, atau hal menarik lainnya tanpa membahas detail cerita penting.
- Jika pengguna secara langsung meminta spoiler, berikan peringatan terlebih dahulu dan tanyakan apakah mereka benar-benar ingin mengetahui spoiler tersebut.
- Jika pengguna belum menyetujui spoiler, tetap gunakan penjelasan tanpa spoiler.

BATASAN TOPIK:
- Fokus utama kamu adalah dunia perfilman.
- Jika pengguna tiba-tiba membahas topik di luar perfilman, seperti matematika, pemrograman, fisika, atau topik umum lainnya, jangan berpura-pura bahwa topik tersebut masih berkaitan dengan film.
- Jika pertanyaan di luar perfilman sederhana dan dapat dijawab dengan baik, kamu boleh memberikan jawaban singkat, kemudian arahkan percakapan kembali ke dunia perfilman.
- Jika pertanyaan di luar perfilman membutuhkan penjelasan yang mendalam, jelaskan dengan santai bahwa fokus utama kamu adalah dunia perfilman.
- Jangan mengarang jawaban hanya untuk menjawab pertanyaan di luar bidang perfilman.
- Jika topik di luar perfilman masih digunakan untuk membahas sebuah film, tetap jawab karena konteksnya masih berkaitan dengan perfilman.

Contoh:
Pengguna: "Berapa 25 x 16?"
Jawaban: "Hasilnya 400 😄 Kalau mau lanjut ngobrol film, aku siap bantu cari tontonan juga."

Pengguna: "Jelasin integral parsial dong."
Jawaban: "Kalau untuk bahas integral secara mendalam aku kurang pas karena fokusku memang dunia film 😄 Tapi kalau kamu lagi cari film yang punya tema matematika, aku bisa kasih beberapa rekomendasi."

Pengguna: "Kenapa Interstellar menggunakan konsep relativitas?"
Jawaban: "Nah, kalau yang ini masih berkaitan dengan film. Konsep relativitas memang punya peran penting dalam pembahasan ilmiah di Interstellar..."

BATASAN KONTEN:
- Jangan membantu pengguna mencari tautan streaming ilegal, situs bajakan, atau cara mengunduh film secara ilegal.
- Jika pengguna meminta hal tersebut, tolak dengan sopan dan arahkan ke layanan resmi.
- Jika pengguna meminta rekomendasi film dengan tema dewasa atau kekerasan, berikan informasi secara netral tanpa menggambarkan konten secara eksplisit.
- Jangan memberikan deskripsi seksual atau kekerasan secara eksplisit.
- Jangan mengarang judul, tahun rilis, sutradara, aktor, penghargaan, atau informasi film lainnya.
- Jika tidak yakin terhadap suatu informasi, sampaikan ketidakpastian tersebut daripada memberikan informasi yang belum diketahui kebenarannya.

CARA MENJAWAB:
Sebelum memberikan jawaban, pertimbangkan:
1. Apa yang sebenarnya ditanyakan atau diinginkan pengguna?
2. Apakah pertanyaan tersebut masih berkaitan dengan dunia perfilman?
3. Apakah ada konteks atau preferensi pengguna sebelumnya yang relevan?
4. Apakah jawaban membutuhkan klarifikasi terlebih dahulu?
5. Apakah jawaban berpotensi mengandung spoiler?
6. Format dan tingkat detail seperti apa yang paling sesuai dengan pertanyaan pengguna?

Gunakan pertimbangan tersebut untuk menghasilkan jawaban yang relevan dan terstruktur. Jangan menampilkan proses berpikir internal secara panjang. Tampilkan hanya jawaban akhir yang diperlukan pengguna.

FORMAT WAJIB UNTUK REKOMENDASI FILM:

Jika hanya satu film:
**Judul Film (Tahun)** - **Sutradara**
**Genre:** [Genre]
**Vibe:** [Minimal tiga kata yang menggambarkan suasana film]
**Sinopsis:** [Sinopsis singkat tanpa spoiler]
**Kenapa kamu mungkin akan suka:** [Alasan personal tanpa spoiler]

Jika lebih dari satu film:
1. **Judul Film (Tahun)** - **Sutradara**
**Genre:** [Genre]
**Vibe:** [Minimal tiga kata]
**Sinopsis:** [Sinopsis singkat tanpa spoiler]
**Kenapa kamu mungkin akan suka:** [Alasan personal tanpa spoiler]

2. **Judul Film (Tahun)** - **Sutradara**
**Genre:** [Genre]
**Vibe:** [Minimal tiga kata]
**Sinopsis:** [Sinopsis singkat tanpa spoiler]
**Kenapa kamu mungkin akan suka:** [Alasan personal tanpa spoiler]

dan seterusnya.

Jika pengguna hanya ingin berdiskusi tentang film tanpa meminta rekomendasi, tidak perlu menggunakan format rekomendasi di atas.

CONTOH PERILAKU:
Pengguna: "Aku lagi pengen film yang mind-blowing."
Jawaban harus menggali atau menggunakan konteks preferensi pengguna sebelum memberikan rekomendasi jika informasi yang tersedia belum cukup.

Pengguna: "Aku suka Interstellar, ada film yang mirip?"
Jawaban harus menggunakan Interstellar sebagai referensi untuk memahami kemungkinan preferensi pengguna dan memberikan rekomendasi yang relevan tanpa membocorkan spoiler.

Pengguna: "Ceritain tentang Parasite."
Jawaban cukup membahas premis, genre, sutradara, pemain, tema, dan hal menarik lainnya tanpa membocorkan twist atau ending.
"""

# AI-assisted: brainstorming chatbot commands

HELP_TEXT = """
Belum tahu mau nonton apa? Tinggal ceritakan genre, mood, atau film yang kamu suka. Kamu juga bisa memakai perintah berikut:

- `/help` - Menampilkan panduan ini.
- `/clear` - Hapus percakapan dan mulai obrolan baru.
- `/exit` - Mengakhiri sesi obrolan.
- `/stats` - Melihat statistik sesi obrolan.
- `/surprise` atau `/random` - Mendapatkan satu rekomendasi film secara acak, termasuk kemungkinan hidden gem.
- `/trivia` - Mendapatkan fakta menarik seputar dunia perfilman.
- `/watchlist` - Melihat daftar film yang pernah direkomendasikan selama sesi ini.

Setiap sesi memiliki 5 kuota AI gratis. Kuota digunakan untuk chat biasa, `/surprise`, `/random`, dan `/trivia`.

Kalau bingung mau mulai dari mana, coba ceritakan:
- "Aku pengen film yang bikin tegang."
- "Ada film mirip Interstellar?"
- "Rekomendasi film buat malam minggu."
- "Aku suka animasi animasi dari Ghibli, ada saran lain ngga?"
"""

FAREWELL_TEXT = """
Oke, sesi ngobrol film kita selesai dulu ya
Terima kasih sudah mampir. Semoga rekomendasi yang diberikan cocok dengan mood dan selera tontonanmu.
Kalau ingin ngobrol atau cari film lagi nanti, tinggal mulai sesi baru saja. Sampai jumpa dan selamat menonton! 🍿
"""

COMMANDS = {
    "/help": "Menampilkan panduan penggunaan chatbot.",
    "/clear": "Hapus percakapan dan mulai obrolan baru.",
    "/exit": "Mengakhiri sesi obrolan.",
    "/stats": "Melihat statistik sesi obrolan.",
    "/surprise": "Mendapatkan satu rekomendasi film secara acak, termasuk kemungkinan hidden gem.",
    "/random": "Mendapatkan satu rekomendasi film secara acak, termasuk kemungkinan hidden gem.",
    "/trivia": "Mendapatkan fakta menarik seputar dunia perfilman.",
    "/watchlist": "Melihat daftar film yang pernah direkomendasikan selama sesi ini."
}

# State
def init_session_state():
    defaults = {
        "messages": [],
        "api_call_count": 0,
        "user_api_key": "",
        "exited": False,
        "temperature": 0.8,
        "max_tokens": 1024,
        "current_chat_id": None,
        "save_history": True,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def reset_conversation():
    st.session_state.messages = []
    st.session_state.current_chat_id = None
    st.session_state.api_call_count = 0

def add_message(role: str, content: str):
    st.session_state.messages.append({"role": role, "content": content})
    save_current_chat()

def is_valid_messages(data) -> bool:
    return isinstance(data, list) and all(
        isinstance(m, dict) and "role" in m and "content" in m for m in data
    )

def get_active_api_key():
    if st.session_state.user_api_key:
        return st.session_state.user_api_key, "byok"

    dev_key = os.getenv("GROQ_API_KEY")
    if dev_key and st.session_state.api_call_count < FREE_QUOTA:
        return dev_key, "default"

    return None, "blocked"

# Chat History Local
def _chat_path(chat_id: str) -> Path:
    if not CHAT_ID_PATTERN.match(chat_id):
        raise ValueError("ID obrolan tidak valid.")
    return HISTORY_DIR / f"{chat_id}.json"

def build_chat_title(messages: list) -> str:
    for m in messages:
        if m["role"] == "user" and m["content"].strip().lower() not in COMMANDS:
            title = " ".join(m["content"].split())
            if len(title) > MAX_TITLE_LEN:
                title = title[:MAX_TITLE_LEN - 3].rstrip() + "..."
            return title
    return "Obrolan baru"


def save_current_chat():
    if not st.session_state.save_history or not st.session_state.messages:
        return

    try:
        HISTORY_DIR.mkdir(parents=True, exist_ok=True)

        now = datetime.now().isoformat(timespec="seconds")

        if not st.session_state.current_chat_id:
            st.session_state.current_chat_id = (
                f"{datetime.now():%Y%m%d_%H%M%S}_{uuid.uuid4().hex[:6]}"
            )

        path = _chat_path(st.session_state.current_chat_id)
        created_at = now

        if path.exists():
            try:
                created_at = json.loads(
                    path.read_text(encoding="utf-8")
                ).get("created_at", now)
            except Exception:
                pass

        payload = {
            "id": st.session_state.current_chat_id,
            "title": build_chat_title(st.session_state.messages),
            "created_at": created_at,
            "updated_at": now,
            "api_calls": st.session_state.api_call_count,
            "messages": st.session_state.messages,
        }

        tmp_path = path.with_suffix(".tmp")
        tmp_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        tmp_path.replace(path)

    except Exception as exc:
        st.toast(f"Gagal menyimpan riwayat obrolan: {exc}")


def list_saved_chats() -> list:
    if not HISTORY_DIR.exists():
        return []

    chats = []

    for path in HISTORY_DIR.glob("*.json"):
        if not CHAT_ID_PATTERN.match(path.stem):
            continue

        try:
            data = json.loads(path.read_text(encoding="utf-8"))

            chats.append(
                {
                    "id": path.stem,
                    "title": data.get("title") or "Obrolan tanpa judul",
                    "updated_at": data.get("updated_at", ""),
                }
            )

        except Exception:
            continue

    chats.sort(key=lambda c: c["updated_at"], reverse=True)

    return chats


def load_saved_chat(chat_id: str) -> bool:
    try:
        data = json.loads(
            _chat_path(chat_id).read_text(encoding="utf-8")
        )

        messages = data.get("messages", [])

        if not is_valid_messages(messages):
            raise ValueError("Format isi riwayat tidak sesuai.")

        calls = data.get("api_calls", 0)

        st.session_state.messages = messages
        st.session_state.current_chat_id = chat_id
        st.session_state.api_call_count = (
            calls if isinstance(calls, int) and calls >= 0 else 0
        )
        st.session_state.exited = False

        return True

    except Exception as exc:
        st.sidebar.error(f"Gagal membuka riwayat: {exc}")
        return False


def delete_saved_chat(chat_id: str):
    try:
        _chat_path(chat_id).unlink(missing_ok=True)

        if st.session_state.current_chat_id == chat_id:
            reset_conversation()

    except Exception as exc:
        st.sidebar.error(f"Gagal menghapus riwayat: {exc}")

# Groq API
def stream_groq_response(
    api_key: str,
    messages: list,
    temperature: float,
    max_tokens: int,
):
    try:
        client = Groq(api_key=api_key)

        stream = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True,
        )

        got_any_chunk = False

        for chunk in stream:
            delta = (
                chunk.choices[0].delta.content
                if chunk.choices
                else None
            )

            if delta:
                got_any_chunk = True
                yield delta

        if not got_any_chunk:
            yield "Chatbot Cinephile tidak dapat balasan dari server. Tolong kirim ulang pesanmu."

    except Exception as exc:
        yield (
            "\n\n[Peringatan] Waduh, ada masalah saat terhubung dengan Groq API: "
            f"{str(exc)}. Coba cek koneksi internet atau API key kamu, "
            "lalu kirim ulang pesanmu ya."
        )


def call_groq_and_store(
    user_facing_history: list,
    hidden_prompt: str | None = None,
):
    api_key, mode = get_active_api_key()

    if mode == "blocked":
        add_message(
            "assistant",
            "Kuota gratis di obrolan ini sudah habis. Masukkan API key Groq kamu sendiri di sidebar, "
            "atau mulai Obrolan Baru untuk dapat kuota gratis lagi.",
        )
        st.rerun()

    api_messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        }
    ]

    for m in user_facing_history:
        api_messages.append(
            {
                "role": m["role"],
                "content": m["content"],
            }
        )

    if hidden_prompt is not None:
        api_messages.append(
            {
                "role": "user",
                "content": hidden_prompt,
            }
        )

    with st.chat_message("assistant"):
        full_response = st.write_stream(
            stream_groq_response(
                api_key,
                api_messages,
                st.session_state.temperature,
                st.session_state.max_tokens,
            )
        )

    st.session_state.api_call_count += 1
    add_message("assistant", full_response)

    st.rerun()

# AI-assisted: brainstorming chatbot commands
# Commands
def handle_clear():
    reset_conversation()
    st.toast("Obrolan baru dimulai. Obrolan sebelumnya tetap tersimpan di riwayat.")


def handle_exit():
    st.session_state.exited = True


def handle_help():
    add_message("assistant", HELP_TEXT)


def handle_stats():
    user_msgs = [
        m for m in st.session_state.messages
        if m["role"] == "user"
    ]

    assistant_msgs = [
        m for m in st.session_state.messages
        if m["role"] == "assistant"
    ]

    total_chars = sum(
        len(m["content"])
        for m in st.session_state.messages
    )

    total_words = sum(
        len(m["content"].split())
        for m in st.session_state.messages
    )

    _, mode = get_active_api_key()

    if mode == "byok":
        sisa_kuota_text = "Menggunakan API key sendiri (mengikuti limit API Groq)"
    else:
        sisa_kuota = max(
            0,
            FREE_QUOTA - st.session_state.api_call_count
        )
        sisa_kuota_text = (
            f"{sisa_kuota}/{FREE_QUOTA} panggilan API gratis"
        )

    stats_text = f"""Statistik obrolan kita sejauh ini:

- Pesan dari kamu: {len(user_msgs)}
- Balasan dari Cinephile: {len(assistant_msgs)}
- Total pesan di sesi ini: {len(st.session_state.messages)}
- Panjang obrolan: {total_words} kata (~{total_chars} karakter)
- Sisa kuota API: {sisa_kuota_text}
- Temperature: {st.session_state.temperature}
- Max tokens: {st.session_state.max_tokens}"""

    add_message("assistant", stats_text)


def handle_surprise():
    hidden_prompt = (
        "Berikan satu rekomendasi film yang tergolong hidden gem atau relatif "
        "kurang dikenal oleh penonton umum. Pilih film yang menurutmu menarik "
        "untuk diperkenalkan kepada pengguna. Jangan mengarang informasi tentang "
        "film tersebut. Ikuti format rekomendasi film yang sudah ditentukan "
        "dalam system prompt dan jelaskan semuanya tanpa spoiler."
    )

    add_message("user", "/surprise")

    with st.chat_message("user"):
        st.markdown("/surprise")

    call_groq_and_store(
        st.session_state.messages[:-1],
        hidden_prompt=hidden_prompt,
    )


def handle_trivia():
    hidden_prompt = (
        "Berikan satu fakta menarik dan benar tentang dunia perfilman. "
        "Faktanya bisa berkaitan dengan film, proses produksi, aktor, sutradara, "
        "atau sejarah sinema. Pilih satu fakta saja dan jelaskan secara singkat "
        "dengan bahasa Indonesia yang santai dan natural seperti sedang ngobrol "
        "dengan teman. Jangan mengarang fakta. Jangan menggunakan emoji."
    )

    add_message("user", "/trivia")

    with st.chat_message("user"):
        st.markdown("/trivia")

    call_groq_and_store(
        st.session_state.messages[:-1],
        hidden_prompt=hidden_prompt,
    )


WATCHLIST_PATTERN = re.compile(
    r"\*\*([^\*\n]+?\s\(\d{4}\))\*\*"
)


def extract_recommended_titles(messages: list) -> list:
    titles = []

    for m in messages:
        if m["role"] != "assistant":
            continue

        for title in WATCHLIST_PATTERN.findall(m["content"]):
            title = title.strip()

            if title not in titles:
                titles.append(title)

    return titles


def handle_watchlist():
    titles = extract_recommended_titles(
        st.session_state.messages
    )

    if titles:
        reply = (
            "Ini film-film yang udah aku rekomendasikan di obrolan ini:\n\n"
            + "\n".join(f"- {title}" for title in titles)
        )
    else:
        reply = (
            "Belum ada film yang aku rekomendasikan di obrolan ini. "
            "Coba ceritain dulu film, genre, atau mood yang lagi kamu cari."
        )

    add_message("assistant", reply)


def dispatch_command(command: str):
    command = command.lower().strip()

    if command == "/clear":
        handle_clear()

    elif command == "/exit":
        handle_exit()

    elif command == "/help":
        handle_help()

    elif command == "/stats":
        handle_stats()

    elif command in ("/surprise", "/random"):
        handle_surprise()

    elif command == "/trivia":
        handle_trivia()

    elif command == "/watchlist":
        handle_watchlist()

# AI-assisted: sidebar UI development
# UI Sidebar
def render_history_sidebar():
    st.sidebar.header("Riwayat Obrolan")

    if st.sidebar.button(
        "Obrolan Baru",
        icon=":material/add:",
        use_container_width=True,
    ):
        reset_conversation()
        st.session_state.exited = False
        st.rerun()

    st.sidebar.toggle(
        "Simpan riwayat obrolan",
        key="save_history",
        help=f"Apabila Simpan Riwayat Obrolan aktif, maka obrolan akan otomatis disimpan sebagai file JSON di folder '{HISTORY_DIR.name}/'.",
    )

    chats = list_saved_chats()

    if not chats:
        st.sidebar.caption("Belum ada riwayat obrolan.")
        return

    for chat in chats:
        is_active = chat["id"] == st.session_state.current_chat_id

        col_open, col_delete = st.sidebar.columns([5, 1])

        with col_open:
            if st.button(
                chat["title"],
                key=f"open_{chat['id']}",
                type="primary" if is_active else "secondary",
                use_container_width=True,
                help=f"Terakhir diperbarui: {chat['updated_at'].replace('T', ' ')}",
            ):
                if load_saved_chat(chat["id"]):
                    st.rerun()

        with col_delete:
            if st.button(
                ":material/delete:",
                key=f"del_{chat['id']}",
                help="Hapus obrolan ini",
            ):
                delete_saved_chat(chat["id"])
                st.rerun()


def render_sidebar():
    render_history_sidebar()

    st.sidebar.divider()
    st.sidebar.header("Pengaturan Cinephile")

    _, mode = get_active_api_key()

    if mode == "byok":
        st.sidebar.success(
            "Status: menggunakan API key sendiri"
        )
        st.sidebar.caption(
            "Limit mengikuti akun Groq kamu."
        )
    else:
        sisa = max(
            0,
            FREE_QUOTA - st.session_state.api_call_count,
        )
        st.sidebar.info(
            f"Sisa kuota gratis: {sisa}/{FREE_QUOTA}"
        )

    if mode == "blocked":
        st.sidebar.warning(
            "Kuota gratis di obrolan ini sudah habis. "
            "Masukkan API key Groq kamu sendiri di bagian bawah berikut, "
            "atau mulai Obrolan Baru untuk mendapatkan kuota gratis lagi."
        )

        entered_key = st.sidebar.text_input(
            "API Key Groq",
            type="password",
            key="byok_input",
            help="API key hanya disimpan sementara selama sesi ini dan akan hilang saat halaman di-refresh.",
        )

        if entered_key:
            st.session_state.user_api_key = entered_key
            st.rerun()

    elif st.session_state.user_api_key:
        masked = (
            "*" * max(
                0,
                len(st.session_state.user_api_key) - 4,
            )
            + st.session_state.user_api_key[-4:]
        )

        st.sidebar.caption(
            f"API key aktif: {masked}"
        )

    st.sidebar.divider()

    st.session_state.temperature = st.sidebar.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=st.session_state.temperature,
        step=0.05,
    )

    st.session_state.max_tokens = st.sidebar.slider(
        "Max Tokens",
        min_value=512,
        max_value=2048,
        value=st.session_state.max_tokens,
        step=64,
    )

    st.sidebar.divider()

    if st.sidebar.button(
        "Cek Statistik",
        use_container_width=True,
    ):
        handle_stats()
        st.rerun()

# Main Content
def render_chat_history():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def main():
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon="🎬",
        layout="centered",
    )

    init_session_state()

    st.title(f"{APP_TITLE}: {APP_TAGLINE}")

    st.caption(
        "Ceritain film, genre, atau mood yang lagi kamu cari. "
        "Ketik `/help` kalau mau lihat daftar perintah yang tersedia."
    )

    render_sidebar()

    if st.session_state.exited:
        render_chat_history()

        st.info(FAREWELL_TEXT)

        if st.button("Mulai Sesi Baru"):
            st.session_state.exited = False
            reset_conversation()
            st.rerun()

        return

    render_chat_history()

    user_input = st.chat_input(
        "Tulis pesan kamu di sini..."
    )

    if not user_input:
        return

    stripped = user_input.strip().lower()

    if stripped in COMMANDS:
        if stripped in ("/exit", "/clear"):
            dispatch_command(stripped)
            st.rerun()

        elif stripped in ("/surprise", "/random", "/trivia"):
            dispatch_command(stripped)

        else:
            add_message("user", user_input)
            dispatch_command(stripped)
            st.rerun()

        return

    add_message("user", user_input)

    with st.chat_message("user"):
        st.markdown(user_input)

    call_groq_and_store(st.session_state.messages)


if __name__ == "__main__":
    main()