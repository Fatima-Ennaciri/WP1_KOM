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
from pandas import unique
from SatFunctions import RIMSIdx
sys.path.append(os.getcwd() + '/' + \
    os.path.dirname(sys.argv[0]) + '/' + 'COMMON')
from SatFunctions import SatIdx
sys.path.append(os.getcwd() + '/' + \
    os.path.dirname(sys.argv[0]) + '/' + 'COMMON')
from SatFunctions import SatStatsIdx
sys.path.append(os.getcwd() + '/' + \
    os.path.dirname(sys.argv[0]) + '/' + 'COMMON')
from COMMON import GnssConstants
from COMMON.Plots import generatePlot


# from pyproj import Transformer
from COMMON.Coordinates import xyz2llh
from array import *
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from mpl_toolkits.axes_grid1 import make_axes_locatable

# Define SAT INFO FILE Columns
SatIdx = OrderedDict({})
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
RIMSIdx["p1"]=0
RIMSIdx["p2"]=1
RIMSIdx["p3"]=2
RIMSIdx["p4"]=3
RIMSIdx["p5"]=4
RIMSIdx["p6"]=5
RIMSIdx["p7"]=6
RIMSIdx["p8"]=7
RIMSIdx["p9"]=8
RIMSIdx["p10"]=9


#Plot RIMS MAP##################################
def Plot_RIMSMAP(RimsData):
    PlotConf= {}

    PlotConf["Type"] = "Map"
    PlotConf["FigSize"] = (9.0,9.0)
    PlotConf["Title"] = "RIMS Network"


    PlotConf["LonMin"] = -75
    PlotConf["LonMax"] = 50
    PlotConf["LatMin"] = -40
    PlotConf["LatMax"] = 90
    PlotConf["LonStep"] = 10
    PlotConf["LatStep"] = 10
    

    PlotConf["yTicks"] = range(PlotConf["LatMin"],PlotConf["LatMax"]+1,10)
    PlotConf["yLim"] = [PlotConf["LatMin"], PlotConf["LatMax"]]

    PlotConf["xTicks"] = range(PlotConf["LonMin"],PlotConf["LonMax"]+1,10)
    PlotConf["xLim"] = [PlotConf["LonMin"], PlotConf["LonMax"]]

    PlotConf["Grid"] = True

    PlotConf["Map"] = True

    PlotConf["Marker"] = '.'
    PlotConf["LineWidth"] = 1.5
    PlotConf["Color"] = 'r'
   
    PlotConf["xData"] = {}
    PlotConf["yData"] = {}
    PlotConf["Text"] = {}
    
    
    PlotConf["xData"] = RimsData[RIMSIdx["p4"]]
    PlotConf["yData"]= RimsData[RIMSIdx["p5"]]
    PlotConf["Text"] = RimsData[RIMSIdx["p2"]]
    

    PlotConf["Path"] = sys.argv[1] + '/OUT/SAT/Figures/' + 'RIMS_REF_POSITIONS_2019.png'

    # Call generatePlot from Plots Library
    generatePlot(PlotConf)


#Plot MON ##################################
def Plot_MON(SatStatsData):
    PlotConf= {}

    PlotConf["Type"] = "Bar1"
    PlotConf["FigSize"] = (12, 8)
    PlotConf["Title"] = "Satellite Monitoring Percentage Y19D014 G123 50s [%]"

    PlotConf["yLabel"] = "MON[%]"
    PlotConf["yLim"] = [34, 50]


    PlotConf["xLabel"] = "GPS-PRN"
    PlotConf["xTicksLabels"] = [ 'GO1', 'GO2', 'GO3', 'GO5', 'GO6', 'G07', 'G08', 'G09', 'G10', 'G11', 'G12', 'G13', 'G14', 'G15', 'G16', 'G17', 'G18', 'G19', 'G20',' G21', 'G22', 'G23', 'G24', 'G25', 'G26', 'G27', 'G28', 'G29', 'G30', 'G31', 'G32']
    PlotConf["xLim"] = [-1, 31]

    PlotConf["Grid"] = 1

    PlotConf["Marker"] = '.'
    PlotConf["LineWidth"] = 1.5
    PlotConf["Color"] = 'y'
    PlotConf["Legend"] = {"Legend1" : "MON[%]"}
    PlotConf["Legend"].keys()

    PlotConf["loc"] = 'top left'

    PlotConf["xData"] = {}
    PlotConf["yData"] = {}
    
    
    Label = 0
    PlotConf["xData"][Label] = SatStatsData[SatStatsIdx["PRN"]]
    PlotConf["yData"][Label] = SatStatsData[SatStatsIdx["MON"]]
    

    PlotConf["Path"] = sys.argv[1] + '/OUT/SAT/Figures/' + 'MON.png'

    # Call generatePlot from Plots Library
    generatePlot(PlotConf)

