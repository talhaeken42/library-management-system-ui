import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

try:
    from ttkthemes import ThemedTk
    root = ThemedTk(theme="breeze")
except ImportError:
    root = tk.Tk()
    style = ttk.Style()
    style.theme_use("vista")

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sifre", #<-- Buraya kendi MySQL şifrenizi girin
    database="LibraryDB",
    buffered=True
)
cursor = db.cursor()

root.title("Kütüphane Sistemi")
root.geometry("400x300")

def giris_ekrani():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Kütüphaneci Girişi", font=("Arial", 16)).pack(pady=10)

    tk.Label(root, text="Kullanıcı Adı:").pack()
    username_entry = tk.Entry(root)
    username_entry.pack()
    username_entry.bind("<Return>", lambda event: giris_yap())

    def giris_yap():
        kullanici_adi = username_entry.get()
        cursor.execute("SELECT * FROM Librarians WHERE Username = %s", (kullanici_adi,))
        if cursor.fetchone():
            messagebox.showinfo("Giriş", f"Hoş geldin {kullanici_adi}")
            ana_menu()
        else:
            messagebox.showerror("Hata", "Kullanıcı adı geçersiz.")

    tk.Button(root, text="Giriş", command=giris_yap).pack(pady=10)

def ana_menu():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Kütüphane Ana Menü", font=("Arial", 16)).pack(pady=10)

    tk.Button(root, text="Kitapları Listele", command=kitaplari_listele).pack(pady=5)
    tk.Button(root, text="Kitapları Düzenle", command=kitaplari_duzenle).pack(pady=5)
    tk.Button(root, text="Üyeleri Düzenle", command=uyeleri_duzenle).pack(pady=5)
    tk.Button(root, text="Veritabanını Görüntüle", command=veritabani_goruntule).pack(pady=5)

    tk.Button(root, text="Kullanıcı Değiştir", command=giris_ekrani).pack(pady=(20, 5))

    tk.Button(root, text="Çıkış", command=root.quit).pack()

