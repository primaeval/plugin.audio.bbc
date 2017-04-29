import xbmcaddon
import xbmc, xbmcgui, xbmcvfs
import requests
import base64
import time, datetime

servicing = False

def Service():
    global servicing
    if servicing:
        return
    servicing = True
    xbmc.log("SERVICE")
    xbmc.executebuiltin('XBMC.RunPlugin(plugin://plugin.video.bbc/pvr_service)')
    time.sleep(2)
    servicing = False

if __name__ == '__main__':
    ADDON = xbmcaddon.Addon('plugin.video.bbc')

    try:
        if ADDON.getSetting('pvr.service') == 'true':
            monitor = xbmc.Monitor()
            xbmc.log("[plugin.video.bbc] pvr service started...", xbmc.LOGDEBUG)
            if ADDON.getSetting('pvr.startup') == 'true':
                Service()
                ADDON.setSetting('last.pvr.update', str(time.time()))
            if ADDON.getSetting('pvr.type') == '0':
                quit()
            while not monitor.abortRequested():
                if ADDON.getSetting('pvr.type') == '1':
                    interval = int(ADDON.getSetting('pvr.interval'))
                    waitTime = 3600 * interval
                    ts = ADDON.getSetting('last.pvr.update') or "0.0"
                    lastTime = datetime.datetime.fromtimestamp(float(ts))
                    now = datetime.datetime.now()
                    nextTime = lastTime + datetime.timedelta(seconds=waitTime)
                    td = nextTime - now
                    timeLeft = td.seconds + (td.days * 24 * 3600)
                    xbmc.log("[plugin.video.bbc] Service waiting for interval %s" % waitTime, xbmc.LOGDEBUG)
                elif ADDON.getSetting('pvr.type') == '2':
                    next_time = ADDON.getSetting('pvr.time')
                    if next_time:
                        hour,minute = next_time.split(':')
                        now = datetime.datetime.now()
                        next_time = now.replace(hour=int(hour),minute=int(minute),second=0,microsecond=0)
                        if next_time < now:
                            next_time = next_time + datetime.timedelta(hours=24)
                        td = next_time - now
                        timeLeft = td.seconds + (td.days * 24 * 3600)
                if timeLeft <= 0:
                    timeLeft = 1
                xbmc.log("[plugin.video.bbc] Service waiting for %d seconds" % timeLeft, xbmc.LOGDEBUG)
                if timeLeft and monitor.waitForAbort(timeLeft):
                    break
                xbmc.log("[plugin.video.bbc] Service now triggered...", xbmc.LOGDEBUG)
                Service()
                now = time.time()
                ADDON.setSetting('last.pvr.update', str(now))

    except:
        pass

        