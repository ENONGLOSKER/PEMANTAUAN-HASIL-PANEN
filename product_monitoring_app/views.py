from django.shortcuts import render, redirect, get_object_or_404
from .models import Tanaman, HasilPanen, Pendapatan, BiayaOperasional
from .forms import HasilPanenForm, BiayaOperasionalForm, PendapatanForm, TanamanForm
from django.db.models import Sum, Avg
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json
from decimal import Decimal


# fitur TAMBAHAN -------------------------------
@login_required 
def prediksi_hasil_panen(request):
    

    context = {
    }
    return render(request, 'prediksi.html', context)
@login_required 
def statistik_laba_rugi(request):
    total_pendapatan = Pendapatan.objects.aggregate(total_pendapatan=Sum('total_pendapatan'))['total_pendapatan'] or 0
    total_biaya = BiayaOperasional.objects.aggregate(total_biaya=Sum('jumlah_biaya'))['total_biaya'] or 0
    laba_rugi = total_pendapatan - total_biaya

    context = {
        'total_pendapatan': total_pendapatan,
        'total_biaya': total_biaya,
        'laba_rugi': laba_rugi,
    }
    return render(request, 'statistik_laba_rugi.html', context)


# auth -------------------------------
def signout_user(request):
    logout(request)
    messages.success(request, "Logout berhasil!")
    return redirect("index")
