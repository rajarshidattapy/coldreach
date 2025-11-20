function text(selector) {
  const el = document.querySelector(selector);
  return el ? el.innerText.trim() : "";
}

function exists(selector) {
  return !!document.querySelector(selector);
}

chrome.runtime.onMessage.addListener((req, sender, sendResponse) => {
  if (req.action === "SCRAPE_LINKEDIN") {
    const name = text("h1.text-heading-xlarge");
    const headline = text(".text-body-medium.break-words");
    const experience = text("#experience ~ ul li div div span:first-child");
    const company = text("#experience ~ ul li div div span.t-14.t-normal");

    // If the "Connect" button appears → NOT connected
    const isConnected = !exists("button[aria-label='Invite']") &&
                        !exists("button[aria-label='Connect']");

    sendResponse({
      name,
      headline,
      experience,
      company,
      isConnected
    });
  }
});
