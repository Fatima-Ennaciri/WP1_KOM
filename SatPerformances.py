#!/usr/bin/env python

########################################################################
# SatPerformances.py:
# This function is the Main Function of SAT Module
#
#  Project:        SBPT
#  File:           SatPerformances.py
#  Date(YY/MM/DD): 20/07/11
#
#   Author: GNSS Academy
#   Copyright 2020 GNSS Academy
#
# -----------------------------------------------------------------
# Date       | Author             | Action
# -----------------------------------------------------------------
#
# Usage:
# i.e: SatPerformances.py $SCEN_PATH
# 
# Internal dependencies:
#   SatFunctions.py
#   COMMON
########################################################################


# Import External and Internal functions and Libraries
#----------------------------------------------------------------------
import sys, os
from collections import OrderedDict
from pandas import read_csv 
from SatFunctions import RIMSIdx
from SatFunctions import SatStatsIdx
from SatFunctions import SatIdx
from SatFunctions import EntGpsIdx
from SatFunctions import computeSatStats
from COMMON.Dates import convertYearMonthDay2JulianDay
from COMMON.Dates import convertJulianDay2YearMonthDay
from COMMON.Dates import convertYearMonthDay2Doy
from yaml import dump
import SatPlots


#----------------------------------------------------------------------
# INTERNAL FUNCTIONS
#----------------------------------------------------------------------

def displayUsage():
    sys.stderr.write("ERROR: Please provide path to SCENARIO as a unique argument\n")

# Function to read the configuration file
def readConf(CfgFile):
    Conf = OrderedDict({})
    with open(CfgFile, 'r') as f:
        # Read file
        Lines = f.readlines()

        # Read each configuration parameter which is compound of a key and a value
        for Line in Lines:
            if "#" in Line: continue
            if not Line.strip(): continue
            LineSplit = Line.split('=')
            try:
                LineSplit = list(filter(None, LineSplit))
                Conf[LineSplit[0].strip()] = LineSplit[1].strip()

            except:
                sys.stderr.write("ERROR: Bad line in conf: %s\n" % Line)

    return Conf

def processConf(Conf):
    ConfCopy = Conf.copy()
    for Key in ConfCopy:
        Value = ConfCopy[Key]
        if Key == "INI_DATE" or Key == "END_DATE":
            ParamSplit = Value.split('/')

            # Compute Julian Day
            Conf[Key + "_JD"] = \
                int(round(
                    convertYearMonthDay2JulianDay(
                        int(ParamSplit[2]),
                        int(ParamSplit[1]),
                        int(ParamSplit[0]))
                    )
                )

    return Conf

#######################################################
# MAIN BODY
#######################################################

# Check Input Arguments
if len(sys.argv) != 2:
    displayUsage()
    sys.exit()

# Extract the arguments
Scen = sys.argv[1]

# Select the conf file name
CfgFile = Scen + '/CFG/satperformances.cfg'

# Read conf file
Conf = readConf(CfgFile)
#print(dump(Conf))

# Process Configuration Parameters
Conf = processConf(Conf)

# Print 
print('------------------------------------')
print('--> RUNNING SAT-PERFORMANCE ANALYSIS:')
print('------------------------------------')


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>> RIMS & SatStats FILE ANALYSES
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# Get RIMS file full path
RimsFile = Scen + '/INP/RIMS/' + Conf["RIMS_FILE"]
SatStatsFile = Scen + '/OUT/SAT/' + Conf["SatStats_FILE"]


