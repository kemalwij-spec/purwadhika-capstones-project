# ----------------------------------------------
# Importing Library
# ----------------------------------------------

import mysql.connector                  # Digunakan untuk menyambungkan mySQL dengan Python di VSCode
import matplotlib.pyplot as plt         # Digunakan untuk visualisasi data
import matplotlib.ticker as mticker     # Digunakan untuk tambahan formatting dalam visualisasi data
import seaborn as sns                   # Digunakan untuk visualisasi data selain matplotlib
import pandas as pd                     # Digunakan untuk data processing 
from datetime import date, datetime     # Digunakan untuk data tanggal 

today = date.today() 

# ----------------------------------------------
# Init: Connecting MySQL Database and Python
# ----------------------------------------------

# Membuat Koneksi ke mySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="uW3uW3!!",
    database="db_rental"
)

# Membuat koneksi ke Database
mycursor = mydb.cursor()

# Membuat fungsi untuk menjalankan query SQL dan return as DataFrame
def sql_df(query):
    """Eksesuksi query SQL dan kembalikan sebagai DataFrame"""
    mycursor.execute(query) # execute the query
    result = mycursor.fetchall() # save the result in 'result' variable
    df = pd.DataFrame(result, columns=mycursor.column_names) # convert to dataframe 
    return df

# ----------------------------------------------
# DataFrame Collections 
# ----------------------------------------------

# DataFrame utama (Join seluruh tables dengan pilihan beberapa kolom)
df_utama = sql_df(""" 
                  SELECT p.*, m.merek, m.kategori, m.harga_per_hari, m.status, r.id_rental, r.id_mobil, r.tgl_mulai, r.durasi_hari, r.total_harga, r.status_rental, pyr.metode_bayar, pyr.jumlah_bayar, pyr.tgl_bayar
                  FROM pelanggan p
                  JOIN rental r ON p.id_pelanggan = r.id_pelanggan
                  JOIN mobil m ON r.id_mobil = m.id_mobil
                  JOIN pembayaran pyr ON r.id_rental = pyr.id_rental
                  ORDER BY id_pelanggan
                  """)

# Dataframe untuk Mobil yang Tersedia
df_mobil_tersedia = sql_df("""
                          SELECT *
                          FROM mobil
                          WHERE status = 'Tersedia'
                          ORDER BY id_mobil
                          """)

# Dataframe untuk Mobil Lengkap
df_mobil_lengkap = sql_df("""
                          SELECT *
                          FROM mobil
                          ORDER BY id_mobil
                          """)

# Dataframe untuk data Pelanggan 
df_pelanggan = sql_df("""
                      SELECT *
                      FROM pelanggan
                      ORDER BY id_pelanggan
                      """)

# ----------------------------------------------
# Collection of Function
# ----------------------------------------------

# Fungsi untuk mengupdate query dengan data terbaru
def update_query():
  global df_pelanggan
  global df_mobil_tersedia
  global df_mobil_lengkap
  global df_utama

  df_pelanggan = sql_df("""
                        SELECT *
                        FROM pelanggan
                        ORDER BY id_pelanggan
                        """)
  df_mobil_tersedia = sql_df("""
                          SELECT *
                          FROM mobil
                          WHERE status = 'Tersedia'
                          ORDER BY id_mobil
                          """)
  df_mobil_lengkap = sql_df("""
                          SELECT *
                          FROM mobil
                          ORDER BY id_mobil
                          """)
  df_utama = sql_df(""" 
                  SELECT p.*, m.merek, m.kategori, m.harga_per_hari, m.status, r.id_rental, r.id_mobil, r.tgl_mulai, r.durasi_hari, r.total_harga, r.status_rental, pyr.metode_bayar, pyr.jumlah_bayar, pyr.tgl_bayar
                  FROM pelanggan p
                  JOIN rental r ON p.id_pelanggan = r.id_pelanggan
                  JOIN mobil m ON r.id_mobil = m.id_mobil
                  JOIN pembayaran pyr ON r.id_rental = pyr.id_rental
                  """)

# Fungsi untuk mencari pelanggan berdasarkan Nama atau No HP Pelanggan
def cari_pelanggan():
    search_keyword = input('Masukkan Nama Pelanggan atau No HP Pelanggan: ')
    df_cari_pelanggan = sql_df(f"""
                              SELECT * 
                              FROM pelanggan
                              WHERE nama LIKE '%{search_keyword}%' OR
                              no_hp LIKE '%{search_keyword}%'
                              """)
    if df_cari_pelanggan.empty:
       print()
       print(f'❌ Pelanggan dengan Nama/No Hp {search_keyword} tidak ditemukan di database \n')
    else:
      print(f'''
            ID Pelanggan    : {df_cari_pelanggan['id_pelanggan'][0]}
            Nama Pelanggan  : {df_cari_pelanggan['nama'][0]}
            No HP Pelanggan : {df_cari_pelanggan['no_hp'][0]}
            Kota Pelanggan  : {df_cari_pelanggan['kota'][0]}
            Email Pelanggan : {df_cari_pelanggan['email'][0]}
            ''')

