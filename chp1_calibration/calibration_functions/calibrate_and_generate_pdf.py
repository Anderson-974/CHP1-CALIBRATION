# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 10:59:56 2024

@author: ander
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from calibration_functions.create_output_dir import create_output_dir
from calibration_functions.calculate_metrics import calculate_metrics
from sklearn.linear_model import LinearRegression
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def calibrate_and_generate_pdf(input_excel: str, 
                                output_dir: str, 
                                ancienne_sensibilite: float) -> tuple:
    """
    Main function for PDF calibration and generation.

    This function takes as input an Excel file, an output directory and an old sensitivity.
    It performs the calibration, generates a calibration certificate in PDF format and saves it in the output directory.
    
    Args:
        input_excel (str): Path of the Excel file containing the calibration data.
        output_dir (str): Output directory where the generated PDF will be saved.
        ancienne_sensibilite (float): Old sensor sensitivity.

    Returns:
        tuple: Contains cleaned data for DNI REF, DNI TEST, predicted DNI TEST,
               identity line data, adjusted DNI TEST, and cleaned time data.
    """
    create_output_dir(output_dir)
    
    pdf_filename = os.path.join(output_dir, 'calibration_certificate.pdf')

    # Importation des données depuis le fichier Excel
    df = pd.read_excel(input_excel)

    # Extraction des valeurs de temps, de DNI_ref et de DNI_test
    time = df.iloc[:, 0]  # Première colonne (Temps)
    DNI_ref = df.iloc[:, 1]  # Deuxième colonne (PMO8)
    DNI_test = df.iloc[:, 2]  # Troisième colonne (CHP 1)

    # Suppression des lignes contenant des NaN ou des valeurs infinies
    valid_indices = np.isfinite(DNI_ref) & np.isfinite(DNI_test)
    time_clean = time[valid_indices]
    DNI_ref_clean = DNI_ref[valid_indices]
    DNI_test_clean = DNI_test[valid_indices]

    # Reshape des données pour les rendre compatibles avec scikit-learn
    DNI_ref_clean = DNI_ref_clean.values.reshape(-1, 1)
    DNI_test_clean = DNI_test_clean.values.reshape(-1, 1)

    # Création du modèle de régression linéaire
    model = LinearRegression()
    model.fit(DNI_ref_clean, DNI_test_clean)

    # Prédiction des valeurs pour tracer la ligne de régression
    DNI_test_pred = model.predict(DNI_ref_clean)

    # Extraction des coefficients de la régression linéaire
    slope = model.coef_[0][0]
    intercept = model.intercept_[0]

    # Création de l'équation de la régression linéaire
    equation = f"y = {slope:.2f}x + {intercept:.2f}"
    # Affichage de l'équation de la régression
    print(f"L'équation de la régression linéaire est : y = {slope:.2f}x + {intercept:.2f}")

    # Calcul du coefficient de détermination R²
    r_squared = model.score(DNI_ref_clean, DNI_test_clean)
    print(f"Le coefficient de détermination R² est : {r_squared:.2f}")

    # Création de la ligne y = x pour le cas où DNI_test = DNI_ref
    DNI_identity = DNI_ref_clean  # Puisque DNI_test = DNI_ref
    slope_identity = 1.0
    intercept_identity = 0.0
    equation_identity = f"y = {slope_identity:.2f}x + {intercept_identity:.2f}"

    # Ajustement des valeurs du CHP 1 (DNI_test) en utilisant les coefficients de régression
    DNI_test_adjusted = (DNI_test_clean - intercept) / slope

    # Calcul de la nouvelle sensibilité
    nouvelle_sensibilite = ancienne_sensibilite * slope

    # Affichage des anciennes et nouvelles sensibilités
    print(f"L'ancienne sensibilité du CHP 1 est : {ancienne_sensibilite:.2f} μV/(W/m²)")
    print(f"La nouvelle sensibilité du CHP 1 après ajustement est : {nouvelle_sensibilite:.2f} μV/(W/m²)")
    
    # Calcul de l'écart relatif entre les moyennes de DNI REF et DNI TEST
    ecart_relatif = abs(DNI_ref_clean.mean() - DNI_test_clean.mean()) / DNI_test_clean.mean()
    # Affichage de l'écart relatif
    print("Écart relatif entre les moyennes de DNI REF et DNI TEST :", ecart_relatif) 
    
    # Calcul de l'écart relatif entre les moyennes de DNI REF et DNI TEST ajusté
    ecart_relatif_test_ajuste = abs(DNI_ref_clean.mean() - DNI_test_adjusted.mean()) / DNI_test_adjusted.mean()
    # Affichage de l'écart relatif
    print("Écart relatif entre les moyennes de DNI REF et DNI TEST ajusté :", ecart_relatif_test_ajuste)

    # Calcul des métriques
    calculate_metrics(DNI_ref_clean, DNI_test_clean, "DNI TEST (CHP 1) Metrics (Before Adjustment)")
    calculate_metrics(DNI_ref_clean, DNI_test_adjusted, "DNI TEST (CHP 1) Metrics (After Adjustment)")    
    
    # Demande des informations supplémentaires à l'utilisateur
    operator = input("OPERATOR [default: EnergyLab]: ")
    if not operator:
        operator = "EnergyLab"
    
    date_of_certificate = input("DATE OF CERTIFICATE [default: current date]: ")
    if not date_of_certificate:
        date_of_certificate = datetime.now().strftime("%d/%m/%Y")
    
    pyrheliometre = input("PYRHELIOMETER [default: CHP 1]: ")
    if not pyrheliometre:
        pyrheliometre = "CHP 1"
    
    reference_radiometre = input("REFERENCE RADIOMETER [default: PMO8]: ")
    if not reference_radiometre:
        reference_radiometre = "PMO8"
    
    series_id = input("MEASUREMENT SERIES ID PMO8: ")
    
    period_calibration = input("PERIOD CALIBRATION: ")
 
    # Création du document PDF avec ReportLab
    doc = SimpleDocTemplate(pdf_filename, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    
    # Ajouter l'image en haut du PDF
    logo_path = "./img/energylab.png"
    logo = Image(logo_path, width=4*inch, height=2*inch)  # Ajustez la taille de l'image selon vos besoins
    story.append(logo)
    
    # Ajouter un espace après l'image
    story.append(Spacer(1, 0.25*inch))

    # Ajout du contenu du certificat
    story.append(Paragraph("Calibration certificate", styles['Title']))
    story.append(Spacer(1, 0.25*inch))
    story.append(Paragraph(f"OPERATOR: {operator}", styles['Normal']))
    story.append(Paragraph(f"DATE OF CERTIFICATE: {date_of_certificate}", styles['Normal']))
    story.append(Paragraph(f"PYRHELIOMETER: {pyrheliometre}", styles['Normal']))   
    story.append(Paragraph(f"REFERENCE RADIOMETER: {reference_radiometre}", styles['Normal']))
    story.append(Paragraph(f"MEASUREMENT SERIES ID PMO8: {series_id}", styles['Normal']))
    story.append(Paragraph(f"PERIOD CALIBRATION: {period_calibration}", styles['Normal']))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("Calibration Procedure:", styles['Heading2']))
    story.append(Paragraph("1. Collect data from reference and test radiometers.", styles['Normal']))
    story.append(Paragraph("2. Perform linear regression analysis.", styles['Normal']))
    story.append(Paragraph("3. Adjust test radiometer sensitivity based on regression results.", styles['Normal']))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("Calibration Results:", styles['Heading2']))
    story.append(Paragraph(f"Old sensibility: {ancienne_sensibilite:.2f} μV/(W/m²)", styles['Normal']))
    story.append(Paragraph(f"New sensibility: {nouvelle_sensibilite:.2f} μV/(W/m²)", styles['Normal']))

    # Construction du PDF
    doc.build(story)

    # Vérification de l'existence du fichier PDF avant de l'ouvrir
    if os.path.exists(pdf_filename):
        print(f"Le fichier PDF '{pdf_filename}' a été généré avec succès.")
        # Ouverture automatique du fichier PDF
        if os.name == 'posix':
            os.system(f'open {pdf_filename}')
        elif os.name == 'nt':
            os.system(f'start {pdf_filename}')
    else:
        print(f"Erreur: Le fichier PDF '{pdf_filename}' n'a pas été trouvé.")
    
    # Retourner les valeurs nécessaires pour la fonction plot_graphs
    return DNI_ref_clean, DNI_test_clean, DNI_test_pred, DNI_identity, DNI_test_adjusted, time_clean

