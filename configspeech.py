#!/usr/bin/python 
"""
SYNOPSIS

    ./configspeech.py [-h,--help] [-v,--verbose] [--version]

DESCRIPTION

    Script to automatically install and configure a system for speech
    recognition.

    Extracts files from supplied URLs to predefined locations.

EXAMPLES

    TODO: Show some examples of how to use this script.

EXIT STATUS

    TODO: List exit codes

AUTHOR

    TODO: Name <name@example.org>

LICENSE

    This script is in the public domain, free from copyrights or restrictions.

VERSION

    $Id$
"""

import sys, os, traceback, optparse
import logging
import time
import re
from urllib2 import urlopen, URLError, HTTPError
from zipfile import ZipFile
from StringIO import StringIO
import shutil
#from pexpect import run, spawn

logger = logging.getLogger('configspeech')
logger.setLevel(logging.DEBUG)

# create stream handler and add to application logger
sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
logger.addHandler(sh)

class FileMap():
    """ keeps a mapping between the file directories input and output """

    def __init__(self, component=None, source=None, local=None,
                 destination=None, extensions=[], isoptional=True):
        self.softwareComponent = component
        self.fileSource = source
        self.sourceDirectory = local
        self.destinationDirectory = destination
        self.fileExts = extensions
        self.isOptDir = isoptional

