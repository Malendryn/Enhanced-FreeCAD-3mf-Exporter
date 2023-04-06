
Current list of properties that Cura recognizes (As of Cura version 5.2.1).  Setting these properties on objects in FreeCAD will override the global slicing settings in Cura.

When creating a property on an object, the following applies in the **Add property** window
* The **`Type`** field must be set to `App:PropertyString
* The **`Group`** field must be set to `Metadata_Cura*`
* Uncheck the **`Prefix group name`** box.
 

The **`Name`** field can be any of the following:

(NOTE: Most if not all of the following information can be gleaned from the [fdmprinter.def.json](https://github.com/Ultimaker/Cura/blob/main/resources/definitions/fdmprinter.def.json) file over in the Cura source tree.)

<b>Settings under the Cura category of **`"Quality"`** are:</b>

| Property Name<br> in FreeCAD | Cura Dialog<br>Description and Tooltip |
|------------------------------|----------------------------------------|
|line_width             | `"Line Width"`              <br> Width of a single line. Generally, the width of each line should correspond to the width of the nozzle. However, slightly reducing this value could produce better prints.|
| wall_line_width       |`"Wall Line Width"`          <br> Width of a single wall line.|
| wall_line_width_0     | `"Outer Wall Line Width"`   <br> Width of the outermost wall line. By lowering this value, higher levels of detail can be printed.|
| skin_line_width       | `"Inner Wall(s) Line Width"`<br> Width of a single wall line for all wall lines except the outermost one.|
| wall_line_width_x     | `"Top/Bottom Line Width"`   <br> Width of a single top/bottom line.
| infill_line_width     | `"Infill Line Width"`       <br> Width of a single infill line. |

<br><b>Settings under the Cura category of **`"Walls"`** are:</b>
| Property Name<br> in FreeCAD | Cura Dialog<br>Description and Tooltip |
|------------------------------|----------------------------------------|
| wall_thickness               | `"Wall Thickness"`<br>The thickness of the walls in the horizontal direction. This value divided by the wall line width defines the number of walls. |
| wall_line_count              | `"Wall Line Count"`<br>The number of walls. When calculated by the wall thickness, this value is rounded to a whole number. |
| optimize_wall_printing_order | `"Optimize Wall Printing Order"`<br>Optimize the order in which walls aer printed so as to reduce the number of retractions and the distance travelled. Most parts will benefit from this being abled but some may actually take longer so please compaer the print time estimates with and without optimization.  First layer is not optimized when choosing brim as build plate adhesion type. |
| xy_offset                    | `"Horizontal Expansion"`<br>Amount of offset applied to all polygons in each layer. Positive values can compensate for too big holes; negative values can compensate for too small holes. \

<br><b>Settings under the Cura category of **`"Top/Bottom"`** are:</b>
| Property Name<br> in FreeCAD | Cura Dialog<br>Description and Tooltip |
|------------------------------|----------------------------------------|
| top_bottom_thickness   | `"Top/Bottom Thickness"`<br>The thickness of the top/bottom layers in the print. This value divided by the layer height defines the number of top/bottom layers. |
| top_thickness          | `"Top Thickness"`<br>The thickness of the top layers in the print. This value divided by the layer height defines the number of top layers. |
| top_layers             | `"Top Layers`"<br>The number of top layers, When calculated by the top thickness, this value is rounded to a whole number. |
| bottom_thickness       | Bottom Thickness<br>The thickness of the bottom layers in the print.  This value divided by the layer height defines the number of bottom layers. |
| bottom_layers          | `"Bottom Layers"`<br>The number of bottom layers. When calculated by the bottom thickness, this value is rounded to a whole number. |
| skin_monotonic         | `"Monotonic Top/Bottom Order"`<br>Print top/bottom lines in an ordering that causes them to always overlap with adjacent lines in a single direction. This takes slightly more time to print, but makes flat surfaces look more consistent. |
| ironing_enabled        | `"Enable Ironing"`<br>Go over the top surface one additional time, but this time extruding very little material. This is meant to melt the plastic on top further, creating a smoother surface. The pressure in the nozzle chamber is kept high so that the creases in the surface are filled with material. |

