# Creating New Database & Use the Database

CREATE DATABASE db_rental;
USE db_rental;

# -------------------------------------
# Rental Mobil Business Tables
# -------------------------------------

# Creating New Tables 

SHOW TABLES;

-- Table 1: Pelanggan 
CREATE TABLE pelanggan (
	id_pelanggan 	INT AUTO_INCREMENT PRIMARY KEY,
    nama			VARCHAR(100) NOT NULL,
    no_hp			VARCHAR(20) NOT NULL,
    kota			VARCHAR(100) NOT NULL,
    email			VARCHAR(100) NOT NULL
);

-- Table 2: Mobil 
CREATE TABLE mobil (
	id_mobil	 	INT AUTO_INCREMENT PRIMARY KEY,
    merek			VARCHAR(100) NOT NULL,
    kategori		VARCHAR(100) NOT NULL,
    harga_per_hari	INT NOT NULL,
    status			VARCHAR(100) NOT NULL
);

-- Table 3: Rental
CREATE TABLE rental (
	id_rental	 	INT AUTO_INCREMENT PRIMARY KEY,
    id_pelanggan	INT NOT NULL,
    id_mobil	 	INT NOT NULL,
    tgl_mulai		DATE NOT NULL,
    durasi_hari		INT NOT NULL,
    total_harga		INT NOT NULL,
    status_rental	VARCHAR(100) NOT NULL, 
    FOREIGN KEY (id_pelanggan) REFERENCES pelanggan(id_pelanggan),
    FOREIGN KEY (id_mobil) REFERENCES mobil(id_mobil)
);

-- Table 4: Pembayaran
CREATE TABLE pembayaran (
	id_pembayaran	INT AUTO_INCREMENT PRIMARY KEY,
    id_rental	 	INT NOT NULL,
    metode_bayar	VARCHAR(100) NOT NULL,
    jumlah_bayar	INT NOT NULL,
    tgl_bayar		DATE NOT NULL,
    FOREIGN KEY (id_rental) REFERENCES rental(id_rental)
);

# ---------------------------------
# Inserting Data into Table
# ---------------------------------