class FileManager():
    """ taskd with managing the files required """

    def __init__(self, urlconf="file_urls.conf", workdir="", zipdir="", 
                 nldir="c:/Temp/Natlink", windir="c:/Temp/"):
                 # nldir="c:/Natlink", windir="c:/"):
        """ initialise reference directories and logger. """

        # test target directories
        nl_root = nldir
        win_root = windir
        self.wd = workdir

        if not self.wd: 
            logger.debug(
                  "no working directory provided, using current directory: %s" % 
                  os.getcwd())
            self.wd = os.getcwd()

        # create file handler and add to application logger
        logfile = os.path.join(self.wd, 
            os.path.splitext(os.path.basename(__file__))[0] + '.log')
        fh = logging.FileHandler(logfile, mode='w')
        fh.setLevel(logging.DEBUG)
        logger.addHandler(fh)

        # file sources
        self.urlFile =  urlconf
        self.zipDir =  zipdir
        self.sourceList = []
        
        # TODO: .dll for dragonfly? do not overwrite macro system or unimacro directories.
        # Windows testing of distribute files needed. problem with git_auto_push again

        # folders in which to extract the zip files, component names are
        # mapped to destination local file system folder paths.
        self.components = [
            ("Natlink-py-scripts", os.path.join(nl_root, "Natlink/Macrosystem"),
             ['.py', '.txt', '.ini'], True),
            ("Unimacro", os.path.join(nl_root, "Unimacro"),
             ['.py', '.txt', '.ini'], True),
            ("Vocola", os.path.join(nl_root, "Vocola"),
             ['.py', '.txt', '.ini'], False),
            ("windows-batch-scripts", os.path.join(win_root, "win scripts"),
             [], False),
            ("new_dns_cust", "",
             [], False),
            ("Pythonfor", "",
             [], False),
            ("windows_apps", "",
             [], False),
            ("new_sw_gen", "",
             [], False),
            ("new_lin_sw", "",
             [], False)
        ]

        self.fileDict = {}
        for c in self.components:
            name = c[0]
            self.fileDict[name] = FileMap(component=name,\
                local=os.path.join(os.getcwd(), name),\
                destination=c[1], fileExts=c[2],\
                isOptDir=c[3])
            print self.fileDict[name]

        # initialise file dictionary which maps component names to file lists
        # self.fileDict = {}.fromkeys(self.destMap.keys())
        
        # initialise temporary directories
        self.set_targets()

        yn = raw_input("update temporary directories? [Y/n]")
        if str(yn) != "n":
            self.get_zip_data()

        yn = raw_input("update local directories? [Y/n]")
        if str(yn) != "n":
            self.distribute_files()

    def set_targets(self, source=""):
        """ retrieve a list of the names of files required in installation """

        # save current directory to be restored later
        original_dir = os.getcwd()

        # change to the working directory
        logger.debug("changing directory to %s"% self.wd)
        os.chdir(self.wd)

        # number of file sources found
        count = 0

        if source != "zip":
            # read target URLs from config file, populate self.fileDict
            count = self.readfile(self.urlFile, self.sourceList)
            logger.debug("%d URLs read from %s"% (count, self.urlFile))

        if not count:
            # try to find existing zip files either because of explicit 
            # instruction with "source" or if urls cannot be read from file
            try:
              self.sourceList = os.listdir(self.zipDir)
              count = len(self.sourceList)
              logger.debug("%d zip files found in %s"% (count,
                                                         self.zipDir))
              # found zip files in zipDir
              source = "zip"
            except:
              logger.debug("problem with accessing ZIP file directory")
        else:
            # successfully read URLs from config file
            source = "url"


        # did we manage to find any file sources?
        if not count:
            logger.debug("no sources found, aborting")
            mdonessreturn
    
        # archives or resources have been collected, initialise 
        # the parent directory for file extractionafter prompting
        # Note: parent directories may persist, subfolders are removed
        # and replaced later as needed.
        if not os.path.isdir("from_%s"% source):
              os.makedirs("from_%s"% source)
            
        os.chdir("from_%s"% source)
            
        for k in self.fileDict.keys():
            # to map file source to requirement in fileDict we need to 
            # find matching string in the source list.
            fileSource = filter(lambda x:str(k).lower() \
                                in x.lower(), self.sourceList)
            if len(fileSource) > 1:
                logger.debug("duplicate sources for component %s... skipping." 
                              % k)
            elif len(fileSource) == 0:
                # target folde has no matching file source target
                logger.debug("skipping component: %s, no matching filesource "
                              % k)
            else:
                logger.debug("component: %s, source: %s" % (k, fileSource))
                # save the mapping to the dictionary
                fileSource = fileSource[0]
                self.fileDict[k].source=fileSource

        # return to previous directory
        os.chdir(original_dir)

    def fetch_zips_from_urls(self):
        """ fetch zips from URLs for respective folders. Meta data stored
        and sourced from self.fileDict. perform after set_targets """

        # location. Because we are downloading zips, extract to local_zips dir.
        zipDir = os.path.join(self.wd, "local_zips")
        if not os.path.isdir(zipDir):
            os.makedirs(zipDir)
        os.chdir(zipDir)

        for file_map in self.fileDict.values():
            # zippedData = None

            if file_map == None: continue

            # initialise target extraction sub-folders in which to extract zips
            # create folder, note file_map.sourceDirectory is the local temporary
            # directory where files are downloaded to and then copied to the target
            # give the destinations zip the software component name which is
            # the source directory folder name
            dest_filename = file_map.softwareComponent + '.zip'

            # extract straight into this directory, overwriting existing files
            if file_map.fileSource.startswith('http'):
                # downloads from URL
                try:
                    response = urlopen(file_map.fileSource)
                    logger.debug("downloading ." + file_map.fileSource + 
                                 "to" + dest_filename)

                    # open local file for writing
                    with open(dest_filename, "wb") as f:
                        f.write(response.read())
                # handle errors
                except HTTPError, e:
                    print "HTTP Error:", e.code, file_map.fileSource
                except URLError, e:
                    print "URL Error:", e.reason, file_map.fileSource

            elif file_map.fileSource.endswith('zip'):
                # zip file already on local disk
                # TODO: is this zip in the same directory as we are now
                continue
            else:
                logger.debug("unknown file format: " + file_map.fileSource)


    def get_zip_data(self, list_only=False):
        """ fetch zips from URLs for respective folders. Meta data stored
        and sourced from self.fileDict. Write extracted files to file system """

        for file_map in self.fileDict.values():
            zippedData = None

            if file_map == None: continue

            # initialise target extraction sub-folders in which to extract files
            # create folder, note file_map.sourceDirectory is the local temporary
            # directory where files are downloaded to and then copied to the target
            # location.
            if os.path.isdir(file_map.sourceDirectory):
                yn = raw_input("source files directory (%s) exists, "
                               "overwrite? [Y/n]" % file_map.sourceDirectory)
                if str(yn) == "n":
                    continue
                shutil.rmtree(file_map.sourceDirectory)

            self.updatesourcedirectory(file_map)
            

    def updatesourcedirectory(self, file_map):
        """ extract files to a local temporary directory """

        logger.debug("updating temporary directory for software component %s",
            file_map.softwareComponent)

        # save current directory to be restored later
        original_dir = os.getcwd()

        if os.path.isdir(file_map.sourceDirectory):
            shutil.rmtree(file_map.sourceDirectory)

        # make and change to temporary folder for this software component
        os.makedirs(file_map.sourceDirectory)
        os.chdir(file_map.sourceDirectory)

        if file_map.fileSource.startswith('http'):
            # downloads from URL
            logger.debug("downloading ." + file_map.fileSource)
            response = urlopen(file_map.fileSource)
            zippedData = StringIO(response.read())
        elif file_map.fileSource.endswith('zip'):
            # zip file already on local disk
            zippedData = os.path.join(self.zipDir, file_map.fileSource)
        else:
            logger.debug("unknown file format: " + file_map.fileSource)

        # extractor zip file to temporary folder
        ZipFile(zippedData).extractall()

        # move files from *-master subdirectories into base temp folder
        master_dir = file_map.softwareComponent + '-master'
        if os.path.isdir(master_dir):
            logger.debug("removing subdirectory: " + 
                os.listdir(file_map.sourceDirectory)[0])
            for t in os.listdir(master_dir):
                shutil.move(os.path.join(master_dir, t), os.getcwd())
            os.rmdir(master_dir)

        # return to previous directory
        os.chdir(original_dir)


    def distribute_files(self):
        """  move extracted files to target directories,
        assumes prerequisites and natlink have been installed,
        extracted files take precedence over existing ones """

        logger.debug("distributing local files to target directories...")
        for file_map in self.fileDict.values():
          # try: 

          if file_map == None: continue

          # for each software component file map object, replace local
          # folder contents with extracted files.
          dest_dir = file_map.destinationDirectory
          if not dest_dir:
              logger.debug("no target directory set for software "
                  "component %s" % file_map.softwareComponent)
              continue

          if os.path.isdir(dest_dir):
              logger.debug("target directory exists: %s", dest_dir)
              yn = raw_input("found local target directory, "
                             "replace? [y/N]")
              if str(yn) != "y":
                  continue
              # shutil.rmtree(dest_dir)
              # os.makedirs(dest_dir)
          else:
              if file_map.opt_dir:
                  os.makedirs(dest_dir)
              else:
                  # target destination directory cannot be found
                  logger.error("target destination directory %s not found. "
                      "this software component may not be installed.",
                      dest_dir)
                  # TODO: install natlink.

              
          # do the files exist to transfer to the local target?
          if not os.path.isdir(file_map.sourceDirectory):
              self.updatesourcedirectory(file_map)

          # We do not want to clobber entire directories, just specified 
          # file types. Assumption made that we don't want to recurse.
          for name in os.listdir(dest_dir):
              if os.path.splitext(dest_dir) in file_map.ext_list:
                  os.remove(dest_dir)

          # iterate through extracted files and move to target dir.
          for name in os.listdir(file_map.sourceDirectory):
              logger.debug("moving " + name)
              shutil.move(os.path.join(file_map.sourceDirectory, name), 
                          os.path.join(dest_dir, name))

          # except AttributeError:
          #   logger.debug("invalid file_map, skipping...(%s)", file_map)
          # except Exception, e:
          #   print 'ERROR, UNEXPECTED EXCEPTION'
          #   print str(e)
          #   traceback.print_exc()
          # finally:

          # remove temporary directory for extracted files
          shutil.rmtree(file_map.sourceDirectory)
        # natlink macrosystem scripts
        # unimacro scripts
        # vocola scripts
 
    def readfile(self, filename, fileList):
        # logger.info("opening %s" % self.wd+filename)
        count=0
        try:
            with open(filename,'r') as myfile:
                for line in myfile.readlines():
                    # logger.debug("reading %s" % line)
                    if line.startswith('http'):
                        try:
                            fileList.append(str(line))
                            count+=1
                        except:
                            logger.info("%s line not a macro entry" % line)
        except:
            logger.error('could not open : %s' % filename)
        finally:
            return count