#Plot NRIMS ##################################
def Plot_NRIMS(SatStatsData):
    PlotConf= {}

    PlotConf["Type"] = "Bar2"
    PlotConf["FigSize"] = (12, 8)
    PlotConf["Title"] = "Minimum and Maximum Number of RIMS in view Y19D014 G123 50s [%]"

    PlotConf["yLabel"] = "[m]"
    PlotConf["yTicks"] = range(0, 50, +5)
    PlotConf["yLim"] = [0, 49]
    


    PlotConf["xLabel"] = "GPS-PRN"
    PlotConf["xTicksLabels"] = [ 'GO1', 'GO2', 'GO3', 'GO5', 'GO6', 'G07', 'G08', 'G09', 'G10', 'G11', 'G12', 'G13', 'G14', 'G15', 'G16', 'G17', 'G18', 'G19', 'G20',' G21', 'G22', 'G23', 'G24', 'G25', 'G26', 'G27', 'G28', 'G29', 'G30', 'G31', 'G32']
    PlotConf["xLim"] = [-1, 31]

    PlotConf["Grid"] = 1

    PlotConf["Marker"] = '.'
    PlotConf["LineWidth"] = 1.5


    PlotConf["xData"] = {}
    PlotConf["yData"] = {}
    PlotConf["Color"] = {}
    PlotConf["Legend"] = {}

    Label = ["RIMS-MAX", "RIMS-MIN"]
    Color = ["mediumaquamarine", "seagreen"]
    

    for index, label in enumerate(Label):
        PlotConf["xData"][label] = SatStatsData[SatStatsIdx["PRN"]] 
        PlotConf["yData"][label] = SatStatsData[SatStatsIdx[label]]
        PlotConf["Color"][label] = Color[index]
          
        PlotConf["xData"].keys()
        PlotConf["yData"].keys()
        PlotConf["Color"].keys()
        PlotConf["Legend"] = {"Legend 1" : "MAX NRIMS", "Legend 2" : "MIN NRIMS"}
        PlotConf["Legend"].keys()
        
    
    PlotConf["Path"] = sys.argv[1] + '/OUT/SAT/Figures/' + 'NRIMS.png'

    # Call generatePlot from Plots Library
    generatePlot(PlotConf)

#Plot RMS-SREACR ##################################
def plotSREacrRMS(SatStatsData):
    PlotConf = {}

    PlotConf["Type"] = "Bar2"
    PlotConf["FigSize"] = (12.0,8.0)
    PlotConf["Title"] = "RMS-SREacr "

    PlotConf["xLabel"] = "GPS-PRN"
    PlotConf["xTicks"] = range(0, 32)
    
    PlotConf["yLabel"] = "[m]"
    PlotConf["yLim"] = [0, 5]
    
    PlotConf["Grid"] = 1

    PlotConf["Marker"] = '.'
    PlotConf["LineWidth"] = 1.5
    
    PlotConf["xData"] = {}
    PlotConf["yData"] = {}
    PlotConf["Color"] = {}

    Label = {}
    Label = ["SREaRMS", "SREcRMS", "SRErRMS"]
    Color = ["deepskyblue", "red", "orchid"]
    
    
    for index, label in enumerate(Label):
        PlotConf["xData"][label] = SatStatsData[SatStatsIdx["PRN"]]
        PlotConf["yData"][label] = SatStatsData[SatStatsIdx[label]]
        PlotConf["Color"][label] = Color[index]
          
        PlotConf["xData"].keys()
        PlotConf["yData"].keys()
        PlotConf["Color"].keys()
        PlotConf["Legend"] = {"Legend1" : "RMS SRE-A[m]","Legend2" : "RMS SRE-C[m]", "Legend3" : "RMS SRE-R[m]"}
        PlotConf["Legend"].keys()
            
    PlotConf["Path"] = sys.argv[1] + '/OUT/SAT/Figures/' + 'SREacrRMS.png'
    
    # Call generatePlot from Plots library
    generatePlot(PlotConf) 