def signup_user(request):
    if request.method == "POST":
        email = request.POST["email"]
        username = request.POST["username"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        
        if password != confirm_password:
            messages.error(request, "Password tidak cocok!")
            return redirect("signup")
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username sudah digunakan!")
            return redirect("signup")
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Akun berhasil dibuat! Silakan login.")
        return redirect("signin")
    
    return render(request, "signup.html")
def signin_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Login berhasil!")
            if user.is_superuser:
                return redirect('dashboard')
            else:
                return redirect('dashboard')
        else:
            messages.error(request, "Username atau password salah!")
            return redirect("signin")
    
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('dashboard')
        else:
            return redirect('index')
    
    return render(request, "singin.html")

def index(request):
    return render(request, 'index.html')

# DASHBOARD
@login_required 
def dashboard(request):
    total_hasil_panen = HasilPanen.objects.aggregate(total=Sum('jumlah_panen'))['total'] or 0
    total_pendapatan = Pendapatan.objects.aggregate(total=Sum('total_pendapatan'))['total'] or 0
    total_biaya_operasional = BiayaOperasional.objects.aggregate(total=Sum('jumlah_biaya'))['total'] or 0

    # Hitung laba atau rugi
    laba_rugi = total_pendapatan - total_biaya_operasional
    if laba_rugi > 0:
        status_laba_rugi = f"Laba {laba_rugi/total_biaya_operasional*100:.2f}%"
    elif laba_rugi < 0:
        status_laba_rugi = f"Rugi {abs(laba_rugi)/total_biaya_operasional*100:.2f}%"
    else:
        status_laba_rugi = "Impas"

     # grafik
    data = HasilPanen.objects.values('tanggal_panen').annotate(total_panen=Sum('jumlah_panen'))
    labels = [item['tanggal_panen'].strftime('%Y-%m-%d') for item in data]
    values = [float(item['total_panen']) for item in data]


    context = {
        'total_hasil_panen': total_hasil_panen,
        'total_pendapatan': total_pendapatan,
        'total_biaya_operasional': total_biaya_operasional,
        'labels': labels,
        'values': values,
        'status_laba_rugi': status_laba_rugi,
    }

    return render(request, 'dashboards.html', context)

def convert_decimal(data):
    """Konversi semua nilai Decimal menjadi float."""
    for item in data:
        for key, value in item.items():
            if isinstance(value, Decimal):
                item[key] = float(value)
    return data
def statistik_panen(request):
    # Statistik berdasarkan musim
    statistik_musim = list(HasilPanen.objects.values('musim_tanam').annotate(total_panen=Sum('jumlah_panen')))
    statistik_musim = convert_decimal(statistik_musim)

    # Statistik berdasarkan jenis tanaman
    statistik_jenis = list(HasilPanen.objects.values('tanaman__nama_tanaman').annotate(total_panen=Sum('jumlah_panen')))
    statistik_jenis = convert_decimal(statistik_jenis)

    # Statistik berdasarkan lokasi
    statistik_lokasi = list(HasilPanen.objects.values('lokasi_lahan').annotate(total_panen=Sum('jumlah_panen')))
    statistik_lokasi = convert_decimal(statistik_lokasi)

    # Rekomendasi tanam berdasarkan produktivitas tertinggi
    rekomendasi = []
    for item in statistik_musim:
        musim = item['musim_tanam']
        hasil_tertinggi = HasilPanen.objects.filter(musim_tanam=musim).order_by('-jumlah_panen').first()
        if hasil_tertinggi:
            rekomendasi.append({
                'musim': musim,
                'tanaman': hasil_tertinggi.tanaman.nama_tanaman,
                'produktivitas': float(hasil_tertinggi.jumlah_panen),  # Konversi langsung ke float
            })

    # grafik
    data = HasilPanen.objects.values('tanggal_panen').annotate(total_panen=Sum('jumlah_panen'))
    labels = [item['tanggal_panen'].strftime('%Y-%m-%d') for item in data]
    values = [float(item['total_panen']) for item in data]

    # Konversi ke JSON
    context = {
        'statistik_musim': json.dumps(statistik_musim),
        'statistik_jenis': json.dumps(statistik_jenis),
        'statistik_lokasi': json.dumps(statistik_lokasi),
        'rekomendasi': json.dumps(rekomendasi),
        'labels': labels,
        'values': values,
    }
    return render(request, 'db_statistik.html', context)

# BIAYA OPRASIONAL
@login_required
def biaya_oprasional(request):
    data = BiayaOperasional.objects.all()

    context = {
        'biaya':data,
    }
@login_required 
def input_biaya_operasional(request):
    if request.method == 'POST':
        form = BiayaOperasionalForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Biaya operasional berhasil ditambahkan.')
            return redirect('pendapatan')  # Redirect ke halaman dashboard setelah data disimpan
    else:
        form = BiayaOperasionalForm()
    
    # Total biaya operasional
    total_biaya = BiayaOperasional.objects.aggregate(total_biaya=Sum('jumlah_biaya'))['total_biaya'] or 0

    return render(request, 'db_form.html', {'form': form, 'total_biaya': total_biaya})
@login_required 
def edit_biaya_operasional(request, id):
    biaya_operasional = get_object_or_404(BiayaOperasional, id=id)
    if request.method == 'POST':
        form = BiayaOperasionalForm(request.POST, instance=biaya_operasional)
        if form.is_valid():
            form.save()
            messages.success(request, 'Biaya operasional berhasil diubah.')
            return redirect('pendapatan')
    else:
        form = BiayaOperasionalForm(instance=biaya_operasional)
    return render(request, 'db_form.html', {'form': form, 'biaya_operasional': biaya_operasional})
@login_required 
def delete_biaya_operasional(request, id):
    biaya_operasional = get_object_or_404(BiayaOperasional, id=id)
    biaya_operasional.delete()
    messages.success(request, 'Biaya operasional berhasil dihapus.')
    return redirect('pendapatan')

# PENDAPATAN
@login_required 
def pendapatan(request):
    pendapatan = Pendapatan.objects.all()
    biaya = BiayaOperasional.objects.all()

    context = {
        'pendapatan':pendapatan,
        'biaya':biaya,
    }
    return render(request, 'db_keuangan.html', context)
@login_required 
def input_pendapatan(request):
    if request.method == 'POST':
        form = PendapatanForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data pendapatan berhasil ditambahkan.')
            return redirect('pendapatan')  # Redirect ke halaman dashboard setelah data disimpan
    else:
        form = PendapatanForm()
    
    # Total pendapatan
    total_pendapatan = Pendapatan.objects.aggregate(total_pendapatan=Sum('total_pendapatan'))['total_pendapatan'] or 0
    return render(request, 'db_form.html', {'form': form, 'total_pendapatan': total_pendapatan})
@login_required 
def edit_pendapatan(request, id):
    pendapatan = get_object_or_404(Pendapatan, id=id)
    if request.method == 'POST':
        form = PendapatanForm(request.POST, instance=pendapatan)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data pendapatan berhasil diubah.')
            return redirect('pendapatan')
    else:
        form = PendapatanForm(instance=pendapatan)
    return render(request, 'db_form.html', {'form': form, 'pendapatan': pendapatan})
@login_required 
def delete_pendapatan(request, id):
    pendapatan = get_object_or_404(Pendapatan, id=id)
    pendapatan.delete()
    messages.success(request, 'Data pendapatan berhasil dihapus.')
    return redirect('pendapatan')

#TANAMAN
@login_required 
def input_tanaman(request):
    if request.method == 'POST':
        form = TanamanForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data tanaman berhasil ditambahkan.')
            return redirect('tanaman')
    else:
        form = TanamanForm()
    return render(request, 'db_form.html', {'form': form})
@login_required 
def edit_tanaman(request, id):
    tanaman = get_object_or_404(Tanaman, id=id)
    if request.method == 'POST':
        form = TanamanForm(request.POST, instance=tanaman)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data tanaman berhasil diubah.')
            return redirect('tanaman')
    else:
        form = TanamanForm(instance=tanaman)
    return render(request, 'db_form.html', {'form': form, 'tanaman': tanaman})
@login_required 
def delete_tanaman(request, id):
    tanaman = get_object_or_404(Tanaman, id=id)
    tanaman.delete()
    messages.success(request, 'Data tanaman berhasil dihapus.')
    return redirect('tanaman')
@login_required 
def tanaman(request):
    tanaman = Tanaman.objects.all()
    return render(request, 'db_tanaman.html', {'tanaman': tanaman})

# HASIL PANEN
@login_required 
def input_hasil_panen(request):
    
    if request.method == 'POST':
        form = HasilPanenForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data hasil panen berhasil ditambahkan.')
            return redirect('hasil_panen')
    else:
        form = HasilPanenForm()
    return render(request, 'db_form.html', {'form': form})
@login_required
def hasil_panen(request):
    hasil_panen = HasilPanen.objects.all()  # Admin melihat semua data
    return render(request, 'db_hasil_panen.html', {'hasil_panen': hasil_panen})
@login_required 
def edit_hasil_panen(request, id):
    hasil_panen = get_object_or_404(HasilPanen, id=id)
    if request.method == 'POST':
        form = HasilPanenForm(request.POST, instance=hasil_panen)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data hasil panen berhasil diubah.')
            return redirect('hasil_panen')
    else:
        form = HasilPanenForm(instance=hasil_panen)
    return render(request, 'db_form.html', {'form': form, 'hasil_panen': hasil_panen})
@login_required 
def delete_hasil_panen(request, id):
    hasil_panen = get_object_or_404(HasilPanen, id=id)
    hasil_panen.delete()
    messages.success(request, 'Data hasil panen berhasil dihapus.')
    return redirect('hasil_panen')
