# pmt_sweep_analysis
User Interface for PMT Calibration using LED and HV Sweep

## High Voltage Graph
This graph displays the relationship between the PMT gain and the applied voltage. 
This relationship is fit with a quadratic curve and the equation is displayed.

## LED Graph
This graph display the gain values across the mean photoelectron values across the LED Sweep.
This shows the stability of the PMT across light intensities. This stability is displayed in the side panel.

## Ideal Gain Entry
This features allows the user to enter an ideal gain and it calculates the necessary voltage based on the fitted equation.

## Data Entry
The user interface takes the data in a very specific form. The data must be comma seperated and follow the format of:
High_Voltage,Q_1,LED,mu_1,HV

The High_Voltage column represents the High Voltage value of that run.
The Q_1 column represents the gain of that run.
The LED column represents the value of the light source (LED) for that run.
The mu_1 column represents mu_1 value from that run (the mean number of photoelectrons)
The HV column represnets the boolen (True/False) value of if the run is in a high voltage sweep or not. 
#### Example
High_Voltage,Q_1,LED,mu_1,HV 
1380,26,2.72,0.6,True 
1400,28.0,2.82,0.70,False 

### High Voltage Sweep
A high voltage sweep is performed by keeping the test setup at a constant LED value while increasing the High Voltage value in steady increments. 
This is done to determine the relationship between the applied voltage and the gain.

### LED Sweep
A LED sweep is performed by keeping the test setup at a consted High Voltage while increasing the LED intensity in steady increments. 
This is done to determine the stability of the gain ($Q_1$) across different light intensities. 
