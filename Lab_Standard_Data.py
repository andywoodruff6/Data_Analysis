import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt

df = pd.read_excel('Lab_Standard_Data.xlsx')
#print(df.head(5))

months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

# NOTES: Started using Labview in Feb, 2019
#        Adjusted instrumentation location in May, 2019
#        Ran in automated mode in May, 2019 
#        2,587 data points ranging from 2015 - 2019

unique_data = df.nunique() 
print(unique_data) 

# Creating two new columns, one as the correction factor from actual CFM to 
# standard CFM and the other is the standard CFM

P_sat_table = [(50,60), (0.3559, 0.6218)]
P_sat = (0.3559 + (df.Wet_bulb - 50) * ( (0.6218 - 0.3559) / 10) )
P_std = 29.9295 #in Hg
T_std = 72 #F
df['correction_factor'] =(P_std / (df.Barometer - P_sat * (df.RH / 100) ) ) * (df.Dry_bulb / T_std)
df['standard_airflow'] = df.CFM / df.correction_factor


#Lab conditions by month (Temp, wetbulb, humidity, pressure)


lab_conditions_dry_bulb = df.groupby('Month').Dry_bulb.mean()
#print(lab_conditions_dry_bulb)
plot1 = plt.bar(months, lab_conditions_dry_bulb)
plt.title('Temperature by Month')
plt.ylabel('Temperature (F)')
plt.ylim(70,80)
plt.show(plot1)

lab_conditions_wet_bulb = df.groupby('Month').Wet_bulb.mean()
#print(lab_conditions_wet_bulb)
plot2 = plt.bar(months, lab_conditions_wet_bulb)
plt.title('Wet Bulb Temp. by Month')
plt.ylabel('Temperature (F)')
plt.ylim(50,70)
plt.show(plot2)

lab_conditions_humidity = df.groupby('Month').RH.mean()
#print(lab_conditions_humidity)
plot3 = plt.bar(months, lab_conditions_humidity)
plt.title('Relative Humidity by Month')
plt.ylabel('RH')
plt.show(plot3)

lab_conditions_pressure = df.groupby('Month').Barometer.mean()
#print(lab_conditions_pressure)
plot4 = plt.bar(months, lab_conditions_pressure)
plt.title('Barometric Pressure by Month')
plt.ylabel('Barometer (in. Hg)')
plt.ylim(29, 30)
plt.show(plot4)

monthly_correction_factor = df.groupby('Month').correction_factor.mean()
print(monthly_correction_factor)
plot5 = plt.bar(months, monthly_correction_factor)
plt.title('Standard Airflow Correction Factor by Month')
plt.ylabel('Correction Factor Value')
plt.ylim(1,1.1)
plt.show(plot5)

# This section is to look into blower performance, particularly of CFM, Watts and RPM.
# The data should be broken down by year, by month and split by Black and Yellow tunnel

blower_performance_CFM = df.groupby(['Tunnel', 'Speed']).standard_airflow.mean().reset_index()
#print(blower_performance_CFM)
pivot_blower_performance_CFM = blower_performance_CFM.pivot(index = 'Speed', columns = 'Tunnel' , values = 'standard_airflow'  )
print(pivot_blower_performance_CFM)

def Airflow_Speed(speed):
    Black_Speed = df.loc[(df['Tunnel'] == 'black') & (df['Speed'] == speed)]
    Black_Speed_CFM = Black_Speed.groupby('Year').CFM.mean().reset_index()
    Yellow_Speed = df.loc[(df['Tunnel'] == 'yellow') & (df['Speed'] == speed)]
    Yellow_Speed_CFM = Yellow_Speed.groupby('Year').CFM.mean().reset_index()
    y_min = Black_Speed_CFM. CFM .min() if Black_Speed_CFM. CFM .min() < \
        Yellow_Speed_CFM. CFM .min() else Yellow_Speed_CFM. CFM .min()
    y_max = Black_Speed_CFM. CFM .max() if Black_Speed_CFM. CFM .max() < \
        Yellow_Speed_CFM. CFM .max() else Yellow_Speed_CFM. CFM .max()
    print(Black_Speed_CFM)
    print(Yellow_Speed_CFM)
    X_months = list(range(2015,2021))
    plt.plot(X_months, Black_Speed_CFM.CFM)
    plt.plot(X_months, Yellow_Speed_CFM.CFM)
    plt.ylabel( 'Airflow (CFM)')
    plt.xlabel( 'Year')
    plt.ylim(y_min * 0.98, y_max * 1.02)
    plt.xticks(X_months)
    plt.show()

