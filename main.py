from tkinter import *
from db import create_tables

# Veritabanı tablolarını oluştur
create_tables()

# Ana pencere
root = Tk()
root.title("Bütçe Yönetimi Uygulaması")
root.geometry("600x400")

Label(root, text="Hoş Geldiniz!", font=("Arial", 20)).pack(pady=20)

from tkinter import messagebox
from db import create_connection

def gelir_ekle_penceresi():
    pencere = Toplevel()
    pencere.title("Gelir Ekle")
    pencere.geometry("400x300")

    Label(pencere, text="Tarih (YYYY-AA-GG):").pack()
    tarih_entry = Entry(pencere)
    tarih_entry.pack()

    Label(pencere, text="Tutar:").pack()
    tutar_entry = Entry(pencere)
    tutar_entry.pack()

    Label(pencere, text="Açıklama:").pack()
    aciklama_entry = Entry(pencere)
    aciklama_entry.pack()

    def kaydet():
        tarih = tarih_entry.get()
        tutar = tutar_entry.get()
        aciklama = aciklama_entry.get()

        if tarih and tutar:
            try:
                conn = create_connection()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO income (date, amount, description) VALUES (?, ?, ?)", (tarih, tutar, aciklama))
                conn.commit()
                conn.close()
                messagebox.showinfo("Başarılı", "Gelir kaydedildi.")
                pencere.destroy()
            except Exception as e:
                messagebox.showerror("Hata", f"Veri eklenemedi: {e}")
        else:
            messagebox.showwarning("Uyarı", "Tarih ve tutar boş bırakılamaz.")

    Button(pencere, text="Kaydet", command=kaydet).pack(pady=10)

Button(root, text="Gelir Ekle", width=20, command=gelir_ekle_penceresi).pack(pady=10)

def gider_ekle_penceresi():
    pencere = Toplevel()
    pencere.title("Gider Ekle")
    pencere.geometry("400x350")

    Label(pencere, text="Tarih (YYYY-AA-GG):").pack()
    tarih_entry = Entry(pencere)
    tarih_entry.pack()

    Label(pencere, text="Tutar:").pack()
    tutar_entry = Entry(pencere)
    tutar_entry.pack()

    Label(pencere, text="Kategori:").pack()
    kategori_var = StringVar()
    kategori_menu = OptionMenu(pencere, kategori_var, "Yemek", "Ulaşım", "Kira", "Fatura", "Eğlence", "Diğer")
    kategori_menu.pack()

    Label(pencere, text="Açıklama:").pack()
    aciklama_entry = Entry(pencere)
    aciklama_entry.pack()

    def kaydet():
        tarih = tarih_entry.get()
        tutar = tutar_entry.get()
        kategori = kategori_var.get()
        aciklama = aciklama_entry.get()

        if tarih and tutar and kategori:
            try:
                conn = create_connection()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO expense (date, amount, category, description) VALUES (?, ?, ?, ?)", (tarih, tutar, kategori, aciklama))
                conn.commit()
                conn.close()
                messagebox.showinfo("Başarılı", "Gider kaydedildi.")
                pencere.destroy()
            except Exception as e:
                messagebox.showerror("Hata", f"Veri eklenemedi: {e}")
        else:
            messagebox.showwarning("Uyarı", "Tarih, tutar ve kategori boş bırakılamaz.")

    Button(pencere, text="Kaydet", command=kaydet).pack(pady=10)


Button(root, text="Gider Ekle", width=20, command=gider_ekle_penceresi).pack(pady=10)

def toplamlari_goster():
    try:
        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT SUM(amount) FROM income")
        toplam_gelir = cursor.fetchone()[0]
        toplam_gelir = toplam_gelir if toplam_gelir else 0

        cursor.execute("SELECT SUM(amount) FROM expense")
        toplam_gider = cursor.fetchone()[0]
        toplam_gider = toplam_gider if toplam_gider else 0

        bakiye = toplam_gelir - toplam_gider

        # Yeni pencere aç
        pencere = Toplevel()
        pencere.title("Toplamlar")
        pencere.geometry("350x200")

        Label(pencere, text=f"Toplam Gelir: {toplam_gelir:.2f} TL", font=("Arial", 12)).pack(pady=10)
        Label(pencere, text=f"Toplam Gider: {toplam_gider:.2f} TL", font=("Arial", 12)).pack(pady=10)
        Label(pencere, text=f"Kalan Bakiye: {bakiye:.2f} TL", font=("Arial", 12, "bold")).pack(pady=10)

        conn.close()

    except Exception as e:
        messagebox.showerror("Hata", f"Veriler alınamadı: {e}")

Button(root, text="Toplamları Göster", width=20, command=toplamlari_goster).pack(pady=10)

def kayitlari_goster():
    try:
        conn = create_connection()
        cursor = conn.cursor()

        # Yeni pencere aç
        pencere = Toplevel()
        pencere.title("Kayıtlar")
        pencere.geometry("600x500")

        # GELİRLER
        Label(pencere, text="Gelirler", font=("Arial", 12, "bold")).pack()
        cursor.execute("SELECT date, amount, description FROM income ORDER BY date DESC")
        gelirler = cursor.fetchall()
        for gelir in gelirler:
            Label(pencere, text=f"{gelir[0]} | {gelir[1]:.2f} TL | {gelir[2]}").pack()

        # GİDERLER
        Label(pencere, text="\nGiderler", font=("Arial", 12, "bold")).pack()
        cursor.execute("SELECT date, amount, category, description FROM expense ORDER BY date DESC")
        giderler = cursor.fetchall()
        for gider in giderler:
            Label(pencere, text=f"{gider[0]} | {gider[1]:.2f} TL | {gider[2]} | {gider[3]}").pack()

        conn.close()

    except Exception as e:
        messagebox.showerror("Hata", f"Kayıtlar alınamadı: {e}")

Button(root, text="Kayıtları Görüntüle", width=20, command=kayitlari_goster).pack(pady=10)


root.mainloop()

