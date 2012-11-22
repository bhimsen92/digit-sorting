from SimpleCV import Image,Color
import os

def removeBlackPatchesL( image, threshold = 12, save = True ):
    for row in xrange( 0, image.height ):
        for col in xrange( 0, image.width ):
            if col < threshold:
                image[ col, row ] = Color.WHITE
            else:
                break
    if save:
        image.save()
    else:
        return image
    
def removeBlackPatchesR( image, threshold = 12 ):
    for row in xrange( 0, image.height ):
        for col in xrange( image.width - 1, 0, -1 ):
            if col > ( image.width - threshold ):
                image[ col, row ] = Color.WHITE
            else:
                break
    image.save()

def rotateClockWise( image, min_angle, max_angle ):
    x = image.width / 2
    y = image.height / 2
    index = os.path.basename( image.filename ).split( "." )[ 0 ][ -1 ]
    for angle in xrange( min_angle, max_angle + 1 ):
        rotated_image = image.rotate( -angle, ( x, y ) )
        rotated_image.resize( 64, 64 )
        rotated_image.save( str( index ) + str( angle ) + "r.jpg" )
        print "rotated %s through %s angle,clockwise." % ( index, angle )


def rotateAntiClockWise( image, min_angle, max_angle ):
    x = image.width / 2
    y = image.height / 2
    index = os.path.basename( image.filename ).split( "." )[ 0 ][ -1 ]
    for angle in xrange( min_angle, max_angle + 1 ):
        rotated_image = image.rotate( angle, ( x, y ) )
        rotated_image.resize( 64, 64 )        
        rotated_image.save( str( index ) + str( angle ) + "l.jpg" )
        print "rotated %s through %s angle,anticlockwise." % ( index, angle )


size = 10
filename = ""
target = "dataset"
image_list = []
for index in xrange( 0, size ):
    filename = "../" + str( index ) + ".jpg"
    image = Image( filename )
    image.resize( 64, 64 ).save( str( index ) + ".jpg" )
    image_list.append( image.filename )
    print "%s thumbnail created." % ( image.filename )

# create rotated images.
# functions will create images at the current directory labeled by number and angle.format: [ angle ][ number ].jpg
os.chdir( target )
for image in image_list:
    rotateClockWise( Image( image ), min_angle = 0, max_angle = 45  )    
    rotateAntiClockWise( Image( image ), min_angle = 0, max_angle = 45 )

