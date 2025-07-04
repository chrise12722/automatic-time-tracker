import pywinctl as pwc
import ScriptingBridge
import datetime
import time
import csv
import threading
from urllib.parse import urlparse
from firefox_grab_url import get_current_browser_url

def Track_App(start_time, last_active_app):
  active_window = pwc.getActiveWindow()
  if active_window:
    active_app = active_window.getAppName()
    #Initial call to function
    if start_time == 0 and last_active_app == "None":
      # start_time = time.time()
      start_time = datetime.datetime.now().replace(microsecond=0)
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
        # end_time = time.time()
        end_time = datetime.datetime.now().replace(microsecond=0)
        elapsed_seconds = round(end_time.timestamp() - start_time.timestamp())
        elapsed_time = str(datetime.timedelta(seconds=elapsed_seconds))
        tab_data = {
          "App/Website": last_active_app,
          "Start_time": start_time,
          "Stop_time": end_time,
          "Total_time": elapsed_time
        }
        try:
          with open('data.csv', 'a', newline='') as csvfile:
            fieldnames = ["App/Website", "Start_time", "Stop_time", "Total_time"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(tab_data)
            csvfile.write('\n')
        except IOError as e:
          print(f"Error writing to file: {e}")
        # start_time = time.time()
        start_time = datetime.datetime.now().replace(microsecond=0)
        time.sleep(10)
        Track_App(start_time, tab)
    else:
      #Is app the same as last time function ran
      if active_app == last_active_app:
        time.sleep(10)
        Track_App(start_time, active_app)
      else:
        end_time = datetime.datetime.now().replace(microsecond=0)
        elapsed_seconds = round(end_time.timestamp() - start_time.timestamp())
        elapsed_time = str(datetime.timedelta(seconds=elapsed_seconds))
        app_data = {
          "App/Website": last_active_app,
          "Start_time": start_time,
          "Stop_time": end_time,
          "Total_time": elapsed_time
        }
        try:
          with open('data.csv', 'a', newline='') as csvfile:
            fieldnames = ["App/Website", "Start_time", "Stop_time", "Total_time"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(app_data)
            csvfile.write('\n')
        except IOError as e:
          print(f"Error writing to file: {e}")
        # start_time = time.time()
        start_time = datetime.datetime.now().replace(microsecond=0)
        time.sleep(10)
        Track_App(start_time, active_app)

def run_tracker():
  Track_App(0, "None")

if __name__ == "__main__":
  #Start tracker in background thread
  tracker_thread = threading.Thread(target=run_tracker, daemon=True)
  tracker_thread.start()
  
  print("Time tracker started in background. Press Ctrl+C to stop.")
  
  try:
    #Keep main thread alive
    while True:
      time.sleep(1)
  except KeyboardInterrupt:
    print("\nStopping time tracker...")

