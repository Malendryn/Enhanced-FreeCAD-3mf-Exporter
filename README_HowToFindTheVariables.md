
The current example shows how to set a property with a value to apply an infill to individual objects, but there are many other variables you can set on an object in Cura (and other slicers too)  but ... how do you find the names of these variables? This
README attempts to explain how!

The easiest way is to create an object, import it into Cura, modify the 'Per Model Settings' on that object and change the settings you want to be able to control in FreeCAD, then export that object to a .3mf file, and look at the contents of the 3mf file.

So, for starters, create a simple .3mf (or .stl) file to load in Cura as follows:

1) In FreeCAD, load the 'Part' workbench, create a cube, select it, and export it to either a .stl or .3mf file.

2) In Cura, open that .3mf or .stl file and you should now have a single object named 'Cube'

3) Select the Cube, and in the toolbar on the left-side of Cura's window, select the icon for 'Per Model Settings'  (In Cura 5.x, it's the 5th icon down from the top of the toolbar)

4) click the 'Select Settings' button and scroll through to find what settings you want to be able to edit in FreeCAD.
    a) for example, scroll down to 'Support' and check the 'Generate Support' button. You should immediately see 'Generate Support' over in the first dialog.
    2) Add another, lets use the Infill Density as per our 'HowToUse' readme.  Scroll to the 'Infill' area and check the 'Infill Density' box, and it should again appear in the other dialog.

5) Click 'Close' and you should now be back to the Per Model Settings dialog.

6) Set a value for Infill Density, and either check or uncheck 'Generate Support' as you choose.

7) Click the topmost icon in the left toolbar (or just press the letter 'T') to go back to move mode, which will close the Per Model Settings dialog.

8) Select the Cube, and in the File menu select 'Export Selection'.

9) Export this object to a .3mf file.


Now, this newly created .3mf file has the information you need, but we have to dig into it to find that info! so, to do that:

1) Rename the .3mf file and change its extension to '.zip'
    This file can now be unzipped into a subdirectory, which will contain a few files and subdirectories.
2) Unzip the file, and then CD into the '3D' directory inside.
3) load the file '3dmodel.model' into a text editor.

You should now be looking at a standard XML formatted file, and the area you're looking for in particular is right at the top, where it says "<metadatagroup>", and inside there are your two settings, and the names you need to know!

That area should look like this:
			<metadatagroup>
				<metadata name="cura:infill_sparse_density">97.5</metadata>
				<metadata name="cura:support_enable">False</metadata>
			</metadatagroup>

So, as you can see in our example in the other file, we used "infill_sparse_density" which you can see right here!

And there you have it! Those are the names of the properties to set in FreeCAD to make them work in Cura!  (When using them, make
sure to drop the 'cura' portion of this name, as the exporter script will put them in on its own.)