def pencereyi_ortala(pencere, genislik=500, yukseklik=500):
    pencere.update_idletasks()
    ekran_genislik = pencere.winfo_screenwidth()
    ekran_yukseklik = pencere.winfo_screenheight()
    x = (ekran_genislik // 2) - (genislik // 2)
    y = (ekran_yukseklik // 2) - (yukseklik // 2)
    pencere.geometry(f"{genislik}x{yukseklik}+{x}+{y}")

def kitaplari_duzenle():
    pencere = tk.Toplevel(root)
    pencere.title("Kitap Listesi ve İşlemleri")
    pencereyi_ortala(pencere, 500, 780)

    arama_frame = tk.Frame(pencere)
    arama_frame.pack(pady=5)
    tk.Label(arama_frame, text="Ara (Ad, Yazar, ISBN):").pack(side="left")
    arama_entry = tk.Entry(arama_frame)
    arama_entry.pack(side="left", padx=5)

    kitap_frame = tk.Frame(pencere)
    kitap_frame.pack(pady=10)

    tree = ttk.Treeview(kitap_frame, columns=("ID", "Title", "Author", "Status"), show="headings", height=6)
    tree.heading("ID", text="ID")
    tree.heading("Title", text="Kitap Adı")
    tree.heading("Author", text="Yazar")
    tree.heading("Status", text="Durum")
    tree.column("ID", width=40, anchor="center")
    tree.column("Title", width=200, anchor="w")
    tree.column("Author", width=150, anchor="w")
    tree.column("Status", width=100, anchor="center")
    tree.pack(fill="x")

    def kitaplari_goster(kelimeler=""):
        tree.delete(*tree.get_children())
        if kelimeler:
            query = """
                SELECT BookID, Title, Author, AvailabilityStatus FROM Books
                WHERE Title LIKE %s OR Author LIKE %s OR ISBN LIKE %s
            """
            like = f"%{kelimeler}%"
            cursor.execute(query, (like, like, like))
        else:
            cursor.execute("SELECT BookID, Title, Author, AvailabilityStatus FROM Books")

        for k in cursor.fetchall():
            durum = f"Stok: {k[3]}" if k[3] > 0 else "Stok Yok"
            tree.insert("", "end", values=(k[0], k[1], k[2], durum))

    arama_entry.bind("<KeyRelease>", lambda e: kitaplari_goster(arama_entry.get()))
    kitaplari_goster()

    ekle_frame = tk.LabelFrame(pencere, text="Yeni Kitap Ekle", padx=10, pady=10)
    ekle_frame.pack(padx=10, pady=10, fill="x")

    etiketler = ["Kitap Adı", "Yazar", "ISBN", "Kategori ID", "Yayınevi", "Yayın Yılı"]
    girisler = []

    for etiket in etiketler:
        tk.Label(ekle_frame, text=etiket + ":").pack()
        e = tk.Entry(ekle_frame)
        e.pack(fill="x")
        girisler.append(e)

    def kitap_secildi(event):
        secim = tree.focus()
        if not secim:
            return
        degerler = tree.item(secim, "values")
        if degerler:
            kitap_id = degerler[0]
            kitap_id_entry.delete(0, tk.END)
            kitap_id_entry.insert(0, kitap_id)

        
            cursor.execute("SELECT Title, Author, ISBN, CategoryID, Publisher, PublicationYear FROM Books WHERE BookID = %s", (kitap_id,))
            kitap = cursor.fetchone()
            if kitap:
                for i in range(len(girisler)):
                    girisler[i].delete(0, tk.END)
                    girisler[i].insert(0, str(kitap[i]))

    tree.bind("<<TreeviewSelect>>", kitap_secildi)

    def kitap_ekle_ui():
        try:
            veri = [e.get() for e in girisler]
            if any(v == "" for v in veri):
                messagebox.showwarning("Uyarı", "Tüm alanları doldurun.")
                return
            veri[3] = int(veri[3]) 
            veri[5] = int(veri[5]) 
            isbn = veri[2]

        
            cursor.execute("SELECT BookID, AvailabilityStatus FROM Books WHERE ISBN = %s", (isbn,))
            sonuc = cursor.fetchone()

            if sonuc:
                kitap_id, mevcut_stok = sonuc
                yeni_stok = mevcut_stok + 1
                cursor.execute("UPDATE Books SET AvailabilityStatus = %s WHERE BookID = %s", (yeni_stok, kitap_id))
                db.commit()
                messagebox.showinfo("Stok Güncellendi", f"Aynı ISBN bulundu. Stok {mevcut_stok} → {yeni_stok} yapıldı.")
            else:
                cursor.execute("""
                    INSERT INTO Books (Title, Author, ISBN, CategoryID, AvailabilityStatus, Publisher, PublicationYear)
                    VALUES (%s, %s, %s, %s, 1, %s, %s)
                """, (veri[0], veri[1], veri[2], veri[3], veri[4], veri[5]))
                db.commit()
                messagebox.showinfo("Başarılı", "Yeni kitap eklendi.")

            kitaplari_goster(arama_entry.get())

        except Exception as e:
            messagebox.showerror("Hata", str(e))


    tk.Button(ekle_frame, text="Kitap Ekle", command=kitap_ekle_ui).pack(pady=5)

    sil_frame = tk.LabelFrame(pencere, text="Kitap Sil", padx=10, pady=10)
    sil_frame.pack(padx=10, pady=10, fill="x")

    tk.Label(sil_frame, text="Silinecek Kitap ID:").pack()
    kitap_id_entry = tk.Entry(sil_frame)
    kitap_id_entry.pack()
    
    def kitap_sil_ui():
        try:
            book_id = int(kitap_id_entry.get())

        
            cursor.execute("SELECT AvailabilityStatus FROM Books WHERE BookID = %s", (book_id,))
            result = cursor.fetchone()
            if not result:
                messagebox.showerror("Hata", "Kitap bulunamadı.")
                return

            mevcut_stok = result[0]

            if mevcut_stok <= 0:
                messagebox.showinfo("Bilgi", "Zaten stokta kitap yok.")
                return

        
            cursor.execute("""
                SELECT COUNT(*) FROM Borrow 
                WHERE BookID = %s AND ReturnDate IS NULL
            """, (book_id,))
            aktif_odunc = cursor.fetchone()[0]

            if aktif_odunc >= mevcut_stok:
                messagebox.showerror("Hata", "Bu kitabın tamamı ödünçte. Stok azaltılamaz.")
                return

            if mevcut_stok == 1:
            
                cursor.execute("DELETE FROM Books WHERE BookID = %s", (book_id,))
                db.commit()
                messagebox.showinfo("Silindi", "Kitabın son kopyası silindi.")
            else:
            
                cursor.execute("""
                    UPDATE Books 
                    SET AvailabilityStatus = AvailabilityStatus - 1 
                    WHERE BookID = %s
                """, (book_id,))
                db.commit()
                messagebox.showinfo("Stok Azaltıldı", "Kitap stoktan 1 azaltıldı.")

            kitaplari_goster(arama_entry.get())

        except Exception as e:
            messagebox.showerror("Hata", str(e))

    tk.Button(sil_frame, text="Kitap Sil", command=kitap_sil_ui).pack(pady=5)

def kitaplari_listele():
    pencere = tk.Toplevel(root)
    pencere.title("Kitap Listesi ve İşlemleri")
    pencereyi_ortala(pencere, genislik=500, yukseklik=600)

    arama_frame = tk.Frame(pencere)
    arama_frame.pack(pady=5)
    tk.Label(arama_frame, text="Ara (Ad, Yazar, ISBN):").pack(side="left")
    arama_entry = tk.Entry(arama_frame)
    arama_entry.pack(side="left", padx=5)

    kitap_frame = tk.Frame(pencere)
    kitap_frame.pack(pady=10, fill="x")

    tree = ttk.Treeview(kitap_frame, columns=("ID", "Title", "Author", "Status"), show="headings", height=8)
    tree.heading("ID", text="ID")
    tree.heading("Title", text="Kitap Adı")
    tree.heading("Author", text="Yazar")
    tree.heading("Status", text="Durum")
    tree.column("ID", width=40, anchor="center")
    tree.column("Title", width=180, anchor="w")
    tree.column("Author", width=140, anchor="w")
    tree.column("Status", width=90, anchor="center")
    tree.pack(fill="x")

    def kitaplari_goster(kelimeler=""):
        tree.delete(*tree.get_children())
        if kelimeler:
            query = """
                SELECT BookID, Title, Author, AvailabilityStatus FROM Books
                WHERE Title LIKE %s OR Author LIKE %s OR ISBN LIKE %s
            """
            like = f"%{kelimeler}%"
            cursor.execute(query, (like, like, like))
        else:
            cursor.execute("SELECT BookID, Title, Author, AvailabilityStatus FROM Books")

        for k in cursor.fetchall():
            durum = f"Stok: {k[3]}" if k[3] > 0 else "Stok Yok"  
            tree.insert("", "end", values=(k[0], k[1], k[2], durum))

    arama_entry.bind("<KeyRelease>", lambda e: kitaplari_goster(arama_entry.get()))
    kitaplari_goster()

    islem_frame = tk.LabelFrame(pencere, text="Kitap İşlemleri", padx=10, pady=10)
    islem_frame.pack(padx=10, pady=10, fill="x")

    tk.Label(islem_frame, text="Kitap ID:").pack()
    kitap_id_entry = tk.Entry(islem_frame)
    kitap_id_entry.pack()

    def kitap_secildi(event):
        secim = tree.focus()
        if not secim:
            return
        degerler = tree.item(secim, "values")
        if degerler:
            kitap_id_entry.delete(0, tk.END)
            kitap_id_entry.insert(0, str(degerler[0]))
    
    tree.bind("<<TreeviewSelect>>", kitap_secildi)

    tk.Label(islem_frame, text="Üye Seç:").pack()
    uye_combobox = ttk.Combobox(islem_frame, state="readonly")
    cursor.execute("SELECT MemberID, FullName FROM Members")
    uyeler = cursor.fetchall()
    uye_combobox['values'] = [f"{u[0]} - {u[1]}" for u in uyeler]
    uye_combobox.pack()

    def get_uye_id():
        secim = uye_combobox.get()
        return secim.split(" - ")[0] if secim else None

    def kitap_odunc_al_ui():
        kitap_id = kitap_id_entry.get()
        uye_id = get_uye_id()
        if not kitap_id or not uye_id:
            messagebox.showerror("Hata", "Kitap ID ve Üye seçimi zorunlu.")
            return
        try:
            cursor.execute("SELECT AvailabilityStatus FROM Books WHERE BookID = %s", (kitap_id,))
            result = cursor.fetchone()
            if not result:
                messagebox.showerror("Hata", "Kitap bulunamadı.")
                return
            stok = result[0]

            if stok <= 0:
                messagebox.showerror("Hata", "Stok yok, kitap ödünç verilemez.")
                return
            
            cursor.execute("""
                SELECT MemberID FROM Reservations 
                WHERE BookID = %s AND Status = 'Active'
                ORDER BY ReservationDate ASC
            """, (kitap_id,))
            rezervasyon_sirasi = [row[0] for row in cursor.fetchall()]
            aktif_rez_sayisi = len(rezervasyon_sirasi)

            today = datetime.today().date()
            due = today + timedelta(days=15)
            
            if int(uye_id) in rezervasyon_sirasi:
                rezerv_sirasi = rezervasyon_sirasi.index(int(uye_id))
            else:
                rezerv_sirasi = -1

            if aktif_rez_sayisi > 0 and rezerv_sirasi == -1:
                
                if stok <= aktif_rez_sayisi:
                    ilk_kisi_id = rezervasyon_sirasi[0]
                    cursor.execute("SELECT FullName FROM Members WHERE MemberID = %s", (ilk_kisi_id,))
                    ad = cursor.fetchone()[0]
                    messagebox.showerror("Rezervasyon Var", f"Bu kitap {ad}'in rezervasyon sırasındadır.")
                    return
            
            if rezerv_sirasi == 0:
                cursor.execute("""
                    UPDATE Reservations 
                    SET Status = 'Completed' 
                    WHERE BookID = %s AND MemberID = %s AND Status = 'Active'
                """, (kitap_id, uye_id))
            
            cursor.execute("""
                INSERT INTO Borrow (BookID, MemberID, BorrowDate, DueDate, ReturnDate)
                VALUES (%s, %s, %s, %s, NULL)
            """, (kitap_id, uye_id, today, due))
            cursor.execute("""
                UPDATE Books SET AvailabilityStatus = AvailabilityStatus - 1 
                WHERE BookID = %s AND AvailabilityStatus > 0
            """, (kitap_id,))
            db.commit()
            messagebox.showinfo("Başarılı", "Kitap ödünç verildi.")
            kitaplari_goster(arama_entry.get())

        except Exception as e:
            messagebox.showerror("Hata", str(e))

    def kitap_iade_et_ui():
        kitap_id = kitap_id_entry.get()
        uye_id = get_uye_id()

        if not kitap_id or not uye_id:
            messagebox.showerror("Hata", "Kitap ID ve üye seçimi zorunlu.")
            return

        try:
        
            cursor.execute("""
                SELECT BorrowID, BorrowDate 
                FROM Borrow 
                WHERE BookID = %s AND MemberID = %s AND ReturnDate IS NULL
            """, (kitap_id, uye_id))
            kayit = cursor.fetchone()

            if not kayit:
            
                cursor.execute("""
                    SELECT Members.FullName, Borrow.BorrowDate
                    FROM Borrow
                    JOIN Members ON Borrow.MemberID = Members.MemberID
                    WHERE BookID = %s AND ReturnDate IS NULL
                """, (kitap_id,))
                alanlar = cursor.fetchall()

                if alanlar:
                    kisi_listesi = "\n".join([f"- {ad} ({tarih})" for ad, tarih in alanlar])
                    messagebox.showwarning("İade Yapılamaz", f"Bu kitabı şu an ödünçte olanlar:\n{kisi_listesi}")
                else:
                    messagebox.showinfo("Bilgi", "Bu kitabı şu an kimse ödünçte tutmuyor.")
                return

            borrow_id, tarih = kayit
            today = datetime.today().date()

        
            cursor.execute("UPDATE Borrow SET ReturnDate = %s WHERE BorrowID = %s", (today, borrow_id))
            cursor.execute("UPDATE Books SET AvailabilityStatus = AvailabilityStatus + 1 WHERE BookID = %s", (kitap_id,))
            db.commit()

            messagebox.showinfo("Başarılı", "Kitap başarıyla iade edildi.")
            kitaplari_goster(arama_entry.get())

        except Exception as e:
            messagebox.showerror("Hata", f"İade işlemi başarısız: {e}")

    def rezervasyon_yap_ui():
        kitap_id = kitap_id_entry.get()
        uye_id = get_uye_id()

        if not kitap_id or not uye_id:
            messagebox.showerror("Hata", "Kitap ID ve Üye seçimi zorunlu.")
            return
        try:           
            cursor.execute("SELECT AvailabilityStatus FROM Books WHERE BookID = %s", (kitap_id,))
            stok_row = cursor.fetchone()
            if not stok_row:
                messagebox.showerror("Hata", "Kitap bulunamadı.")
                return
            stok = stok_row[0]
            
            cursor.execute("""
                SELECT COUNT(*) FROM Reservations 
                WHERE BookID = %s AND Status = 'Active'
            """, (kitap_id,))
            rezervasyon_sayisi = cursor.fetchone()[0]
            
            cursor.execute("""
                SELECT 1 FROM Reservations 
                WHERE BookID = %s AND MemberID = %s AND Status = 'Active'
            """, (kitap_id, uye_id))
            if cursor.fetchone():
                messagebox.showinfo("Zaten Rezerve", "Bu kitabı zaten rezerve etmişsiniz.")
                return
            
            if stok > rezervasyon_sayisi:
                proceed = messagebox.askyesno("Stok Var", 
                    "Kitap şu an stokta mevcut.\nYine de rezervasyon yapmak istiyor musunuz?")
                if not proceed:
                    return
            
            today = datetime.today().date()
            cursor.execute("""
                INSERT INTO Reservations (BookID, MemberID, ReservationDate, Status)
                VALUES (%s, %s, %s, 'Active')
            """, (kitap_id, uye_id, today))
            db.commit()
            messagebox.showinfo("Başarılı", "Rezervasyon yapıldı.")

        except Exception as e:
            messagebox.showerror("Hata", str(e))

    def rezervasyon_iptal_ui():
        kitap_id = kitap_id_entry.get()
        uye_id = get_uye_id()

        if not kitap_id or not uye_id:
            messagebox.showerror("Hata", "Kitap ID ve Üye seçimi zorunlu.")
            return
        try:
            cursor.execute("""
                UPDATE Reservations 
                SET Status = 'Cancelled' 
                WHERE BookID = %s AND MemberID = %s AND Status = 'Active'
            """, (kitap_id, uye_id))
            db.commit()
            messagebox.showinfo("Başarılı", "Rezervasyon iptal edildi.")
        except Exception as e:
            messagebox.showerror("Hata", str(e))
    
    def rezervasyon_sil_ui():
        kitap_id = kitap_id_entry.get()

        if not kitap_id:
            messagebox.showerror("Hata", "Kitap ID gerekli.")
            return
        try:
            cursor.execute("""
                UPDATE Reservations 
                SET Status = 'Cancelled' 
                WHERE BookID = %s AND Status = 'Active'
            """, (kitap_id,))
            db.commit()
            messagebox.showinfo("Başarılı", "Kitabın tüm rezervasyonları iptal edildi.")
        except Exception as e:
            messagebox.showerror("Hata", str(e))

    tk.Button(islem_frame, text="Kitap Ödünç Al", command=kitap_odunc_al_ui).pack(pady=2)
    tk.Button(islem_frame, text="Kitap İade Et", command=kitap_iade_et_ui).pack(pady=2)
    tk.Button(islem_frame, text="Rezervasyonu Yap", command=rezervasyon_yap_ui).pack(pady=2)
    tk.Button(islem_frame, text="Rezervasyonu İptal Et", command=rezervasyon_iptal_ui).pack(pady=2)
    tk.Button(islem_frame, text="Rezervasyonları Sil", command=rezervasyon_sil_ui).pack(pady=2)

def uyeleri_duzenle():
    pencere = tk.Toplevel(root)
    pencere.title("Üye Düzenle")
    pencereyi_ortala(pencere, 500, 600)

    uye_frame = tk.Frame(pencere)
    uye_frame.pack(pady=10)

    tk.Label(uye_frame, text="Kayıtlı Üyeler", font=("Arial", 12, "bold")).pack()

    tree = ttk.Treeview(uye_frame, columns=("ID", "Ad", "Email"), show="headings", height=8)
    tree.heading("ID", text="ID")
    tree.heading("Ad", text="Ad Soyad")
    tree.heading("Email", text="E-posta")
    tree.column("ID", width=50, anchor="center")
    tree.column("Ad", width=150, anchor="w")
    tree.column("Email", width=200, anchor="w")
    tree.pack(fill="x")

    cursor.execute("SELECT MemberID, FullName, Email FROM Members")
    for u in cursor.fetchall():
        tree.insert("", "end", values=u)

    def satir_secildi(event):
        secim = tree.focus()
        if not secim:
            return
        degerler = tree.item(secim, "values")
        if degerler:
            sil_entry.delete(0, tk.END)
            sil_entry.insert(0, degerler[0]) 

    tree.bind("<<TreeviewSelect>>", satir_secildi)

    ekle_frame = tk.LabelFrame(pencere, text="Yeni Üye Ekle", padx=10, pady=10)
    ekle_frame.pack(padx=10, pady=10, fill="x")

    tk.Label(ekle_frame, text="Ad Soyad:").pack()
    ad_entry = tk.Entry(ekle_frame)
    ad_entry.pack(fill="x")

    tk.Label(ekle_frame, text="E-posta:").pack()
    email_entry = tk.Entry(ekle_frame)
    email_entry.pack(fill="x")

    def uye_ekle_ui():
        ad = ad_entry.get()
        email = email_entry.get()
        if not ad or not email:
            messagebox.showwarning("Eksik Bilgi", "Ad ve e-posta gerekli.")
            return
        try:
            today = datetime.today().date()
            cursor.execute("INSERT INTO Members (FullName, Email, MembershipDate) VALUES (%s, %s, %s)", (ad, email, today))
            db.commit()
            messagebox.showinfo("Başarılı", "Üye eklendi.")
            pencere.destroy()
            uyeleri_duzenle()
        except Exception as e:
            messagebox.showerror("Hata", str(e))

    tk.Button(ekle_frame, text="Üye Ekle", command=uye_ekle_ui).pack(pady=5)

    sil_frame = tk.LabelFrame(pencere, text="Üye Sil", padx=10, pady=10)
    sil_frame.pack(padx=10, pady=10, fill="x")

    tk.Label(sil_frame, text="Silinecek Üye ID:").pack()
    sil_entry = tk.Entry(sil_frame)
    sil_entry.pack()

    def uye_sil_ui():
        try:
            uye_id = int(sil_entry.get())

            cursor.execute("SELECT * FROM Borrow WHERE MemberID = %s", (uye_id,))
            if cursor.fetchone():
                messagebox.showerror("Hata", "Bu üyeye ait ödünç kayıtları var.")
                return

            cursor.execute("SELECT * FROM Reservations WHERE MemberID = %s", (uye_id,))
            if cursor.fetchone():
                messagebox.showerror("Hata", "Bu üyeye ait rezervasyonlar var.")
                return

            cursor.execute("DELETE FROM Members WHERE MemberID = %s", (uye_id,))
            db.commit()
            messagebox.showinfo("Başarılı", "Üye silindi.")
            pencere.destroy()
            uyeleri_duzenle()
        except Exception as e:
            messagebox.showerror("Hata", str(e))

    tk.Button(sil_frame, text="Üye Sil", command=uye_sil_ui).pack(pady=5)

def veritabani_goruntule():
    pencere = tk.Toplevel(root)
    pencere.title("Veritabanı Tabloları")
    pencereyi_ortala(pencere, genislik=1000, yukseklik=600)

    tablo_frame = tk.Frame(pencere)
    tablo_frame.pack(side="left", padx=10, pady=10, fill="y")

    tk.Label(tablo_frame, text="Tablolar", font=("Arial", 12, "bold")).pack()

    tablo_tree = ttk.Treeview(tablo_frame, columns=("Tablo",), show="headings", height=20)
    tablo_tree.heading("Tablo", text="Tablolar")
    tablo_tree.column("Tablo", anchor="w", width=180)
    tablo_tree.pack(fill="y")

    cursor.execute("SHOW TABLES")
    tablolar = [row[0] for row in cursor.fetchall()]
    for tablo in tablolar:
        tablo_tree.insert("", "end", values=(tablo,))

    icerik_frame = tk.Frame(pencere)
    icerik_frame.pack(side="left", padx=10, pady=10, fill="both", expand=True)

    tree = ttk.Treeview(icerik_frame)
    tree.pack(fill="both", expand=True)

    scrollbar = tk.Scrollbar(icerik_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    def tablo_secildi(event):
        secim = tablo_tree.focus()
        if not secim:
            return
        tablo_adi = tablo_tree.item(secim, "values")[0]

        try:
            cursor.execute(f"SELECT * FROM `{tablo_adi}`")
            rows = cursor.fetchall()
            kolonlar = [desc[0] for desc in cursor.description]

        
            tree.delete(*tree.get_children())
            tree["columns"] = kolonlar
            tree["show"] = "headings"

        
            for k in kolonlar:
                tree.heading(k, text=k)

        
            genislikler = [len(str(k)) for k in kolonlar]
            for row in rows:
                for i, deger in enumerate(row):
                    genislikler[i] = max(genislikler[i], len(str(deger)))

        
            for i, k in enumerate(kolonlar):
                piksel_genislik = min(300, max(80, genislikler[i] * 8))
                tree.column(k, width=piksel_genislik, anchor="w")

        
            for row in rows:
                tree.insert("", "end", values=row)

        except Exception as e:
            tree.delete(*tree.get_children())
            tree["columns"] = ["Hata"]
            tree["show"] = "headings"
            tree.heading("Hata", text="⚠️ Hata")
            tree.insert("", "end", values=[str(e)])

    tablo_tree.bind("<<TreeviewSelect>>", tablo_secildi)

giris_ekrani()
root.mainloop()
