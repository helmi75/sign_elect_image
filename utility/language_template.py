from datetime import date

today = date.today()
formatted_date = today.strftime("%d/%m/%Y")  # Format : jour/mois/année

def template_text_doc(language, firstname, lastname, birthday, adress, email):
    # Texte du document

    if language == "french":
        document_text = f"""
        
        Je soussigné(e), {firstname} {lastname}
        né(e) le : {birthday}
        demeurant au {adress}
        email :{email}

        Autorise sans réserve la société TURTLE SAS à disposer pleinement et irrévocablement des photos ou vidéos prises de moi à l’occasion des photos prises :

        à bord d’un tricycle Turtle dans le cadre d’un témoignage.
        Les images seront destinées à être diffusées, représentées et/ou adaptées en tout ou en partie, s’il y a lieu, dans le cadre de la communication interne et externe de Turtle, notamment sur les réseaux sociaux, site internet, presse et voies électroniques.
        Cette autorisation gracieuse vaut sans restriction géographique et sans limite de durée.

        Fait pour servir et valoir ce que de droit.


        fait à Paris le : {formatted_date}
        Nom et Signature précédée de la mention Lu et approuvé: {firstname} {lastname} 

        """
        
        return document_text

    elif language == "english":

        document_text = f"""

        I, the undersigned, {firstname} {lastname}
        born on: {birthday}
        residing at {adress}
        email :{email}


        Hereby authorize, without reservation, the company TURTLE SAS to fully and irrevocably dispose of any photos or videos taken of me on the occasion of photos taken:

        on board a Turtle tricycle as part of a testimonial.
        The images are intended to be disseminated, represented and/or adapted in whole or in part, as the case may be, as part of Turtle's internal and external communication, including on social networks, websites, press and electronic media.
        This gratuitous authorization is valid without geographical restriction and without time limit.

        Done for what it may be worth.


        Done in Paris on: {formatted_date}
        Name and Signature preceded by the words Read and approved:: {firstname}   {lastname}
        """
       
        return document_text