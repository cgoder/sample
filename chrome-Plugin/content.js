document.addEventListener("click", function (event) {
  const target = event.target;

  if (target.tagName.toLowerCase() === "img") {
    const imgSrc = target.src;
    const imgAlt = target.alt || "无alt信息";

    chrome.runtime.sendMessage({
      action: "collectImage",
      data: { imgSrc, imgAlt },
    });
  }
});
