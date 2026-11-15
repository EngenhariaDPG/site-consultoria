/* Número no formato internacional, somente dígitos.
   Exemplo ilustrativo: 5532999999999. Deixe vazio para copiar o briefing. */
const WHATSAPP_NUMBER = "";

document.documentElement.classList.add("js-ready");

const menuButton = document.querySelector(".menu-toggle");
const navigation = document.querySelector(".nav");

function closeMenu() {
  if (!menuButton || !navigation) return;
  menuButton.setAttribute("aria-expanded", "false");
  menuButton.setAttribute("aria-label", "Abrir menu");
  navigation.classList.remove("is-open");
}

if (menuButton && navigation) {
  menuButton.addEventListener("click", function () {
    const open = menuButton.getAttribute("aria-expanded") === "true";
    menuButton.setAttribute("aria-expanded", String(!open));
    menuButton.setAttribute("aria-label", open ? "Abrir menu" : "Fechar menu");
    navigation.classList.toggle("is-open", !open);
  });
  navigation.querySelectorAll("a").forEach(function (link) {
    link.addEventListener("click", closeMenu);
  });
  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") closeMenu();
  });
}

const revealItems = document.querySelectorAll(".reveal");
if ("IntersectionObserver" in window) {
  const observer = new IntersectionObserver(function (entries, currentObserver) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
        currentObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12, rootMargin: "0px 0px -30px 0px" });
  revealItems.forEach(function (item) { observer.observe(item); });
} else {
  revealItems.forEach(function (item) { item.classList.add("is-visible"); });
}

const year = document.getElementById("current-year");
if (year) year.textContent = String(new Date().getFullYear());

const form = document.getElementById("contact-form");
const result = document.getElementById("form-result");
const resultText = document.getElementById("form-result-text");
const copyButton = document.getElementById("copy-message");
let messageToCopy = "";

function buildMessage(data) {
  return [
    "Olá! Gostaria de conversar com a DPG Engenharia Mecânica.",
    "",
    "Nome: " + data.get("nome"),
    "Empresa: " + (data.get("empresa") || "Não informada"),
    "Cidade/Estado: " + data.get("cidade"),
    "Serviço: " + data.get("servico"),
    "",
    "Descrição da necessidade:",
    data.get("mensagem")
  ].join("\n");
}

async function copyMessage() {
  if (!messageToCopy) return;
  try {
    await navigator.clipboard.writeText(messageToCopy);
    copyButton.innerHTML = "Mensagem copiada <span aria-hidden='true'>✓</span>";
  } catch (error) {
    const field = document.createElement("textarea");
    field.value = messageToCopy;
    field.style.position = "fixed";
    field.style.opacity = "0";
    document.body.appendChild(field);
    field.select();
    const copied = document.execCommand("copy");
    field.remove();
    copyButton.innerHTML = copied ? "Mensagem copiada <span aria-hidden='true'>✓</span>" : "Não foi possível copiar";
  }
}

if (form) {
  form.addEventListener("submit", function (event) {
    event.preventDefault();
    if (!form.reportValidity()) return;
    messageToCopy = buildMessage(new FormData(form));
    result.hidden = false;

    if (WHATSAPP_NUMBER.trim()) {
      resultText.textContent = "Seu briefing está pronto. Abra o WhatsApp para encaminhar a solicitação.";
      copyButton.innerHTML = "Abrir WhatsApp <span aria-hidden='true'>↗</span>";
      copyButton.onclick = function () {
        const url = "https://wa.me/" + WHATSAPP_NUMBER.trim() + "?text=" + encodeURIComponent(messageToCopy);
        window.open(url, "_blank", "noopener,noreferrer");
      };
    } else {
      resultText.textContent = "O briefing foi preparado neste navegador. Copie a mensagem e encaminhe pelo canal de contato da DPG.";
      copyButton.innerHTML = "Copiar mensagem <span aria-hidden='true'>⧉</span>";
      copyButton.onclick = copyMessage;
    }
    result.scrollIntoView({ behavior: "smooth", block: "nearest" });
  });
}