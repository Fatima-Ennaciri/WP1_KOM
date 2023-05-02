#!/usr/bin/env python

########################################################################
# SatFunctions.py:
# This script defines all internal functions of SatPerformance Module
#
#  Project:        SBPT
#  File:           SatFunctions.py
#  Date(YY/MM/DD): 20/07/11
#
#   Author: GNSS Academy
#   Copyright 2020 GNSS Academy
# 
# Internal dependencies:
#   COMMON
########################################################################


# Import External and Internal functions and Libraries
#----------------------------------------------------------------------
import sys, os
# Add path to find all modules
Common = os.path.dirname(os.path.dirname(
    os.path.abspath(sys.argv[0]))) + '/COMMON'
sys.path.insert(0, Common)
from collections import OrderedDict
from COMMON import GnssConstants
from math import sqrt
import numpy as np

# Define SAT INFO FILE Columns
SatIdx= OrderedDict({})
SatIdx["SoD"]=0
SatIdx["DOY"]=1
SatIdx["PRN"]=2
SatIdx["SAT-X"]=3
SatIdx["SAT-Y"]=4
SatIdx["SAT-Z"]=5
SatIdx["MONSTAT"]=6
SatIdx["SRESTAT"]=7
SatIdx["SREx"]=8
SatIdx["SREy"]=9
SatIdx["SREz"]=10
SatIdx["SREb1"]=11
SatIdx["SREW"]=12
SatIdx["SFLT-W"]=13
SatIdx["UDREI"]=14
SatIdx["FC"]=15
SatIdx["AF0"]=16
SatIdx["AF1"]=17
SatIdx["LTCx"]=18
SatIdx["LTCy"]=19
SatIdx["LTCz"]=20
SatIdx["NRIMS"]=21
SatIdx["RDOP"]=22

# Define SAT STATISTICS file Columns
SatStatsIdx = OrderedDict({})
SatStatsIdx["PRN"]=0
SatStatsIdx["MON"]=1
SatStatsIdx["RIMS-MIN"]=2
SatStatsIdx["RIMS-MAX"]=3
SatStatsIdx["SREaRMS"]=4
SatStatsIdx["SREcRMS"]=5
SatStatsIdx["SRErRMS"]=6
SatStatsIdx["SREbRMS"]=7
SatStatsIdx["SREWRMS"]=8
SatStatsIdx["SREWMAX"]=9 
SatStatsIdx["SFLTMAX"]=10
SatStatsIdx["SFLTMIN"]=11
SatStatsIdx["SIMAX"]=12
SatStatsIdx["FCMAX"]=13
SatStatsIdx["LTCbMAX"]=14
SatStatsIdx["LTCxMAX"]=15
SatStatsIdx["LTCyMAX"]=16
SatStatsIdx["LTCzMAX"]=17
SatStatsIdx["NMI"]=18
SatStatsIdx["NTRANS"]=19

#Define  SAT ENTGPS file Columns
EntGpsIdx = OrderedDict({})
EntGpsIdx["SoD"]=0
EntGpsIdx["ENT-GPS"]=1

# Define RIMS file Columns
RIMSIdx = OrderedDict({})
RIMSIdx["p1"]=0              #p1: Selection flag [0:OFF/1:ON]
RIMSIdx["p2"]=1              #p2: Station Name Acronym [%4s]
RIMSIdx["p3"]=2              #p3: Station Number ID [%2d]
RIMSIdx["p4"]=3              #p4: Longitude [deg]          
RIMSIdx["p5"]=4              #p5: Latitude [deg]
RIMSIdx["p6"]=5              #p6: Height [meters]
RIMSIdx["p7"]=6              #p7: Mask Angle [deg]
RIMSIdx["p8"]=7              #p8: Acquisition Time [minutes]
RIMSIdx["p9"]=8              #p10: Country [%s]
RIMSIdx["p10"]=9             #p9: Site [%s]


# FUNCTION: Display Message
#-----------------------------------------------------------------------

