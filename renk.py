import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

st.title("🎨 Bilgisayar Görüsü ile Renk Tanıma Uygulaması")
st.write("Bir resim yükleyin ve piksel koordinatlarını girerek rengin adını öğrenin.")

# 1. Renk Veri Setini Yükle
index = ["color_code", "color_name", "hex", "R", "G", "B"]
df = pd.read_csv('colors.csv', names=index, header=None)


# 2. En Yakın Rengi Hesaplayan Fonksiyon
def get_color_name(R, G, B):
    minimum = 10000
    color_name = ""
    for i in range(len(df)):
        d = abs(R - int(df.loc[i, "R"])) + abs(G - int(df.loc[i, "G"])) + abs(B - int(df.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            color_name = df.loc[i, "color_name"]
    return color_name

# 3. Kullanıcıdan Resim Yüklemesini İste
uploaded_file = st.file_uploader("Lütfen bir resim seçin (JPG, JPEG, PNG)...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Resmi aç ve ekrana bas
    image = Image.open(uploaded_file)
    st.image(image, caption="Yüklenen Resim", use_container_width=True)
    
    # Resmin boyutlarını al
    img_array = np.array(image)
    height, width, _ = img_array.shape
    st.write(f"Resim Boyutları: {width}x{height} piksel")
    
    # 4. Piksel Seçim Alanları
    st.subheader("📍 Renk Analizi Yapılacak Noktayı Seçin")
    x = st.number_input("X Koordinatı (Genişlik)", min_value=0, max_value=width-1, value=int(width/2))
    y = st.number_input("Y Koordinatı (Yükseklik)", min_value=0, max_value=height-1, value=int(height/2))
    
    # Butona basıldığında rengi bul
    if st.button("Rengi Tespit Et"):
        # Seçilen koordinattaki RGB değerini al
        pixel_rgb = img_array[y, x]
        r, g, b = int(pixel_rgb[0]), int(pixel_rgb[1]), int(pixel_rgb[2])
        
        # En yakın renk ismini bul
        color_result = get_color_name(r, g, b)
        
        # Sonuçları ekrana renk kutusuyla bas
        st.markdown(f"### 🎯 Sonuç: **{color_result}**")
        st.write(f"**RGB Değerleri:** R:{r}, G:{g}, B:{b}")
        
        # Seçilen rengi gösteren küçük bir kutu çizdirme
        st.markdown(
            f'<div style="background-color:rgb({r},{g},{b}); width:100px; height:50px; border-radius:5px; border:1px solid #000;"></div>', 
            unsafe_allow_html=True
        )