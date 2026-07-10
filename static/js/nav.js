(() => {
  const burger = document.getElementById("burgerBtn");
  const overlay = document.getElementById("navOverlay");
  const closeBtn = document.getElementById("navClose");

  const openNav = () => {
    overlay.classList.add("is-open");
    burger.setAttribute("aria-expanded", "true");
    document.body.style.overflow = "hidden";
  };

  const closeNav = () => {
    overlay.classList.remove("is-open");
    burger.setAttribute("aria-expanded", "false");
    document.body.style.overflow = "";
  };

  burger.addEventListener("click", openNav);
  closeBtn.addEventListener("click", closeNav);
  overlay.querySelectorAll("a").forEach((link) => link.addEventListener("click", closeNav));
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") closeNav(); });

  overlay.querySelectorAll(".nav-overlay__toggle").forEach((btn) => {
    btn.addEventListener("click", () => {
      const expanded = btn.getAttribute("aria-expanded") === "true";
      btn.setAttribute("aria-expanded", String(!expanded));
      btn.nextElementSibling.classList.toggle("is-open");
    });
  });
})();
