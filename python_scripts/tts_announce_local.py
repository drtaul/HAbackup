#import pdb
#import logging
#logger = logging.getLogger(__name__)
#data = {'speaker': "all"}
def get_devices(sl, echolist, gcastlist):
    speakers = {'office_echo': ('echo', 'media_player.office_echo'),
                'garage_echo': ('echo', 'media_player.garage_echo'),
                'bonus_room_dashboard': ('echo', 'media_player.dennis_s_3rd_fire'),
                'bonus_room_speaker': ('gcast', 'media_player.bonus_room_speaker'),
                'google_home': ('gcast', 'media_player.master_bedroom_home'),
                'living_room_echo': ('echo', 'media_player.living_room_echo'),
                'pavilion_echo': ('echo', 'media_player.pavilion_echo'),
                'master_bedroom_echo': ('echo', 'media_player.master_bedroom_echo'),
                'bonus_room_cube': ('echo', 'media_player.bonus_room_cube')
                'all_echos': ('broadcast_echo', 'NA'),
                'all_googles': ('broadcast_gcast', 'NA'),
                'all': ('broadcast', 'NA')}
    #logger.error("get_devices called with sl: %s", sl)    
    for spitem in sl:
        fn = spitem.replace(" ", "_").lower().strip("_")
        if fn.startswith("all"):
            # we are here if this is a broadcast request
            if (fn == "all") or (fn == "all_echos"):
                for key, ditem in speakers.items():
                    if ditem[0] == 'echo':
                        echolist.append(ditem[1])
            elif (fn == "all") or fn == ("all_googles"):
                for key, ditem in speakers.items():
                    if ditem[0] == 'gcast':
                        gcastlist.append(ditem[1])
            else:
                logger.error("Invalid broadcast speaker name %s", fn)
                
        else:
            spkdata = speakers.get(fn)
            if spkdata is not None:
                if spkdata[0] == 'echo':
                    #logger.warn("appending echo device %s", spkdata[1])            
                    echolist.append(spkdata[1])
                elif spkdata[0] == 'gcast':
                    #logger.warn("appending gcast device %s", spkdata[1])            
                    gcastlist.append(spkdata[1])
            else:
                logger.error("Invalid speaker name %s:%s", spitem, fn)
            
    

echo_devices = []
echo_devices.clear()
gcast_devices = []
gcast_devices.clear()
# list of friendly smart speaker names
ispeakerlist = data.get('speaker')
#logger.warn("ispeakerlist: %s", ispeakerlist)

# text to announce
txtmessage = data.get('message')
vol = data.get('volume')
if vol is None:
    vol = 0.7
sl = ispeakerlist.split(",")
get_devices(sl, echo_devices, gcast_devices)

if echo_devices:
    service_data = {"speaker": echo_devices, "message": txtmessage, "volume": vol}
    #logger.warn("calling announce_echo script with %s", service_data)
    hass.services.call('script', 'announce_echo', service_data)
if gcast_devices:
    service_data = {"speaker": gcast_devices, "message": txtmessage, "volume": vol}
    #logger.warn("calling announce_gcast script with %s", service_data)
    hass.services.call('script', 'announce_gcast', service_data)
        
if (len(echo_devices) == 0) and (len(gcast_devices) == 0):
    logger.error("tts_announce failed with invalid speakers: %s", ispeakerlist)
        
