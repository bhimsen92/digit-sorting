from flask import Flask, request, send_from_directory, redirect, url_for
from werkzeug import secure_filename
import test_main,os

app = Flask(__name__)
app.debug = True
app.config['UPLOAD_FOLDER'] = "uploads/"

@app.route("/")
def index():
    html_form = """
        <html>
            <head>
                <title>AIW Project</title>
            </head>
            <body>
                <h1>Sorting Digits present in an image using SimpleCV Image Processing Library</h1>                
                <h2>Algorithm:</h2>
                <ol>
                    <li>Read the dataset of digits.</li>
                    <li>Generate z-score for each image. Here every pixel will act as feature.</li>
                    <li>Read the image submitted by user.</li>
                    <li>Get the all the <b><i>connected components( CC )</i></b> present in the image.</li>
                    <li>Find out <i>Pearson Correlation Coefficient(PCC)</i> for the CC with respect to all the images present in the database.</li>                    
                    <li>Sort the PCC values.</li>
                    <li>Regenerate the image and show it to the user.</li>
                </ol>
                <h2>What it can do...</h2>
                <ol>
                    <li>It can sort Single digit numbers( black and white images ).</li>
                    <li>They can be digital( computer generated digits ) or hand written.</li>
                    <li>Digits whose orientation is in between ( -45deg to +45deg ).</li>
                </ol>
                <h2>What it can not do...</h2>
                <ol>
                    <li>It can`t sort images which contain noise :). Background needs to be very clean and Black and white images are MUST.</li>
                </ol>
                
                <b><i>If you are seeing the same image again and agiain then Please clear your browser CACHE.. :)</i></b>
                <hr />
                <h1>Submit your image here: </h1>
                <form action="process/" method="post" enctype="multipart/form-data">
                    <table>
                        <tr>
                            <td><input type="file" name="file" /></td>
                        </tr>
                        <tr>
                            <td><input type="submit" name="submit" value="Sort IT!!" /></td>
                        </tr>
                    </table>
                </form>
            </body>
    """
    return html_form

@app.route( "/process/", methods=[ "POST" ] )
def process():
    html = """
        <html>
            <head>
                <title>AIW Project</title>
            </head>
            <body>
                <h1>Input Image</h1>
                <img src="/%s" height = "300" />
                <h1>Sorted Image</h1>
                <img src="/uploads/%s" height = "128" />
            </body>
        </html>
    """
    if request.method == "POST":
        file = request.files[ "file" ]
        f = secure_filename(file.filename)
        file.save( os.path.join(app.config['UPLOAD_FOLDER'], f) )
        out = test_main.get_output( os.path.join(app.config['UPLOAD_FOLDER'], f) )
        return html % ( os.path.join(app.config['UPLOAD_FOLDER'], f ), "output.jpg" )
        """ 
        return redirect( url_for('uploaded_file',
                                    filename= "output.jpg" ) """
    else:
        return "This method only accepts POST methods!!"

@app.route( "/about" )
def about():
    return "In about"
    
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)    
if __name__ == "__main__":
    app.run()
