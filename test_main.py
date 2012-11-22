"""
This program tries to predict digits using KNN classifier with k = 1.
similarity metric used: Pearson Correlation Coefficient.

It sorts only single digit positive numbers, and numbers can be digital or handwritten.
requirement:
    Image must be noise free.
    
Once detected, the program will give back the sorted image.
"""
dest = "uploads/"
import glob
import os
from SimpleCV import *
import sys,time

def zscore( num1 ):
    mean = np.mean( num1 )
    std = np.std( num1 )
    
    return ( num1 - mean ) / std
    
class Number:
    def __init__( self, image, num ):
        self.number = num
        self.image = image

size = 10
pwd = os.getcwd()
max_size = ( 64 * 64 * 3 )


def generate_features():
    os.chdir( "./dataset" )
    feature_list = []
    target_list = []
    for index in xrange( 0, size ):
        label = index
        files = glob.glob( str( index ) + "*.jpg" )[ : 5 ]
        if True:
            for filename in files:
                image = Image( filename )
                image = image.invert().findBlobs()[-1].crop().adaptiveScale( ( 64, 64 ) )
                
                feature = zscore( image.getNumpy().ravel() )
                feature_list.append( feature )
                target_list.append( label )
    os.chdir( pwd )
    return ( feature_list, target_list )

feature_list, target_list = generate_features()

def get_output( input_image ):
    f = open( "log.txt", mode = "w" )
    f.write( input_image )
    f.close()
    image = Image ( input_image ).invert()
    output_image = "output.jpg"

    binarized = image
    num_list = []
    output = []
    im_list = []

    for blob in binarized.findBlobs():
        output = []
        blob = blob.crop().adaptiveScale( ( 64, 64 ) )
        feature = zscore( blob.getNumpy().ravel() )
        for i in range( 0, len( feature_list ) ):
            s = np.sum( feature * feature_list[ i ] )
            p = s / max_size
            output.append( ( target_list[ i ], p ) )
            
        output = sorted( output, key = lambda val : val[ 1 ], reverse = True )
        num_list.append( Number( blob, output[ 0 ][ 0 ] ) )
    
    
    num_list = sorted( num_list, key = lambda x : x.number )
    j = num_list[ 0 ].image.invert()
    
    for i in range( 1, len( num_list ) ):
        j = j.sideBySide( num_list[ i ].image.invert() )
    
    j.save( dest + output_image )
    return j.filename

if __name__ == "__main__":
    print get_output( "four.jpg" )
