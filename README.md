## Enhanced 3mf File Exporter for FreeCAD

This FreeCAD macro improves upon FreeCAD's built-in 3mf file exporter in the following ways:

* By adding specially named properties to your models in FreeCAD, and then exporting those models using this script (instead of the built-in .stl or .3mf exporter), you can add more control to your models in the slicer you import them to.  (At the present time, only Ultimaker Cura is supported.) such as per-model infill density and type, wall thickness, supports, etc...  This allows you to store these settings on a per-model basis in FreeCAD, right where the model is being designed, where it makes the most sense for these settings to be stored.

* Multiple models can be exported to the same .3mf file by selecting them and then running this macro, and (unlike FreeCAD's built-in exporter), they remain seperate objects when imported, with seperate independent settings as well.

### Installation Procedure
#### Manual Installation
Download this macro into your FreeCAD macro directory, and execute it from your macros dialog.

#### Automatic Installation
Unsupported at this time.

### Usage
#### <b>First time execution</b>
##### The first time this script is run, it will create a config file named '3mfExporter.cfg' in the FreeCAD Macro Directory.  This file will contain defaults for a print bed set to 200mm wide by 200mm deep. These values are used by this script to center your models on the printbed when the .3mf file is loaded by Cura. On first execution, this file will be created immediately, so you can hit cancel on the 'save as' dialog at this time and edit this file to make the printbed size closer to your printer's dimensions.

<details>
<summary><b><h3>How to set the properties on your FreeCAD models</h3></b></summary>

The properties that you can set, that Cura will recognize (as of Cura 5.2.1) are located in the [README_Properties.md](README_Properties.md) file.

Here is a video showing how to set these properties on your FreeCAD models, and how they affect Cura when they are loaded.

[![Macro-Explained-Pt1](https://img.youtube.com/vi/YgbacugzE6c/0.jpg)](https://www.youtube.com/watch?v=YgbacugzE6c)

While all the variables Cura currently recognizes (as of 5.2.1) are in the readme, more will likely be added over time.  you can read the [README_HowToFindTheVariables.md](README_HowToFindTheVariables.md) document to learn how to find the names of those new variables when they become available, and use them in your FreeCAD Models.

The following description complements the video above and gives a textual description of how to set the infill density on a model.

### Step 1: In Freecad
1. Select a model to be exported for printing.
2. In the [Combo View](https://wiki.freecad.org/Combo_view) pane, make sure the <b>Data</b> tab is selected
3. Right-click on any existing property, and check `Show all` in the dropdown that appears.
4. Right-click on any existing property again and select `Add property`
    <br>  Note: `Add property` will not appear if you do not have 'Show all' checked. (see step 3)

5. In the dialog that pops up:  
    a. Make sure the **`Type`** field is set to `App:PropertyString`  
    b. In the **`Group`** field enter `Metadata_Cura`  
    c. in the **`Name`** field enter `infill_sparse_density`  
    d. Uncheck **`Prefix group name`** at the bottom of the dialog  
    e. click **`OK`** to close the dialog.  
    You can enter anything in the `Documentation` field if you so wish.
6. Now if you scroll to the bottom of the Property window, you should see a new group named `Metadata_Cura`, and in that group you should see an entry named `infill_sparse_density`.  Click in the **`Value`** field to the right of that entry and enter a value from 0 to 100 as the infill value you want this model to have.

7. repeat this process for all models you want to assign an infill to.

8. Finally, select all the models you want to export, and run this macro.

### Step 2: In Ultimaker Cura
  Simply load the exported file! If you click on a model and then click the `Per Model Settings` in the toolbar on the lefthand side, you'll see that the Infill Density for this model has been set by the value you entered for it in FreeCad.
</details>
<details>
<summary><b><h3>Major improvements since initial release!</h3></b></summary>

The first release (now renamed to [3mfExporter_old(v0.1.1).py](Prior_working_version/3mfExporter_old(v0.1.1).py) was only able to accurately import toplevel objects. Any objects that resided inside a group were effectively removed from the group and placed at the toplevel as well, and their relative positioning was lost in the process.

This new release now supports the Part object as well, and retains the relative positioning of the children as well as any Parts-Inside-Of-Parts.  <i>However, it only handles Part Position, and does not YET handle Part Rotation (Angle and Axis), so be mindful of this when exporting parts.</i>

The cumulative nature of Parts with children also applies to the properties as follows:
* Properties on children of Parts get stored just like toplevel objects.
* Properties on the Part object itself (and all parent Part objects as well), get added to this object as if they were a property on that object.
* Properties that already exist on a child, will <i>NOT</i> get overwritten by a parent Part's property.

This allows you to have a number of objects that have specific settings, and have them all placed under a Part object which has even more properties that will apply to all its children.

Note that once this export has been imported to Cura, selecting the grouped part won't show the properties. To see the properties, you can <b>Ctrl+Left-Click</b> single object inside the group, and then you can see its Per Model Settings. (You can also move the single object around in this manner while still keeping the objects together in a group.)

<i>You can also Right-Click the entire group and select <b>Ungroup Models</b> (or press <b>Ctrl+Shift+G</b>) but this is unwise as it removes the integrity of the model group, especially if you have 'Drop Down Model' enabled.</i>

There is now an included .FCStd file under the 'testfiles' folder named [Gooseneck_Section_Example.FCStd](testfiles/Gooseneck_Section_Example.FCStd) that demonstrates this new functionality.
</details>

## Known Issues

Grouped objects (aka Part objects) still do not support the Angle property under Placement, only Position is presently supported.

## Feedback and Bug reports

I've now moved all the issues up to github's issue tracker, so will start to work on them from there.

## Developer

Ron Stanions ([@Malendryn](https://github.com/Malendryn))  -- DragonsFire Development  
Initial Creation Date: 03/31/2023

## License

GPLv3 ([LICENSE](LICENSE))