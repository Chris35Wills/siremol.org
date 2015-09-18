
# Script to convert all of the markdown files to HTML,
# using the template and CSS in the pandoc directory

import os
import shutil
import sys
import shutil
import copy

basedir = os.path.abspath( "%s/../" % os.path.dirname( sys.argv[0] ) )

topdir = os.path.abspath(sys.argv[1])

pandoc_data = "%s/pandoc" % basedir

def findTitle(filename):
    FILE = open(filename, "r")

    line = FILE.readline()

    while line:
        line = line.lstrip().rstrip()
        if line.find("#") == 0:
            title = line.replace("#","")
            return title.lstrip().rstrip()

        line = FILE.readline()

    return "unknown"

def convertDir(dir):
    relpath = os.path.relpath(basedir, dir)

    for file in os.listdir(dir):
        fullfile = os.path.abspath("%s/%s" % (dir,file))

        if os.path.islink(fullfile):
            continue

        if os.path.isdir(fullfile):
            convertDir(fullfile)
            continue

        if fullfile.endswith(".md"):
            relfile = "%s.html" % os.path.relpath(fullfile, basedir)[0:-3]
            #print("Converting %s | %s | %s" % (fullfile, relpath, relfile))
            print("Creating %s..." % relfile)

            # first, find the title of this page. This is the first header
            title = findTitle(fullfile)

            # pandoc options
            options = [ "-V \"urlpath=%s\"" % relfile,
                        "-V \"rootdir=%s\"" % relpath,
                        "-V \"title=%s\"" % title,
                        "--from=markdown_github",
                        "--to=html5",
                        "--smart",
                        "--template=%s/html5.template.html" % pandoc_data,
                        fullfile,
                        "-o %s.tmp" % fullfile ]

            # run pandoc to convert the file
            cmd = "pandoc %s" % (" ".join(options))
            #print(cmd)
            os.system(cmd)

            # now convert links to markdown files to links to the html documents
            FILE = open("%s.tmp" % fullfile, "r")
            WFILE = open("%s.html" % fullfile[0:-3], "w")

            line = FILE.readline()

            while line:
                while line.find(".md") != -1:
                    line = line.replace(".md", ".html")

                while line.find("<br />") != -1:
                    line = line.replace("<br />"," ")

                WFILE.write(line)
                line = FILE.readline()

            FILE.close()
            WFILE.close()

            os.unlink("%s.tmp" % fullfile)

    if os.path.exists("%s/README.html" % dir):
        shutil.copy("%s/README.html" % dir, "%s/index.html" % dir)

convertDir(topdir)