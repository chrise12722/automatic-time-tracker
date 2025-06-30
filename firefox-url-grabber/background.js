async function sendUrlToTimeTracker() {
  let [tab] = await chrome.tabs.query({ active: true, currentWindow: true })
  if (!tab || !tab.url.startsWith("http")) {
    console.log("No valid tab or URL found");
    return;
  }

  try {
    await fetch("http://localhost:5001/update-url", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ url: tab.url })
    });
  }
  catch (err) {
    console.error("Failed to send URL to Python app", err);
  }
}

setInterval(sendUrlToTimeTracker, 10000);