-- Table 1: Pelanggan Data
INSERT INTO pelanggan (nama, no_hp, kota, email) 
VALUES
('Budi Santoso',     '081234567890', 'Jakarta',   'budi.santoso@gmail.com'),
('Ani Rahayu',       '082345678901', 'Bandung',   'ani.rahayu@gmail.com'),
('Cahyo Pratama',    '083456789012', 'Surabaya',  'cahyo.pratama@gmail.com'),
('Dewi Lestari',     '084567890123', 'Yogyakarta','dewi.lestari@gmail.com'),
('Eko Wibowo',       '085678901234', 'Medan',     'eko.wibowo@gmail.com'),
('Fitri Handayani',  '086789012345', 'Semarang',  'fitri.handayani@gmail.com'),
('Gunawan Susanto',  '087890123456', 'Bali',      'gunawan.susanto@gmail.com'),
('Hani Kusuma',      '088901234567', 'Makassar',  'hani.kusuma@gmail.com'),
('Ivan Saputra',     '089012345678', 'Palembang', 'ivan.saputra@gmail.com'),
('Joko Purnomo',     '081123456789', 'Solo',      'joko.purnomo@gmail.com'),
('Rini Anggraini',    '081987654321', 'Bandung',    'rini.anggraini@gmail.com'),
('Doni Setiawan',     '082876543210', 'Surabaya',   'doni.setiawan@gmail.com'),
('Maya Sari',         '083765432109', 'Jakarta',    'maya.sari@gmail.com'),
('Agus Permana',      '084654321098', 'Semarang',   'agus.permana@gmail.com'),
('Sinta Dewi',        '085543210987', 'Bali',       'sinta.dewi@gmail.com'),
('Rizky Pratama',     '086432109876', 'Medan',      'rizky.pratama@gmail.com'),
('Nurul Hidayah',     '087321098765', 'Yogyakarta', 'nurul.hidayah@gmail.com'),
('Bagas Wicaksono',   '088210987654', 'Makassar',   'bagas.wicaksono@gmail.com'),
('Tia Lestari',       '089109876543', 'Solo',       'tia.lestari@gmail.com'),
('Fandi Ahmad',       '081098765432', 'Palembang',  'fandi.ahmad@gmail.com'),
('Lina Marlina',      '082987654321', 'Jakarta',    'lina.marlina@gmail.com'),
('Hendra Gunawan',    '083876543210', 'Bandung',    'hendra.gunawan@gmail.com'),
('Wulandari',         '084765432109', 'Surabaya',   'wulandari@gmail.com'),
('Arif Budiman',      '085654321098', 'Malang',     'arif.budiman@gmail.com'),
('Nadia Putri',       '086543210987', 'Bali',       'nadia.putri@gmail.com'),
('Yusuf Mahendra',    '087432109876', 'Jakarta',     'yusuf.mahendra@gmail.com'),
('Sri Wahyuni',       '088321098765', 'Jakarta',    'sri.wahyuni@gmail.com'),
('Dimas Aditya',      '089210987654', 'Semarang',   'dimas.aditya@gmail.com'),
('Kartika Sari',      '081209876543', 'Yogyakarta', 'kartika.sari@gmail.com'),
('Bambang Sugiarto',  '082108765432', 'Surabaya',   'bambang.sugiarto@gmail.com'),
('Lia Puspita',       '083097654321', 'Medan',      'lia.puspita@gmail.com'),
('Gilang Ramadhan',   '084986543210', 'Bandung',    'gilang.ramadhan@gmail.com'),
('Fitri Yuliani',     '085875432109', 'Jakarta',    'fitri.yuliani@gmail.com'),
('Rendi Kurniawan',   '086764321098', 'Makassar',   'rendi.kurniawan@gmail.com'),
('Amanda Putri',      '087653210987', 'Bali',       'amanda.putri@gmail.com'),
('Wahyu Santoso',     '088542109876', 'Solo',       'wahyu.santoso@gmail.com'),
('Novita Sari',       '089431098765', 'Palembang',  'novita.sari@gmail.com'),
('Andi Kusuma',       '081320987654', 'Semarang',   'andi.kusuma@gmail.com'),
('Melati Indah',      '082219876543', 'Yogyakarta', 'melati.indah@gmail.com'),
('Teguh Prasetyo',    '083108765432', 'Surabaya',   'teguh.prasetyo@gmail.com');

-- Table 2: Mobil Data
INSERT INTO mobil (merek, kategori, harga_per_hari, status) 
VALUES
('Toyota Avanza',    'MPV',       350000,  'Tersedia'),
('Honda Jazz',       'Hatchback', 300000,  'Disewa'),
('Mitsubishi Pajero','SUV',       750000,  'Tersedia'),
('Toyota Innova',    'MPV',       500000,  'Disewa'),
('Suzuki Ertiga',    'MPV',       350000,  'Tersedia'),
('Daihatsu Xenia',   'MPV',       320000,  'Maintenance'),
('Honda CR-V',       'SUV',       650000,  'Tersedia'),
('Toyota Camry',     'Sedan',     600000,  'Disewa'),
('Suzuki Jimny',     'SUV',       700000,  'Tersedia'),
('Daihatsu Sigra',   'Hatchback', 280000,  'Tersedia'),
('Honda Brio',           'Hatchback', 250000,  'Tersedia'),   
('Toyota Rush',          'SUV',       450000,  'Tersedia'),   
('Mitsubishi Xpander',   'MPV',       400000,  'Disewa'),     
('Nissan X-Trail',       'SUV',       600000,  'Tersedia'),   
('Hyundai Tucson',       'SUV',       550000,  'Tersedia'),   
('Honda HR-V',           'SUV',       500000,  'Disewa'),     
('Toyota Raize',         'SUV',       420000,  'Tersedia'),   
('Daihatsu Rocky',       'SUV',       400000,  'Tersedia'),   
('Suzuki Baleno',        'Hatchback', 300000,  'Tersedia'),   
('Toyota Veloz',         'MPV',       380000,  'Disewa'),     
('Honda Freed',          'MPV',       370000,  'Tersedia'),   
('Mitsubishi Outlander', 'SUV',       700000,  'Tersedia'),   
('Toyota Hilux',         'Pick-up',   550000,  'Tersedia'),  
('Isuzu Panther',        'MPV',       350000,  'Maintenance'),
('Mazda CX-5',           'SUV',       650000,  'Tersedia'),   
('Honda Mobilio',        'MPV',       330000,  'Tersedia'),   
('Toyota Fortuner',      'SUV',       800000,  'Disewa'),     
('Suzuki APV',           'MPV',       300000,  'Tersedia'),   
('Daihatsu Terios',      'SUV',       420000,  'Tersedia'),   
('Honda BR-V',           'SUV',       480000,  'Tersedia'),   
('Mitsubishi Galant',    'Sedan',     500000,  'Tersedia'),   
('Toyota Yaris',         'Hatchback', 290000,  'Disewa'),     
('Honda City',           'Sedan',     350000,  'Tersedia'),   
('Nissan Livina',        'MPV',       360000,  'Tersedia'),   
('Hyundai Creta',        'SUV',       520000,  'Tersedia'),   
('Toyota Sienta',        'MPV',       400000,  'Maintenance'),
('Suzuki Ignis',         'Hatchback', 270000,  'Tersedia'),   
('Suzuki XL7',           'SUV',       450000,  'Disewa'),     
('Daihatsu Gran Max',    'MPV',       280000,  'Tersedia'),   
('Toyota Alphard',       'MPV',       1500000, 'Tersedia');   

