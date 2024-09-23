const journalistNameElement = document.querySelector('.media_end_head_journalist_name');

if (journalistNameElement) {
  const journalistName = journalistNameElement.innerText.trim();
  
  chrome.storage.local.set({ journalist: journalistName }, function() {
    console.log("Journalist name saved:", journalistName);
  });
}
