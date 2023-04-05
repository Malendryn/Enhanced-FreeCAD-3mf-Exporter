import os

# create a file '3mfExporter_debug_enabled' in the same directory as this script, to enable remote debugging

scriptdir = os.path.dirname(__file__)

denabled = os.path.join(scriptdir, "3mfExporter_debug_enabled");
debug = os.path.exists(denabled);    # set to true to enable remote debugging (presently using ptvsd, plan to switch to debugpy soon)

if debug:
   import ptvsd

def enableDebugging():
    if debug:
      ptvsd.enable_attach();
      # ptvsd.break_into_debugger();

def _break():
    if debug:
      ptvsd.break_into_debugger();

enableDebugging();       # open a listener and allow a debugger to attach to it.

##################### debugger setup and funcs above this line #######################################################
import PySide
from PySide import QtGui ,QtCore
from PySide.QtGui import *
from PySide.QtCore import *

# import FreeCAD
import zipfile    #from zipfile import ZipFile
from io import BytesIO


############################################################################################################
def getVersion():
    global version;

    if ("experimental" in __file__):
        version = "0.0.0";
    else:
        try:
            fp = open(os.path.join(scriptdir, "3mfExporter.ver"), "r");
            version = fp.readline();
            fp.close();
        except:
            msgDlg("Could not open version file.");
            return False;
    return True;


############################################################################################################
def loadConfig():
    global scriptdir, config;
    import configparser

    config = configparser.ConfigParser();
    configfile = os.path.join(scriptdir, "3mfExporter.cfg");
    if config.read(configfile) == []:     # no configuration?  create the basics:
      config["PrintBed"] = {};
      config["PrintBed"]["Width"] = "200";
      config["PrintBed"]["Depth"] = "200";

      config["LastSession"] = {};
      config["LastSession"]["SaveFile"] = "";

      fp = open(configfile, "w")
      config.write(fp);
      fp.close();
    return True;


############################################################################################################
def getSaveFileName():
    global config;

    path = config["LastSession"]["SaveFile"];

    try:
        saveFileName = QFileDialog.getSaveFileName(None, QString.fromLocal8Bit("Save a file txt"),path, "*.3mf") # PyQt4
    except Exception:
        saveFileName, Filter = PySide.QtGui.QFileDialog.getSaveFileName(None, "Save a file txt", path, "*.3mf") # PySide

    if saveFileName != '' and saveFileName != path:
      config["LastSession"]["SaveFile"] = saveFileName;
      configfile = os.path.join(scriptdir, "3mfExporter.cfg");

      fp = open(configfile, "w");
      config.write(fp);
      fp.close();

    return saveFileName;


############################################################################################################
def startZipFile():     # return the zipstream with the basic setup already inserted
      zipstream = BytesIO();
      zipobj = zipfile.ZipFile(zipstream, 'w');
      ff = zipfile.ZipInfo("[Content_Types].xml");
      ff.compress_type = zipfile.ZIP_DEFLATED;
      zipobj.writestr(ff, b"""<?xml version='1.0' encoding='UTF-8'?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
    <Default ContentType="application/vnd.openxmlformats-package.relationships+xml" Extension="rels" />
    <Default ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml" Extension="model" />
</Types>
""");

      ff = zipfile.ZipInfo("_rels/.rels");
      ff.compress_type = zipfile.ZIP_DEFLATED;
      zipobj.writestr(ff, b"""<?xml version='1.0' encoding='UTF-8'?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
    <Relationship Id="rel0" Target="/3D/3dmodel.model" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel" />
</Relationships>
""");
      return zipstream,zipobj;


############################################################################################################
rsrcDict = {};    # dict of {'obj.Label': [oid, obj, None-or-'childOfObj.Label', [] or ['1stchildLabel','2ndchildLabel',...]]}
                  # [2]=[...] is a list of the parents of this object or [] if this is a toplevel object
                  # [3]=None means this has no children and therefore is a standard mesh object.
                  # [3]=[...] means this is a group object and here are its children