-- Table 3: Rental Data
-- Note: total_harga = harga_per_hari x durasi_hari

INSERT INTO rental (id_pelanggan, id_mobil, tgl_mulai, durasi_hari, total_harga, status_rental) 
VALUES
(1,  1,  '2025-11-01', 3,  1050000, 'Selesai'),     
(2,  2,  '2025-01-15', 5,  1500000, 'Aktif'),        
(3,  3,  '2025-12-10', 2,  1500000, 'Selesai'),      
(4,  4,  '2025-01-10', 7,  3500000, 'Aktif'),       
(5,  5,  '2025-10-20', 4,  1400000, 'Selesai'),      
(6,  6,  '2025-09-05', 3,   960000, 'Dibatalkan'),   
(7,  7,  '2025-11-15', 5,  3250000, 'Selesai'),      
(8,  8,  '2025-01-12', 6,  3600000, 'Aktif'),        
(9,  9,  '2025-12-20', 3,  2100000, 'Selesai'),      
(10, 10, '2025-12-01', 2,   560000, 'Selesai'),    
(11, 1,  '2025-08-05', 4, 1400000,  'Selesai'),    
(12, 3,  '2025-07-10', 2, 1500000,  'Selesai'),   
(13, 13, '2025-01-18', 5, 2000000,  'Aktif'),      
(14, 5,  '2025-06-15', 3, 1050000,  'Selesai'),    
(15, 7,  '2025-09-20', 4, 2600000,  'Selesai'),    
(16, 16, '2025-01-14', 3, 1500000,  'Aktif'),      
(17, 9,  '2025-08-01', 5, 3500000,  'Selesai'),    
(18, 10, '2025-10-10', 7, 1960000,  'Selesai'),    
(19, 11, '2025-11-20', 3, 750000,   'Selesai'),    
(20, 20, '2025-01-16', 4, 1520000,  'Aktif'),      
(21, 12, '2025-12-05', 5, 2250000,  'Selesai'),   
(22, 14, '2025-07-22', 3, 1800000,  'Selesai'),    
(23, 15, '2025-08-30', 6, 3300000,  'Selesai'),    
(24, 17, '2025-09-12', 4, 1680000,  'Dibatalkan'), 
(25, 27, '2025-01-17', 7, 5600000,  'Aktif'),      
(26, 18, '2025-10-05', 5, 2000000,  'Selesai'),    
(27, 19, '2025-11-08', 3, 900000,   'Selesai'),    
(28, 21, '2025-12-15', 4, 1480000,  'Selesai'),    
(29, 22, '2025-07-05', 2, 1400000,  'Selesai'),    
(30, 25, '2025-08-18', 5, 3250000,  'Selesai'),    
(31, 23, '2025-09-25', 3, 1650000,  'Selesai'),    
(32, 32, '2025-01-13', 6, 1740000,  'Aktif'),      
(33, 26, '2025-10-18', 4, 1320000,  'Selesai'),    
(34, 28, '2025-11-25', 5, 1500000,  'Selesai'),    
(35, 29, '2025-12-08', 3, 1260000,  'Selesai'),    
(36, 30, '2025-07-15', 7, 3360000,  'Selesai'),    
(37, 31, '2025-08-25', 4, 2000000,  'Dibatalkan'), 
(38, 38, '2025-01-19', 5, 2250000,  'Aktif'),      
(39, 33, '2025-09-30', 6, 2100000,  'Selesai'),    
(40, 34, '2025-10-22', 4, 1440000,  'Selesai');    

