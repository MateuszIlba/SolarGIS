#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""
from typing import Any, Optional
from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingException,
                       QgsProcessingAlgorithm,
                       QgsProcessingContext,
                       QgsProcessingFeedback, #
                       QgsFeatureRequest, 
                       QgsProject,
                       QgsCoordinateReferenceSystem,#
                       QgsCoordinateTransform,#
                       QgsPoint, #
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterFile,
                       QgsProcessingParameterField,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterBoolean)
from qgis import processing
from qgis.core import QgsField, QgsFields, QgsFeature
from qgis.PyQt.QtCore import QVariant
import numpy as np
import pandas as pd
from numpy.linalg import inv
import math
import re


yearr=2023 #abstract yer for calculation n-day in year

#################calculate solar time from EPW file###################################
def zamianagodzinynaw(godzina):
    global w
    localmeridian0=UTCZONE * 15 #LSTM Local Standard Time Meridian
    BBB=(n-81)*(360.0/365.0)
    BBB=math.radians(BBB)
    EOT=9.87*math.sin(2*BBB)-7.53*math.cos(BBB)-1.5*math.sin(BBB) #in minutes
    TC=4*(dlugoscgeograficzna-localmeridian0)+EOT #in minutes
    godzina=(godzina*60+TC)/60
    if godzina==12:
        w=0
    elif godzina<12:
        w=(12-godzina)*(-15)
    elif godzina>12:
        w=(godzina-12)*15
    else:
        pass
    return w

################def for calculate correction insolation from EPW file ####################
def korektaradiacjisolarnej(x):#w1, w2, I, Ib, Id, n):
    global n
    gamma_rad=math.radians(gamma-180) #korekta azymut od kierunku poludnia
    szerokoscgeograficzna_rad=math.radians(szerokoscgeograficzna)
    beta_rad=math.radians(beta)
    n=pd.Timestamp(yearr, int(x.month), int(x.day)).dayofyear
    w2=x.hour #godzinazplikunaslonecznienia
    w1=w2-1 #godzinaprzed
    I=x.global_r * 0.0036 #caĹ‚kowite promieniowanie w Wh (*0.0036 na MJ)  ###########
    Ib=x.direct_r * 0.0036 
    Id=x.diffuse_r * 0.0036
    ###
    zamianagodzinynaw(w1)
    w1=w
    zamianagodzinynaw(w2)
    w2=w
    w1_rad=math.radians(w1)
    w2_rad=math.radians(w2)
    #####
    deklinacja=23.45*math.sin(math.radians(360*(284+n)/365))
    deklinacja_rad=math.radians(deklinacja)
    #####
    costeta1=math.sin(deklinacja_rad)*math.sin(szerokoscgeograficzna_rad)*math.cos(beta_rad)
    costeta2=math.sin(deklinacja_rad)*math.cos(szerokoscgeograficzna_rad)*math.sin(beta_rad)*math.cos(gamma_rad)
    costeta3=math.cos(deklinacja_rad)*math.cos(szerokoscgeograficzna_rad)*math.cos(beta_rad)*math.cos(w2_rad)
    costeta4=math.cos(deklinacja_rad)*math.sin(szerokoscgeograficzna_rad)*math.sin(beta_rad)*math.cos(gamma_rad)*math.cos(w2_rad)
    costeta5=math.cos(deklinacja_rad)*math.sin(beta_rad)*math.sin(gamma_rad)*math.sin(w2_rad)
    costeta=costeta1-costeta2+costeta3+costeta4+costeta5
    costetaz=math.cos(szerokoscgeograficzna_rad)*math.cos(deklinacja_rad)*math.cos(w2_rad)+math.sin(szerokoscgeograficzna_rad)*math.sin(deklinacja_rad)
    costetaz_godzpoprz=math.cos(szerokoscgeograficzna_rad)*math.cos(deklinacja_rad)*math.cos(w1_rad)+math.sin(szerokoscgeograficzna_rad)*math.sin(deklinacja_rad)
    if costetaz_godzpoprz>0:
        Rb=costeta/costetaz
        Rb_flush=Rb
    else:
        Rb_flush=costeta/costetaz
        w1_rad=math.acos(-math.tan(szerokoscgeograficzna_rad)*math.tan(deklinacja_rad))
        aaa=math.cos(szerokoscgeograficzna_rad-beta_rad)*math.cos(deklinacja_rad)*math.cos((w1_rad+w2_rad)/2)+math.sin(szerokoscgeograficzna_rad-beta_rad)*math.sin(deklinacja_rad)
        bbb=math.cos(szerokoscgeograficzna_rad)*math.cos(deklinacja_rad)*math.cos((w1_rad+w2_rad)/2)+math.sin(szerokoscgeograficzna_rad)*math.sin(deklinacja_rad)
        Rb=aaa/bbb
    IO1=18797599.34265204*(1+0.033*math.cos(math.radians(360*n/365)))
    IO2=math.cos(szerokoscgeograficzna_rad)*math.cos(deklinacja_rad)*(math.sin(w2_rad)-math.sin(w1_rad))+math.pi*(w2-w1)/180*math.sin(szerokoscgeograficzna_rad)*math.sin(deklinacja_rad)
    IO=IO1*IO2 
    #anizotropowe
    Ai=Ib/IO
    beam=((Ib+Id*Ai)*costeta)/0.0036 #bezposrednie Rb zmienione na costeta z uwagi na to ze radiacja jest normalna
    f=math.sqrt(Ib/I)
    diffuse1=1-Ai
    diffuse2=(1+math.cos(beta_rad))/2
    diffuse3=1+f*((math.sin(beta_rad/2))**3)
    diffuse4=Ai*Rb
    diffuse=(Id*(diffuse1*diffuse2*diffuse3+diffuse4))/0.0036 #rozproszone
    reflect=(I*pg*((1-math.cos(beta_rad))/2))/0.0036 #odbite
    power = beam + diffuse + reflect
    return power