grpStack = [];  # array of ['objLabel','objLabel',...], each time we enter/exit a group, this gets updated, grpStack[-1] = current grpLabel
oid = 1;        # object id, every mesh and group (groups are also objects) get their own id starting at 1 and counting upwards
hasRoot = False;  # do we have any entries on the root?  (must have at least one for a valid output file)

############################################################################################################
def addObjectToResources(obj, isGrp):
    global rsrcDict, grpStack, oid, hasRoot;
#    _break();
    if obj.Label in rsrcDict:     # is it already in the resource list?
      return False;

    data = [oid, obj, [], None];
    oid += 1;

    if isGrp:
       data[3] = [];
    
    if len(grpStack) > 0:         # if we have parents...
      data[2] = grpStack.copy();    # set the list of parents of this object
      pd = rsrcDict[grpStack[-1]];  # get the parent's data
      pd[3].append(obj.Label);      # add this child to parent's data[3]
    else:
      hasRoot = True;
    
    rsrcDict[obj.Label] = data;
    return True;


############################################################################################################
def processObjectList(objs):
    global rsrcDict, grpStack, oid;
    
    for idx in range(0, len(objs)):
        obj = objs[idx];
#        _break();
        if not hasattr(obj, "Shape"):   # no shape? no export!
           continue;

        if str(type(obj)) == "<class 'App.Part'>":  # this is a part, so it might have children
          if not addObjectToResources(obj, True):
            continue;
          grpStack.append(obj.Label);       # grow the parent stack
          processObjectList(obj.OutList);   # walk this part and add its children to the resources!
          del grpStack[-1];                 # and shrink the parent stack again!
        else:                                       # this is a mesh
          addObjectToResources(obj, False);
             


############################################################################################################
def msgDlg(msg):
    diag = QtGui.QMessageBox(QtGui.QMessageBox.Warning, "Enhanced 3MF Exporter v" + version, msg);
    diag.setWindowModality(QtCore.Qt.ApplicationModal);
    diag.exec_();


############################################################################################################

def writeObject(ioObj, ioBld, data):
    oid,obj,parents,children = data;

    ioObj.write(bytes('        <object id="%d" name="%s" type="model">\n' % (oid, obj.Label), "utf-8"));

    if parents == []:       # this is a toplevel object and therefore gets put into the Build section
      ioBld.write(bytes('        <item objectid="%d" />\n' % (oid), "utf-8"));

# now gather and write the metadata (properties)
    metaheader = False;

#    _break();
    propNames = [];                         # prevents parent objects from overwriting children properties
    for label in [obj.Label] + parents:     # walk chain of parents starting with self
      tmp = rsrcDict[label][1];
      for propName in tmp.PropertiesList:
        v1 = tmp.getGroupOfProperty(propName);  # we only care when this is "Metadata_Cura"
        v2 = tmp.getPropertyByName(propName);   # the value of the property
        v3 = tmp.getTypeOfProperty(propName);   # this should always be App::PropertyString but we don't really care
        if v1 != "Metadata_Cura":
            continue;

#        _break();
        if propName in propNames:       # prevent parents from clobbering
           continue;
        propNames.append(propName);

        if metaheader == False:     # if we haven't yet written the wrapper around the metadata entries
          metaheader = True;
          ioObj.write(b"            <metadatagroup>\n");
        
        ioObj.write(bytes('                <metadata name="cura:%s">%s</metadata>\n' % (propName, v2), "utf-8"));
#      _break();
#    _break();

    if metaheader == True:          # if any properties actually got written, close the wrapper
      ioObj.write(b"            </metadatagroup>\n");

