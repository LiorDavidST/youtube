// פונקציה לבדיקת קלט URL חוקי
function isValidUrl(url) {
    // נוסיף Regex לבדוק אם ה-URL חוקי
    const regex = /^(https?:\/\/)?(www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,6}(\.[a-zA-Z]{2})?(\/[^\s]*)?$/;
    return regex.test(url);
  }
  
  // בעת טעינת הדף: הגדרת כפתור הפורמט והחלפה בלחיצה
  document.addEventListener('DOMContentLoaded', () => {
    const formatButton = document.getElementById("formatToggle");
  
    formatButton.addEventListener("click", () => {
      let currentFormat = formatButton.getAttribute("data-format");
      const newFormat = currentFormat === "mp4" ? "mp3" : "mp4";
      const icon = newFormat === "mp4" ? "🎞️" : "🎧";
      formatButton.setAttribute("data-format", newFormat);
      formatButton.innerHTML = `${icon} Format: ${newFormat.toUpperCase()} <i class="fas fa-exchange-alt"></i>`;
    });
  });
  
  // פונקציה להתחלת הורדה
  function startDownload() {
    document.getElementById("filename").innerText = ""; // איפוס שם הקובץ בכל התחלה
  
    const urlInput = document.getElementById("url");
    const url = urlInput.value;
    const format = document.getElementById("formatToggle").getAttribute("data-format");
  
    const progress = document.getElementById("progress");
    const progressContainer = document.getElementById("progress-container");
    const progressText = document.getElementById("progress-text");
    const message = document.getElementById("message");
    const link = document.getElementById("link");
  
    // בדיקה אם ה-URL לא ריק ואימות חוקיות ה-URL
    if (!url || !isValidUrl(url)) {
      alert("❌ Please paste a valid YouTube URL.");
      return;
    }
  
    // 🚫 חסימת Playlist או MIX
    if (url.includes("list=") || url.includes("RDMM") || url.includes("&index=")) {
      alert("❌ Playlists and YouTube Mix links are not supported. Please paste a single video URL.");
      return;
    }
  
    progress.style.width = "0%";
    progressText.innerText = "0%";
    progressContainer.style.display = "block";
    message.innerText = "";
    message.style.opacity = 0;
    link.style.display = "none";
    link.style.opacity = 0;
  
    let width = 0;
    let filename = "";
    let downloadSuccess = false;
  
    const progressInterval = setInterval(() => {
      if (width < 100) {
        width += 1;
        progress.style.width = width + "%";
        progressText.innerText = width + "%";
      }
    }, 50);
  
    fetch("/", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded"
      },
      body: `url=${encodeURIComponent(url)}&format=${format}&save_path=`
    })
    .then(response => response.json())
    .then(data => {
      if (data.filename) {
        filename = data.filename;
        link.href = `/download/${encodeURIComponent(filename)}`;
        downloadSuccess = true;
      } else {
        throw new Error(data.message || "Unknown error. Please try again.");
      }
    })
    .catch(err => {
      clearInterval(progressInterval);
      progressContainer.style.display = "none";
      const errorText = String(err);
      let userFriendlyMessage = "❌ Error: Something went wrong during download. Please try again.";
  
      if (errorText.includes("WinError 32")) {
        userFriendlyMessage = "❌ Download failed: The file is being used by another program. Please close any apps that may be using it and try again.";
      } else if (errorText.includes("fragment not found")) {
        userFriendlyMessage = "❌ Download failed: One or more video fragments were missing. Try downloading again.";
      }
  
      message.innerText = userFriendlyMessage;
      message.style.opacity = 1;
    });
  
    setTimeout(() => {
      clearInterval(progressInterval);
      progress.style.width = "100%";
      progressText.innerText = "100%";
      progressContainer.style.display = "none";
  
      if (downloadSuccess && filename) {
        message.innerText = "✅ Download completed successfully!";
        document.getElementById("filename").innerText = ` ${filename}`;
        urlInput.value = ""; // ניקוי שדה הלינק
        message.style.transition = "opacity 0.5s ease-in-out";
        message.style.opacity = 1;
  
        setTimeout(() => {
          link.style.display = "block";
          link.style.transition = "opacity 0.5s ease-in-out";
          link.style.opacity = 1;
        }, 1000);
      } else if (!message.innerText) {
        message.innerText = "⚠️ Download may not have completed. Please try again.";
        message.style.opacity = 1;
      }
    }, 5000); // Simulate download duration
  }
  