# Loop over Julian Days in simulation
#-----------------------------------------------------------------------
for Jd in range(Conf["INI_DATE_JD"], Conf["END_DATE_JD"] + 1):

    # Compute Year, Month and Day in order to build input file name
    Year, Month, Day = convertJulianDay2YearMonthDay(Jd)
    
    # Estimate the Day of Year DOY
    Doy = convertYearMonthDay2Doy(Year, Month, Day)

    # Define the full path and name to the SAT INFO file to read
    SatFile = Scen + \
        '/OUT/SAT/' + 'SAT_INFO_Y%02dD%03d_G123_%ss.dat' % \
            (Year % 100, Doy, Conf["TSTEP"])

    # Define the name of the ENT-GPS instantaneous file
    EntGpsFile = Scen + \
        '/OUT/SAT/' + 'ENTGPS_Y%02dD%03d_G123_%ss.dat' % \
            (Year % 100, Doy, Conf["TSTEP"])

    # Define the name of the Output file Statistics
    SatStatsFile = SatFile.replace("INFO", "STAT")


    # Display Message
    print('\n*** Processing Day of Year: ', Doy, '...***')

    # Display Message
    print('1. Processing file:', SatFile)
    
    # Compute Satellite Statistics  FILE
    computeSatStats(SatFile, EntGpsFile, SatStatsFile)

    # Display Creation message
    print('2. Created files:', SatStatsFile, EntGpsFile)
    
    # Display Reading Message
    print('3. Reading file:', SatStatsFile, RimsFile)
    
    
    # Read Statistics file
       

    # Display Generating figures Message
    print('4. Generating Figures...\n')
    
    # Generate Satellite Performances figures

# Display RIMS MAP
    if(Conf["Plot_RIMS_MAP"] == '1'):
    # Read the cols we need from RIMS file
        RimsData = read_csv(RimsFile, delim_whitespace=True, skiprows=15, header=None,\
        usecols=[RIMSIdx["p4"],RIMSIdx["p5"],RIMSIdx["p2"]])
        
        print( 'Display the network of RIMS...')

        # Configure plot and call plot generation function
        SatPlots.Plot_RIMSMAP(RimsData)

    #Plot Satellite Monitoring Percentage
    if(Conf["Plot_MON"] == '1'):
    # Read the cols we need from SatStats file
        SatStatsData = read_csv(SatStatsFile, delim_whitespace=True, skiprows=1, header=None,\
        usecols=[SatStatsIdx["PRN"],SatStatsIdx["MON"]])
        
        print( 'Plot Satellite Monitoring Percentage...')

        # Configure plot and call plot generation function
        SatPlots.Plot_MON(SatStatsData)

#Plot Minimum and Max. Number of RIMS in View
    if(Conf["Plot_NRIMS"] == '1'):
    # Read the cols we need from Sat file
       SatStatsData = read_csv(SatStatsFile, delim_whitespace=True, skiprows=1, header=None,\
       usecols=[SatStatsIdx["PRN"],SatStatsIdx["RIMS-MIN"],SatStatsIdx["RIMS-MAX"]])
    
       print( 'Plot Minimum and Max. Number of RIMS in View...')

        # Configure plot and call plot generation function
       SatPlots.Plot_NRIMS(SatStatsData)

#Plot RMS SREA for all satellites as a box-plot   
    if(Conf["Plot_RMS-SREACR"] == '1'):  
    # Read the cols we need from Rims file
        SatStatsData = read_csv(SatStatsFile, delim_whitespace=True, skiprows=1 , header=None,\
        usecols=[SatStatsIdx["PRN"], SatStatsIdx["SREaRMS"], SatStatsIdx["SREcRMS"], SatStatsIdx["SRErRMS"]])
    
        print( 'Plot RMS of SREW along/cross/radial along the day  ...')
        
        # Configure plot and call plot generation function
        SatPlots.plotSREacrRMS(SatStatsData)
    

#Plot RMS SREB for all satellites as a box-plot
    if(Conf["Plot_RMS-SREB"] == '1'):
    # Read the cols we need from SatStats file
        SatStatsData = read_csv(SatStatsFile, delim_whitespace=True, skiprows=1, header=None,\
        usecols=[SatStatsIdx["PRN"],SatStatsIdx["SREbRMS"]])
        
        print( 'Plot RMS SREB for all satellites as a box-plot...')

        # Configure plot and call plot generation function
        SatPlots.plotSREbRMS(SatStatsData)

