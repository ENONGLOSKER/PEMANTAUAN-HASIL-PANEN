from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User Model
class Tanaman(models.Model):
    nama_tanaman = models.CharField(max_length=100)
    jenis_tanaman = models.CharField(max_length=50)  # Misal: Pangan, Hortikultura
    deskripsi = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nama_tanaman

class HasilPanen(models.Model):
    MUSIM_CHOICES = [
        ('musim_hujan', 'Musim Hujan'),
        ('musim_kemarau', 'Musim Kemarau'),
    ]

    tanaman = models.ForeignKey(Tanaman, on_delete=models.CASCADE)
    jumlah_panen = models.DecimalField(max_digits=10, decimal_places=2)  # Dalam kg
    tanggal_panen = models.DateField()
    lokasi_lahan = models.CharField(max_length=100)
    musim_tanam = models.CharField(max_length=50, choices=MUSIM_CHOICES)

    def __str__(self):
        return f"{self.tanaman.nama_tanaman} - {self.jumlah_panen} kg"
    
class BiayaOperasional(models.Model):
    KATEGORI_CHOICES = [
        ('pupuk', 'Pupuk'),
        ('pestisida', 'Pestisida'),
        ('tenaga_kerja', 'Tenaga Kerja'),
        ('lainnya', 'Lainnya'),
    ]

    hasil_panen = models.ForeignKey(HasilPanen, on_delete=models.CASCADE)
    kategori = models.CharField(max_length=50, choices=KATEGORI_CHOICES)
    jumlah_biaya = models.DecimalField(max_digits=10, decimal_places=2)  # Dalam Rupiah
    tanggal_pengeluaran = models.DateField()

    def __str__(self):
        return f"{self.kategori} - Rp{self.jumlah_biaya}"
    
class Pendapatan(models.Model):
    hasil_panen = models.ForeignKey(HasilPanen, on_delete=models.CASCADE)
    harga_per_kg = models.DecimalField(max_digits=10, decimal_places=2)  # Dalam Rupiah
    total_pendapatan = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Hitung total pendapatan otomatis
        self.total_pendapatan = self.hasil_panen.jumlah_panen * self.harga_per_kg
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Pendapatan dari {self.hasil_panen.tanaman.nama_tanaman}: Rp{self.total_pendapatan}"
    