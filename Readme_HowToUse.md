
###############################################################################################
Title:    Enhanced FreeCAD 3mf Exporter
By:       Ron Stanions (Malendryn)
Created:  03/31/2023
Updated:  03/31/2023
Version:  0.1.0
###############################################################################################
This macro improves upon FreeCAD's builtin 3mf file exporter in the following ways:

1) Certain user-definable properties added to objects in FreeCAD will be exported into the 3mf file, which will in
turn be used by other programs that load this file. (Most notably Ultimaker Cura, and the infill density)

2) Multiple objects can be exported to the same .3mf file by selecting them and then running this macro, and (unlike FreeCAD's
builtin exporter), they remain seperate objects when imported, with seperate independent properties and values as well.

  (Unless they are in a Part or are in some other way tied to each other, then they import as a single object (the Part), 
  and will NOT have the benefit of having individual properties for the objects inside the Part)

    (Note alsothat you can still go inside the Part, and select the individual objects and export them that way, 
    and then they WILL export as seperate objects)
###############################################################################################
How to use:

This example shows how to set the infill density on an object, which will be recognized when loaded into
Ultimaker Cura

1) In Freecad:
  1) Select an object to be exported for printing.
  2) In the 'Combo View' pane, make sure the 'Data' tab is selected
  3) Rightclick on an existing property, and check 'Show all' in the dropdown that appears.
  4) Rightclick on an existing property again and select 'Add property'
      Note: 'Add property' will not appear if you do not have 'Show all' checked. (see step 3)
  5) In the dialog that pops up:
      a) Make sure the 'Type' field is set to 'App:PropertyString'
      b) In the 'Group' field enter 'Metadata_Cura'
      c) in the 'Name' field enter 'infill_sparse_density'
      d) Uncheck 'Prefix group name' at the bottom of the dialog
      3) click 'OK' to close the dialog.
          Note: You may enter anything in the Documentation field if you so wish.
  6) Scroll to the bottom of the Property window and you should see a new group named 'Metadata_Cura',
     and in that group you should see an entry named 'infill_sparse_density.  Click in the Value field
     to the right of that entry and enter a value from 0 to 100 as the infill value you want this object
     to have.
  
  7) repeat this process for all objects you want to assign an infill to.

  8) Select all the objects you want to export, and run this 3mfExporter macro!

At the present time, this exports to a file named 'export.3mf'
2) In Ultimaker Cura
  simply load the exported file! If you click on an object and then click the 'Per Model Settings' on the lefthand side, you'll see that the Infill Density for this object has been set by the value you entered for it in FreeCad!

Known Issues:

First, this was a super-simple slap-together hack, I'm SURE there are better ways to do it than what I've done in this code, but I just wanted to get SOMEthing working, and FAST!  So, don't rip into me about 'how wrong I did this' or 'how stupid I did that when there's already another way'.  I'll improve it as I go along and get feedback and input from others, but right now I just wanted something that works for what I intend to use it for, without taking 3 days to learn ALL the ins and outs of the FreeCAD API first!

Issue: it doesnt remember your last save-as location or filename.

Issue: it loads objects at the origin in cura instead of near the center of the bed

Issue: I'm sure there are more issues! :)

