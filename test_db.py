try:
    engine = create_engine(URL)
    conn = engine.connect()
    print("✅ MANTAP PAK! KONEKSI DATABASE BERHASIL.")
    conn.close()
except Exception as e:
    print(f"❌ KONEKSI GAGAL: {e}")
