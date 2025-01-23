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
min_date = date(1930, 1, 1) 
birthday = st.date_input("birthday :", value=date.today(), min_value = min_date)
adress = st.text_input("adress")
email  = st.text_input("email")
language = st.selectbox("select language", ["french","english"])


# Texte du document
fr_document_text = f"""
Autorisation d’exploitation du droit à l’image

Je soussigné(e), {firstname} {lastname}
né(e) le : {birthday}
demeurant au {adress}

Autorise sans réserve la société TURTLE SAS à disposer pleinement et irrévocablement des photos ou vidéos prises de moi à l’occasion des photos prises :

à bord d’un tricycle Turtle dans le cadre d’un témoignage.
Les images seront destinées à être diffusées, représentées et/ou adaptées en tout ou en partie, s’il y a lieu, dans le cadre de la communication interne et externe de Turtle, notamment sur les réseaux sociaux, site internet, presse et voies électroniques.
Cette autorisation gracieuse vaut sans restriction géographique et sans limite de durée.

Fait pour servir et valoir ce que de droit.


fait à Paris le : {formatted_date}
Nom et Signature : {firstname}
"""

en_document_text = f"""
Image Rights Authorization

I, the undersigned, {firstname} {lastname}
born on: {birthday}
residing at {adress}

Hereby authorize, without reservation, the company TURTLE SAS to fully and irrevocably dispose of any photos or videos taken of me on the occasion of photos taken:

on board a Turtle tricycle as part of a testimonial.
The images are intended to be disseminated, represented and/or adapted in whole or in part, as the case may be, as part of Turtle's internal and external communication, including on social networks, websites, press and electronic media.
This gratuitous authorization is valid without geographical restriction and without time limit.

Done for what it may be worth.


Done in Paris on: {formatted_date}
Name and Signature: {firstname}
"""


st.subheader("Document à signer")
if language == "french":
    st.text_area("Prévisualisation du document :", fr_document_text, height=200, disabled=True)
    document_text = fr_document_text
elif language == "english":
    st.text_area("Prévisualisation du document :", en_document_text, height=200, disabled=True)
    document_text = en_document_text



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
            pdf.multi_cell(0, 10, document_text.replace("’", "'"))


            # Positionnement ajusté pour éviter d'écraser le texte
            x_signature = 50  # Position X (inchangé)
            y_signature = pdf.get_y() + 20  # Ajouter de l'espace après le texte actuel
            width_signature = 60  # Largeur

            # Ajouter la signature au PDF
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