-- Table 4: Pembayaran Data
-- jumlah_bayar mengikuti total_harga dari rental masing-masing
INSERT INTO pembayaran (id_rental, metode_bayar, jumlah_bayar, tgl_bayar) 
VALUES
(1,  'Transfer',     1050000, '2025-11-01'),
(2,  'QRIS',         1500000, '2025-01-15'),
(3,  'Cash',         1500000, '2025-12-10'),
(4,  'Kartu Kredit', 3500000, '2025-01-10'),
(5,  'Transfer',     1400000, '2025-10-20'),
(6,  'Transfer',      960000, '2025-09-05'),
(7,  'Cash',         3250000, '2025-11-15'),
(8,  'QRIS',         3600000, '2025-01-12'),
(9,  'Kartu Kredit', 2100000, '2025-12-20'),
(10, 'Transfer',      560000, '2025-12-01'),
(11, 'Transfer',     1400000, '2025-08-05'),
(12, 'Cash',         1500000, '2025-07-10'),
(13, 'QRIS',         2000000, '2025-01-18'),
(14, 'Transfer',     1050000, '2025-06-15'),
(15, 'Kartu Kredit', 2600000, '2025-09-20'),
(16, 'Transfer',     1500000, '2025-01-14'),
(17, 'Cash',         3500000, '2025-08-01'),
(18, 'QRIS',         1960000, '2025-10-10'),
(19, 'Transfer',      750000, '2025-11-20'),
(20, 'Kartu Kredit', 1520000, '2025-01-16'),
(21, 'Cash',         2250000, '2025-12-05'),
(22, 'Transfer',     1800000, '2025-07-22'),
(23, 'QRIS',         3300000, '2025-08-30'),
(24, 'Transfer',     1680000, '2025-09-12'),
(25, 'Kartu Kredit', 5600000, '2025-01-17'),
(26, 'Cash',         2000000, '2025-10-05'),
(27, 'Transfer',      900000, '2025-11-08'),
(28, 'QRIS',         1480000, '2025-12-15'),
(29, 'Kartu Kredit', 1400000, '2025-07-05'),
(30, 'Transfer',     3250000, '2025-08-18'),
(31, 'Cash',         1650000, '2025-09-25'),
(32, 'QRIS',         1740000, '2025-01-13'),
(33, 'Transfer',     1320000, '2025-10-18'),
(34, 'Kartu Kredit', 1500000, '2025-11-25'),
(35, 'Transfer',     1260000, '2025-12-08'),
(36, 'Cash',         3360000, '2025-07-15'),
(37, 'Transfer',     2000000, '2025-08-25'),
(38, 'QRIS',         2250000, '2025-01-19'),
(39, 'Kartu Kredit', 2100000, '2025-09-30'),
(40, 'Transfer',     1440000, '2025-10-22');

# ---- Test Table

SELECT * FROM pelanggan;
SELECT * FROM mobil;
SELECT * FROM rental;
SELECT * FROM pembayaran;

# --- Drop Table Query
-- DROP TABLE IF EXISTS pelanggan, mobil, rental, pembayaran;
DELETE FROM pelanggan
WHERE id_pelanggan in (41);

DELETE FROM rental
WHERE id_rental in (41,42);

DELETE FROM pembayaran
WHERE id_pembayaran in (41);

# Alter Numbering
ALTER TABLE pelanggan AUTO_INCREMENT = 41;
ALTER TABLE rental AUTO_INCREMENT = 41;
ALTER TABLE pembayaran AUTO_INCREMENT = 41;