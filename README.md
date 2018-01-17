File: proj3.py, model.py
Description: allows a user to navigate a small image library, add/save tags, provides search functions
Environment: Python3/ PyQt5

Author: Kanakapriya Krishnakumar
Last edited: 10/1/2017
"""

The following Python code should be run on the terminal with the following command line:
	python3 proj3.py W

Before the user does that, they should cd to the directory they have the project saved. 
W is an integer that contains the width of the main window. Make sure it is within 600 to 1200 frame. **PREFERRED TO BE 800**
   EX:python3 proj3.py 800

1.
There are seven used cases-
   Cursor begins with the left most picture, following keys will allow you to move the   
   cursor. 
	1. Left arrow: will let you browse/select the images going in the left direction
	2. Right arrow: will let you browse/select the images going in the right direction
	3. ‘>’: move image bar to the next 5 images in the list 
	4. ‘<’: move image bar to the previous 5 images in the list 
	5. Up arrow: zooms in the image the cursor is at
	6. Down arrow: zooms out image, going back to the image browser
	7. MOUSE EVENT: clicking on any image will zoom in that image, and then zoom out
2. 
Auditory Icons
	When any key is pressed or mouse is clicked, you will hear a sound. If you press 	the greater than or less than key, you will notice that it makes a louder noise.
3.
Text Annotations
	When you zoom in a picture, make sure to enlarge the window to see the following buttons and textbox. You can type anything in the textbox, and when you click add tag, it will be added to the list on the right hand side that says tags. If you click save all tags, it will be saved in that image. When you exit out and zoom in that image, you will notice that the tag is still there. 

	Another feature to this is, all tags will be saved in a text file with the name of the image so that you will know what image you added the tag on.

4. 
UI Actions- five functions
	1. Test Button: interpret the text in the left textbook as url and gets image at 	   the url
	2. Search Button: Using Flickr Photo Database, search for tags displayed in the 	   search box
	3. Save Button: saves images into the folder that were search
	4. Exit Button: Application exits
	5. Delete Button: selected image is deleted	