def displayUsage():
    sys.stderr.write("ERROR: Please provide SAT.dat file (satellite instantaneous\n\
information file) as a unique argument\n")


# FUNCTION: Split line
#-----------------------------------------------------------------------

def splitLine(Line):
    LineSplit = Line.split()

    return LineSplit


# FUNCTION: Read Sat Info Epoch
#-----------------------------------------------------------------------

def readSatInfoEpoch(f):
    EpochInfo = []
    
    # Read one line
    Line = f.readline()
    if(not Line):
        return []
    LineSplit = splitLine(Line)
    Sod = LineSplit[SatIdx["SoD"]]
    SodNext = Sod

    while SodNext == Sod:
        EpochInfo.append(LineSplit)
        Pointer = f.tell()
        Line = f.readline()
        LineSplit = splitLine(Line)
        try: 
            SodNext = LineSplit[SatIdx["SoD"]]

        except:
            return EpochInfo

    f.seek(Pointer)

    return EpochInfo

# FUNCTION: Initialized Output Statistics
#-----------------------------------------------------------------------

def initializeOutputs(Outputs):
    
    # Loop over GPS and Galileo Satellites
    for Const in ['G', 'E']:
        
        # Loop over all satellites of each constellation 
        for Prn in range(1,33):

            SatLabel = Const + "%02d" % Prn
            Outputs[SatLabel] = OrderedDict({})
            for var in SatStatsIdx.keys():
                
                if (var == "PRN"):
                    Outputs[SatLabel][var] = SatLabel
                
                elif (var == "RIMS-MIN"):
                    Outputs[SatLabel][var] = 1e12
                
                elif (var == "SFLTMIN"):
                    Outputs[SatLabel][var] = 1e12

                else:
                    Outputs[SatLabel][var] = 0.0

# FUNCTION: Initialize Intermediate Outputs
#-----------------------------------------------------------------------

def initializeInterOutputs(InterOutputs):
    
    # Loop over GPS and Galileo Satellites
    for Const in ['G', 'E']:
        
        for Prn in range(1,33):

            SatLabel = Const + "%02d" % Prn
            InterOutputs[SatLabel] = OrderedDict({})
            InterOutputs[SatLabel]["NSAMPS"] = 0
            InterOutputs[SatLabel]["SODPREV"] = 0
            InterOutputs[SatLabel]["MONPREV"] = 0
            InterOutputs[SatLabel]["SREb"] = 0
            InterOutputs[SatLabel]["SREbSUM2"] = 0
            InterOutputs[SatLabel]["SREaSUM2"] = 0
            InterOutputs[SatLabel]["SREcSUM2"] = 0
            InterOutputs[SatLabel]["SRErSUM2"] = 0
            InterOutputs[SatLabel]["SREACRSAMPS"] = 0
            InterOutputs[SatLabel]["SREWSUM2"] = 0
            InterOutputs[SatLabel]["SREWSAMPS"] = 0
            InterOutputs[SatLabel]["XPREV"] = 0
            InterOutputs[SatLabel]["YPREV"] = 0
            InterOutputs[SatLabel]["ZPREV"] = 0

    InterOutputs["ENT-GPS"] = 0

    return

# FUNCTION: Project a vector into a given direction
def projectVector(Vector, Direction):
    
    # Compute the Unitary Vector
    UnitaryVector = Direction / np.linalg.norm(Direction)

    return Vector.dot(UnitaryVector)

# FUNCTION: Estimate SRE-Along/Cross/Radial
#-----------------------------------------------------------------------

def computeSreAcr(DeltaT, PosPrev, Pos, Sre):

    # Compute Velocity computation deriving the position
    Vel = (Pos - PosPrev) / DeltaT
    
    # Add Earth's Rotation Effect on the Reference frame
    Vel = Vel + np.cross(np.array([0, 0, GnssConstants.OMEGA_EARTH]), Pos)

    # Compute unitary vectors
    Ur = Pos / np.linalg.norm(Pos)
    Uv = Vel / np.linalg.norm(Vel)
    Uc = np.cross(Ur, Uv)
    Ua = np.cross(Uc, Ur)

    # Compute SRE in ACR frame by projecting the SRE in XYZ
    SreA = projectVector(Sre, Ua)
    SreC = projectVector(Sre, Uc)
    SreR = projectVector(Sre, Ur)

    return SreA, SreC, SreR