#####calculate areo on 3d polygon
def loadwkt(wkt):
    global poligonyzenklawami22
    wkt=wkt[wkt.find('(('):]
    podzialnapolygony=wkt.split('))')
    poligonyzenklawami=[]
    for i in podzialnapolygony:
        podzialnaenklawy = i.split('),(')
        poligonyzenklawami.append(podzialnaenklawy)
    poligonyzenklawami2=[]
    for i in poligonyzenklawami:
        sett=[]
        for ii in i:
            iii=ii.replace(',(','').replace('(','').replace(')','')
            if len(iii)>5:
                sett.append(iii.split(','))
            else:
                1==1
        if not sett:
            1==1
        else:
            poligonyzenklawami2.append(sett)
    poligonyzenklawami22=[]
    for objekt in poligonyzenklawami2:
        object2=[]
        for obwiednia in objekt:
            oobwiednia2=[]
            for punkt in obwiednia:
                
                wsp=punkt.split(' ')
                wspolrzedne=[]
                for i in wsp:
                    if not i:
                        1==1
                    else:
                        wspolrzedne.append(float(i))
                oobwiednia2.append(wspolrzedne)
            object2.append(oobwiednia2)
        poligonyzenklawami22.append(object2)
    #print(poligonyzenklawami22)
    #print(poligonyzenklawami22[0])
    return poligonyzenklawami22
        #print (i, len(i))
        #print (i[0][0])

def polygon_area_3d(points):
    global powierzchnia
    P1X,P1Y,P1Z = points[0][0],points[0][1],points[0][2]
    P2X,P2Y,P2Z = points[1][0],points[1][1],points[1][2]
    P3X,P3Y,P3Z = points[2][0],points[2][1],points[2][2]
    a = pow(((P2Y-P1Y)*(P3Z-P1Z)-(P3Y-P1Y)*(P2Z-P1Z)),2) + pow(((P3X-P1X)*(P2Z-P1Z)-(P2X-P1X)*(P3Z-P1Z)),2) + pow(((P2X-P1X)*(P3Y-P1Y)-(P3X-P1X)*(P2Y-P1Y)),2)
    cosnx = ((P2Y-P1Y)*(P3Z-P1Z)-(P3Y-P1Y)*(P2Z-P1Z))/(pow(a,1/2))
    cosny = ((P3X-P1X)*(P2Z-P1Z)-(P2X-P1X)*(P3Z-P1Z))/(pow(a,1/2))
    cosnz = ((P2X-P1X)*(P3Y-P1Y)-(P3X-P1X)*(P2Y-P1Y))/(pow(a,1/2))
    s = cosnz*((points[-1][0])*(P1Y)-(P1X)*(points[-1][1])) + cosnx*((points[-1][1])*(P1Z)-(P1Y)*(points[-1][2])) + cosny*((points[-1][2])*(P1X)-(P1Z)*(points[-1][0]))
    for i in range(len(points)-1):
        p1 = points[i]
        p2 = points[i+1]
        ss = cosnz*((p1[0])*(p2[1])-(p2[0])*(p1[1])) + cosnx*((p1[1])*(p2[2])-(p2[1])*(p1[2])) + cosny*((p1[2])*(p2[0])-(p2[2])*(p1[0]))
        s += ss 
    powierzchnia = abs(s/2.0)
    #print(powierzchnia)
    return powierzchnia




