(function () {
  const header = document.querySelector(".site-header");
  if (!header) return;

  const toggle = header.querySelector(".nav-toggle");
  const nav = header.querySelector(".main-nav");
  if (!toggle || !nav) return;

  function setOpen(open) {
    header.classList.toggle("is-open", open);
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    toggle.setAttribute("aria-label", open ? "Zavřít menu" : "Otevřít menu");
    document.body.classList.toggle("nav-open", open);
  }

  toggle.addEventListener("click", function () {
    setOpen(!header.classList.contains("is-open"));
  });

  nav.querySelectorAll("a").forEach(function (link) {
    link.addEventListener("click", function () {
      setOpen(false);
    });
  });

  document.addEventListener("click", function (event) {
    if (!header.classList.contains("is-open")) return;
    if (!header.contains(event.target)) setOpen(false);
  });

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") setOpen(false);
  });
})();