# Plot SREbRMS ##################################
def plotSREbRMS(SatStatsData):

    PlotConf = {}

    PlotConf["Type"] = "Bar2"
    PlotConf["FigSize"] = (12.0,8.0)
    PlotConf["Title"] = "RMS of SREb clock Error Component Y19D014 G123 50s  "

    PlotConf["xLabel"] = "GPS-PRN"
    PlotConf["xTicks"] = range(0, 32)

    PlotConf["yLabel"] = "[m]"
    PlotConf["yLim"] = [0.2, 1.6]
   
    
    PlotConf["Grid"] = 1

    PlotConf["Marker"] = '.'
    PlotConf["LineWidth"] = 1.5
    
    PlotConf["xData"] = {}
    PlotConf["yData"] = {}
    PlotConf["Color"] = {}
    

    Label = {}
    Label = ["SREbRMS"]
    Color = ["darkviolet"]
    
    
    for index, label in enumerate(Label):
        PlotConf["xData"][label] = SatStatsData[SatStatsIdx["PRN"]]
        PlotConf["yData"][label] = SatStatsData[SatStatsIdx[label]]
        PlotConf["Color"][label] = Color[index]
        

    PlotConf["yData"].keys()
    PlotConf["Color"].keys()
    PlotConf["Legend"] = {"Legend1" : "RMS SRE-B[m]"}
    PlotConf["Legend"].keys()
            
    PlotConf["Path"] = sys.argv[1] + '/OUT/SAT/Figures/' + 'SREbRMS.png'
    
    # Call generatePlot from Plots library
    generatePlot(PlotConf) 
    
# Plot RMS SREW and MAX SREW ##################################

def plotRmsSrewMaxSrew(SatStatsData):
    PlotConf = {}

    PlotConf["Type"] = "Bar2"
    PlotConf["FigSize"] = (12.0,8.0)
    PlotConf["Title"] = "RMS SREW and MAX SREW Y19D014 G123 50s "

    PlotConf["xLabel"] = "GPS-PRN"
    
    PlotConf["yLabel"] = "[m]"
    PlotConf["yLim"] = [0, 3]

    PlotConf["Grid"] = 1

    PlotConf["Marker"] = '.'
    PlotConf["LineWidth"] = 1.5
    
    PlotConf["xData"] = {}
    PlotConf["yData"] = {}
    PlotConf["Color"] = {}

    Label = {}
    Label = ["SREWMAX", "SREWRMS"]
    color = ["darkviolet", "deepskyblue"]
    
    for index, label in enumerate(Label):
        PlotConf["xData"][label] = SatStatsData[SatStatsIdx["PRN"]]
        PlotConf["yData"][label] = SatStatsData[SatStatsIdx[label]]
        PlotConf["Color"][label] = color[index]
        
        PlotConf["yData"].keys()
        PlotConf["Color"].keys()
        PlotConf["Legend"] = {"Legend1" : "MAX SREW[m]","Legend2" : "RMS SREW[m]"}
        PlotConf["Legend"].keys()
            
    PlotConf["Path"] = sys.argv[1] + '/OUT/SAT/Figures/' + 'RMS_and_Maximum_Value_of_SRE_at_the_WUL_Y19D014_G123_50s.png'
    
    # Call generatePlot from Plots library
    generatePlot(PlotConf)
    
# Plot RMS SREW and MAX SREW ##################################

def plotMinMaxSFLT(SatStatsData):
    PlotConf = {}

    PlotConf["Type"] = "Bar2"
    PlotConf["FigSize"] = (12.0,8.0)
    PlotConf["Title"] = "Maximum and Minimum Sigma FLT (=Sigma UDRE) Y19D014 G123 50s "

    PlotConf["xLabel"] = "GPS-PRN"
    
    PlotConf["yLabel"] = "[m]"
    PlotConf["yLim"] = [0.5, 5]

    PlotConf["Grid"] = 1

    PlotConf["Marker"] = '.'
    PlotConf["LineWidth"] = 1.5
    
    PlotConf["xData"] = {}
    PlotConf["yData"] = {}
    PlotConf["Color"] = {}

    Label = {}
    Label = ["SFLTMAX", "SFLTMIN"]
    color = ["skyblue","dodgerblue"]
    
    for index, label in enumerate(Label):
        PlotConf["xData"][label] = SatStatsData[SatStatsIdx["PRN"]]
        PlotConf["yData"][label] = SatStatsData[SatStatsIdx[label]]
        PlotConf["Color"][label] = color[index]
        
        PlotConf["yData"].keys()
        PlotConf["Color"].keys()
        PlotConf["Legend"] = {"Legend1" : "MAX SFLT[m]","Legend2" : "MIN SFLT[m]"}
        PlotConf["Legend"].keys()
            
    PlotConf["Path"] = sys.argv[1] + '/OUT/SAT/Figures/' + 'Maximum_and_Minimum_Sigma_FLT_(=Sigma_UDRE)_Y19D014_G123_50s.png'
    
    # Call generatePlot from Plots library
    generatePlot(PlotConf) 
    