# Fungsi untuk menambah data pelanggan baru
def tambah_pelanggan():
    nama_pelanggan = input('Masukkan Nama Pelanggan   : ').title()
    hp_pelanggan = input('Masukkan No HP Pelanggan  : ')
    kota_pelanggan = input('Masukkan Kota Pelanggan   : ').title()
    email_pelanggan = input('Masukkan email Pelanggan  : ').lower()
    print()
    print(f'''Data yang akan dimasukkan adalah: 
          Nama Pelanggan  : {nama_pelanggan}
          No HP Pelanggan : {hp_pelanggan}
          Kota Pelanggan  : {kota_pelanggan}
          Email Pelanggan : {email_pelanggan}
          ''')
    
    konfirmasi = input('Apakah Data tersebut sudah benar? (Y/N): ').upper() # Proses Konfirmasi sebelum memasukkan data baru ke table Pelanggan

    if konfirmasi == 'Y': # Jika Data sudah benar, maka akan dilakukan proses penambahan data dan push ke database
      mycursor.execute(f"""
          INSERT INTO pelanggan(nama, no_hp, kota, email) 
          VALUES
          ('{nama_pelanggan}', '{hp_pelanggan}', '{kota_pelanggan}', '{email_pelanggan}')
           """)  
      mydb.commit()
      update_query()
      print('✅ Data sudah berhasil dimasukkan ke database rental')

    else:
      print('-' * 100)
      print('Data Tidak Jadi Dimasukkan ke Database - Anda akan kembali ke Menu Utama')
      print('-' * 100)

# Fungsi untuk menambah data penyewaan baru
def tambah_sewa():
  print('Menampilkan daftar pelanggan:')
  print(df_pelanggan.to_string(index=False))
  
  try: 
    while True: # Loop proses untuk pemilihan ID Pelanggan, jika tidak ditemukan maka user perlu resubmit 
      tambah_sewa_idpelanggan = int(input('Pilih ID Pelanggan: '))
      
      if tambah_sewa_idpelanggan in df_pelanggan['id_pelanggan'].values: # Jika ID Pelanggan ditemukan akan lanjut ke proses selanjutnya
          break
      print('ID Pelanggan tidak ditemukan \n')
    
    print('\nMenampilkan daftar mobil yang tersedia:')
    print(df_mobil_tersedia.to_string(index=False))

    while True: # Loop proses untuk pemilihan ID Mobil, jika tidak ditemukan maka user perlu resubmit 
      tambah_sewa_idmobil = int(input('Pilih ID mobil: '))
      if tambah_sewa_idmobil in df_mobil_tersedia['id_mobil'].values: # Jika ID mobil ditemukan akan lanjut ke proses selanjutnya
         break
      print('ID Mobil tidak tersedia \n')

    tambah_sewa_tanggal = datetime.strptime(input('Masukkan tanggal penyewaan (YYYY-MM-DD): '), '%Y-%m-%d').date()
    tambah_sewa_durasi = int(input('Masukkan berapa hari sewa: '))

    while True: # Loop proses untuk metode pembayaran memastikan sesuai dengan pilihan yang ada
      tambah_sewa_pembayaran = input('Masukkan metode pembayaran (QRIS/Transfer/Kartu Kredit/Cash): ').title()
      if tambah_sewa_pembayaran == 'Qris': # mengubah formatting metode pembayaran QRIS
        tambah_sewa_pembayaran = 'QRIS'

      if tambah_sewa_pembayaran in ['QRIS','Transfer','Kartu Kredit','Cash']:
         break
      print('Metode Pembayaran yang diinput salah')

  except ValueError as e: # Mengembalikan error jika input tidak sesuai data type
     print(f'Input tidak valid: {e}')
     return

  print('=' * 100)
  print('Proses tambah penyewaan sedang diproses')
  print('=' * 100)

  # Variable Assignment & Calculation berdasarkan input data 
  harga_sewa = df_mobil_tersedia[df_mobil_tersedia['id_mobil'] == tambah_sewa_idmobil]
  tambah_sewa_total = tambah_sewa_durasi * harga_sewa['harga_per_hari'].values[0]
  jumlah_bayar = tambah_sewa_total
  
  # Proses Konfirmasi Data 
  print('Berikut ringkasan data yang akan dimasukkan dalam database: ')
  print(f"""
        ID Pelanggan        : {tambah_sewa_idpelanggan}
        Nama Pelanggan      : {df_pelanggan[df_pelanggan['id_pelanggan'] == tambah_sewa_idpelanggan]['nama'].values[0]}
        Merek Mobil         : {df_mobil_tersedia[df_mobil_tersedia['id_mobil'] == tambah_sewa_idmobil]['merek'].values[0]}
        Tanggal Penyewaan   : {tambah_sewa_tanggal:%d-%B-%Y}
        Durasi Penyewaan    : {tambah_sewa_durasi} hari
        Harga per Hari      : Rp {harga_sewa['harga_per_hari'].values[0]:,}/hari
        Total Harga         : Rp {tambah_sewa_total:,}
        Metode Pembayaran   : {tambah_sewa_pembayaran}
        Tanggal Pembayaran  : {tambah_sewa_tanggal:%d-%B-%Y} 
        """) # tanggal pembayaran sesuai dengan Tanggal Penyewaan
  
  # Proses Menambah informasi data penyewaan ke database
  konfirmasi = input('Apakah Data tersebut sudah benar? (Y/N): ').upper()

  if konfirmasi == 'Y': # Jika Data sudah benar, maka akan dilakukan proses penambahan data dan push ke database
    mycursor.execute(f"""
        INSERT INTO rental(id_pelanggan, id_mobil, tgl_mulai, durasi_hari, total_harga, status_rental)
        VALUES
        ({tambah_sewa_idpelanggan}, {tambah_sewa_idmobil}, {tambah_sewa_tanggal:'%Y-%m-%d'}, {tambah_sewa_durasi}, {tambah_sewa_total}, 'Aktif')
        """)
    
    id_rental_baru = mycursor.lastrowid # Mendapatkan latest rental id yang baru di insert

    mycursor.execute(f"""
        INSERT INTO pembayaran (id_rental, metode_bayar, jumlah_bayar, tgl_bayar)
        VALUES
        ({id_rental_baru}, '{tambah_sewa_pembayaran}', {jumlah_bayar}, {tambah_sewa_tanggal:'%Y-%m-%d'})
        """)
    
    mycursor.execute(f"""
        UPDATE mobil
        SET status = 'Disewa'            
        WHERE id_mobil = {tambah_sewa_idmobil}
        """)

    mydb.commit()
    update_query()
    print('✅ Data sudah berhasil dimasukkan ke database rental')

  else:
    print('-' * 100)
    print('Data Tidak Jadi Dimasukkan ke Database - Anda akan kembali ke Menu Utama')
    print('-' * 100)

