## Cura List of Properties

Current list of properties that Cura recognizes (as of Cura version 5.2.1).  
Setting these properties on objects in FreeCAD will override the global slicing settings in Cura.

When creating a property on an object, the following applies in the '**Add property**' dialog box.  
The **`Type`** field must be set to `App:PropertyString`  
The **`Group`** field must be set to `Metadata_Cura`  
**Important**: uncheck the `Prefix group name` check box.

The 'Name' field can be any of the following:
__________________________________________________________
Settings under the Cura category of 'Quality' are:
-----------------------------------------
Property Name          | Cura Dialog
in FreeCAD             | Description and Tooltip
-----------------------|-----------------
line_width             | Line Width
    Width of a single line. Generally, the width of each line should correspond to the width of the nozzle. However, slightly reducing this value could produce better prints.

wall_line_width        | Wall Line Width
    Width of a single wall line.

wall_line_width_0      | Outer Wall Line Width
    Width of the outermost wall line. By lowering this value, higher levels of detail can be printed.

skin_line_width        | Inner Wall(s) Line Width
    Width of a single wall line for all wall lines except the outermost one.

wall_line_width_x      | Top/Bottom Line Width
    Width of a single top/bottom line.

infill_line_width      | Infill Line Width
    Width of a single infill line.

__________________________________________________________
Settings under the Cura category of 'Walls' are:
Property Name                   | Cura Dialog
in FreeCAD                      | Text Name
--------------------------------|-----------------
 wall_thickness                 | Wall Thickness
    The thickness of the walls in the horizontal direction. This value divided by the wall line width defines the number of walls.

 wall_line_count                | Wall Line Count
    The number of walls. When calculated by the wall thickness, this value is rounded to a whole number.

optimize_wall_printing_order    | Optimize Wall Printing Order
    Optimize the order in which walls aer printed so as to reduce the number of retractions and the distance travelled. Most parts will benefit from this being abled but some may actually take longer so please compaer the print time estimates with and without optimization.  First layer is not optimized when choosing brim as build plate adhesion type.

xy_offset                       | Horizontal Expansion
    Amount of offset applied to all polygons in each layer. Positive values can compensate for too big holes; negative values can compensate for too small holes.

__________________________________________________________
Settings under the Cura category of 'Top/Bottom' are:
Property Name          | Cura Dialog
in FreeCAD             | Text Name
-----------------------|-----------------
top_bottom_thickness   | Top/Bottom Thickness
    The thickness of the top/bottom layers in the print. This value divided by the layer height defines the number of top/bottom layers.

top_thickness          | Top Thickness
    The thickness of the top layers in the print. This value divided by the layer height defines the number of top layers.

top_layers             | Top Layers
    The number of top layers, When calculated by the top thickness, this value is rounded to a whole number.

bottom_thickness       | Bottom Thickness
    The thickness of the bottom layers in the print.  This value divided by the layer height defines the number of bottom layers.

bottom_layers          | Bottom Layers
    The number of bottom layers. When calculated by the bottom thickness, this value is rounded to a whole number.

skin_monotonic         | Monotonic Top/Bottom Order
    Print top/bottom lines in an ordering that causes them to always overlap with adjacent lines in a single direction. This takes slightly more time to print, but makes flat surfaces look more consistent.

ironing_enabled        | Enable Ironing
    Go over the top surface one additional time, but this time extruding very little material. This is meant to melt the plastic on top further, creating a smoother surface. The pressure in the nozzle chamber is kept high so that the creases in the surface are filled with material.

__________________________________________________________
Settings under the Cura category of 'Infill' are:
Property Name           | Cura Dialog
in FreeCAD              | Text Name
------------------------|-----------------
infill_sparse_density   | Infill Density
    Adjusts the density of infill of the print.

infill_line_distance    | Infill Line Distance
    Distance between the printed infill lines. This setting is calculated by the infill density and the infill line width.