# Plot MAX SIW##################################    
def plotMaxSiw(SatStatsData):
    PlotConf = {}

    PlotConf["Type"] = "Bar"
    
    PlotConf["FigSize"] = (12.0,8.0)
    PlotConf["Title"] = "Maximum Satellite Safety Index at WUL SREW/5.33UDRE Y19D014 G123 50s "

    PlotConf["xLabel"] = "GPS-PRN"
    
    PlotConf["yLabel"] = "[m]"
    PlotConf["yLim"] = [0, 1.2]

    
    PlotConf["Grid"] = 1

    PlotConf["Marker"] = '.'
    PlotConf["LineWidth"] = 1.5
    
    PlotConf["xData"] = {}
    PlotConf["yData"] = {}
    PlotConf["Color"] = {}

    Label= 0
    PlotConf["xData"][Label] = SatStatsData[SatStatsIdx["PRN"]]
    PlotConf["yData"][Label] = SatStatsData[SatStatsIdx["SIMAX"]]
    PlotConf["Color"] = 'y'
    
    PlotConf["Legend"] = {"Legend1" : "LIMIT","Legend2" : "MAX SI"}
    PlotConf["Legend"].keys()
            
    PlotConf["Path"] = sys.argv[1] + '/OUT/SAT/Figures/' + 'Maximum_Satellite_Safety_Index_at_WUL_Y19D014_G123_50s.png'
    
    # Call generatePlot from Plots library
    generatePlot(PlotConf)

# Plot Satellite Clock Fast and Long Term Correctons Y19D014 G123 50s ##################################

def plotMaxFcLTCb(SatStatsData):
    PlotConf = {}
        
    PlotConf["Type"] = "Lines"
    PlotConf["FigSize"] = (12.0,8.0)
    PlotConf["Title"] = "Satellite Clock Fast and Long Term Correctons Y19D014 G123 50s "

    PlotConf["xLabel"] = "GPS-PRN"
    PlotConf["xTicks"] = range(0, 32)
    
    PlotConf["yLabel"] = "[m]"
    PlotConf["yLim"] = [0.5, 4]
    
   
    PlotConf["Grid"] = 1

    PlotConf["Marker"] = '-s'
    PlotConf["LineWidth"] = 1.5
    
    PlotConf["xData"] = {}
    PlotConf["yData"] = {}
    PlotConf["Color"] = {}

    Label = {}
    Label = ["LTCbMAX", "FCMAX"]
    
    c = ['s', 'g']
    
    for index, label in enumerate(Label):
        PlotConf["xData"][label] = SatStatsData[SatStatsIdx["PRN"]]
        PlotConf["yData"][label] = SatStatsData[SatStatsIdx[label]]
        PlotConf["Color"][label] = c[index]
        
        PlotConf["yData"].keys()
        PlotConf["Color"].keys()
        PlotConf["Legend"] = {"Legend1" : "MAX LTCb[m]", "Legend2" : "MAX FC[m]"}
        PlotConf["Legend"].keys()
            
    PlotConf["Path"] = sys.argv[1] + '/OUT/SAT/Figures/' + 'Satellite Clock Fast and Long Term Correctons Y19D014 G123 50s.png'
    
    # Call generatePlot from Plots library
    generatePlot(PlotConf)

# Plot Maximum Satellite LTC-XYZ Y19D014 G123 50s ##################################

def plotMaxLTCxyz(SatStatsData):
    PlotConf = {}
        
    PlotConf["Type"] = "Lines"
    PlotConf["FigSize"] = (12.0,8.0)
    PlotConf["Title"] = "Maximum Satellite LTC-XYZ Y19D014 G123 50s "

    PlotConf["xLabel"] = "GPS-PRN"
    PlotConf["xTicks"] = range(0, 32)
    
    PlotConf["yLabel"] = "[m]"
    PlotConf["yLim"] = [0, 8]
    
   
    PlotConf["Grid"] = 1

    PlotConf["Marker"] = '-s'
    PlotConf["LineWidth"] = 1.5
    
    PlotConf["xData"] = {}
    PlotConf["yData"] = {}
    PlotConf["Color"] = {}

    Label = {}
    Label = ["LTCxMAX", "LTCyMAX", "LTCzMAX"]
    
    c = ['s', 'g', 'p']
    
    for index, label in enumerate(Label):
        PlotConf["xData"][label] = SatStatsData[SatStatsIdx["PRN"]]
        PlotConf["yData"][label] = SatStatsData[SatStatsIdx[label]]
        PlotConf["Color"][label] = c[index]
        
        PlotConf["yData"].keys()
        PlotConf["Color"].keys()
        PlotConf["Legend"] = {"Legend1" : "MAX LTCx[m]", "Legend2" : "MAX LTCy[m]", "Legend3" : "MAX LTCz[m]"}
        PlotConf["Legend"].keys()
            
    PlotConf["Path"] = sys.argv[1] + '/OUT/SAT/Figures/' + 'Maximum Satellite LTC-XYZ Y19D014 G123 50s.png'
    
    # Call generatePlot from Plots library
    generatePlot(PlotConf)
    
