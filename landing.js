(() => {
  "use strict";

  const buttons = [...document.querySelectorAll("[data-language]")];
  const translated = [...document.querySelectorAll("[data-pl][data-en]")];

  const setLanguage = (language) => {
    const next = language === "en" ? "en" : "pl";
    document.documentElement.lang = next;
    localStorage.setItem("site-language", next);
    buttons.forEach((button) => button.classList.toggle("is-active", button.dataset.language === next));
    translated.forEach((node) => {
      node.textContent = node.dataset[next];
    });
  };

  buttons.forEach((button) => {
    button.addEventListener("click", () => setLanguage(button.dataset.language));
  });

  const saved = localStorage.getItem("site-language");
  const browserLanguage = navigator.language?.toLowerCase().startsWith("en") ? "en" : "pl";
  setLanguage(saved || browserLanguage);
})();
