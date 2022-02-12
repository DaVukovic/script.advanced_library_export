import xbmc
import xbmcaddon
import xbmcgui
import json


ADDON = xbmcaddon.Addon()
ADDONID = ADDON.getAddonInfo('id')
ADDONNAME = ADDON.getAddonInfo('name')
LANGUAGE = ADDON.getLocalizedString
DIALOG = xbmcgui.Dialog()


def getSettings():
    build_all = xbmc.getInfoLabel('System.BuildVersionShort')
    build_split = build_all.split('-')
    build = float(build_split[0])
    if float(build) >= 20.0:
        SETTINGS = xbmcaddon.Addon().getSettings()
        getSettings.enable_separated = SETTINGS.getBool('enable_separated')
        getSettings.images = SETTINGS.getBool('images')
        getSettings.actor = SETTINGS.getBool('actor')
        getSettings.overwrite = SETTINGS.getBool('overwrite')
        getSettings.enable_single = SETTINGS.getBool('enable_single')
        getSettings.path = SETTINGS.getString('path')
    else:
        getSettings.enable_separated = ADDON.getSettingBool('enable_separated')
        getSettings.images = ADDON.getSettingBool('images')
        getSettings.actor = ADDON.getSettingBool('actor')
        getSettings.overwrite = ADDON.getSettingBool('overwrite')
        getSettings.enable_single = ADDON.getSettingBool('enable_single')
        getSettings.path = ADDON.getSettingString('path')

def execJSONSingle(path):
    req = {
        "jsonrpc": "2.0",
        "method": "VideoLibrary.Export",
        "id": 1,
        "params": {
            "options": {
                "path": path
            }
        }
    }
    rpc_request = json.dumps(req)
    response = json.loads(xbmc.executeJSONRPC(rpc_request))
    if "OK" not in response['result']:
        DIALOG.ok(ADDONNAME, LANGUAGE(32001) + str(response))

def execJSONSeparate(images, actor, overwrite):
    req = {
        "jsonrpc": "2.0",
        "method": "VideoLibrary.Export",
        "id": 1,
        "params": {
            "options": {
                "images": images,
                "actorthumbs": actor,
                "overwrite": overwrite
            }
        }
    }
    rpc_request = json.dumps(req)
    response = json.loads(xbmc.executeJSONRPC(rpc_request))
    if "OK" not in response['result']:
        DIALOG.ok(ADDONNAME, LANGUAGE(32001) + str(response))

def main():
    getSettings()
    separated = getSettings.enable_separated
    single = getSettings.enable_single
    path = getSettings.path
    images = getSettings.images
    actor = getSettings.actor
    overwrite = getSettings.overwrite

    if separated:
        execJSONSeparate(images, actor, overwrite)
    elif single:
        execJSONSingle(path)
    else:
        DIALOG.ok(ADDONNAME, LANGUAGE(32002))
