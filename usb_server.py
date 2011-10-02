import dbus, gobject
from dbus.mainloop.glib import DBusGMainLoop
from pprint import pprint

DBusGMainLoop(set_as_default=True)
bus = dbus.SystemBus()

def device_added_callback(device):
    print('Added:')
    dev_obj = bus.get_object('org.freedesktop.UDisks', device)
    dev_props = dbus.Interface(dev_obj, dbus.PROPERTIES_IFACE)
    pprint (dev_props.Get('org.freedesktop.UDisks.Device', 'DeviceMountPaths'))

def device_changed_callback(device):
    print('Changed:')
    dev_obj = bus.get_object('org.freedesktop.UDisks', device)
    dev_props = dbus.Interface(dev_obj, dbus.PROPERTIES_IFACE)
    pprint (dev_props.Get('org.freedesktop.UDisks.Device', 'DeviceMountPaths'))

proxy = bus.get_object('org.freedesktop.UDisks', '/org/freedesktop/UDisks')
iface = dbus.Interface(proxy, 'org.freedesktop.UDisks')

iface.connect_to_signal('DeviceAdded', device_added_callback)
iface.connect_to_signal('DeviceChanged', device_changed_callback)

mainloop = gobject.MainLoop()
mainloop.run()