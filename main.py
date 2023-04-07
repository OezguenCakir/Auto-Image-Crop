import imageio.v2 as imageio
from PIL import Image
import streamlit as st
import io


def has_transparency(img):
    if img.info.get("transparency", None) is not None:
        return True
    if img.mode == "P":
        transparent = img.info.get("transparency", -1)
        for _, index in img.getcolors():
            if index == transparent:
                return True
    elif img.mode == "RGBA":
        extrema = img.getextrema()
        if extrema[3][0] < 255:
            return True
    return False


st.set_page_config(
    page_title="Auto zuschneiden",
    page_icon="🐈",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

st.title('Dein transparentes Bild automatisch zuschneiden')
st.image('https://raw.githubusercontent.com/OezguenCakir/Auto-Image-Crop/main/thumbnail.jpg')

uploaded_file = st.file_uploader("Wähle dein Bild")

if uploaded_file is not None:
    picture = Image.open(uploaded_file)
    if has_transparency(picture):
        img = picture.convert("RGBA")
        pixel_data = img.load()
        width, height = img.size

        non_transparent_pixels = []
        for y in range(height):
            for x in range(width):
                if pixel_data[x, y][3] != 0:
                    non_transparent_pixels.append([x,y])

        non_transparent_x = []
        non_transparent_y = []
        for pixel_number in range(len(non_transparent_pixels)):
            non_transparent_x.append(non_transparent_pixels[pixel_number][0])
            non_transparent_y.append(non_transparent_pixels[pixel_number][1])

        top = min(non_transparent_y) 
        right = max(non_transparent_x) + 1
        bottom = max(non_transparent_y) + 1
        left = min(non_transparent_x)
        cropped_image = img.crop((left, top, right, bottom))
        
        st.image(cropped_image, 'Dein zugeschnittenes Bild')
        output = io.BytesIO()
        cropped_image.save(output, format="PNG")
        binary_img = output.getvalue()
        file_name = uploaded_file.name[:uploaded_file.name.rfind('.')]
        st.download_button(label="Download dein zugeschnittenes Bild", data=binary_img, file_name=file_name+"_cropped.png")

    else:
        st.write("""
        **Ich kann nur schon transparente Bilder zuschneiden.** \n
        Nutze eine Plattform wie [remove.bg](https://www.remove.bg/de) oder [Canva](https://www.canva.com/de_de/) (Premium) um das Bild freizustellen """)