#Plot RMS and MAX SREW for all satellites as a box-plot
    if(Conf["Plot_SREW"] == '1'):
    # Read the cols we need from SatStats file
        SatStatsData = read_csv(SatStatsFile, delim_whitespace=True, skiprows=1, header=None,\
        usecols=[SatStatsIdx["PRN"],SatStatsIdx["SREWRMS"],SatStatsIdx["SREWMAX"]])
    
        print( 'Plot RMS and MAX SREW for all satellites as a box-plot...')

        # Configure plot and call plot generation function
        SatPlots.plotRmsSrewMaxSrew(SatStatsData)

#Plot MAX and MIN SigmaFLT for all satellites as a box-plot
    if(Conf["Plot_SFLTW"] == '1'):
    # Read the cols we need from SatStats file
        SatStatsData = read_csv(SatStatsFile, delim_whitespace=True, skiprows=1, header=None,\
        usecols=[SatStatsIdx["PRN"],SatStatsIdx["SFLTMIN"],SatStatsIdx["SFLTMAX"]])
    
        print( 'Plot MAX and MIN SigmaFLT for all satellites as a box-plot...')

        # Configure plot and call plot generation function
        SatPlots.plotMinMaxSFLT(SatStatsData)


#Plot MAX SIW for all satellites as a box-plot
    if(Conf["Plot_MAXSIW"] == '1'):
    # Read the cols we need from SatStats file
       SatStatsData = read_csv(SatStatsFile, delim_whitespace=True, skiprows=1, header=None,\
       usecols=[SatStatsIdx["PRN"],SatStatsIdx["SIMAX"]])
    
       print( 'Plot MAX SIW for all satellites as a box-plot...')

        # Configure plot and call plot generation function
       SatPlots.plotMaxSiw(SatStatsData)


#Plot MAX SIW for all satellites as a box-plot
    if(Conf["Plot_MAXFCLTCb"] == '1'):
    # Read the cols we need from SatStats file
        SatStatsData = read_csv(SatStatsFile, delim_whitespace=True, skiprows=1, header=None,\
        usecols=[SatStatsIdx["PRN"],SatStatsIdx["LTCbMAX"],SatStatsIdx["FCMAX"]])
    
        print( 'Plot MAX Satellite Clock Fast and Long term Corrections for all satellites...')

        # Configure plot and call plot generation function
        SatPlots.plotMaxFcLTCb(SatStatsData)

#Plot MAX LTC-XYZ for all satellites
    if(Conf["Plot_MAXLTC-XYZ"] == '1'):
    # Read the cols we need from SatStats file
        SatStatsData = read_csv(SatStatsFile, delim_whitespace=True, skiprows=1, header=None,\
        usecols=[SatStatsIdx["PRN"],SatStatsIdx["LTCxMAX"],SatStatsIdx["LTCyMAX"],SatStatsIdx["LTCzMAX"]])
    
        print( 'Plot MAX LTC-XYZ for all satellites...')

        # Configure plot and call plot generation function
        SatPlots.plotMaxLTCxyz(SatStatsData)

#Plot Number of MIs for all satellites as a box-plot
    if(Conf["Plot_NMI"] == '1'):
    # Read the cols we need from SatStats file
        SatStatsData = read_csv(SatStatsFile, delim_whitespace=True, skiprows=1, header=None,\
        usecols=[SatStatsIdx["PRN"],SatStatsIdx["NMI"]])
    
        print( 'Plot Number of MIs for all satellites as a box-plot...')

        # Configure plot and call plot generation function
        SatPlots.plotNmi(SatStatsData)

#Plot Number of Transitions for all satellites as a box-plot
    if(Conf["Plot_NTRANS"] == '1'):
    # Read the cols we need from SatStats file
        SatStatsData = read_csv(SatStatsFile, delim_whitespace=True, skiprows=1, header=None,\
        usecols=[SatStatsIdx["PRN"],SatStatsIdx["NTRANS"]])
    
        print( 'Plot Number of Transitions for all satellites as a box-plot...')

        # Configure plot and call plot generation function
        SatPlots.plotNtrans(SatStatsData)