# FUNCTION: Compute SRE-B
# ----------------------------------------------------------------------
def computeSreb(EpochInfo, InterOutputs):
    # List of SRE-B of the monitored satellites
    SrebMonitored = []

    # Loop over all satellites Information in Epoch
    # -------------------------------------------
    for SatInfo in EpochInfo:
        # Check if satellite is monitored
        if(SatInfo[SatIdx["SRESTAT"]] == '1'):
            # Got Satellite positions
            SatX = float(SatInfo[SatIdx["SAT-X"]])*1000
            SatY = float(SatInfo[SatIdx["SAT-Y"]])*1000
            SatZ = float(SatInfo[SatIdx["SAT-Z"]])*1000

            #Got norm of the satellite position vector
            GeomNorm = np.linalg.norm([SatX, SatY, SatZ])

            #Compute SRE-Radial
            Srer = \
                (float(SatInfo[SatIdx["SREx"]])* SatX +\
                    float(SatInfo[SatIdx["SREy"]])* SatY +\
                        float(SatInfo[SatIdx["SREz"]])* SatZ) /\
                            GeomNorm

            #Build list of SRE-B of each monitored satellite
            SrebMonitored.append(float(SatInfo[SatIdx["SREb1"]]) - Srer)            

    # Compute ENT-GPS Offset
    InterOutputs["ENT-GPS"] = np.median(SrebMonitored) 
    
    # Loop over all satellites Information in Epoch
    # --------------------------------------------
    for SatInfo in EpochInfo:
        #Check if satellite is monitored
        if(SatInfo[SatIdx["SRESTAT"]] == '1'):
            #Remove ENT-GPS offset from SREb1
            InterOutputs[SatInfo[SatIdx["PRN"]]]["SREb"] = \
             float(SatInfo[SatIdx["SREb1"]]) - InterOutputs["ENT-GPS"]

    return


# FUNCTION: Update Statistics Information
#-----------------------------------------------------------------------

