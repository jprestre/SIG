# encoding: utf-8

'''
Función que permite remuestrear un raster en función de un raster de entrada.
La salida de la función, es un nuevo raster que entrega el raster de entrada remuestreado en otra escala espacial.
***************************
raster_resample(inputfile, referencefile, outputfile):

inputfile = Ruta, nombre y extensión del archivo a procesar. Debe ir dentro de comillas
referencefile = Ruta, nombre y extensión del archivo que tiene la extensión espacial de referencia. Debe ir dentro de comillas
outputfile = = Ruta, nombre y extensión del archivo procesado. Debe ir dentro de comillas

'''
def raster_resample(inputfile, referencefile, outputfile):
    from osgeo import gdal, gdalconst

    input_ = gdal.Open(inputfile, gdalconst.GA_ReadOnly)
    inputProj = input_.GetProjection()
    inputTrans = input_.GetGeoTransform()
    bandreference = input_.GetRasterBand(1) 

 
    reference = gdal.Open(referencefile)
    referenceProj = reference.GetProjection()
    referenceTrans = reference.GetGeoTransform()
    bandreference = reference.GetRasterBand(1)    
    x = reference.RasterXSize 
    y = reference.RasterYSize

    
    inputTrans = list(inputTrans)
    referenceTrans = list(referenceTrans)
    inputTrans[1] = referenceTrans[1]
    inputTrans[-1] = referenceTrans[-1]
    inputTrans = tuple(inputTrans)
    referenceTrans = inputTrans
    
    driver= gdal.GetDriverByName('GTiff')
    output = driver.Create(outputfile,x,y,1,bandreference.DataType)
    output.SetGeoTransform(referenceTrans)
    output.SetProjection(referenceProj)

    gdal.ReprojectImage(input_,output,inputProj,referenceProj,gdalconst.GRA_Bilinear)

    del output