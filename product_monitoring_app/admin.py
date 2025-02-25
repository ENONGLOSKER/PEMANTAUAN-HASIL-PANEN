from django.contrib import admin
from django.contrib import admin
from .models import Tanaman, HasilPanen, BiayaOperasional, Pendapatan

@admin.register(Tanaman)
class TanamanAdmin(admin.ModelAdmin):
    list_display = ('nama_tanaman', 'jenis_tanaman', 'deskripsi')

@admin.register(HasilPanen)
class HasilPanenAdmin(admin.ModelAdmin):
    list_display = ('tanaman', 'jumlah_panen', 'tanggal_panen', 'lokasi_lahan')

@admin.register(BiayaOperasional)
class BiayaOperasionalAdmin(admin.ModelAdmin):
    list_display = ('kategori', 'jumlah_biaya', 'tanggal_pengeluaran')

@admin.register(Pendapatan)
class PendapatanAdmin(admin.ModelAdmin):
    list_display = ('hasil_panen', 'harga_per_kg', 'total_pendapatan')