class ExampleProcessingAlgorithm(QgsProcessingAlgorithm):
    INPUT = 'INPUT'#vector layer 3d
    FIELDINPUT='FIELDINPUT' #field for join data
    INPUT2 ='INPUT2' #epw file
    ALBEDO = 'ALBEDO' #albedo wartość
    UTCZONE = 'UTCZONE'
    BOOLEAN1='BOOLEAN1'
    BOOLEAN2='BOOLEAN2'
    BOOLEAN3='BOOLEAN3'
    OUTPUT = 'OUTPUT' #new vector layer with calculation

#####################description of the algorithm###############################
    def tr(self, string):
        return QCoreApplication.translate('Processing', string)
    def createInstance(self):
        return ExampleProcessingAlgorithm()
    def name(self):
        return 'SolarQGIS'
    def displayName(self):
        return self.tr('SolarQGIS')
    def group(self):
        return self.tr('SolarQGIS')
    def groupId(self):
        return 'SolarQGIS'
    def shortHelpString(self):
        return self.tr("The algorithm computes the geodetic azimuth, tilt of the 3D plane and annual insolation based on them. \
        Load the data for calculating insolation in the *.epw extension. Shading is not taken into consideration by the algorithm. \n \
        Prior to running the algorithm, ensure the following: \n \
        - the input layer has a predefined planar rectangular coordinate system [EPSG]; \n \
        - the input layer contains polygon geometry with a Z coordinate. \n \
        Currently, the algorithm has undergone validation for the northern hemisphere [N].")