# Fungsi untuk update status sewa mobil
def update_sewa():
  print('Menampilkan Daftar mobil dan status: ')
  print(df_mobil_lengkap.to_string(index=False))

  while True:
    update_idmobil = int(input('Pilih ID Mobil yang akan diupdate: '))

    if update_idmobil in df_mobil_lengkap['id_mobil'].values:
        break
    print('ID Mobil yang dipilih tidak tersedia')

  while True:
    status_baru = input('Update status Mobil Terbaru (Tersedia/Disewa/Maintenance): ').title()
    if status_baru in ['Tersedia','Disewa','Maintenance']:
        break
    print('Input Status Mobil Salah')

  df_mobil_filtered = df_mobil_lengkap[df_mobil_lengkap['id_mobil'] == update_idmobil]

  print('Ringkasan perubahan Status Mobil: ')
  print(f"""
      ID Mobil        : {update_idmobil}
      Merek Mobil     : {df_mobil_filtered['merek'].values[0]}
      Kategori Mobil  : {df_mobil_filtered['kategori'].values[0]}
      Harga per Hari  : Rp {df_mobil_filtered['harga_per_hari'].values[0]:,}/hari
      Status Lama     : {df_mobil_filtered['status'].values[0]}
      Status Terbaru  : {status_baru}
        """)
   
  konfirmasi = input('Apakah Data tersebut sudah benar? (Y/N): ').upper()

  if konfirmasi == 'Y':    # Jika Data sudah benar, maka akan dilakukan proses update data dan push ke database
    mycursor.execute(f"""
        UPDATE mobil
        SET status = '{status_baru}'            
        WHERE id_mobil = {update_idmobil}
        """)

    mydb.commit()
    update_query()
    print('✅ Data sudah berhasil dimasukkan ke database rental')

  else:
    print('-' * 100)
    print('Data Tidak Jadi Dimasukkan ke Database - Anda akan kembali ke Menu Utama')
    print('-' * 100)

# Fungsi Statistik Dasar berdasarkan DataFrame Utama
def statistik_dasar(stat_filter):
  global columns_filter # Variable untuk Kolom yang Dipilih

  # Assignment Variable Pemilihan Kolom (Stat_filter 1-3 Numerik, 4-8 Kategori)
  if stat_filter == 1:
    columns_filter = ['durasi_hari']
  elif stat_filter == 2:
    columns_filter = ['total_harga']
  elif stat_filter == 3:
    columns_filter = ['harga_per_hari']
  elif stat_filter == 4: 
    columns_filter = ['kota']
  elif stat_filter == 5:
    columns_filter = ['merek']
  elif stat_filter == 6:
    columns_filter = ['kategori']
  elif stat_filter == 7:
    columns_filter = ['status']
  elif stat_filter == 8:
    columns_filter = ['metode_bayar']
  else: 
    print('Pilihan Anda Salah - Keluar Program')

  print(f'Menampilkan Data Statistik untuk Kolom "{columns_filter[0]}"')
  print(df_utama[columns_filter].describe().round(2))
  print()
  
  if stat_filter >= 1 and stat_filter <= 3: # menghighlight tambahan informasi statistik
    print(f'- Kolom {columns_filter[0]} memiliki jumlah data    : {df_utama[columns_filter[0]].count()} data')
    print(f'- Kolom {columns_filter[0]} memiliki rata-rata nilai: {df_utama[columns_filter[0]].mean():,.1f}')
    print(f'- Kolom {columns_filter[0]} memiliki median nilai   : {df_utama[columns_filter[0]].median():,.1f}')
    print(f'- Kolom {columns_filter[0]} memiliki modus nilai    : {df_utama[columns_filter[0]].mode().to_list()[0]:,.1f}')

  else: # menampilkan tambahan informasi list nilai unik untuk data kategori
    unique_data = df_utama[columns_filter[0]].unique().tolist()
    print(f'Nilai Unik dari kolom "{columns_filter[0]}" sebanyak {len(unique_data)} yang berisikan: {unique_data}')

# Fungsi untuk menampilkan Bar Chart untuk data Kategori
def visualisasi_kategori():
  
  # DataFrame creation untuk Data Kategori
  df_visual = df_utama.groupby(columns_filter)['id_pelanggan'].count().reset_index()
  df_visual.columns = ['kategori','jumlah_data']
  df_visual = df_visual.sort_values(by='jumlah_data',ascending=True)
  x = df_visual['kategori']
  y = df_visual['jumlah_data']

  # Show Bar Chart for Data Kategori
  fig, ax = plt.subplots(figsize=(10, 10))
  bars = ax.barh(x, y, color="#E32D276F", edgecolor='white')
  
  # Add labels and titles
  ax.set_xlabel('Jumlah Data', fontsize=12, fontweight='bold', labelpad=10)
  ax.set_ylabel(f'{columns_filter[0].title()}', fontsize=12, fontweight='bold', labelpad=10)
  ax.set_title(f'Jumlah Data berdasarkan {columns_filter[0].title()}', fontsize=14, fontweight='bold', pad=10)
  ax.bar_label(bars, padding=8)

  # Menampilkan Visualisasi
  plt.tight_layout()
  plt.show()