def updateEpochStats(SatInfo, InterOutputs, Outputs):
    
    # Extract PRN Column
    sat = SatInfo[SatIdx["PRN"]]

    # Add Number of samples
    InterOutputs[sat]["NSAMPS"] = InterOutputs[sat]["NSAMPS"] + 1

    # Add Satellite Monitoring if Satellite is Monitored
    Outputs[sat]["MON"] = Outputs[sat]["MON"] + (SatInfo[SatIdx["MONSTAT"]] == '1')

    # Update the Number of Transitions MtoNM and MtoDU
    if((SatInfo[SatIdx["MONSTAT"]] != '1') and \
        (InterOutputs[sat]["MONPREV"]== '1')):
        Outputs[sat]["NTRANS"] = Outputs[sat]["NTRANS"] + 1

    # Ignore the first Epoch in the Statistcs due to Velocity 
    if(int(SatInfo[SatIdx["SoD"]]) > 0.0):  

        ###IF SATELLITE IS MONITORED and SRE_STATUS IS OK:
        if((SatInfo[SatIdx["MONSTAT"]] == '1') and \
            (SatInfo[SatIdx["SRESTAT"]] == '1')):

            #Update the minimum number of rims in view 
            if(int(SatInfo[SatIdx["NRIMS"]])<Outputs[sat]["RIMS-MIN"]): 
                Outputs[sat]["RIMS-MIN"] = int(SatInfo[SatIdx["NRIMS"]])


            #ESTIMATE SRE_ACR FROM SRE_XYZ PROJECTED INTO ACR DIRECTION
            #-----------------------------------------------------------------
            #Estimate the Delta Time between previous epoch and current
            DeltaT = int(SatInfo[SatIdx["SoD"]]) - InterOutputs[sat]["SODPREV"]

            #Extract Previous Satellite Position
            PosPrev = np.array([
                InterOutputs[sat]["XPREV"],
                InterOutputs[sat]["YPREV"],
                InterOutputs[sat]["ZPREV"]])
                
            #Extract Correct Satellite Position
            Pos = np.array([
                SatInfo[SatIdx["SAT-X"]],
                SatInfo[SatIdx["SAT-Y"]],
                SatInfo[SatIdx["SAT-Z"]],
                ], dtype = 'float64')

            #Extract SRE-XYZ Components
            Sre = np.array([
                SatInfo[SatIdx["SREx"]],
                SatInfo[SatIdx["SREy"]],
                SatInfo[SatIdx["SREz"]],
                ], dtype = 'float64')

            #Compute Along-Cross-Radial Components
            SreA, SreC, SreR = computeSreAcr(DeltaT, PosPrev, Pos, Sre)

            #Update sum of SREacr for RMS computation
            InterOutputs[sat]["SREaSUM2"] = InterOutputs[sat]["SREaSUM2"] + SreA**2
            InterOutputs[sat]["SREcSUM2"] = InterOutputs[sat]["SREcSUM2"] + SreC**2
            InterOutputs[sat]["SRErSUM2"] = InterOutputs[sat]["SRErSUM2"] + SreR**2

            #Update number of samples used for RMS of RSE in ACR frame
            InterOutputs[sat]["SREACRSAMPS"] = InterOutputs[sat]["SREACRSAMPS"] + 1

            #Estimate Extreme Values for the other Variables
            #----------------------------------------------------------------------

            # Update number of samples Monitored & SRE OK
            InterOutputs[sat]["SREWSAMPS"] = InterOutputs[sat]["SREWSAMPS"] + 1
            #Update the Minimum Number of RIMS in view  
            if(Outputs[sat]["RIMS-MIN"] > int(SatInfo[SatIdx["NRIMS"]])):
                Outputs[sat]["RIMS-MIN"] = int(SatInfo[SatIdx["NRIMS"]])

            #Update the Maximum Number of RIMS in view
            if(Outputs[sat]["RIMS-MAX"] < int(SatInfo[SatIdx["NRIMS"]])):
                Outputs[sat]["RIMS-MAX"] = int(SatInfo[SatIdx["NRIMS"]])

            #Compute Safety Index (SI) = SREW/(5.33*SigmaFLT)
            if(float(SatInfo[SatIdx["SFLT-W"]])!=0):
                Siw = \
                    float(SatInfo[SatIdx["SREW"]]) /\
                        (5.33 * float(SatInfo[SatIdx["SFLT-W"]]))
            else:
                Siw = -1

            #Update the Maximum Safety Index
            if(Outputs[sat]["SIMAX"] < Siw ):
                Outputs[sat]["SIMAX"] = Siw
            
            #Count the Misleading Informations SIW>1
            if(Siw > 1):
                Outputs[sat]["NMI"]=Outputs[sat]["NMI"] + 1

            #Update the Maximum SigmaFLT
            if(Outputs[sat]["SFLTMAX"] < float(SatInfo[SatIdx["SFLT-W"]])):
                Outputs[sat]["SFLTMAX"] = float(SatInfo[SatIdx["SFLT-W"]])

            #Update the Minimum SigmaFLT
            if(Outputs[sat]["SFLTMIN"] > float(SatInfo[SatIdx["SFLT-W"]])):
                Outputs[sat]["SFLTMIN"] = float(SatInfo[SatIdx["SFLT-W"]])

            #Update the Maximum FC
            if(Outputs[sat]["FCMAX"] < abs(float(SatInfo[SatIdx["FC"]]))):
                Outputs[sat]["FCMAX"] = abs(float(SatInfo[SatIdx["FC"]]))

            #Update the Maximum LTCb (Af0)
            if(Outputs[sat]["LTCbMAX"] < abs(float(SatInfo[SatIdx["AF0"]]))):
               Outputs[sat]["LTCbMAX"] = abs(float(SatInfo[SatIdx["AF0"]]))

            #Update the Maximum LTCx)
            if(Outputs[sat]["LTCxMAX"] < abs(float(SatInfo[SatIdx["LTCx"]]))):
                Outputs[sat]["LTCxMAX"] = abs(float(SatInfo[SatIdx["LTCx"]]))

            #Update the Maximum LTCy)
            if(Outputs[sat]["LTCyMAX"] < abs(float(SatInfo[SatIdx["LTCy"]]))):
                Outputs[sat]["LTCyMAX"] = abs(float(SatInfo[SatIdx["LTCy"]]))

            #Update the Maximum LTCz)
            if(Outputs[sat]["LTCzMAX"] < abs(float(SatInfo[SatIdx["LTCz"]]))):
                Outputs[sat]["LTCzMAX"] = abs(float(SatInfo[SatIdx["LTCz"]]))
            
            #Update the Maximum SREW
            if(Outputs[sat]["SREWMAX"] < abs(float(SatInfo[SatIdx["SREW"]]))):
                Outputs[sat]["SREWMAX"] = abs(float(SatInfo[SatIdx["SREW"]]))

            #Update sum of SREb^2 for RMS computation
            InterOutputs[sat]["SREbSUM2"] = \
                InterOutputs[sat]["SREbSUM2"] + float(InterOutputs[sat]["SREb"])**2

            #Update sum of SREW^2 for RMS computation
            InterOutputs[sat]["SREWSUM2"] = \
                InterOutputs[sat]["SREWSUM2"] + float(SatInfo[SatIdx["SREW"]])**2

        #End of if(SatInfo[SatIdx["SRESTAT"]] == '1'):

    #End of if(SatInfo[SatIdx["MONSTAT"]] == '1'):
    #End of if(int(SatInfo(SatIdx["SoD"])) > 0.0):

    # KEEP CURRENT INFORMATION FOR NEXT EPOCH

    #Keep Current SOD
    InterOutputs[sat]["SODPREV"] = int(SatInfo[SatIdx["SoD"]])
    
    #Keep Current Monitoring Status
    InterOutputs[sat]["MONPREV"] = SatInfo[SatIdx["MONSTAT"]]

    #Keep Current Satellite Position 
    InterOutputs[sat]["XPREV"] = float(SatInfo[SatIdx["SAT-X"]])
    InterOutputs[sat]["YPREV"] = float(SatInfo[SatIdx["SAT-Y"]])
    InterOutputs[sat]["ZPREV"] = float(SatInfo[SatIdx["SAT-Z"]])

    #end if(SatInfo[SatIdx["SRESTAT"]] == '1'):


