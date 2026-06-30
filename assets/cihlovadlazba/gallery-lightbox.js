(function () {
  const lightbox = document.getElementById("gallery-lightbox");
  if (!lightbox) return;

  const images = Array.from(
    document.querySelectorAll(".gallery-stack .gallery-item img")
  );
  if (!images.length) return;

  const imageEl = lightbox.querySelector(".lightbox__image");
  const captionEl = lightbox.querySelector(".lightbox__caption");
  const counterEl = lightbox.querySelector(".lightbox__counter");
  const prevBtn = lightbox.querySelector(".lightbox__nav--prev");
  const nextBtn = lightbox.querySelector(".lightbox__nav--next");
  const closeBtn = lightbox.querySelector(".lightbox__close");

  let currentIndex = 0;
  let lastFocus = null;

  function getCaption(index) {
    const group = images[index].closest(".gallery-group");
    return group?.querySelector(".gallery-group-title")?.textContent?.trim() ?? "";
  }

  function updateView() {
    const source = images[currentIndex];
    imageEl.src = source.currentSrc || source.src;
    imageEl.alt = source.alt;
    captionEl.textContent = getCaption(currentIndex);
    counterEl.textContent = `${currentIndex + 1} / ${images.length}`;
    prevBtn.disabled = currentIndex === 0;
    nextBtn.disabled = currentIndex === images.length - 1;
  }

  function open(index) {
    lastFocus = document.activeElement;
    currentIndex = index;
    updateView();
    lightbox.hidden = false;
    lightbox.setAttribute("aria-hidden", "false");
    document.body.classList.add("lightbox-open");
    closeBtn.focus();
  }

  function close() {
    lightbox.hidden = true;
    lightbox.setAttribute("aria-hidden", "true");
    document.body.classList.remove("lightbox-open");
    imageEl.removeAttribute("src");
    if (lastFocus instanceof HTMLElement) {
      lastFocus.focus();
    }
  }

  function showPrev() {
    if (currentIndex > 0) {
      currentIndex -= 1;
      updateView();
    }
  }

  function showNext() {
    if (currentIndex < images.length - 1) {
      currentIndex += 1;
      updateView();
    }
  }

  images.forEach((img, index) => {
    const item = img.closest(".gallery-item");
    if (!item) return;

    item.addEventListener("click", () => open(index));
    item.setAttribute("role", "button");
    item.setAttribute("tabindex", "0");
    item.setAttribute(
      "aria-label",
      `Zvětšit fotografii ${index + 1} z ${images.length}`
    );

    item.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        open(index);
      }
    });
  });

  prevBtn.addEventListener("click", showPrev);
  nextBtn.addEventListener("click", showNext);
  closeBtn.addEventListener("click", close);

  lightbox.addEventListener("click", (event) => {
    if (event.target === lightbox) {
      close();
    }
  });

  document.addEventListener("keydown", (event) => {
    if (lightbox.hidden) return;

    if (event.key === "Escape") close();
    if (event.key === "ArrowLeft") showPrev();
    if (event.key === "ArrowRight") showNext();
  });
})();
