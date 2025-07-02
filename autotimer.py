import pywinctl as pwc
import ScriptingBridge
import time
from urllib.parse import urlparse
from firefox_grab_url import get_current_browser_url

def Track_App(start_time, last_active_app):
  active_window = pwc.getActiveWindow()
  if active_window:
    active_app = active_window.getAppName()
    #Initial call to function
    if start_time == 0 and last_active_app == "None":
      start_time = time.time()
      Track_App(start_time, active_app)
    if active_app == 'Google Chrome' or active_app == 'Safari' or active_app == 'firefox':
      match active_app:
        case 'Google Chrome':
          browser = ScriptingBridge.SBApplication.applicationWithBundleIdentifier_("com.google.Chrome")
          window = browser.windows()[0]
          tab = window.activeTab().URL()
          tab = urlparse(tab).netloc
        case 'Safari':
          browser = ScriptingBridge.SBApplication.applicationWithBundleIdentifier_("com.apple.Safari")
          window = browser.windows()[0]
          tab = window.currentTab().URL()
          tab = urlparse(tab).netloc
        case 'firefox':
          tab = get_current_browser_url()
          tab = urlparse(tab).netloc
      #Is tab the same as last time function ran
      if tab == last_active_app:
        time.sleep(10)
        Track_App(start_time, tab)
      else:
        end_time = time.time()
        elapsed_time = end_time - start_time
        # Add entry to data.json
        start_time = time.time()
        time.sleep(10)
        Track_App(start_time, tab)
    else:
      #Is app the same as last time function ran
      if active_app == last_active_app:
        time.sleep(10)
        Track_App(start_time, active_app)
      else:
        end_time = time.time()
        elapsed_time = end_time - start_time
        # Add entry to data.json
        start_time = time.time()
        time.sleep(10)
        Track_App(start_time, active_app)
  
  while True:
    Track_App(0, "None")