# END OF FUNCTION: def updateEpochStats(SatInfo, InterOutputs, Outputs):


# FUNCTION: Compute the final Statistics
#-----------------------------------------------------------------------
def computeFinalStatistics(InterOutputs, Outputs):
    for sat in Outputs.keys():

        # Estimate the Monitoring Percentage
        if(InterOutputs[sat]["NSAMPS"] != 0):

            # Monitoring percentage = Monitored epochs / Total epochs
            Outputs[sat]["MON"] = Outputs[sat]["MON"] * 100.0 / InterOutputs[sat]["NSAMPS"]
        
        # Estimate RMS of SREW and SREb
        if(InterOutputs[sat]["SREWSAMPS"] != 0):
            Outputs[sat]["SREaRMS"] = sqrt(InterOutputs[sat]["SREaSUM2"] / InterOutputs[sat]["SREWSAMPS"])
            Outputs[sat]["SREcRMS"] = sqrt(InterOutputs[sat]["SREcSUM2"] / InterOutputs[sat]["SREWSAMPS"])
            Outputs[sat]["SRErRMS"] = sqrt(InterOutputs[sat]["SRErSUM2"] / InterOutputs[sat]["SREWSAMPS"])
            Outputs[sat]["SREbRMS"] = sqrt(InterOutputs[sat]["SREbSUM2"] / InterOutputs[sat]["SREWSAMPS"])
            Outputs[sat]["SREWRMS"] = sqrt(InterOutputs[sat]["SREWSUM2"] / InterOutputs[sat]["SREWSAMPS"])

