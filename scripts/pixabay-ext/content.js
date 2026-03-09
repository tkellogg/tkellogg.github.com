// Extract the CDN image URL from the og:image meta tag
const og = document.querySelector('meta[property="og:image"]');
if (og) {
  const url = og.content;
  navigator.clipboard.writeText(url).then(() => {
    const toast = document.createElement("div");
    toast.textContent = "Copied: " + url;
    Object.assign(toast.style, {
      position: "fixed", top: "10px", right: "10px", zIndex: "999999",
      background: "#333", color: "#fff", padding: "12px 20px",
      borderRadius: "8px", fontSize: "14px", fontFamily: "monospace",
      maxWidth: "600px", wordBreak: "break-all",
    });
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 5000);
  });
}
