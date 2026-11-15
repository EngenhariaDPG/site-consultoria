/* Configure com o número em formato internacional, sem espaços ou símbolos.
   Exemplo: 5532999999999. Deixe vazio para apenas preparar/copiar a mensagem. */
const WHATSAPP_NUMBER = "";

document.documentElement.classList.add("js-ready");

const menuButton = document.querySelector(".menu-toggle");
const navigation = document.querySelector(".nav");

function closeMenu() {
  if (!menuButton || !navigation) return;
  menuButton.setAttribute("aria-expanded", "false");
  menuButton.setAttribute("aria-label", "Abrir menu");
  navigation.classList.remove("is-open");
  document.body.classList.remove("menu-open");
}

if (menuButton && navigation) {
  menuButton.addEventListener("click", function () {
    const isOpen = menuButton.getAttribute("aria-expanded") === "true";
    menuButton.setAttribute("aria-expanded", String(!isOpen));
    menuButton.setAttribute("aria-label", isOpen ? "Abrir menu" : "Fechar menu");
    navigation.classList.toggle("is-open", !isOpen);
    document.body.classList.toggle("menu-open", !isOpen);
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
  }, { threshold: 0.12, rootMargin: "0px 0px -35px 0px" });

  revealItems.forEach(function (item) { observer.observe(item); });
} else {
  revealItems.forEach(function (item) { item.classList.add("is-visible"); });
}

const year = document.getElementById("current-year");
if (year) year.textContent = String(new Date().getFullYear());

const form = document.getElementById("lead-form");
const result = document.getElementById("form-result");
const resultText = document.getElementById("form-result-text");
const copyButton = document.getElementById("copy-message");
let preparedMessage = "";

function getFormMessage(data) {
  return [
    "Olá! Gostaria de conversar sobre um serviço de engenharia mecânica.",
    "",
    "Nome: " + data.get("nome"),
    "Empresa: " + (data.get("empresa") || "Não informada"),
    "Cidade/Estado: " + data.get("cidade"),
    "Serviço de interesse: " + data.get("servico"),
    "",
    "Descrição da necessidade:",
    data.get("mensagem"),
    "",
    "Enviado pelo site Denys Pinto | Engenharia Mecânica."
  ].join("\n");
}

async function copyPreparedMessage() {
  if (!preparedMessage) return false;
  try {
    await navigator.clipboard.writeText(preparedMessage);
    copyButton.innerHTML = "Mensagem copiada <span aria-hidden='true'>✓</span>";
    return true;
  } catch (error) {
    const helper = document.createElement("textarea");
    helper.value = preparedMessage;
    helper.setAttribute("readonly", "");
    helper.style.position = "fixed";
    helper.style.opacity = "0";
    document.body.appendChild(helper);
    helper.select();
    const copied = document.execCommand("copy");
    helper.remove();
    copyButton.innerHTML = copied ? "Mensagem copiada <span aria-hidden='true'>✓</span>" : "Selecione e copie a mensagem";
    return copied;
  }
}

if (form) {
  form.addEventListener("submit", async function (event) {
    event.preventDefault();
    if (!form.reportValidity()) return;

    const data = new FormData(form);
    preparedMessage = getFormMessage(data);
    result.hidden = false;

    if (WHATSAPP_NUMBER.trim()) {
      const url = "https://wa.me/" + WHATSAPP_NUMBER.trim() + "?text=" + encodeURIComponent(preparedMessage);
      resultText.textContent = "Seu briefing está pronto. Use o botão abaixo para copiar ou abra a conversa pelo WhatsApp.";
      copyButton.innerHTML = "Abrir WhatsApp <span aria-hidden='true'>↗</span>";
      copyButton.onclick = function () { window.open(url, "_blank", "noopener,noreferrer"); };
    } else {
      resultText.textContent = "O briefing foi montado. Copie a mensagem e encaminhe pelo seu canal de contato. O WhatsApp pode ser configurado no arquivo script.js.";
      copyButton.innerHTML = "Copiar mensagem <span aria-hidden='true'>⧉</span>";
      copyButton.onclick = copyPreparedMessage;
      await copyPreparedMessage();
    }

    result.scrollIntoView({ behavior: "smooth", block: "nearest" });
  });
}

if (copyButton && !copyButton.onclick) {
  copyButton.addEventListener("click", copyPreparedMessage);
}
