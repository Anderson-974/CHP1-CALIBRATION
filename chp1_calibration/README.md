REQUIREMNTS

python~=3
numpy~=1.22.4
pandas~=2.2.2
argparse~=1.1
scikit-learn

****************************************************************************************
DATA EXAMPLE FORMAT

The excel file must be under the .xslx

****************************************************************************************
HOW TO RUN THE CODE ?

1) Run calibration_chp1.py
2) In a terminal put the path of chp1_calibration folder
3) Also in the terminal tape : run calibration_chp1.py data_example.xlsx OUTPUT --ancienne_sensibilite 7.9 
(You can change the old sensibility here)
4) Complete the information requested via the terminal as follows:

OPERATOR [default: EnergyLab]: Your name (by default it’s EnergyLab)
DATE OF CERTIFICATE [default: current date]: Date (by default it’s the current date)
PYRHELIOMETER [default: CHP 1]: Pyrheliometer model (by default it’s the CHP 1)
REFERENCE RADIOMETER [default: PMO8]: Radiometer model (by default it’s the PMO8)
MEASUREMENT SERIES ID PMO8: ID (for example : 195)
PERIOD CALIBRATION: (for example : April-May)

****************************************************************************************
HOW TO CHANGE DADASETS ?

1) In the chp1_calibration folder
2) Open the calibration_functions folder
3) In calibrate_and_generate_pdf.py python file
4) Find :

    time = df.iloc[:, 0]  # Première colonne (Temps)
    DNI_ref = df.iloc[:, 1]  # Deuxième colonne (PMO8)
    DNI_test = df.iloc[:, 2]  # Troisième colonne (CHP 1)

And change 0, 1, 2 value by 4, 5, 6 (select the fourth, fifth, sixth column)

5) Save calibrate_and_generate_pdf.py and re run calibration_chp1.py

****************************************************************************************