# END OF FUNCTION: def computeFinalStatistics(InterOutputs, Outputs):


# FUNCTION: Function to compute the Satellite Statistics
#-----------------------------------------------------------------------
def computeSatStats(SatFile, EntGpsFile, SatStatsFile):
    
    # Initialize Variables
    EndOfFile = False
    EpochInfo = []

    # Open SAT INFO file
    with open(SatFile, 'r') as fsat:
        
        # Read header line of Sat Information file
        fsat.readline()

        # Open ENT-GPS Offset output file
        with open(EntGpsFile, 'w') as fEntGps:

            # Write Header of Output files
            fEntGps.write("#SoD  ENT-GPS\n")

            # Open Output File Satellite Statistics file
            with open(SatStatsFile, 'w') as fOut:
                
                # Write Header of Output files
                fOut.write("#PRN  MON   minRIMS MaxRIMS SREaRMS  SREcRMS  SRErRMS  SREbRMS  SREWRMS  SREWMAX SFLTMAX   SFLTMIN   SIMAX    FCMAX   LTCbMAX  LTCxMAX  LTCyMAX  LTCzMAX   NMI  NTRANS \n")

                # Define and Initialize Variables            
                Outputs = OrderedDict({})
                InterOutputs = OrderedDict({})
                
                # Initialize Outputs
                initializeOutputs(Outputs)
                initializeInterOutputs(InterOutputs)

                # LOOP over all Epochs of SAT INFO file
                # ----------------------------------------------------------
                while not EndOfFile:
                    
                    # Read Only One Epoch
                    EpochInfo = readSatInfoEpoch(fsat)
                    
                    # If EpochInfor is not Null
                    if EpochInfo != []:
                        # Compute SRE b
                        computeSreb(EpochInfo, InterOutputs)

                        # Write ENT-GPS Offset file
                        fEntGps.write("%5s %10.4f\n" % \
                            (
                                EpochInfo[0][SatIdx["SoD"]],
                                InterOutputs["ENT-GPS"]
                            ))

                        # Loop over all Satellites Information in Epoch
                        # --------------------------------------------------
                        for SatInfo in EpochInfo:
                            
                            # Update the Output Statistics
                            updateEpochStats(SatInfo, InterOutputs, Outputs)
                            
                        #End of for SatInfo in EpochInfo:
                                            
                    # end if EpochInfo != []:
                    else:
                        EndOfFile = True

                    #End of if EpochInfo != []:
                    
                # End of while not EndOfFile:

                # Compute the final Statistics
                # ----------------------------------------------------------
                computeFinalStatistics(InterOutputs, Outputs)
                
                # Write Statistics File
                # ----------------------------------------------------------
                
                # Define Output file format
                Format = "%s %6.2f %4d %6d %10.3f %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f %4d"
                FormatList = Format.split()

                for sat in Outputs.keys():
                    
                    # Remove 0% monitored satellites because we're not interested in them
                    if(Outputs[sat]["MON"] != 0):
                       # print(Outputs[sat].keys())

                        for i, result in enumerate(Outputs[sat]):
                            fOut.write(((FormatList[i] + " ") % Outputs[sat][result]))

                        fOut.write("\n")

                        # End of for i, result in enumerate(Outputs[sat]):
                    # End of if(Outputs[sat]["MON"] != 0):
                # End of for sat in Outputs.keys():
            # End of with open(SatStatsFile, 'w') as fOut:
        # End of with open(EntGpsFile, 'w') as fEntGps:
    # End of with open(SatFile, 'r') as f:

#End of def computeSatStats(SatFile, EntGpsFile, SatStatsFile):
    
########################################################################
#END OF SAT FUNCTIONS MODULE
########################################################################