def Watts_Speed(speed):
    Black_Speed = df.loc[(df['Tunnel'] == 'black') & (df['Speed'] == speed)]
    Black_Speed_parameter = Black_Speed.groupby('Year').Watt.mean().reset_index()

    Yellow_Speed = df.loc[(df['Tunnel'] == 'yellow') & (df['Speed'] == speed)]
    Yellow_Speed_parameter = Yellow_Speed.groupby('Year').Watt.mean().reset_index()

    y_min = Black_Speed_parameter. Watt .min() if Black_Speed_parameter. Watt .min() < \
        Yellow_Speed_parameter. Watt .min() else Yellow_Speed_parameter. Watt .min()
    y_max = Black_Speed_parameter. Watt .max() if Black_Speed_parameter. Watt .max() < \
        Yellow_Speed_parameter. Watt .max() else Yellow_Speed_parameter. Watt .max()

    print(y_min)
    print(y_max) 
    print(    )
    X_months = list(range(2015,2020))
    plt.plot(X_months, Black_Speed_parameter.Watt)
    plt.plot(X_months, Yellow_Speed_parameter.Watt)
    plt.ylabel('Power (Watts)')
    plt.xlabel( 'Year')
    plt.ylim(y_min * 0.98, y_max * 1.02)
    plt.xticks(X_months)
    plt.show()

def RPM_Speed(speed):
    Black_Speed = df.loc[(df['Tunnel'] == 'black') & (df['Speed'] == speed)]
    Black_Speed_parameter = Black_Speed.groupby('Year').RPM.mean().reset_index()

    Yellow_Speed = df.loc[(df['Tunnel'] == 'yellow') & (df['Speed'] == speed)]
    Yellow_Speed_parameter = Yellow_Speed.groupby('Year').RPM.mean().reset_index()

    y_min = Black_Speed_parameter. RPM .min() if Black_Speed_parameter. RPM .min() < \
        Yellow_Speed_parameter. RPM .min() else Yellow_Speed_parameter. RPM .min()
    y_max = Black_Speed_parameter. RPM .max() if Black_Speed_parameter. RPM .max() < \
        Yellow_Speed_parameter. RPM .max() else Yellow_Speed_parameter. RPM .max()

    print(Black_Speed_parameter.min())
    print(Black_Speed_parameter.max())

    X_months = list(range(2015,2020))
    plt.plot(X_months, Black_Speed_parameter.RPM)
    plt.plot(X_months, Yellow_Speed_parameter.RPM)
    plt.xlabel( 'Year')
    plt.ylabel('Wheel Speed (RPM)')
    plt.ylim(y_min * 0.98, y_max * 1.02)
    plt.xticks(X_months)
    plt.show()

Airflow_Speed('high')
Airflow_Speed('medium')
Airflow_Speed('low')

Watts_Speed('high')
Watts_Speed('medium')
Watts_Speed('low')

RPM_Speed('high')
RPM_Speed('medium')
RPM_Speed('low')

