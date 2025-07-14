import streamlit as st
from supabase import create_client, Client
from datetime import datetime, timezone
import pandas as pd

# Supabase URL dan API Key kamu
SUPABASE_URL = "https://nlqhurbhvqxvdjzrhfep.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5scWh1cmJodnF4dmRqenJoZmVwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI0NzIzNTQsImV4cCI6MjA2ODA0ODM1NH0.CC-0HUV6m416AD-kkfcJtKS9C4F5_Z6n7wcCIS-YjUQ"

# Buat koneksi
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Fungsi ambil data
def get_data():
    response = supabase.table("pelaku_ekraf").select("*").order("created_at", desc=True).execute()
    return pd.DataFrame(response.data)

# Streamlit UI
st.title("📊 Pelaku Ekonomi Kreatif Sulawesi Selatan")
st.caption("Data pelaku ekonomi kreatif dari berbagai kabupaten/kota.")

df = get_data()
st.dataframe(df, use_container_width=True)

# Form tambah data
with st.form("form_tambah"):
    st.subheader("➕ Tambah Pelaku Ekraf")
    nama = st.text_input("Nama")
    subsektor = st.selectbox("Subsektor", [
        "Pengembang Permainan (Game)", "Arsitektur", "Desain Interior", "Seni Rupa",
        "Desain Produk", "Animasi Dan Video", "Fotografi", "Desain Komunikasi Visual",
        "Televisi dan Radio", "Fashion", "Kriya", "Musik", "Kuliner",
        "Film", "Periklanan", "Seni Pertunjukan", "Penerbitan"
    ])
    kab_kota = st.selectbox("Kabupaten/Kota", [
        "Makassar", "Parepare", "Palopo", "Bantaeng", "Barru", "Bone", "Bulukumba", "Enrekang",
        "Gowa", "Jeneponto", "Kepulauan Selayar", "Luwu", "Luwu Timur", "Luwu Utara", "Maros",
        "Pangkajene dan Kepulauan", "Pinrang", "Sidenreng Rappang", "Sinjai", "Soppeng",
        "Takalar", "Tana Toraja", "Toraja Utara", "Wajo"
    ])
    tahun = st.number_input("Tahun Mulai", 1990, 2025, 2020)
    submit = st.form_submit_button("Simpan")

if submit:
    if not nama.strip():
        st.warning("⚠️ Nama pelaku wajib diisi!")
    else:
        response = supabase.table("pelaku_ekraf").insert({
            "nama_pelaku": nama.strip(),
            "subsektor": subsektor,
            "kab_kota": kab_kota,
            "tahun_mulai": tahun,
            "created_at": datetime.now(timezone.utc).isoformat()
        }).execute()

        if response.data:
            st.success("✅ Data berhasil ditambahkan!")
            st.experimental_rerun()
        else:
            st.error("❌ Gagal menambahkan data.")
            st.json(response.error)