def plot_graphs(DNI_ref_clean, DNI_test_clean, DNI_test_pred, DNI_identity, DNI_test_adjusted, time_clean):
    """
    Plot graphs based on the calibration data.
    
    Args:
        DNI_ref_clean (numpy.ndarray): Cleaned data for DNI REF.
        DNI_test_clean (numpy.ndarray): Cleaned data for DNI TEST.
        DNI_test_pred (numpy.ndarray): Predicted data for DNI TEST.
        DNI_identity (numpy.ndarray): Identity line data.
        DNI_test_adjusted (numpy.ndarray): Adjusted data for DNI TEST.
        time_clean (numpy.ndarray): Cleaned data for time.

    Returns:
        None
    """
    # Tracé du nuage de points et des lignes de régression
    plt.figure(figsize=(12, 6))

    # Graphique avant ajustement
    plt.subplot(1, 2, 1)
    plt.scatter(DNI_ref_clean, DNI_test_clean, color='blue', label='Data')
    plt.plot(DNI_ref_clean, DNI_test_pred, color='red', linewidth=2, label='Linear regression')
    plt.plot(DNI_ref_clean, DNI_identity, color='green', linestyle='--', linewidth=2, label='y = x')
    plt.xlabel('DNI REF (PMO8) [W/m²]')
    plt.ylabel('DNI TEST (CHP 1) [W/m²]')
    plt.title('Linear regression (Before adjustment)')
    plt.legend()

    # Graphique après ajustement
    plt.subplot(1, 2, 2)
    plt.scatter(DNI_ref_clean, DNI_test_adjusted, color='blue', label='Adjusted data')
    plt.plot(DNI_ref_clean, DNI_identity, color='green', linestyle='--', linewidth=2, label='y = x')
    plt.xlabel('DNI REF (PMO8) [W/m²]')
    plt.ylabel('DNI TEST ajusté (CHP 1) [W/m²]')
    plt.title('Linear regression (After adjustment)')
    plt.legend()

    plt.tight_layout()

    # Tracé du graphique du DNI en fonction du temps
    plt.figure(figsize=(12, 6))
    plt.plot(time_clean, DNI_ref_clean, label='DNI REF (PMO8)', color='red')
    plt.plot(time_clean, DNI_test_clean, label='DNI TEST (CHP 1)', color='blue')
    plt.plot(time_clean, DNI_test_adjusted, label='DNI TEST ajusté (CHP 1)', color='green')
    plt.xlabel('TIME')
    plt.ylabel('DNI [W/m²]')
    plt.title('DNI as a function of time')
    plt.legend()

    plt.tight_layout()

    # Affichage des graphiques
    plt.show()