# Plot NMI ##################################
def plotNmi(SatStatsData):
    PlotConf = {}

    PlotConf["Type"] = "Bar1"
    
    PlotConf["FigSize"] = (12.0,8.0)
    PlotConf["Title"] = "Number of MIs Y19D014 G123 50s "

    PlotConf["xLabel"] = "GPS-PRN"
    
    PlotConf["yLabel"] = "[m]"
    PlotConf["yLim"] = [0, 1]
    
    
    PlotConf["Grid"] = 1

    PlotConf["Marker"] = '.'
    PlotConf["LineWidth"] = 1.5
    
    PlotConf["xData"] = {}
    PlotConf["yData"] = {}
    PlotConf["Color"] = {}

    Label= 0
  
    PlotConf["xData"][Label] = SatStatsData[SatStatsIdx["PRN"]]
    PlotConf["yData"][Label] = SatStatsData[SatStatsIdx["NMI"]]
    PlotConf["Color"] = 'y'
    
    PlotConf["Legend"] = {"Legend1" : "NMI"}
    PlotConf["Legend"].keys()
            
    PlotConf["Path"] = sys.argv[1] + '/OUT/SAT/Figures/' + 'Number_of_MIs_Y19D014_G123_50s.png'
    
    # Call generatePlot from Plots library
    generatePlot(PlotConf)
    
# Plot NTRANS ##################################
def plotNtrans(SatStatsData):
    PlotConf = {}

    PlotConf["Type"] = "Bar1"
    
    PlotConf["FigSize"] = (12.0,8.0)
    PlotConf["Title"] = "Number of Transitions M to NM or M to DU Y19D104 G123 50s"

    PlotConf["xLabel"] = "GPS-PRN"
    
    PlotConf["yLabel"] = "[m]"
    PlotConf["yLim"] = [0, 8]
    
    
    PlotConf["Grid"] = 1

    PlotConf["Marker"] = ''
    PlotConf["LineWidth"] = 1.5
    
    PlotConf["xData"] = {}
    PlotConf["yData"] = {}
    PlotConf["Color"] = {}

    Label= 0
  
    PlotConf["xData"][Label] = SatStatsData[SatStatsIdx["PRN"]]
    PlotConf["yData"][Label] = SatStatsData[SatStatsIdx["NTRANS"]]
    PlotConf["Color"] = 'm'
    
    PlotConf["Legend"] = {"Legend1" : "Number of Transitions"}
    PlotConf["Legend"].keys()
            
    PlotConf["Path"] = sys.argv[1] + '/OUT/SAT/Figures/' + 'Number_of_Transitions_M_to_NM_or_M_to_DU_Y19D014_G123_50s.png'
    
    # Call generatePlot from Plots library
    generatePlot(PlotConf)
##PLOT VS TIMES
# Plot Number_of_Satellites_Monitored_EGNOS_SIS_D014Y19  
def plotMON1(SatData):
    PlotConf = {}

    PlotConf["Type"] = "Lines"
    PlotConf["FigSize"] = (12.0,8.0)
    PlotConf["Title"] = "Number of Satellites Monitored EGNOS SIS Y19D014 G123 50s "

    PlotConf["xLabel"] = "Hour of DoY 01419"
    PlotConf["xTicks"] = range(0, 25)
    PlotConf["xLim"] = [0, 24]

    PlotConf["yLim"] = [0, 25]
 
    PlotConf["Grid"] = 1

    PlotConf["Marker"] = '.'
    PlotConf["LineWidth"] = 0.01
    
    PlotConf["xData"] = {}
    PlotConf["yData"] = {}

    PlotConf["Color"] = {}
    PlotConf["Legend"] = {}

    NMON = []
    NNM = []
    NDU = []

    for SoD in unique (SatData[SatIdx["SoD"]]):
        M = 1
        NM = 0
        DU = -1
        FilterCond = (SatData[SatIdx["SoD"]]) == SoD
        MonstatSoD = SatData[SatIdx["MONSTAT"]][FilterCond]
        

        FilterCond = MonstatSoD == 1
        M = np.sum(FilterCond)
        NMON.append(M)

        FilterCond = MonstatSoD == 0
        NM = np.sum(FilterCond)
        NNM.append(NM)
       
        FilterCond = MonstatSoD == -1
        DU = np.sum(FilterCond)
        NDU.append(DU)
    
    Label = ["MONITORED", "NOT-MONITORED", "DONT USE"]
    Color = ["red","green", "blue"]

    
    PlotConf["xData"]["MONITORED"] = unique (SatData[SatIdx["SoD"]]) / GnssConstants.S_IN_H
    PlotConf["yData"]["MONITORED"] = NMON

    PlotConf["xData"]["NOT-MONITORED"] = unique (SatData[SatIdx["SoD"]]) / GnssConstants.S_IN_H
    PlotConf["yData"]["NOT-MONITORED"] = NNM

    PlotConf["xData"]["DONT USE"] = unique (SatData[SatIdx["SoD"]]) / GnssConstants.S_IN_H
    PlotConf["yData"]["DONT USE"] = NDU

    PlotConf["Path"] = sys.argv[1] + '/OUT/SAT/Figures/' + 'Number_of_Satellites_Monitored_EGNOS_SIS_D014Y19.png'

    # Call generatePlot from Plots library
    generatePlot(PlotConf)

