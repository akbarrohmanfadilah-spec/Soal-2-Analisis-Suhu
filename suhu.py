BATAS_PANAS = 32 

def baca_data(nama_file):
    """Membaca file baris demi baris, mengembalikan list of dictionary."""
    data = []
    try:
        with open(nama_file, "r") as file:        
            for baris in file:                    
                baris = baris.strip()
                if not baris:                     
                    continue
                try:
                    hari, suhu = baris.split(";")
                    data.append({"hari": hari, "suhu": int(suhu)})  
                except ValueError:
                    print(f"Peringatan: baris dilewati -> {baris!r}")
    except FileNotFoundError:
        print(f"Error: file {nama_file} tidak ditemukan")
    return data

def hitung_rata_rata(*suhu):
    """Menghitung rata-rata dari sejumlah suhu (*args)."""
    if not suhu:
        raise ValueError("Data suhu tidak boleh kosong")
    return sum(suhu) / len(suhu)

def tentukan_kategori(suhu, batas_panas=BATAS_PANAS):
    """Panas jika suhu >= batas_panas, selain itu Normal."""
    return "Panas" if suhu >= batas_panas else "Normal"

def analisis(data, batas_panas=BATAS_PANAS):
    """Menganalisis data: rata-rata, tertinggi, terendah, kategori, jumlah hari panas."""
    if not data:
        raise ValueError("Data kosong, tidak dapat dianalisis")
    rata_rata = hitung_rata_rata(*[d["suhu"] for d in data])
    tertinggi = max(data, key=lambda d: d["suhu"])   
    terendah = min(data, key=lambda d: d["suhu"])
    kategori = [
        {"hari": d["hari"], "suhu": d["suhu"],
         "kategori": tentukan_kategori(d["suhu"], batas_panas=batas_panas)}  
        for d in data
    ]
    jumlah_panas = len(list(filter(lambda k: k["kategori"] == "Panas", kategori)))
    return {"rata_rata": rata_rata, "tertinggi": tertinggi, "terendah": terendah,
            "kategori": kategori, "jumlah_panas": jumlah_panas}

def tulis_laporan(hasil, nama_file="laporan_suhu.txt"):
    """Menulis hasil analisis ke file laporan (mode w) lalu menampilkannya."""
    with open(nama_file, "w") as file:            
        file.write("LAPORAN SUHU MINGGUAN\n")
        file.write("=====================\n")
        for k in hasil["kategori"]:
            file.write(f"{k['hari']:<8}: {k['suhu']} C ({k['kategori']})\n")
        file.write("---------------------\n")
        file.write(f"Rata-rata suhu  : {hasil['rata_rata']:.2f} C\n")
        file.write(f"Suhu tertinggi  : {hasil['tertinggi']['suhu']} C ({hasil['tertinggi']['hari']})\n")
        file.write(f"Suhu terendah   : {hasil['terendah']['suhu']} C ({hasil['terendah']['hari']})\n")
        file.write(f"Jumlah hari Panas: {hasil['jumlah_panas']}\n")
    with open(nama_file, "r") as file:            
        print(file.read())

if __name__ == "__main__":
    data = baca_data("suhu.txt")
    if data:
        tulis_laporan(analisis(data))