<br><b>Settings under the Cura category of **`"Infill"`** are:</b>
| Property Name<br> in FreeCAD | Cura Dialog<br>Description and Tooltip |
|------------------------------|----------------------------------------|
| infill_sparse_density   | **`"Infill Density"`**<br>Adjusts the density of infill of the print. |
| infill_line_distance    | **`"Infill Line Distance"`**<br>Distance between the printed infill lines. This setting is calculated by the infill density and the infill line width. |
| infill_pattern          | **`"Infill Pattern"`**<br>The pattern of the infill material of the print. The current known values for this field are:<br><b>grid, triangles, trihexagon, cubic, cubicsubdiv, tetrahedral, quarter_cubic, cross, cross_3d, lightning</b> |
| infill_multiplier       | **`"Infill Line Multiplier"`**<br>Convert each infill line to this many lines.  The extra lines do not cross over each other, but avoid each other.   This makes the infill stiffer, but increases print time and material usage. |
| infill_overlap          | **`"Infill Overlap Percentage"`**<br>The amount of overlap between the infill and the walls as a percentage of the infill line width.  A slight overlap allows the walls to connect firmly to the infill. |
| infill_sparse_thickness | **`"Infill Layer Thickness"`**<br>The thickness per layer of infill material.  This value should always be a multiple of the layer height and is otherwise rounded. |
| gradual_infill_steps    | **`"Gradual Infill Steps"`**<br>Number of times to reduce the infill density by half when getting further below top surfaces. Areas which are closer to top surfaces get a higher density, up to the Infill Density. |

<br><b>Settings under the Cura category of **`"Speed"`** are:</b>
| Property Name<br> in FreeCAD | Cura Dialog<br>Description and Tooltip |
|------------------------------|----------------------------------------|
| speed_print     | **`"Print Speed"`**<br>The speed at which printing happens. |
| speed_infill    | **`"Infill Speed"`**<br>The speed at which infill is printed. |
| speed_wall      | **`"Wall Speed"`**<br>The speed at which the walls are printed. |
| speed_wall_0    | **`"Outer Wall Speed"`**<br>The speed at which the outermost walls are printed.  Printing the outer wall at a lower speed improves the final skin quality.  However, having a large difference between the inner wall speed and the outer wall speed will affect quality in a negative way. |
| speed_wall_x    | **`"Inner Wall Speed"`**<br>The speed at which all inner walls are printed.  Printing the inner wall faster than the outer wall will reduce printing time.  It works well to set this in between the outer wall speed and the infill speed. |
| speed_topbottom | **`"Top/Bottom Speed"`**<br>The speed at which top/bottom layers are printed. |
| speed_layer_0   | **`"Initial Layer Speed"`**<br>The speed for the initial layer. A lower value is advised to improve adhesion to the build plate. Does not affect the build plate adhesion structures themselves, like brim and raft. |

<br><b>Settings under the Cura category of **`"Support"`** are:</b>
| Property Name<br> in FreeCAD | Cura Dialog<br>Description and Tooltip |
|------------------------------|----------------------------------------|
| support_enable           | **`"Generate Support"`**<br>Generate structures to support parts of the model which have overhangs.  Without these structures, such parts would collapse during printing. |
| support_angle            | **`"Support Overhang Angle"`**<br>The minimum angle of overhangs for which support is added. At a value of 0 degrees all overhangs are supported.  90 degrees will not provide any support. |
| support_interface_enable | **`"Enable Support Interface"`**<br>Generate a dense interface between the model and the support. This will create a skin at the top of the support on which the model is printed and at the bottom of the support, where it rests on the model. |
| support_roof_enable      | **`"Enable Support Roof"`**<br>Generate a dense slab of material between the top of support and the model.  This will create a skin between the model and support. |
| support_bottom_enable    | **`"Enable Support Floor"`**<br>Generate a dense slab of material between the bottom of the support and the model.  This will create a skin between the model and the support. |

<br><b>Settings under the Cura category of **`"Special Modes"`** are:</b>
| Property Name<br> in FreeCAD | Cura Dialog<br>Description and Tooltip |
|------------------------------|----------------------------------------|
| magic_mesh_surface_mode | **`"Surface Mode"`**<br>Treat the model as a surface only, a volume, or volumes with loose surfaces.  The normal print mode only prints enclosed volumes.  "Surface" prints a single wall tracing the mesh surface with no infill and no top/bottom skin.  "Both" prints enclosed volumes like normal and any remaining polygons as surfaces. |

<br><b>Settings under the Cura category of **`"Experimental"`** are:</b>
| Property Name<br> in FreeCAD | Cura Dialog<br>Description and Tooltip |
|------------------------------|----------------------------------------|
| conical_overhang_enabled    | **`"Make Overhang Printable"`**<br>Change the geometry of the printed model such that minimal support is required.  Steep overhangs will become shallow overhangs.  Overhanging areas will drop down to become more vertical. |
| support_conical_enabled     | **`"Enable Conical Support"`**<br>Make support areas smaller at the bottom than at the overhang. |