#Plot satellites monitoring windows
def plotMon2(SatData):
    PlotConf = {}

    PlotConf["Type"] = "Lines"
    PlotConf["FigSize"] = (8.4,7.6)
    PlotConf["Title"] = "Satellite Monitoring EGNOS SIS DO14Y19"
    PlotConf["yLabel"] = "GPS-PRN"
    PlotConf["yLim"] = [0,31]
    PlotConf["yTicksLabels"] = ['1','2','3','5','6','7','8','9','10','11','12','13','14','15', '16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32']
   
    PlotConf["xLabel"] = "Hour of DoY 01419"
    PlotConf["xTicks"] = range(0, 25)
    PlotConf["xLim"] = [0, 24]
    PlotConf["Grid"] = 1

    PlotConf["Marker"] = '.'
    PlotConf["LineWidth"] = 2

    PlotConf["ColorBar"] = "gnuplot"
    PlotConf["ColorBarLabel"] = "Number of RIMS"
    PlotConf["ColorBarMin"] = 0.
    PlotConf["ColorBarMax"] = 40.

    
    PlotConf["xData"] = {}
    PlotConf["yData"] = {}
    PlotConf["zData"] = {}

    FilterCond = (SatData[SatIdx["MONSTAT"]]) == 1
    
    
    for prn in sorted(unique(SatData[SatIdx["PRN"]])):
        Label = prn 
        FilterCond2 = SatData[SatIdx["PRN"]] == prn
        PlotConf["xData"][Label] = SatData[SatIdx["SoD"]][FilterCond][FilterCond2]/ GnssConstants.S_IN_H
        PlotConf["yData"][Label] = SatData[SatIdx["PRN"]][FilterCond][FilterCond2]
        PlotConf["zData"][Label] = SatData[SatIdx["NRIMS"]][FilterCond][FilterCond2]

    PlotConf["Path"] = sys.argv[1] + '/OUT/SAT/Figures/' + 'Satellite_Monitoring_EGNOS_SIS_DO14Y19.png'

    # Call generatePlot from Plots library
    generatePlot(PlotConf)

