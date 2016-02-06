# device_watch.py

""" python script to poll USB devices and restart Dragon when relevant USB device
detection notification event is detected. """

import wmi
from subprocess import Popen
import logging as log
import pythoncom
import win32api
import traceback as tb

log.basicConfig(level=log.DEBUG)

def enumWMI(wmiClass):
    for d in wmiClass:
        yield d

## last component of deviceID (delimited by double "\") used as id
## both devices appear as generic USB audio. this seems to change when 
## using different USB ports?

## Jabra DeviceID = "USB\\VID_0B0E&PID_090A&MI_00\\8&38DDCE61&0&0000";

#targetCaps = [
#              "Jabra"
#              "Andrea" # sometimes just appears as "USB input device"
#             ]
#targetIDs = [
#             "VID_0B0E&PID_090A&MI_03&COL01" #\\9&3AC21659&0&0000",
#             "VID_08A8&PID_0018&MI_03\\8&2122B52B&0&0000",
##             JabraDeviceID = "USB\\VID_0B0E&PID_090A&MI_00\\7&2913CD2D&0&0000";
#            ]


nsrstPath = r"C:\win scripts\nsrst.bat"
JabraIDs = [r"8&38DDCE61&0&0000", r"7&2913CD2D&0&0000"];

# Flag for testing, when true, voice recognition is reset on each USB device
# connection.
force = False
#force = True

#global dev_dump;
#dev_dump = None
#
#def detect_and_compare(dev_dump):
#    """ compare device outputs with the previous dump """
#    print "running detect and compare"
#    wusbo = wmi.WMI().Win32_USBControllerDevice()
#    if dev_dump:
#        with open("dump_old.wmi.txt",'w') as myfile:
#            print "old dump"
#            myfile.write(str(dev_dump))
#        with open("dump_new.wmi.txt",'w') as myfile:
#            myfile.write(str(wusbo))
#    else:
#        dev_dump = wusbo

def execute_restart(dev):
  """ compare device ID string with known IDs, assign profile name 
  appropriately and pass to Dragon restart script as commandline arg """

  id_tuple = dev.DeviceID.split("\\")
  # which device was detected? Jabra or Andrea?
  script_arg = ""
  if id_tuple[0] == "USB":
    script_arg = "andrea wnc1500"
    if filter(lambda x:id_tuple[2] == x, JabraIDs):
      script_arg = "Jabra BIZ"
      print "Jabra BIZ: %s" % id_tuple[2]
    else:
      print "assuming andrea wnc1500: %s" % id_tuple[2]

    # Load relevant profile
    print("executing %s with arguments: %s" %
      (nsrstPath, script_arg))
    p = Popen([nsrstPath, script_arg])
    stdout, stderr = p.communicate()
    print "executed voice recognition restart script"
  else:
    print "non-USB audio device ignored"


# on initialisation after system start-up, try to determine profile to load
devices = enumWMI(wmi.WMI().Win32_SoundDevice())
for dev in devices:
  try:
    execute_restart(dev)
  except:
    log.debug("unhandled exception, polling device IDs!")
    tb.print_exc()
    pass


# watch for USB device added notifications
while True:
    watcher = wmi.WMI().watch_for (
        notification_type="Creation",
        wmi_class="Win32_SoundDevice",
        delay_secs=1
    )

    # returns Unicode string only
    watchRes = watcher()
    try:
        # record detected sound device ID
#        with open("device_watch_devlist.txt",'a') as myfile:
#            myfile.write(str(watchRes) + '\n')
        # print dir(watchRes) 
        # print watchRes.Caption,  watchRes.Description
        # print watchRes.Manufacturer,  watchRes.DeviceID 
        execute_restart(watchRes)
    except:
        log.debug("unhandled exception: comparing with known strings!")
        tb.print_exc()

#    watchDevVIDStr = \
#      watchRes.DeviceID.split("\"")[1].replace("\\\\","\\").split("\\")[1]
#    log.debug("USB device detected, VID: {0}, ID short string: {1}"
#              .format(watchRes.Dependent, watchDevVIDStr))
#    #.DeviceID, watchRes.Dependent.Caption))
#    #detect_and_compare(dev_dump)
# 
#    #  Check for valid identifier starting with "VID_" in return string from
#    #  watcher (dependent string). Find relevant WMI object
#    if watchDevVIDStr.startswith("VID_"):
#        caption = ""
#        devID = ""
#        devices = enumWMI(wmi.WMI().Win32_USBControllerDevice())
#        for dev in devices:
# #            print(dev.Dependent.Caption)
# #            print(dev.Dependent.DeviceID)
#            try:
#                if watchDevVIDStr in dev.Dependent.DeviceID:
#                    caption = dev.Dependent.Caption
#                    devID = dev.Dependent.DeviceID
# 
#                    log.debug("Attached USB device detected: {0} \n{1}".format(caption, dev.Dependent))
#                    break
#            except pythoncom.com_error as error:
#                log.debug("Error with reading wmi coption: {1}",
#                    win32api.FormatMessage(error.excepinfo[5]))
#                pass
#            except:
#                log.debug("unhandled exception, polling device IDs!")
#                tb.print_exc()
#                pass
# 
#        #  Check for Jabra device (if the device creation event is for the jabra)
#        try:
#            #for targid in targetIDs:
#            #    if targid in devID:
#            #        log.info(" USB device for voice recognition is present: %s, %s"%
#            #                (caption, devID))
#            #        p = Popen(nsrstPath)
#            #        stdout, stderr = p.communicate()
#            #        break
#            for targcap in targetCaps:
#                if (targcap. in caption or force == True:
#                    log.info(" USB device for voice recognition is present: %s, %s"%
#                             (caption, devID))
#    ##            #if ('NatSpeak.exe' or 'natspeak.exe') in [c.Name for c in wmiObj.Win32_Process()]:
#                    p = Popen(nsrstPath)
#                    stdout, stderr = p.communicate()
#                    break
#        except:
#            log.debug("unhandled exception: comparing with known strings!")
#            tb.print_exc()
#            pass
#
#        # TODO: instead of just blindly restarting Dragon, could use Win32_Process to
#        # check the process is running, kill gracefully and then restart. I'm
#        # being lazy and using pre-existing batch script.