# Fungsi untuk menampilkan Histogram untuk data Numerik
def visualisasi_numerik():
  # Membuat Kanvas dan Histogram
  fig, ax = plt.subplots(figsize=(10, 10))
  ax.hist(df_utama[columns_filter], bins='auto', color="#6fc76e", edgecolor='white', alpha=0.8)

  # Menambahkan Garis Data Mean & Median
  ax.axvline(df_utama[columns_filter[0]].mean(), color='red',   linestyle='--', linewidth=1.8, label=f'Mean: {df_utama[columns_filter[0]].mean():,.1f}')
  ax.axvline(df_utama[columns_filter[0]].median(), color='blue',   linestyle='-', linewidth=1.8, label=f'Median: {df_utama[columns_filter[0]].median():,.1f}')

  # Menambahkan labels, titles, legends
  ax.set_xlabel(f'Range untuk {columns_filter[0]}', fontsize=12, fontweight='bold', labelpad=10)
  ax.ticklabel_format(style='plain', axis='x')
  ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, pos: f'{x:,.0f}'))
  ax.set_ylabel(f'Frekuensi Data', fontsize=12, fontweight='bold', labelpad=10)
  ax.ticklabel_format(style='plain', axis='y')
  ax.set_title(f'Histogram Data {columns_filter[0].title()}', fontsize=14, fontweight='bold', pad=10)
  ax.legend()

  # Menampilkan Visualisasi
  plt.tight_layout()
  plt.show()

# Fungsi untuk keterangan menampilkan konfirmasi kembali ke menu utama
def kembali():
    print('-' * 100)
    print('Anda akan kembali ke menu utama')
    print('-' * 100)

# Fungsi untuk keterangan mengakhirkan proses/keluar dari dashboard
def selesai():
    print('=' * 100)
    print("Terima kasih telah menggunakan dashboard ini. Sampai jumpa!")
    print('=' * 100)

# Fungsi untuk kembali ke menu utama atau keluar dari dashboard
def kembali_ke_menu():
    menu_awal = input('\nKembali ke menu utama? (Y/N): ').upper()
    if menu_awal == 'Y':
        kembali()
        return True   # sinyal: lanjut ke menu utama
    else:
        selesai()
        return False  # sinyal: keluar dari program
# ----------------------------------------------
# Tampilan Menu Utama
# ----------------------------------------------
while True:
  print(
    """
      ╔═══════════════════════════════════════════╗
      ║   DASHBOARD RENTAL MOBIL — PT. XYZ        ║
      ╠═══════════════════════════════════════════╣
      ║  1. 📋  Manajemen Data Rental             ║
      ║  2. 📊  Statistik & Visualisasi Penyewaan ║
      ║  3. 🔧  Kalkulator Estimasi Biaya Sewa    ║
      ║  4. 🚪  Keluar dari Dashboard             ║
      ╚═══════════════════════════════════════════╝
    """)
  menu = int(input('Masukkan angka Menu yang ingin dijalankan: '))

# ----------------------------------------------
# Fungsi 1: Manajemen Data
# ----------------------------------------------
  if menu == 1:
      print("""
      MENU MANAJEMEN DATA:
      1. Lihat Semua Data Rental
      2. Lihat Mobil yang Tersedia
      3. Cari Pelanggan
      4. Tambah Pelanggan Baru
      5. Tambah Data Penyewaan Baru
      6. Update Status Sewa Mobil
      7. Kembali ke Menu Utama
      """)
      
      menu_manajemen = int(input('Pilih angka Menu Manajemen Data: '))

      if menu_manajemen == 1: # Menampilkan Semua Data Rental
        df_lengkap = sql_df('''
            SELECT p.*, r.tgl_mulai, m.merek, r.durasi_hari, r.total_harga, pyr.metode_bayar
            FROM pelanggan p
            JOIN rental r ON p.id_pelanggan = r.id_pelanggan
            JOIN mobil m ON r.id_mobil = m.id_mobil
            JOIN pembayaran pyr ON r.id_rental = pyr.id_rental
            ORDER BY p.id_pelanggan
        ''')
        print()
        print(f'Per Tanggal {today} Terdapat {len(df_lengkap)} data pelanggan rental \n')
        print(df_lengkap.to_string(index=False))

        # Pemanggilan Fungsi kembali ke Menu
        if kembali_ke_menu():
          continue
        else: 
          break 

      elif menu_manajemen == 2: # Menampilkan Data Mobil yang Tersedia
        print('Berikut list mobil yang tersedia: ')
        print(df_mobil_tersedia.to_string(index=False))

        # Pemanggilan Fungsi kembali ke Menu
        if kembali_ke_menu():
          continue
        else: 
          break 

      elif menu_manajemen == 3: # Memanggil Fungsi Cari Pelanggan
        cari_pelanggan()

       # Pemanggilan Fungsi kembali ke Menu
        if kembali_ke_menu():
          continue
        else: 
          break 

      elif menu_manajemen == 4: # Memanggil Fungsi Tambah Pelanggan
        tambah_pelanggan()

        # Pemanggilan Fungsi kembali ke Menu
        if kembali_ke_menu():
          continue
        else: 
          break 

      elif menu_manajemen == 5: # Memanggil Fungsi Tambah Sewa Mobil
        tambah_sewa()

        # Pemanggilan Fungsi kembali ke Menu
        if kembali_ke_menu():
          continue
        else: 
          break 

      elif menu_manajemen == 6: # Memanggil Fungsi Update Status Sewa Mobil
        update_sewa()
         
        # Pemanggilan Fungsi kembali ke Menu
        if kembali_ke_menu():
          continue
        else: 
          break 

      else:
        kembali()
        continue
  