#Plot the satellites ground tracks on a map during monitoring periods
def plotMon3(SatData):
    PlotConf = {}

    PlotConf["Type"] = "Lines"
    PlotConf["FigSize"] = (16.8,15.2)
    PlotConf["Title"] = "Satellite Tracks during Monitoring periods D014Y19"

    PlotConf["LonMin"] = -135
    PlotConf["LonMax"] = 135
    PlotConf["LatMin"] = -70
    PlotConf["LatMax"] = 90
    PlotConf["LonStep"] = 15
    PlotConf["LatStep"] = 10

    
    PlotConf["yTicks"] = range(PlotConf["LatMin"],PlotConf["LatMax"]+1,10)
    PlotConf["yLim"] = [PlotConf["LatMin"], PlotConf["LatMax"]]

  
    PlotConf["xTicks"] = range(PlotConf["LonMin"],PlotConf["LonMax"]+1,15)
    PlotConf["xLim"] = [PlotConf["LonMin"], PlotConf["LonMax"]]

    PlotConf["Grid"] = True

    PlotConf["Map"] = True

    PlotConf["Marker"] = '.'
    PlotConf["LineWidth"] = 1.5
    PlotConf["Color"] = 'g'
    PlotConf["Legend"] = {"Legend1" : "RIMS"}
    PlotConf["Legend"].keys()

    PlotConf["ColorBar"] = "gnuplot"
    PlotConf["ColorBarLabel"] = "Number of RIMS"
    PlotConf["ColorBarMin"] = 0.
    PlotConf["ColorBarMax"] = 40.

    # Transform ECEF to Geodetic  
    SatData[SatIdx["SAT-X"]].to_numpy()
    SatData[SatIdx["SAT-Y"]].to_numpy()
    SatData[SatIdx["SAT-Z"]].to_numpy()
    DataLen = len(SatData[SatIdx["SAT-X"]])
    Longitude = np.zeros(DataLen)
    Latitude = np.zeros(DataLen)
    # transformer = Transformer.from_crs('epsg:4978', 'epsg:4326')
    for index in range(DataLen):
        x = SatData[SatIdx["SAT-X"]][index] * 1000
        y = SatData[SatIdx["SAT-Y"]][index] * 1000
        z = SatData[SatIdx["SAT-Z"]][index] * 1000
        if x + y + z != 0:
           Longitude[index], Latitude[index],h = xyz2llh(x, y, z)
           # Latitude[index], Longitude[index], h = transformer.transform(x, y, z)
    
    PlotConf["Legend"] = {"Legend1" : "RIMS"}
    PlotConf["Legend"].keys()
    PlotConf["Color"] = 'g'

    PlotConf["xData"] = {}
    PlotConf["yData"] = {}
    PlotConf["zData"] = {}

    
    FilterCond = (SatData[SatIdx["MONSTAT"]]) == 1
    PlotConf["xData"]["RIMS"] = Longitude[FilterCond]
    PlotConf["yData"]["RIMS"] = Latitude[FilterCond]
    PlotConf["zData"]["RIMS"] = SatData[SatIdx["NRIMS"]][FilterCond]
    
    PlotConf["Path"] = sys.argv[1] + '/OUT/SAT/Figures/' + 'SAT_TRACKS_D014Y19.png'

    # Call generatePlot from Plots library
    generatePlot(PlotConf)

#Plot the SREW for all satellites as a function of the hour of the day
def plotSREW(SatData):
    PlotConf = {}

    PlotConf["Type"] = "Lines"
    PlotConf["FigSize"] = (8.4,6.6)
    PlotConf["Title"] = "Satellite SREW EGNOS SIS DO14Y19"
    PlotConf["yLabel"] = "[m]"
    PlotConf["yLim"] = [0, 2.5]
   

    PlotConf["xLabel"] = "Hour of DoY 01419"
    PlotConf["xTicks"] = range(0, 25)
    PlotConf["xLim"] = [0, 24]

    PlotConf["Grid"] = 1

    PlotConf["Marker"] = '.'
    PlotConf["LineWidth"] = 1

    PlotConf["ColorBar"] = "gnuplot"
    PlotConf["ColorBarLabel"] = "PRN"
    PlotConf["ColorBarMin"] = 1.
    PlotConf["ColorBarMax"] = 32.
    PlotConf["ColorBarTicks"] = sorted(unique(SatData[SatIdx["NRIMS"]])) 

    PlotConf["xData"] = {}
    PlotConf["yData"] = {}
    PlotConf["zData"] = {}

    Label = 0
    PlotConf["xData"][Label] = (SatData[SatIdx["SoD"]]) / GnssConstants.S_IN_H
    PlotConf["yData"][Label] = SatData[SatIdx["SREW"]]
    PlotConf["zData"][Label] = SatData[SatIdx["NRIMS"]]

    PlotConf["Path"] = sys.argv[1] + '/OUT/SAT/Figures/' + 'SAT_SREW_EGNOS_D014Y19.png'

    # Call generatePlot from Plots library
    generatePlot(PlotConf)

#Plot the SigmaFLT for all satellites as a function of the hour of the day
def plotSigmaFLTPRN(SatData):
    PlotConf = {}

    PlotConf["Type"] = "Lines"
    PlotConf["FigSize"] = (8.4,6.6)
    PlotConf["Title"] = "Satellite SigmaFLT at Wul EGNOS SIS DO14Y19"
    PlotConf["yLabel"] = "[m]"
    PlotConf["yLim"] = [0.5, 5]
   

    PlotConf["xLabel"] = "Hour of DoY 01419"
    PlotConf["xTicks"] = range(0, 25)
    PlotConf["xLim"] = [0, 24]

    PlotConf["Grid"] = 1

    PlotConf["Marker"] = '.'
    PlotConf["LineWidth"] = 1

    PlotConf["ColorBar"] = "gnuplot"
    PlotConf["ColorBarLabel"] = "Inverse Radial DOP"
    PlotConf["ColorBarMin"] = 0.
    PlotConf["ColorBarMax"] = 100.
    


    PlotConf["xData"] = {}
    PlotConf["yData"] = {}
    PlotConf["zData"] = {}

    Label = []
    for prn in sorted(unique(SatData[SatIdx["PRN"]])):
        Label = prn
        FilterCond = SatData[SatIdx["PRN"]]== prn 
        PlotConf["xData"][Label] = ((SatData[SatIdx["SoD"]])[FilterCond]) / GnssConstants.S_IN_H
        PlotConf["yData"][Label] = ((SatData[SatIdx["SFLT-W"]])[FilterCond])
        PlotConf["zData"][Label] = ((SatData[SatIdx["RDOP"]])[FilterCond])

        PlotConf["Path"] = sys.argv[1] + '/OUT/SAT/Figures/' + 'SAT_SFLT_EGNOS_D014Y19.png'

    # Call generatePlot from Plots library
    generatePlot(PlotConf)