infill_pattern          | Infill Pattern
    The pattern of the infill material of the print.

infill_multiplier       | Infill Line Multiplier
    Convert each infill line to this many lines.  The extra lines do not cross over each other, but avoid each other.   This makes the infill stiffer, but increases print time and material usage.

infill_overlap          | Infill Overlap Percentage
    The amount of overlap between the infill and the walls as a percentage of the infill line width.  A slight overlap allows the walls to connect firmly to the infill.

infill_sparse_thickness | Infill Layer Thickness
    The thickness per layer of infill material.  This value should always be a multiple of the layer height and is otherwise rounded.

gradual_infill_steps    | Gradual Infill Steps
    Number of times to reduce the infill density by half when getting further below top surfaces. Areas which are closer to top surfaces get a higher density, up to the Infill Density.

__________________________________________________________
Settings under the Cura category of 'Speed' are:
Property Name          | Cura Dialog
in FreeCAD             | Text Name
-----------------------|-----------------
speed_print     | Print Speed
    The speed at which printing happens.

speed_infill    | Infill Speed
    The speed at which infill is printed.

speed_wall      | Wall Speed
    The speed at which the walls are printed.

speed_wall_0    | Outer Wall Speed
    The speed at which the outermost walls are printed.  Printing the outer wall at a lower speed improves the final skin quality.  However, having a large difference between the inner wall speed and the outer wall speed will affect quality in a negative way.

speed_wall_x    | Inner Wall Speed
    The speed at which all inner walls are printed.  Printing the inner wall faster than the outer wall will reduce printing time.  It works well to set this in between the outer wall speed and the infill speed.
    
speed_topbottom | Top/Bottom Speed
    The speed at which top/bottom layers are printed.

speed_layer_0   | Initial Layer Speed
    The speed for the initial layer. A lower value is advised to improve adhesion to the build plate. Does not affect the build plate adhesion structures themselves, like brim and raft.

				<metadata name="cura:">25.0</metadata>
				<metadata name="cura:">25.0</metadata>

__________________________________________________________
Settings under the Cura category of 'Support' are:
Property Name            | Cura Dialog
in FreeCAD               | Text Name
-------------------------|-----------------
support_enable           | Generate Support
    Generate structures to support parts of the model which have overhangs.  Without these structures, such parts would collapse during printing.

support_angle            | Support Overhang Angle
    The minimum angle of overhangs for which support is added. At a value of 0 degrees all overhangs are supported.  90 degrees will not provide any support.

support_interface_enable | Enable Support Interface
    Generate a dense interface between the model and the support. This will create a skin at the top of the support on which the model is printed and at the bottom of the support, where it rests on the model.

support_roof_enable      | Enable Support Roof
    Generate a dense slab of material between the top of support and the model.  This will create a skin between the model and support.

support_bottom_enable    | Enable Support Floor
    Generate a dense slab of material between the bottom of the support and the model.  This will create a skin between the model and the support.

__________________________________________________________
Settings under the Cura category of 'Special Modes' are:
Property Name           | Cura Dialog
in FreeCAD              | Text Name
------------------------|-----------------
magic_mesh_surface_mode | Surface Mode
    Treat the model as a surface only, a volume, or volumes with loose surfaces.  The normal print mode only prints enclosed volumes.  "Surface" prints a single wall tracing the mesh surface with no infill and no top/bottom skin.  "Both" prints enclosed volumes like normal and any remaining polygons as surfaces.

__________________________________________________________
Settings under the Cura category of 'Experimental' are:
Property Name               | Cura Dialog
in FreeCAD                  | Text Name
----------------------------|-----------------
conical_overhang_enabled    | Make Overhang Printable
    Change the geometry of the printed model such that minimal support is required.  Steep overhangs will become shallow overhangs.  Overhanging areas will drop down to become more vertical.

support_conical_enabled     | Enable Conical Support
    Make support areas smaller at the bottom than at the overhang.
