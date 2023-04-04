chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
  if (message.action === "collectImage") {
    const { imgSrc, imgAlt } = message.data;

    // 保存图片信息到浏览器的存储
    chrome.storage.sync.get("collectedImages", function (result) {
      const collectedImages = result.collectedImages || [];
      collectedImages.push({ imgSrc, imgAlt });

      chrome.storage.sync.set({ collectedImages }, function () {
        console.log("图片已收藏");
      });
    });

    // 展示图片的alt信息
    alert(`图片已收藏！\n图片alt信息：${imgAlt}`);
  }
});