#PLOTS Vs. TIME /////////////////////////////////////////////////////////////////////////////////
# Plot Satellite monitored
if(Conf["PLOT_MON1"] == '1'):
    # Read the cols we need from SAT file
    SatData = read_csv(SatFile, delim_whitespace=True, skiprows=1, header=None,\
    usecols=[SatIdx["SoD"], SatIdx["MONSTAT"]])
    
    print( 'Plot the instantaneous number of satellites monitored...')

    # Configure plot and call plot generation function
    SatPlots.plotMON1(SatData)
#Plot satellites monitoring windows
if(Conf["PLOT_MON2"] == '1'):
    # Read the cols we need from SAT file
    SatData = read_csv(SatFile, delim_whitespace=True, skiprows=1, header=None,\
    usecols=[SatIdx["SoD"],SatIdx["PRN"],SatIdx["NRIMS"],SatIdx["MONSTAT"]])
    
    print( 'Plot satellites monitoring windows...')

    # Configure plot and call plot generation function
    SatPlots.plotMon2(SatData)

# Plot Satellite Tracks figures
if(Conf["PLOT_MON3"] == '1'):
    # Read the cols we need from SAT file
    SatData = read_csv(SatFile, delim_whitespace=True, skiprows=1, header=None,\
    usecols=[SatIdx["SoD"],SatIdx["SAT-X"], SatIdx["SAT-Y"], SatIdx["SAT-Z"], SatIdx["NRIMS"],SatIdx["MONSTAT"]])
    
    print( 'Plot the satellites ground tracks on a map during monitoring periods...')

    # Configure plot and call plot generation function
    SatPlots.plotMon3(SatData)

# Plot SREW figures
if(Conf["PLOT_SREWvsTime"] == '1'):
    # Read the cols we need from SAT file
    SatData = read_csv(SatFile, delim_whitespace=True, skiprows=1, header=None,\
    usecols=[SatIdx["SoD"],SatIdx["NRIMS"], SatIdx["SREW"]])
    
    print( 'Plot the SREW for all satellites as a function of the hour of the day...')

    # Configure plot and call plot generation function
    SatPlots.plotSREW(SatData)

# Plot SigmaFLT (PRN) figures
if(Conf["PLOT_SigmaFLT_PRN"] == '1'):
    # Read the cols we need from SAT file
    SatData = read_csv(SatFile, delim_whitespace=True, skiprows=1, header=None,\
    usecols=[SatIdx["SoD"],SatIdx["PRN"], SatIdx["SFLT-W"],SatIdx["RDOP"]])
    
    print( 'Plot the SigmaFLT for all satellites...')

    # Configure plot and call plot generation function
    SatPlots.plotSigmaFLTPRN(SatData)
# Plot Si figures
if(Conf["PLOT_SI"] == '1'):
    # Read the cols we need from SAT file
    SatData = read_csv(SatFile, delim_whitespace=True, skiprows=1, header=None,\
    usecols=[SatIdx["SoD"],SatIdx["NRIMS"], SatIdx["SFLT-W"],SatIdx["SREW"]])
    
    print( 'Plot the SI for all satellites...')

    # Configure plot and call plot generation function
    SatPlots.plotSI(SatData)

# Plot ENT-GPS Offset figures
if(Conf["PLOT_ENT-GPSOffset"] == '1'):
    # Read the cols we need from SAT file
    EntGpsData = read_csv(EntGpsFile, delim_whitespace=True, skiprows=1, header=None,\
    usecols=[EntGpsIdx["SoD"],EntGpsIdx["ENT-GPS"]])
    
    print( 'Plot the ENT-GPS Offset along the day...')

    # Configure plot and call plot generation function
    SatPlots.plotENTGps(EntGpsData)



print('------------------------------------')
print('--> END OF SAT-PERFORMANCE ANALYSIS:')
print('------------------------------------')

print('Check figures at the Output folder SAT/figures/')


#######################################################
#END OF SAT PERFORMANCES MODULE
#######################################################
