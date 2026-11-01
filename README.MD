
projeyi çalıştırmak için gerekli komut ve işlemler:

! hata çıkarsa= -Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
python -m venv .venv

1-.venv aktif et =.\.venv\Scripts\Activate.ps1
 pip install -r .\requirements.txt
2-test edilecek resmi eval/test_set klasörünün üçüne koyun(jpeg,jpg veya png)

3-python -m scripts.test_receipt eval/test_set/fis.jpg



**Ödev** : bir fotoğrafı yan çevirip kaydet. Ön işleme olmadan ve olunca sonuç farkını karşılaştır.

modül 2 sonu: proje durumu
fotoğraf-vlm-şema-doğrulama zinciri çalışıyor.
