import pywinctl as pwc
import ScriptingBridge
import datetime
import time
import csv
import threading
import atexit
import pandas as pd
from urllib.parse import urlparse
from firefox_grab_url import get_current_browser_url

class TimeTracker:
  def __init__(self):
    self.start_time = 0
    self.last_active_app = "None"

  def track_app(self):
    active_window = pwc.getActiveWindow()
    if active_window:
      active_app = active_window.getAppName()
      #Initial call to function
      if self.start_time == 0 and self.last_active_app == "None":
        self.start_time = datetime.datetime.now().replace(microsecond=0)
        self.last_active_app = active_app
        empty_csv = False
        try:
          df = pd.read_csv('data.csv')
        except (pd.errors.EmptyDataError):
          empty_csv = True
        if empty_csv:
          with open('data.csv', 'w', newline='') as csvfile:
            fieldnames=["App/Website", "Start_time", "Stop_time", "Total_time"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            csvfile.write('\n')
        return
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
        if tab == self.last_active_app:
          return
        else:
          end_time = datetime.datetime.now().replace(microsecond=0)
          elapsed_seconds = round(end_time.timestamp() - self.start_time.timestamp())
          elapsed_time = str(datetime.timedelta(seconds=elapsed_seconds))
          tab_data = {
            "App/Website": self.last_active_app,
            "Start_time": self.start_time,
            "Stop_time": end_time,
            "Total_time": elapsed_time
          }
          try:
            with open('data.csv', 'a', newline='') as csvfile:
              fieldnames = ["App/Website", "Start_time", "Stop_time", "Total_time"]
              writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
              writer.writerow(tab_data)
              csvfile.write('\n')
          except IOError as e:
            print(f"Error writing to file: {e}")
          self.start_time = datetime.datetime.now().replace(microsecond=0)
          self.last_active_app = tab
          return
      else:
        #Is app the same as last time function ran
        if active_app == self.last_active_app:
          return
        else:
          end_time = datetime.datetime.now().replace(microsecond=0)
          elapsed_seconds = round(end_time.timestamp() - self.start_time.timestamp())
          elapsed_time = str(datetime.timedelta(seconds=elapsed_seconds))
          app_data = {
            "App/Website": self.last_active_app,
            "Start_time": self.start_time,
            "Stop_time": end_time,
            "Total_time": elapsed_time
          }
          try:
            with open('data.csv', 'a', newline='') as csvfile:
              fieldnames = ["App/Website", "Start_time", "Stop_time", "Total_time"]
              writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
              writer.writerow(app_data)
              csvfile.write('\n')
          except IOError as e:
            print(f"Error writing to file: {e}")
          self.start_time = datetime.datetime.now().replace(microsecond=0)
          self.last_active_app = active_app
          return

  def sort_csv_file(self):
    try:
      #Read CSV data
      rows = []
      with open('data.csv', 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
          rows.append(row)

      if not rows:
        return
      
      sorted_rows = sorted(rows, key=lambda row: row['App/Website'])

      #Write sorted data to CSV
      with open('data.csv', 'w', newline='') as csvfile:
        fieldnames=["App/Website", "Start_time", "Stop_time", "Total_time"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        csvfile.write('\n')
        for row in sorted_rows:
          writer.writerow(row)
          csvfile.write('\n')
    except FileNotFoundError:
      print("CSV file was not found")
    except Exception as e:
      print(f"Error sorting CSV file: {e}")

  def exit_record(self):
    end_time = datetime.datetime.now().replace(microsecond=0)
    elapsed_seconds = round(end_time.timestamp() - self.start_time.timestamp())
    elapsed_time = str(datetime.timedelta(seconds=elapsed_seconds))
    app_data = {
      "App/Website": self.last_active_app,
      "Start_time": self.start_time,
      "Stop_time": end_time,
      "Total_time": elapsed_time
    }
    try:
      with open('data.csv', 'a', newline='') as csvfile:
        fieldnames = ["App/Website", "Start_time", "Stop_time", "Total_time"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(app_data)
        csvfile.write('\n')
    except IOError as e:
      print(f"Error writing to file: {e}")

def run_tracker(tracker):
  while True:
    tracker.track_app()
    time.sleep(10)

if __name__ == "__main__":
  # Create tracker instance
  tracker = TimeTracker()
  
  #Run sorting function at exit
  atexit.register(tracker.sort_csv_file)
  atexit.register(tracker.exit_record)
  
  #Start tracker in background thread
  tracker_thread = threading.Thread(target=run_tracker, args=(tracker,), daemon=True)
  tracker_thread.start()
  
  print("Time tracker started in background. Press Ctrl+C to stop.")
  
  try:
    #Keep main thread alive
    while True:
      time.sleep(1)
  except KeyboardInterrupt:
    print("\nStopping time tracker...")