def main ():

    global options, args

    # hardcoded values here to override defaults
    zip_dir = "/cygdrive/u/software/Speech related/current/configspeech_zips"
    work_dir = "c:\win scripts"
    # look for this file in working directory only?
    url_conf = "file_urls.conf"

    # retrieve URLs from config file, extract files tfrom zip
    fm = FileManager(
        urlconf=url_conf,
        zipdir=zip_dir,
        workdir=work_dir)

    # fm.set_targets(source="url")
    # # fm.fetch_zips_from_urls()
    # #fm.set_targets(source="zip")
    # fm.get_zip_data()

    # # install prerequisites and natlink
    # # move the vocola, unimacro, natlink, Windows scripts to the correct
    # # locations on local file system
    # fm.distribute_files()
    for k,v in fm.fileDict.iteritems():
      if v:
        logger.debug("\nTARGET file mapping as follows: KEY: %s "\
              "\n\tComponent: %s\n\tSource: %s\n\tLocal dir: %s\n\t Target dir: %s" %
              (k, str(v.softwareComponent), v.fileSource, v.sourceDirectory,
               v.destinationDirectory))
      else:
        logger.debug("TARGET file mapping is empty! KEY: %s\n" % k)

if __name__ == '__main__':
    # boilerplate
    try:
        start_time = time.time()
        parser = optparse.OptionParser(formatter=optparse.TitledHelpFormatter(), usage=globals()['__doc__'], version='$Id$')
        parser.add_option ('-v', '--verbose', action='store_true', default=False, help='verbose output')
        (options, args) = parser.parse_args()
        #if len(args) < 1:
        #    parser.error ('missing argument')
        if options.verbose: print time.asctime()
        main()
        if options.verbose: print time.asctime()
        if options.verbose: print 'TOTAL TIME IN MINUTES:',
        if options.verbose: print (time.time() - start_time) / 60.0
        sys.exit(0)
    except KeyboardInterrupt, e: # Ctrl-C
        raise e
    except SystemExit, e: # sys.exit()
        raise e
    except Exception, e:
        print 'ERROR, UNEXPECTED EXCEPTION'
        print str(e)
        traceback.print_exc()
        os._exit(1)