# ----------------------------------------------
# Fungsi 2: Statistik Penyewaan 
# ----------------------------------------------
  if menu == 2:
     print("""
     MENU STATISTIK & VISUALISASI PENYEWAAN:
     1. Informasi Dataset PT XYZ
     2. Statistik Dasar Dataset PT XYZ
     3. Statistik & Visualisasi Pendapatan per Kota
     4. ⁠Statistik & Visualisasi Pendapatan per Bulan
     5. Statistik & Visualisasi Pendapatan per Kategori Mobil
     6. Kembali ke Menu Utama
     """)

     menu_statistik = int(input('Pilih angka Menu Statistik & Visualisasi Penyewaan: '))

     if menu_statistik == 1: # Informasi Dataset PT XYZ 
      print(f'Dataset PT XYZ terdapat {df_utama.shape[0]} baris dan {df_utama.shape[1]} kolom \n')
      print(f'Kolom dataset: {list(df_utama.columns)}\n')
      print(f'5 Data pertama adalah: \n{df_utama.head()} \n')
      print(f'5 Data terakhir adalah: \n{df_utama.tail()} \n')
      print('Informasi lebih lengkap mengenai dataset:')
      print(f'{df_utama.info()}')

      # Pemanggilan Fungsi kembali ke Menu
      if kembali_ke_menu():
        continue
      else: 
        break 
      
     elif menu_statistik == 2: # Statistik Dasar Dataset PT XYZ 
      print("""
    Silakan untuk memilih data statistik dasar dataset yang tersedia berdasarkan data penjualan:
    --------- Data Numerik -----------
    1. Durasi Hari 
    2. Total Harga 
    3. Harga per Hari 
    --------- Data Kategori ----------
    4. Kota Pelanggan 
    5. Merek Mobil 
    6. Kategori Mobil 
    7. Status Sewa 
    8. Metode Bayar Pelanggan 
            """)
      stat_filter = int(input('Data Statistik yang akan ditampilkan: '))
      print()

      # Memanggil Fungsi Statistik Dasar
      statistik_dasar(stat_filter) 
 
      # Konfirmasi untuk menampilkan Chart
      print()
      visual_show = input('Tampilkan Visualisasi Data Statistik Dasar Dataset PT XYZ? (Y/N): ').upper()
      
      if visual_show == 'Y':
        print('Menampilkan Visualisasi Data...')
        if stat_filter <= 3:  # Menampilkan Histogram untuk Data Numerik
          visualisasi_numerik()
        else:  # Menampilkan Bar Chart Horizontal untuk Data Kategori
          visualisasi_kategori()

      # Pemanggilan Fungsi kembali ke Menu
      if kembali_ke_menu():
        continue
      else: 
        break 

     elif menu_statistik == 3: # Statistik Persebaran Rental di seluruh Kota
      print('Berikut Statistik Persebaran Rental dikelompokkan Kota: ')

      persebaran_rental = df_utama.groupby('kota').agg(
        jumlah_pelanggan=('id_pelanggan', 'nunique'),
        total_pendapatan=('total_harga', 'sum'),
        kategori_paling_laku=('kategori', lambda x: x.mode().iloc[0]),
        metode_bayar_paling_laku=('metode_bayar', lambda x: x.mode().iloc[0] )
      )

      persebaran_rental = persebaran_rental.reset_index()
      
      print(persebaran_rental.sort_values('jumlah_pelanggan', ascending=False).to_string(index=False, formatters={'total_pendapatan': '{:,.0f}'.format}))
      
      kota_terbanyak = persebaran_rental[persebaran_rental['jumlah_pelanggan'] == persebaran_rental['jumlah_pelanggan'].max()]
      kota_tersedikit = persebaran_rental[persebaran_rental['jumlah_pelanggan'] == persebaran_rental['jumlah_pelanggan'].min()]

      kota_max_pendapatan = persebaran_rental.loc[persebaran_rental['total_pendapatan'].idxmax()]
      kota_min_pendapatan = persebaran_rental.loc[persebaran_rental['total_pendapatan'].idxmin()]

      kategori_laku = persebaran_rental['kategori_paling_laku'].mode()
      metode_laku = persebaran_rental['metode_bayar_paling_laku'].mode()

      print()
      print('INFORMASI STATISTIK PT XYZ:')
      print(f'- Kota dengan paling banyak pelanggan adalah: {kota_terbanyak['kota'].tolist()}')
      print(f'- Kota dengan paling sedikit pelanggan adalah: {kota_tersedikit['kota'].tolist()}')
      print(f'- Kota dengan pendapatan tertinggi adalah: {kota_max_pendapatan['kota']} dengan pendapatan sebesar Rp {persebaran_rental['total_pendapatan'].max():,.0f} ')
      print(f'- Kota dengan pendapatan terendah adalah: {kota_min_pendapatan['kota']} dengan pendapatan sebesar Rp {persebaran_rental['total_pendapatan'].min():,.0f} ')
      print(f'- Kategori Mobil Paling Laku di PT XYZ adalah: {kategori_laku.tolist()}')
      print(f'- Metode Pembayaran Paling Laku di PT XYZ adalah: {metode_laku.tolist()}')
      print()
      
      visual_show = input('Tampilkan Visualisasi Data Statistik Persebaran Rental PT XYZ? (Y/N): ').upper()

      if visual_show == 'Y':
        print('Menampilkan Visualisasi Data...')
        
        # Set Up Kanvas untuk Menampilkan Chart
        fig, axes = plt.subplots(3, 2, figsize=(16, 10))
        ax = axes.flatten()

        # Chart 1 - Bar Chart Jumlah Pelanggan
        x0 = persebaran_rental['kota']
        y0 = persebaran_rental['jumlah_pelanggan']
        
        bar0 = ax[0].bar(x0, y0, color="#82b0ff", edgecolor='black')

        # Menambahkan labels, titles, legends
        ax[0].set_xlabel(f'Kota', fontsize=10, fontweight='bold', labelpad=10)
        ax[0].set_ylabel(f'Jumlah Pelanggan', fontsize=10, fontweight='bold', labelpad=10)
        ax[0].set_title(f'Jumlah Pelanggan per Kota ', fontsize=14, fontweight='bold', pad=10)
        ax[0].bar_label(bar0, label_type='center')
        ax[0].set_xticks(range(len(x0)),labels=x0, rotation=90)
        
        # Chart 2 - Bar Chart Revenue per City
        x1 = persebaran_rental['kota']
        y1 = persebaran_rental['total_pendapatan']
        
        bar1 = ax[1].bar(x1, y1, color="#f98c60", edgecolor='black')

        # Menambahkan labels, titles, legends
        ax[1].set_xlabel(f'Kota', fontsize=10, fontweight='bold', labelpad=10)
        ax[1].set_ylabel(f'Total Pendapatan (Juta)', fontsize=10, fontweight='bold', labelpad=10)
        ax[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, pos: f'{x/1000000:,.1f}'))
        ax[1].set_title(f'Total Pendapatan (Juta) per Kota ', fontsize=14, fontweight='bold', pad=10)
        ax[1].bar_label(bar1, fmt=lambda x: f'{x/1000000:,.1f}' ,label_type='edge')
        ax[1].set_xticks(range(len(x1)),labels=x1, rotation=90)

        # Chart 3 - Scatter Plot Customers vs Revenue
        x2 = persebaran_rental['jumlah_pelanggan']
        y2 = persebaran_rental['total_pendapatan']
        
        ax[2].scatter(x2, y2, c="#3bca4e", edgecolor='black')

        # Menambahkan labels, titles, legends
        ax[2].set_xlabel(f'Jumlah Pelanggan', fontsize=10, fontweight='bold', labelpad=10)
        ax[2].set_ylabel(f'Total Pendapatan (Juta)', fontsize=10, fontweight='bold', labelpad=10)
        ax[2].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, pos: f'{x/1000000:,.1f}'))
        ax[2].set_title(f'Scatter Plot antara Jumlah Pelanggan & Total Pendapatan', fontsize=14, fontweight='bold', pad=10)

        # Chart 4 - Pie Chart Car Category
        y3 = persebaran_rental['kategori_paling_laku'].value_counts()

        ax[3].pie(y3.values, labels=y3.index, colors=['#e8a5a5', '#a5c8e8', '#a5e8b8', '#dea5e8'], autopct='%1.0f%%', textprops={'fontsize': 10, 'color': 'black'}, radius=1.2, shadow=True)

        # Menambahkan labels, titles, legends
        ax[3].set_title(f'Distribusi Kategori Mobil Paling Laku', fontsize=14, fontweight='bold', pad=15)

        # Chart 5 - Pie Chart Payment Method
        y4 = persebaran_rental['metode_bayar_paling_laku'].value_counts()

        ax[4].pie(y4.values, labels=y4.index, colors=['#e8a5a5', '#a5c8e8', '#a5e8b8', '#dea5e8'], autopct='%1.0f%%', textprops={'fontsize': 10, 'color': 'black'}, radius=1.2, wedgeprops={'width': 0.6, 'edgecolor': 'white', 'linewidth': 2}, pctdistance=0.75)

        # Menambahkan labels, titles, legends
        ax[4].set_title(f'Distribusi Metode Pembayaran Paling Laku', fontsize=14, fontweight='bold', pad=15)

        # Chart 6 - Average Revenue per Customer
        persebaran_rental['rata_rata_pendapatan'] = persebaran_rental['total_pendapatan']/persebaran_rental['jumlah_pelanggan']
        persebaran_rental['rata_rata_pendapatan'] = persebaran_rental['rata_rata_pendapatan'].round(0)
        persebaran_rental = persebaran_rental.sort_values(by='rata_rata_pendapatan',ascending=True)

        x5 = persebaran_rental['kota']
        y5 = persebaran_rental['rata_rata_pendapatan']

        bar5 = ax[5].barh(x5[-5:], y5[-5:], color="#faf757", edgecolor='black') # Top 5 Only

        # Menambahkan labels, titles, legends
        ax[5].set_xlabel(f'Rata-rata Pendapatan (Jt)', fontsize=10, fontweight='bold', labelpad=10)
        ax[5].set_ylabel(f'Kota', fontsize=10, fontweight='bold', labelpad=10)
        ax[5].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, pos: f'{x/1000000:,.1f}'))
        ax[5].set_title(f'Top 5 Kota Rata-Rata Pendapatan Tertinggi per Pelanggan ', fontsize=14, fontweight='bold', pad=10)
        ax[5].bar_label(bar5, padding=3, fmt=lambda x: f'{x/1000000:.1f}')

        # Menampilkan Visualisasi
        fig.suptitle('Visualisasi Statistik Persebaran Data Rental PT XYZ', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.show()

      # Pemanggilan Fungsi kembali ke Menu
      if kembali_ke_menu():
        continue
      else: 
        break 

     elif menu_statistik == 4: # Statistik Pendapatan Rental per Bulan
      print('Berikut Statistik Pendapatan Per Bulan PT XYZ (status rental = Selesai dan Aktif)')
      df_pendapatan_bulanan = sql_df(f"""
                                    SELECT MONTHNAME(pyr.tgl_bayar) AS bulan, SUM(pyr.jumlah_bayar) AS total_pendapatan, COUNT(pyr.id_pembayaran) AS jumlah_transaksi
                                    FROM rental r
                                    JOIN pembayaran pyr ON r.id_rental = pyr.id_rental
                                    WHERE r.status_rental in ('Selesai','Aktif') 
                                    GROUP BY MONTH(pyr.tgl_bayar), bulan
                                    ORDER BY MONTH(pyr.tgl_bayar)
                                     """)
      print(df_pendapatan_bulanan.to_string(index=False, formatters={'total_pendapatan': '{:,.0f}'.format}))

      # Perhitungan Beberapa statistik tertinggi & terendah untuk menampilkan insights tambahan 
      bulan_rev_tertinggi = df_pendapatan_bulanan[df_pendapatan_bulanan['total_pendapatan'] == df_pendapatan_bulanan['total_pendapatan'].max()]
      bulan_rev_terendah = df_pendapatan_bulanan[df_pendapatan_bulanan['total_pendapatan'] == df_pendapatan_bulanan['total_pendapatan'].min()]

      bulan_trx_tertinggi = df_pendapatan_bulanan[df_pendapatan_bulanan['jumlah_transaksi'] == df_pendapatan_bulanan['jumlah_transaksi'].max()]
      bulan_trx_terendah = df_pendapatan_bulanan[df_pendapatan_bulanan['jumlah_transaksi'] == df_pendapatan_bulanan['jumlah_transaksi'].min()]

      print(f"""
INSIGHTS PENDAPTAN PER BULAN PT XYZ: 
- Bulan dengan Pendapatan Tertinggi: {bulan_rev_tertinggi['bulan'].tolist()} senilai Rp {df_pendapatan_bulanan['total_pendapatan'].max():,}
- Bulan dengan Transaksi Tertinggi: {bulan_trx_tertinggi['bulan'].tolist()} sebanyak {df_pendapatan_bulanan['jumlah_transaksi'].max()} transaksi
- Bulan dengan Pendapatan Terendah: {bulan_rev_terendah['bulan'].tolist()} senilai Rp {df_pendapatan_bulanan['total_pendapatan'].min():,}
- Bulan dengan Transaksi Terendah: {bulan_trx_terendah['bulan'].tolist()} sebanyak {df_pendapatan_bulanan['jumlah_transaksi'].min()} transaksi
            """)
      
      visual_show = input('Tampilkan Visualisasi Pendapatan per Bulan PT XYZ? (Y/N): ').upper()
      
      if visual_show == 'Y': 
        print('Menampilkan Visualisasi Data...')
        
        # Set Up Kanvas & Variable Relevan untuk Menampilkan Chart
        bulan = df_pendapatan_bulanan['bulan']
        pendapatan = df_pendapatan_bulanan['total_pendapatan']
        transaksi = df_pendapatan_bulanan['jumlah_transaksi']
                
        fig, axes = plt.subplots(1, 2, figsize=(13, 5))

        # Visualisasi Bagian Kiri - Pendapatan per Bulan
        axes[0].plot(bulan, pendapatan,
             label='Pendapatan Bulanan', marker='o', linewidth=2, color="#E32E27")
        
        axes[0].set_title('Pendapatan Bulanan', fontsize=12, fontweight='bold')
        axes[0].set_xlabel('Bulan')
        axes[0].set_ylabel('Pendapatan (dalam juta)')
        axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, pos: f'{x/1000000:,.1f}'))
        axes[0].set_xticks(range(len(bulan)), labels=bulan, rotation=30, ha='right')   
        
        # Menampilkan Data Label
        for x, y in zip(bulan, pendapatan):
           axes[0].text(
                    x,
                    y,
                    str(f'{y/1000000:.1f}'),
                    ha='center',
                    va='baseline'
                    )
        
        # Visualisasi Bagian Kanan - Transaksi per Bulan
        axes[1].plot(bulan, transaksi,
             label='Transaksi Bulanan', marker='s', linewidth=2, color="#EB9868", linestyle='--')
        
        axes[1].set_title('Transaksi Bulanan', fontsize=12, fontweight='bold')
        axes[1].set_xlabel('Bulan')
        axes[1].set_ylabel('Jumlah Transaksi')
        axes[1].set_xticks(range(len(bulan)), labels=bulan, rotation=30, ha='right')

        # Menampilkan Data Label
        for x, y in zip(bulan, transaksi):
           axes[1].text(
                    x,
                    y,
                    str(y),
                    ha='center',
                    va='baseline'
                    )
        
        # Menampilkan Visualisasi 
        fig.suptitle('Visualisasi Pendapatan & Transaksi Per Bulan PT XYZ', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.show()

      # Pemanggilan Fungsi kembali ke Menu
      if kembali_ke_menu():
        continue
      else: 
        break  

     elif menu_statistik == 5: # ⁠Statistik Pendapatan per Kategori Mobil 
      print('Berikut Statistik Pendapatan per Kategori Mobil PT XYZ (status rental = Selesai dan Aktif)')
      df_statistik_mobil = sql_df(f"""
                                    SELECT m.kategori AS kategori_mobil, COUNT(DISTINCT m.merek) AS jumlah_mobil, COUNT(r.id_rental) AS jumlah_transaksi, AVG(m.harga_per_hari) AS rata_rata_sewa, SUM(r.total_harga) AS total_pendapatan
                                    FROM mobil m
                                    JOIN rental r ON r.id_mobil = m.id_mobil
                                    JOIN pembayaran pyr ON r.id_rental = pyr.id_rental
                                    WHERE r.status_rental in ('Selesai','Aktif') 
                                    GROUP BY kategori_mobil
                                    ORDER BY total_pendapatan
                                     """)
      print(df_statistik_mobil.sort_values('total_pendapatan',ascending=False).to_string(index=False, formatters={'total_pendapatan': '{:,.0f}'.format, 'rata_rata_sewa': '{:,.0f}'.format}))
      print()

      visual_show = input('Tampilkan Visualisasi Data Statistik Kategori Mobil PT XYZ? (Y/N): ').upper()
      
      if visual_show == 'Y': 
        print('Menampilkan Visualisasi Data...')

        # Set Up Kanvas untuk Menampilkan Chart
        fig, axes = plt.subplots(2, 2, figsize=(13, 5))
        ax = axes.flatten()

        # Set Up Tema dari Seaborn
        sns.set_theme(style='whitegrid', palette='deep')

        # Chart 1 - Bar Chart Jumlah Mobil per Kategori
        sns.barplot(data=df_statistik_mobil, x='kategori_mobil', y='jumlah_mobil', ax=ax[0], hue='kategori_mobil', legend=False)
        ax[0].set_title('Jumlah Mobil per Kategori')
        ax[0].set_xlabel('')
        ax[0].set_ylabel('Jumlah Mobil')

        # Chart 2 - Bar Chart Jumlah Pendapatan per Kategori
        sns.barplot(data=df_statistik_mobil, x='kategori_mobil', y='total_pendapatan', ax=ax[1], hue='kategori_mobil', legend=False)
        ax[1].set_title('Total Pendapatan per Kategori')
        ax[1].set_xlabel('')
        ax[1].set_ylabel('Total Pendapatan (Juta)')
        ax[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, pos: f'{x/1000000:,.1f}'))

        # Chart 3 - Bar Chart Horizontal Rata Rata Sewa per Kategori
        df_stat_sorted = df_statistik_mobil.sort_values(by='rata_rata_sewa', ascending=True)

        sns.barplot(data=df_stat_sorted, x='rata_rata_sewa', y='kategori_mobil', ax=ax[2], hue='kategori_mobil', legend=False, orient='h')
        ax[2].set_title('Rata-rata Sewa per Kategori')
        ax[2].set_ylabel('')
        ax[2].set_xlabel('Rata-rata Sewa (IDR)')
        ax[2].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, pos: f'{x:,.0f}'))

        # Chart 4 - Scatterplot Jumlah Transaksi x Jumlah Mobil 
        df_statistik_mobil['total_pendapatan'] = df_statistik_mobil['total_pendapatan'].astype(float) 

        sns.scatterplot(
          data=df_statistik_mobil, x='jumlah_mobil', y='jumlah_transaksi',
          size='total_pendapatan', sizes=(100,1000), hue='kategori_mobil', ax=ax[3], legend=False
        ) 

        for i, row in df_statistik_mobil.iterrows(): # Menampilkan label kategori mobil 
          ax[3].text(row['jumlah_mobil']+0.2, row['jumlah_transaksi'], row['kategori_mobil'], fontsize=9)
        
        ax[3].set_title('Utilisasi: Jumlah Mobil vs Transaksi\n(ukuran = pendapatan)')
        ax[3].set_ylabel('Jumlah Transaksi')
        ax[3].set_xlabel('Jumlah Mobil')

        # Menampilkan Visualisasi Chart
        fig.suptitle('Visualisasi Data Statistik Kategori Mobil', fontweight='bold', fontsize=14)
        plt.tight_layout()
        plt.show()

      # Pemanggilan Fungsi kembali ke Menu
      if kembali_ke_menu():
        continue
      else: 
        break  
     
     else:
        kembali()
        continue


