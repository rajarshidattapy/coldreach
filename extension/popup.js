// ---------- Utility ----------
function clean(text) {
  return text ? text.trim() : "";
}

// ---------- Message Generators ----------
function connectedMessage(name, company, headline, experience, resume) {
  return `Hey ${name},

Hope you’re doing well. I came across your work at ${company} — especially your experience in ${experience}. Solid stuff.

I’m exploring tech intern roles and wanted to check if your team has openings, or if you’d be open to giving a referral.

Here’s my resume: ${resume}

Thanks!`;
}

function notConnectedMessage(name, company, experience) {
  // must stay under 200 chars
  let msg = `Hi ${name}, exploring tech intern roles at ${company}. Saw your work in ${experience}. Would love to connect & check if openings exist. Thanks!`;

  return msg.slice(0, 200);
}

// ---------- Scrape LinkedIn using content script ----------
function getLinkedInData(callback) {
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    const tabId = tabs[0].id;

    chrome.tabs.sendMessage(tabId, { action: "SCRAPE_LINKEDIN" }, (response) => {
      if (!response) {
        callback({ error: "Unable to read profile. Are you on a LinkedIn profile page?" });
        return;
      }
      callback(response);
    });
  });
}

// ---------- Populate output ----------
function fillOutput(data) {
  const resume = document.getElementById("resume").value;

  const name = clean(data.name) || "there";
  const company = clean(data.company) || clean(data.headline) || "your company";
  const experience = clean(data.experience) || clean(data.headline) || "your work";

  let output = "";

  if (data.isConnected) {
    output = connectedMessage(name, company, data.headline, experience, resume);
  } else {
    output = notConnectedMessage(name, company, experience);
  }

  document.getElementById("output").value = output;
}

// ---------- Button Click ----------
document.getElementById("generate").addEventListener("click", () => {
  document.getElementById("output").value = "Extracting LinkedIn data...";

  getLinkedInData((data) => {
    if (data.error) {
      document.getElementById("output").value = data.error;
      return;
    }
    fillOutput(data);
  });
});

// ---------- Copy Button ----------
document.getElementById("copy").addEventListener("click", () => {
  const text = document.getElementById("output").value;
  navigator.clipboard.writeText(text).then(() => {
    alert("Copied!");
  });
});