#Plot the SI for all satellites as a function of the hour of the day
def plotSI(SatData):
    PlotConf = {}

    PlotConf["Type"] = "Lines"
    PlotConf["FigSize"] = (8.4,6.6)
    PlotConf["Title"] = "Satellite SREW/5.33SigmaFLT at WYL EGNOS SIS DO14Y19"
    PlotConf["yLabel"] = "[m]"
    PlotConf["yLim"] = [0, 0.45]
   

    PlotConf["xLabel"] = "Hour of DoY 01419"
    PlotConf["xTicks"] = range(0, 25)
    PlotConf["xLim"] = [0, 24]

    PlotConf["Grid"] = 1

    PlotConf["Marker"] = '.'
    PlotConf["LineWidth"] = 1

    PlotConf["ColorBar"] = "gnuplot"
    PlotConf["ColorBarLabel"] = "PRN"
    PlotConf["ColorBarMin"] = 1.
    PlotConf["ColorBarMax"] = 39.
    PlotConf["ColorBarTicks"] = sorted(unique(SatData[SatIdx["NRIMS"]]))

    PlotConf["xData"] = {}
    PlotConf["yData"] = {}
    PlotConf["zData"] = {}
    
    PlotConf["xData"]["SREW/5.33SigmaFLT"] = (SatData[SatIdx["SoD"]])/ GnssConstants.S_IN_H
    PlotConf["yData"]["SREW/5.33SigmaFLT"] =((SatData[SatIdx["SREW"]]) / (5.33 * (SatData[SatIdx["SFLT-W"]])))
    PlotConf["zData"]["SREW/5.33SigmaFLT"] = SatData[SatIdx["NRIMS"]]

    PlotConf["Legend"] = {"Legend1" : "SREW/5.33SigmaFLT"}
    PlotConf["Legend"].keys() 

    PlotConf["Path"] = sys.argv[1] + '/OUT/SAT/Figures/' + 'SAT_SI_EGNOS_D014Y19.png'

    # Call generatePlot from Plots library
    generatePlot(PlotConf)

#Plot the ENT-GPS Offset along the day
def plotENTGps(EntGpsData):
    PlotConf = {}

    PlotConf["Type"] = "Lines"
    PlotConf["FigSize"] = (8.4,6.6)
    PlotConf["Title"] = "ENTGPS EGNOS SIS DO14Y19"
    PlotConf["yLabel"] = "[m]"
    PlotConf["yLim"] = [-2.6, -1]
   

    PlotConf["xLabel"] = "Hour of DoY 01419"
    PlotConf["xTicks"] = range(0, 25)
    PlotConf["xLim"] = [0, 24]

    PlotConf["Grid"] = 1

    PlotConf["Marker"] = ''
    PlotConf["LineWidth"] = 1


    PlotConf["xData"] = {}
    PlotConf["yData"] = {}
    


    Label = 0
    PlotConf["xData"]["ENTGPS [m]"] = EntGpsData[EntGpsIdx["SoD"]] /  GnssConstants.S_IN_H
    PlotConf["yData"]["ENTGPS [m]"] = EntGpsData[EntGpsIdx["ENT-GPS"]]
    PlotConf["Color"] = 'm'
    
    PlotConf["Legend"] = {"Legend1" : "ENTGPS [m]"}
    PlotConf["Legend"].keys()
    PlotConf["Color"].keys()
     
    PlotConf["Path"] = sys.argv[1] + '/OUT/SAT/Figures/' + 'SAT_ENT-GPS_Offset_EGNOS_D014Y19.png'

    # Call generatePlot from Plots library
    generatePlot(PlotConf)

########################################################################
#END OF SAT FUNCTIONS MODULE
########################################################################