# # ----------------------------------------------
# # Fungsi 3: Kalkulator Estimasi Biaya 
# # ----------------------------------------------
  if menu == 3: # Tools Kalkulator Estimasi Biaya Sewa
      menu_kalkulator = input('Apakah Anda akan melakukan kalkulasi estimasi Biaya Rental? (Y/N): ').upper()
      
      if menu_kalkulator == 'Y' :  # Jika memilih 'Y' untuk melakukan estimasi Biaya Rental
        # Menampilkan Daftar Mobil yang Tersedia menggunakan Query SQL
        
        print()
        print('=' * 100)
        print('Berikut List dari Mobil yang Tersedia/Tidak Disewa')
        print('=' * 100)
        print(df_mobil_tersedia.to_string(index=False))
        print()
        
        # Proses input memilih mobil berdasarkan ID mobil 
        id_mobil_sewa = int(input('Silakan input ID mobil yang akan di sewa: '))
        
        # Jika ID Mobil yang dipilih tersedia, maka proses akan dilanjutkan
        if id_mobil_sewa in df_mobil_tersedia['id_mobil'].values: 
          
          # Proses input estimasi hari sewa mobil 
          hari_mobil_sewa = int(input('Silakan input berapa hari mobil akan di sewa: '))
          
          # Extract data mobil berdasarkan input id_mobil_sewa
          mobil_pilihan = df_mobil_tersedia[df_mobil_tersedia['id_mobil'] == id_mobil_sewa] 
          
          # Output Variable berupa Nama Mobil, Kategori Mobil, Harga per Hari yang akan ditampilkan di summary kalkulasi sewa mobil
          nama_mobil = mobil_pilihan['merek'].values[0] 
          kategori_mobil = mobil_pilihan['kategori'].values[0]
          harga_mobil = mobil_pilihan['harga_per_hari'].values[0]

          print()
          print('Terima Kasih atas Input Anda. Berikut estimasi sewa mobil: ')
          print(f"""
          Nama Mobil  : {nama_mobil}
          Kategori    : {kategori_mobil}
          Harga/hari  : Rp {harga_mobil:,} per hari
          Durasi      : {hari_mobil_sewa} hari
          Est. Total  : Rp {harga_mobil * hari_mobil_sewa:,}
          """)
         
          # Pemanggilan Fungsi kembali ke Menu
          if kembali_ke_menu():
            continue
          else: 
            break 

        # Jika ID Mobil yang dipilih tidak tersedia, maka proses akan diberhentikan dan kembali ke menu utama
        else:
           print('-' * 100)
           print('Pilihan ID mobil tidak tersedia - Anda akan kembali ke menu utama')
           print('-' * 100)
           continue
        
      # Jika memilih 'N' untuk tidak melakukan estimasi Biaya Rental dan kembali ke menu utama
      else: 
        kembali()
        continue
          
# ----------------------------------------------
# Fungsi 4 : Fungsi Exit Program 
# ----------------------------------------------
  if menu == 4:  # Keluar dari Program 
      selesai()
      break