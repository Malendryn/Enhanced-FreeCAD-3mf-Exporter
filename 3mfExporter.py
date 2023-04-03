import os

# RSTODO follow this link https://github.com/microsoft/ptvsd#readme to learn more about replacing ptvsd with debugpy
# (*** I tried my damnedest to get debugpy to work but it absolutely refuses, so falling back to ptvsd (at least for now) ***)

# create a file '3mfExporter_debug_enabled' in the same directory as this script, to enable remote debugging
scriptdir = os.path.dirname(__file__)

denabled = os.path.join(scriptdir, "3mfExporter_debug_enabled");
debug = os.path.exists(denabled);    # set to true to enable remote debugging (presently using ptvsd, plan to switch to debugpy soon)

if debug:
   import ptvsd

def enableRemoteDebugger():
    if debug:
      ptvsd.enable_attach();
      # ptvsd.break_into_debugger();

def _break():
    if debug:
      ptvsd.break_into_debugger();

enableRemoteDebugger();       # look for a debugger that's listening on the default port (5678) and if found, attach to it

##################### debugger setup and funcs above this line #######################################################

_break();
configfile = os.path.join(scriptdir, "3mfExporter.cfg");

import configparser
config = configparser.ConfigParser();
if config.read(configfile) == []:     # no configuration?  create the basics:
  config["PrintBed"] = {};
  config["PrintBed"]["Width"] = "200";
  config["PrintBed"]["Depth"] = "200";
  config["LastSession"] = {};
  config["LastSession"]["SaveFile"] = "";
  fp = open(configfile, "w")
  config.write(fp);
  fp.close();


import PySide
from PySide import QtGui ,QtCore
from PySide.QtGui import *
from PySide.QtCore import *


_break();

# import FreeCAD

import zipfile    #from zipfile import ZipFile
from io import BytesIO

sels = Gui.Selection.getSelection();     # gui is autoloaded by FreeCad

if len(sels) == 0:  # RSTODO if sels == 0 open dialog with error and exit
  _break();
  diag = QtGui.QMessageBox(QtGui.QMessageBox.Warning, "Enhanced 3MF Exporter", "No objects selected for exporting.");
  diag.setWindowModality(QtCore.Qt.ApplicationModal);
  diag.exec_();
else:
  def getSaveFile():
    _break();
    # path = FreeCAD.ConfigGet("UserAppData")
    path = config["LastSession"]["SaveFile"];

    try:
        saveFile = QFileDialog.getSaveFileName(None,QString.fromLocal8Bit("Save a file txt"),path,             "*.3mf") # PyQt4
    except Exception:
        saveFile, Filter = PySide.QtGui.QFileDialog.getSaveFileName(None, "Save a file txt", path,             "*.3mf") # PySide
    return saveFile;

  def startZipFile():     # return the zipstream with the basic setup already inserted
  #    _break();
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


  saveFile = getSaveFile();
  if saveFile != '':
    config["LastSession"]["SaveFile"] = saveFile;

    fp = open(configfile, "w");
    config.write(fp);
    fp.close();
    zipstream,zipobj = startZipFile();

    bb = BytesIO()    # place to store our object data to be written into the zipfile at the end

    bb.write(b"""<?xml version="1.0" encoding="UTF-8"?>
<model unit="millimeter" xml:lang="en-US" mlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">
<metadata name="Application">FreeCAD</metadata>
    <resources>
""");

    oid = 1;

    # _break();

    for sel in sels:
      bb.write(bytes('        <object id="%d" name="%s" type="model">\n' % (oid, sel.Label), "utf-8"));
      oid = oid + 1
      bb.write(b"            <metadatagroup>\n");

      props = sel.PropertiesList;
      for propName in props:
          v1 = sel.getGroupOfProperty(propName);
          v2 = sel.getPropertyByName(propName);
          v3 = sel.getTypeOfProperty(propName);
          if v1 != "Metadata_Cura":
              continue;
          _break();
          bb.write(bytes('                <metadata name="cura:%s">%s</metadata>\n' % (propName, v2), "utf-8"));

      _break();
      bb.write(b"""            </metadatagroup>
            <mesh>
                <vertices>
""");    
      
      shape = sel.Shape
      tess = shape.tessellate(0.01);

      offx = int(config["PrintBed"]["Width"]) / 2;
      offy = int(config["PrintBed"]["Depth"]) / 2;
      for vv in tess[0]:
        bb.write(bytes('                    <vertex x="%f" y="%f" z="%f" />\n' % (offx + vv[0], offy + vv[1], vv[2]), "utf-8"));
      bb.write(b"""                </vertices>
                <triangles>
""");
      for tt in tess[1]:
        bb.write(bytes('                    <triangle v1="%d" v2="%d" v3="%d" />\n' % (tt[0], tt[1], tt[2]), "utf-8"));      

      _break();

    # finished writing the vertices and triangles of all the objects
      bb.write(b"""                </triangles>
            </mesh>
        </object>
""");

    #end of selections, write closure lines and then put this all into the zipfile
    bb.write(b"""    </resources>
    <build>
""");

    oid = 1
    for sel in sels:
      bb.write(bytes('        <item objectid="%d" />\n' % (oid), "utf-8"));
      oid = oid + 1;

    bb.write(b"""    </build>
</model>
""");


    ff = zipfile.ZipInfo("3D/3dmodel.model");
    ff.compress_type = zipfile.ZIP_DEFLATED;

    bb.seek(0);
    zipobj.writestr(ff, bb.read());

    zipobj.close();



    ff = open(saveFile, "wb");
    ff.seek(0);
    ff.write(zipstream.getbuffer());
    ff.truncate();
    ff.close();
    zipstream.close();

    # print("done");