'''
def Accurized_Tables(speed2):
    Accurized = df.loc[(df['Year'] == 2019) & (df['Month'] > 4) & (df['Speed'] == speed2) & (df['Tunnel'] == 'black')]
    Accurized_grouped = Accurized.groupby(['Month']).standard_airflow.mean().reset_index()
    Accurized2 = df.loc[(df['Year'] == 2019) & (df['Month'] > 4) & (df['Speed'] == speed2) & (df['Tunnel'] == 'yellow')]
    Accurized_grouped2 = Accurized2.groupby(['Month']).standard_airflow.mean().reset_index()

    X_month_black = [5, 6, 7, 8, 9, 10]
    X_month_yellow =[5, 6, 8, 10, 12]
    plt.plot(X_month_black, Accurized_grouped.standard_airflow)
    plt.plot(X_month_yellow, Accurized_grouped2.standard_airflow)
    plt.ylabel('Airflow (SCFM)')
    plt.xlabel('Months of 2019')
    plt.show()

Accurized_Tables('high')
Accurized_Tables('medium')
Accurized_Tables('low')


def months_for_graphing(speed3):
    month_df_B = df.loc[(df['Tunnel'] == 'black') & (df['Speed'] == speed3)]
    month_df_B_grouped = month_df_B.groupby(['Year' , 'Month']).standard_airflow.mean().reset_index()
    month_df_Y = df.loc[(df['Tunnel'] == 'yellow') & (df['Speed'] == speed3)]
    month_df_Y_grouped = month_df_Y.groupby(['Year' , 'Month']).standard_airflow.mean().reset_index()
    #print(month_df_B)
    #print(month_df_B_grouped)
    #print(month_df_Y_grouped)
    X_month_black = range(1, 33)
    X_month_yellow = range(1, 31)
    plt.plot(X_month_black, month_df_B_grouped.standard_airflow)
    plt.plot(X_month_yellow, month_df_Y_grouped.standard_airflow)
    plt.ylabel('Airflow (SCFM)')
    plt.xlabel('Months')
    plt.show()

# Inconsistant data means only one of these graphs will work at a time. Review Power Point for presentation. 
#months_for_graphing('high')
#months_for_graphing('medium')
#months_for_graphing('low')
'''
'''
Variation1 = df.loc[(df['Year'] == 2019) & (df['Month'] > 4) & (df['Speed'] == 'high') & (df['Tunnel'] == 'black')]
Variation1_grouped = Variation1.standard_airflow.std()

Variation2 = df.loc[(df['Year'] == 2019) & (df['Month'] > 4) & (df['Speed'] == 'high') & (df['Tunnel'] == 'yellow')]
Variation2_grouped = Variation2.standard_airflow.std()

Variation3 = df.loc[(df['Year'] == 2019) & (df['Month'] > 4) & (df['Speed'] == 'medium') & (df['Tunnel'] == 'black')]
Variation3_grouped = Variation3.standard_airflow.std()

Variation4 = df.loc[(df['Year'] == 2019) & (df['Month'] > 4) & (df['Speed'] == 'medium') & (df['Tunnel'] == 'yellow')]
Variation4_grouped = Variation4.standard_airflow.std()

Variation5 = df.loc[(df['Year'] == 2019) & (df['Month'] > 4) & (df['Speed'] == 'low') & (df['Tunnel'] == 'black')]
Variation5_grouped = Variation5.standard_airflow.std()

Variation6 = df.loc[(df['Year'] == 2019) & (df['Month'] > 4) & (df['Speed'] == 'low') & (df['Tunnel'] == 'yellow')]
Variation6_grouped = Variation6.standard_airflow.std()

print(Variation1_grouped)
print(Variation2_grouped)
print(Variation3_grouped)
print(Variation4_grouped)
print(Variation5_grouped)
print(Variation6_grouped)

Variation1 = df.loc[(df['Speed'] == 'high') & (df['Tunnel'] == 'black')]
Variation1_grouped = Variation1.standard_airflow.std()

Variation2 = df.loc[(df['Speed'] == 'high') & (df['Tunnel'] == 'yellow')]
Variation2_grouped = Variation2.standard_airflow.std()

Variation3 = df.loc[(df['Speed'] == 'medium') & (df['Tunnel'] == 'black')]
Variation3_grouped = Variation3.standard_airflow.std()

Variation4 = df.loc[(df['Speed'] == 'medium') & (df['Tunnel'] == 'yellow')]
Variation4_grouped = Variation4.standard_airflow.std()

Variation5 = df.loc[(df['Speed'] == 'low') & (df['Tunnel'] == 'black')]
Variation5_grouped = Variation5.standard_airflow.std()

Variation6 = df.loc[(df['Speed'] == 'low') & (df['Tunnel'] == 'yellow')]
Variation6_grouped = Variation6.standard_airflow.std()

print(Variation1_grouped)
print(Variation2_grouped)
print(Variation3_grouped)
print(Variation4_grouped)
print(Variation5_grouped)
print(Variation6_grouped)
'''