###################inputs and output############################################
    def initAlgorithm(self, config: Optional[dict[str, Any]] = None):#config=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                self.tr('Input layer'),
                [QgsProcessing.TypeVectorAnyGeometry]
            )
            
        )
        
        self.addParameter(
            QgsProcessingParameterField(
                self.FIELDINPUT,
                #self.asPythonString,
                self.tr('ID field'),
                parentLayerParameterName='INPUT',
                type=QgsProcessingParameterField.Any,
            )
        )
        
        self.addParameter(
            QgsProcessingParameterFile(
                self.INPUT2,
                self.tr('EPW file'),
                extension='epw'
            )
        )
        
        self.addParameter(
            QgsProcessingParameterNumber(
                self.ALBEDO,
                self.tr('Ground albedo (0 to 1)'),
                type=QgsProcessingParameterNumber.Double,
                defaultValue=0.2
            )
        )
        
        self.addParameter(
            QgsProcessingParameterNumber(
                self.UTCZONE,
                self.tr('Time Zone (-12 to 12 )'),
                type=QgsProcessingParameterNumber.Double,
                defaultValue=1
            )
        )
        
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.BOOLEAN1,
                self.tr('save azimuth'),
                #type=0,
                defaultValue=True
            )
        )
        
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.BOOLEAN2,
                self.tr('save tilt angle'),
                #type=0,
                defaultValue=True
            )
        )
        
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.BOOLEAN3,
                self.tr('save real 3D area'),
                #type=0,
                defaultValue=True
            )
        )
       
        # add a feature sink in which to store our processed features
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                self.tr('Output layer')
            )
        )

    def processAlgorithm(
        self,
        parameters: dict[str, Any],
        context: QgsProcessingContext,
        feedback: QgsProcessingFeedback,
    ) -> dict[str, Any]:
        
        global gamma, szerokoscgeograficzna, beta, pg, UTCZONE, n, dlugoscgeograficzna # global variable for analyses 
        source = self.parameterAsSource(
            parameters,
            self.INPUT,
            context
        )
        #get localization of epw file i and name of ID
        EPW_file = self.parameterAsString(parameters, self.INPUT2, context)
        FIELDINPUT = self.parameterAsString(parameters, self.FIELDINPUT, context)
        ALBEDO_=self.parameterAsDouble(parameters, self.ALBEDO, context)
        UTCZONE=self.parameterAsInt(parameters, self.UTCZONE, context)
        BOOLEAN1=self.parameterAsBoolean(parameters, self.BOOLEAN1, context)
        BOOLEAN2=self.parameterAsBoolean(parameters, self.BOOLEAN2, context)
        BOOLEAN3=self.parameterAsBoolean(parameters, self.BOOLEAN3, context)
        pg=ALBEDO_
        if source is None: #if any layer not match data print error
            raise QgsProcessingException(self.invalidSourceError(parameters, self.INPUT))
        if EPW_file is None: #error if epw file is not loaded
            raise QgsProcessingException(self.invalidSourceError(parameters, self.INPUT2))
            
        ################ new calculated atttributes#############################
        fieldss = QgsFields()
        fieldss.append(QgsField('id', QVariant.Int))
        if BOOLEAN2 is True:
            fieldss.append(QgsField('tiltangle', QVariant.Double))
        if BOOLEAN1 is True:
            fieldss.append(QgsField('azimuth', QVariant.Double))
        fieldss.append(QgsField('annual_solar_radiation', QVariant.Double))
        if BOOLEAN3 is True:
            fieldss.append(QgsField('area3D', QVariant.Double))
        
        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            fieldss,
            source.wkbType(),
            source.sourceCrs()
        )

        feedback.pushInfo('CRS is {}'.format(source.sourceCrs().authid())) # Send information to the user
        if sink is None:
            raise QgsProcessingException(self.invalidSinkError(parameters, self.OUTPUT))
            
        ##############################prepare epw ################################## 
        epwdat=pd.read_csv(EPW_file, delimiter=',', header=None, skiprows=8, dtype=None, encoding='utf-8')
        epwdatt=epwdat.drop([0,4,5,7,8,9,10,11,12,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34], axis=1).rename(columns={1: "month", 2: "day", 3: "hour",6:"tempdry", 13:"global_r", 14:"direct_r", 15:"diffuse_r"})
        epwdata=epwdatt.query('global_r > 0').reset_index()
        feedback.pushInfo('EPW loaded')
        feedback.pushInfo( str(ALBEDO_))
         
        ################################################################################
        # Compute the number of steps to display within the progress bar and get features from source
        total = 100.0 / source.featureCount() if source.featureCount() else 0
        try:
            features = source.getFeatures()
        except:
            feedback.pushInfo(' Please fix the geometry or change the Invalid features filtering')
        for current, feature in enumerate(features):
            if feedback.isCanceled():# Stop the algorithm if cancel button has been clicked
                break
        ################################# calculate geodetic azimuth and tilt angle################################
            #########finding the best 3 points representing the surface#########
            try:
                geom = feature.geometry()
            except:
                break
            verticess=geom.vertices()
            points = []
            for v in verticess: #remove duplicates vertices
                point=[v.x(), v.y(), v.z()]
                if point not in points:
                    points.append(point)
                    
                    
                    
                    
            ###calculate 3D area data
            pointarea=[]
            allvertices=str(geom.asWkt())
            
            loadwkt(allvertices)
            sumapowierzchnimultigeometry=0
            for objects in poligonyzenklawami22:
                powierzchniazenklawami=0
                for obwiedn in objects:
                    polygon_area_3d(obwiedn)
                    if powierzchniazenklawami==0:
                        powierzchniazenklawami=powierzchnia
                    else:
                        powierzchniazenklawami=powierzchniazenklawami-powierzchnia
                sumapowierzchnimultigeometry=sumapowierzchnimultigeometry+powierzchniazenklawami
            
            countpoint=len(points)
            point_one=min(points, key = lambda t: t[2]) #point one with min Z
            points.remove(point_one)
            point_two=max(points, key = lambda t: t[2]) #point two with max Z
            points.remove(point_two)
            points_d=[] #serch optimal point tree, located farthest from the other two 
            for point in points:
                d1=math.sqrt((point_one[0]-point[0])**2+(point_one[1]-point[1])**2)
                d2=math.sqrt((point_two[0]-point[0])**2+(point_two[1]-point[1])**2)
                sumd=d1+d2
                pointss=[point, sumd]
                points_d.append(pointss)
            point_tree_tmp=max(points_d, key = lambda t: t[1])
            point_tree=point_tree_tmp[0]
            
            #######conversion to EPSG 4326 for longitute and latitude############
            punktdokonwersji=QgsPoint(point_one[0], point_one[1])
            sourceCrs = source.sourceCrs()
            destCrs = QgsCoordinateReferenceSystem('EPSG:4326')
            tr = QgsCoordinateTransform(sourceCrs,destCrs, QgsProject.instance())
            punktdokonwersji.transform(tr)
            szerokoscgeograficzna=float(punktdokonwersji.y())
            dlugoscgeograficzna=float(punktdokonwersji.x())
            
            #######################calculate normal#############################
            
            a=[point_one[0]-point_tree[0], point_one[1]-point_tree[1], point_one[2]-point_tree[2]]
            b=[point_two[0]-point_tree[0], point_two[1]-point_tree[1], point_two[2]-point_tree[2]]
            xnorm=a[1]*b[2]-a[2]*b[1]
            ynorm=a[2]*b[0]-a[0]*b[2]
            znorm=a[0]*b[1]-a[1]*b[0]
            normal=[xnorm, ynorm, znorm]
            if normal[2] >0:
                normal=normal
            elif normal[2] <0:
                normal=[normal[0]*(-1), normal[1]*(-1), normal[2]*(-1)]
            
            ######################calculate tilt angle##########################
            #https://www.youtube.com/watch?v=VT5tYJhN-70&ab_channel=JamesRantschler
            
            modulwektora=math.sqrt(normal[0]*normal[0]+normal[1]*normal[1]+normal[2]*normal[2])
            try:
                tiltangle=(math.acos(normal[2]/modulwektora))*180/math.pi
                isnan=math.isnan(tiltangle)
                if isnan==True:
                    tiltangle=0
            except:
                tiltangle=0

            #########################calculate azimuth##########################
            perpendicularvector=math.sqrt(normal[0]*normal[0]+normal[1]*normal[1])
            try:
                azimuth=(math.acos(normal[0]/perpendicularvector))*180/math.pi
            except:
                azimuth=0 #tylko do znalezienia wyjatku
            azimuthk=azimuth
            if normal[0]>0 and normal[1]>0:
                azimuth=90-azimuth
            elif normal[0]<0 and normal[1]>0:
                azimuth=450-azimuth
            elif normal[0]<0 and normal[1]<0:
                azimuth=azimuth+90
            elif normal[0]>0 and normal[1]<0:
                azimuth=azimuth+90
            
            ####################calcualte correrct insolation ######################
            beta=tiltangle     #tilt angle
            gamma_fir=azimuth    #azimuth of normal 
            if gamma_fir>180:
                gamma=gamma_fir-360
            else:
                gamma=gamma_fir
            corekt_solar_radiation=epwdata.apply(korektaradiacjisolarnej, axis=1).sum()#wywolanie definicji
            
            ########################create output fields########################
            atrybut=feature.attribute(str(FIELDINPUT))
            feat = QgsFeature()
            feat.setFields(fieldss)
            feat['id'] = int(atrybut)
            if BOOLEAN2 is True:
                feat['tiltangle'] = float(tiltangle)
            if BOOLEAN1 is True: 
                feat['azimuth'] = float(azimuth)
            feat['annual_solar_radiation'] = float(corekt_solar_radiation)
            if BOOLEAN3 is True:
                feat['area3D'] = float(sumapowierzchnimultigeometry)
            feat.setGeometry(geom)
            sink.addFeature(feat, QgsFeatureSink.FastInsert) 
            feedback.setProgress(int(current * total))# Update the progress bar
        return {self.OUTPUT: dest_id}
    
    def createInstance(self):
        return self.__class__()
