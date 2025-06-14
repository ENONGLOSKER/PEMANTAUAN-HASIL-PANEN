from django import forms
from .models import Tanaman,HasilPanen, Pendapatan, BiayaOperasional


class TanamanForm(forms.ModelForm):
    class Meta:
        model = Tanaman
        fields = ['nama_tanaman', 'jenis_tanaman', 'deskripsi']

        widgets = {
            'nama_tanaman': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Tanaman'}),
            'jenis_tanaman': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Jenis Tanaman'}),
            'deskripsi': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Deskripsi'}),
        }


class PendapatanForm(forms.ModelForm):
    class Meta:
        model = Pendapatan
        fields = ['hasil_panen', 'harga_per_kg']

        widgets = {
        'hasil_panen': forms.Select(attrs={'class': 'form-control'}),
        'harga_per_kg': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_harga_per_kg(self):
        harga_per_kg = self.cleaned_data.get('harga_per_kg')
        if harga_per_kg <= 0:
            raise forms.ValidationError("Harga per kg harus lebih besar dari 0.")
        return harga_per_kg
    

class BiayaOperasionalForm(forms.ModelForm):
    class Meta:
        model = BiayaOperasional
        fields = ['hasil_panen', 'kategori', 'jumlah_biaya', 'tanggal_pengeluaran']
        widgets = {
            'hasil_panen': forms.Select(attrs={'class': 'form-control'}),
            'kategori': forms.Select(attrs={'class': 'form-control'}),
            'jumlah_biaya': forms.TextInput(attrs={'class': 'form-control'}),
            'tanggal_pengeluaran': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def clean_jumlah_biaya(self):
        jumlah_biaya = self.cleaned_data.get('jumlah_biaya')
        if jumlah_biaya <= 0:
            raise forms.ValidationError("Jumlah biaya harus lebih besar dari 0.")
        return jumlah_biaya
    
class HasilPanenForm(forms.ModelForm):
    class Meta:
        model = HasilPanen
        fields = ['tanaman', 'jumlah_panen', 'tanggal_panen', 'lokasi_lahan', 'musim_tanam']
        widgets = {
            'tanaman': forms.Select(attrs={'class': 'form-control'}),
            'jumlah_panen': forms.NumberInput(attrs={'class': 'form-control'}),
            'tanggal_panen': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'lokasi_lahan': forms.TextInput(attrs={'class': 'form-control'}),
            'musim_tanam': forms.Select(attrs={'class': 'form-control'}),
        }