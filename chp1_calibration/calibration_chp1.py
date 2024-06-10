# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 11:02:55 2024

@author: ander
"""

import argparse
from calibration_functions.calibrate_and_generate_pdf import calibrate_and_generate_pdf
from calibration_functions.calibrate_and_generate_pdf import plot_graphs

if __name__ == "__main__":
    
    # Configuration des arguments de la ligne de commande
    parser = argparse.ArgumentParser(description="Calibration of radiometers.")
    parser.add_argument('input_excel', type=str, help="Input Excel file containing the data.")
    parser.add_argument('output_dir', type=str, help="Directory to save the output PDF.")
    parser.add_argument('--ancienne_sensibilite', type=float, required=True, help="Old sensitivity of the CHP 1 radiometer.")

    args = parser.parse_args()
     
    # Exécution de la fonction principale avec les arguments fournis
    DNI_ref_clean, DNI_test_clean, DNI_test_pred, DNI_identity, DNI_test_adjusted, time_clean = calibrate_and_generate_pdf(args.input_excel, args.output_dir, args.ancienne_sensibilite)
    
    # Appel de la fonction pour afficher les graphiques
    plot_graphs(DNI_ref_clean, DNI_test_clean, DNI_test_pred, DNI_identity, 
                            DNI_test_adjusted, time_clean)