# metadata stuff is done, move on to object data!
    if children == None:            # if it's a mesh object, write the mesh data here
      ioObj.write(b"""            <mesh>
                <vertices>
""");    

      shape = obj.Shape;
      tess = shape.tessellate(0.01);

      offx = int(config["PrintBed"]["Width"]) / 2;
      offy = int(config["PrintBed"]["Depth"]) / 2;
      for parent in parents:      # walk the parents and add their offsets
        _break();
        tmp = rsrcDict[parent];
        off = tmp[1].Placement.Base;
        offx += off[0];
        offy += off[1];

      for vv in tess[0]:                              # write all the tesselated vertex info PLUS my acumulated offsets
        ioObj.write(bytes('                    <vertex x="%f" y="%f" z="%f" />\n' % (offx + vv[0], offy + vv[1], vv[2]), "utf-8"));

      ioObj.write(b"""                </vertices>
                <triangles>
""");
      for tt in tess[1]:                              # write all the tesselated triangle info
        ioObj.write(bytes('                    <triangle v1="%d" v2="%d" v3="%d" />\n' % (tt[0], tt[1], tt[2]), "utf-8"));      

# finished writing the vertices and triangles of all the objects, close the wrappers!
      ioObj.write(b"""                </triangles>
            </mesh>
""");
    else:                           # it's a group object, write all the group info here
      ioObj.write(b"            <components>\n");
      for child in data[3]:
        cdata = rsrcDict[child];
        ioObj.write(bytes('                <component objectid="%s" />\n' % (cdata[0]), "utf-8"));

        _break();

      ioObj.write(b"            </components>\n");

    ioObj.write(b"        </object>\n");  # finally, close the object and move on


############################################################################################################
def export():
    global config, rsrcDict, version;

    if not loadConfig():
       return;

    sels = Gui.Selection.getSelection();     # Gui is autoloaded by FreeCad

    if len(sels) == 0:
      msgDlg("No objects selected for exporting.");
      return;

    processObjectList(sels);    # gather all the selected objects and their children into rsrcDict

    if hasRoot == False:
      msgDlg("No selections were valid for export, aborted.");
      return;

# all information is gathered and ready for export, lets get a filename and get busy!
    saveFileName = getSaveFileName();
    if saveFileName == '':
      return;

    zipstream,zipobj = startZipFile();

    iostr = BytesIO();    # primary output string which writes straight to the zipfile
    ioObj = BytesIO();    # place to store our object data(resources) to be written into the zipfile
    ioBld = BytesIO();    # place to store the build info portion of the zipfile

    iostr.write(bytes("""<?xml version="1.0" encoding="UTF-8"?>
<model unit="millimeter" xml:lang="en-US" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">
    <metadata name="Application">FreeCAD</metadata>
    <metadata name="3mfExporter">Created using the DragonsFire 3mfExporter macro version %s</metadata>
    <resources>
""" % (version), "utf-8"));
    ioBld.write(b"    <build>\n");

    for label,data in rsrcDict.items():
      writeObject(ioObj, ioBld, data);

    _break();
    ioObj.write(b"    </resources>\n");       #end of selections, write closure lines and then put this all into the zipfile
    ioBld.write(b"""    </build>
</model>
""");

    ff = zipfile.ZipInfo("3D/3dmodel.model");
    ff.compress_type = zipfile.ZIP_DEFLATED;

    iostr.seek(0);
    ioObj.seek(0);
    ioBld.seek(0);
    zipobj.writestr(ff, iostr.read() + ioObj.read() + ioBld.read());
    zipobj.close();
    ioBld.close();
    ioObj.close();
    iostr.close();

    try:
      ff = open(saveFileName, "wb");
      ff.seek(0);
      ff.write(zipstream.getbuffer());
      ff.truncate();
      ff.close();
      zipstream.close();
    except:
      msgDlg("An error occurred trying to save the export file.");
       

############################### execution starts here #####################################
def begin():
    if not getVersion():
       return;
    export();


############################################################################################################
#_break();
begin();