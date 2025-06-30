import pywinctl as pwc
import ScriptingBridge
import time
from firefox_grab_url import get_current_browser_url

while True:
  active_window = pwc.getActiveWindow()
  if active_window:
    active_app = active_window.getAppName()
    if active_app == 'Google Chrome' or active_app == 'Safari' or active_app == 'firefox':
      match active_app:
        case 'Google Chrome':
          browser = ScriptingBridge.SBApplication.applicationWithBundleIdentifier_("com.google.Chrome")
          window = browser.windows()[0]
          tab = window.activeTab()
        case 'Safari':
          browser = ScriptingBridge.SBApplication.applicationWithBundleIdentifier_("com.apple.Safari")
          window = browser.windows()[0]
          tab = window.currentTab()
        case 'firefox':
          tab = get_current_browser_url()
          if tab:
            print(tab)
          else:
            print("Firefox - No URL available yet")
    else:
      print(active_app)
  
  time.sleep(10)

