import streamlit as st
from streamlit_drawable_canvas import st_canvas
from fpdf import FPDF
from PIL import Image, ImageOps
import os
from datetime import date


today = date.today()
formatted_date = today.strftime("%d/%m/%Y")  # Format : jour/mois/année


# Titre de l'application
st.title("Signature et Enregistrement d'un Document de Droit d'Image")
firstname  = st.text_input("firstname")
lastname = st.text_input("lastname")


# Texte du document
document_text = f"""
DROIT À L'IMAGE
Je soussigné(e), autorise l'utilisation de mon image par [Nom de l'Organisation]
dans le cadre des activités de communication, de publicité ou autres supports numériques.
prénom   : {firstname}
nom : {lastname}



Date : {formatted_date}
Nom et Signature : {firstname}
"""

st.subheader("Document à signer")
st.text_area("Prévisualisation du document :", document_text, height=200, disabled=True)

# Zone de signature
st.subheader("Zone de signature")
stroke_width = st.sidebar.slider("Épaisseur du trait", 1, 25, 3)
stroke_color = st.sidebar.color_picker("Couleur du trait", "#000000")
bg_color = st.sidebar.color_picker("Couleur de fond", "#FFFFFF")

canvas_result = st_canvas(
    fill_color="rgba(0, 0, 0, 0)",  # Fond transparent
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    height=200,
    width=400,
    drawing_mode="freedraw",
    key="canvas",
)

# Enregistrement en PDF
if st.button("Enregistrer le document en PDF"):
    if canvas_result.image_data is not None:
        # Conversion de la signature en image
        signature_image = Image.fromarray((canvas_result.image_data * 255).astype("uint8"))
        signature_image = signature_image.convert("L")  # Convertir en niveaux de gris
        signature_image = ImageOps.invert(signature_image)  # Inverser les couleurs
        signature_image = signature_image.convert("RGB")  # Convertir en RGB
        signature_path = f"pdf/{firstname}_signature.png"
        signature_image.save(signature_path)

        # Vérification du fichier de signature
        if os.path.exists(signature_path):
            st.success("La signature a été sauvegardée.")
            st.image(signature_image, caption="Aperçu de la signature")

            # Création du PDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, document_text)

            # Ajouter la signature au PDF
            x_signature = 50  # Position X
            y_signature = 100  # Position Y
            width_signature = 60  # Largeur
            pdf.image(signature_path, x=x_signature, y=y_signature, w=width_signature)

            # Sauvegarde du PDF
            pdf_output = f"pdf/{firstname}_droit_image.pdf"
            pdf.output(pdf_output)
            st.success(f"Document enregistré en PDF : {pdf_output}")
            with open(pdf_output, "rb") as pdf_file:
                st.download_button(
                    label="Télécharger le document signé",
                    data=pdf_file,
                    file_name=pdf_output,
                    mime="application/pdf",
                )
        else:
            st.error("Erreur lors de la génération de la signature.")
    else:
        st.error("Veuillez ajouter une signature avant d'enregistrer.")


