const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
const tooltipList = [...tooltipTriggerList].map(
  (tooltipTriggerEl) => new bootstrap.Tooltip(tooltipTriggerEl)
);

document.addEventListener("DOMContentLoaded", () => {
  // Cargar el tema almacenado en localStorage al cargar la página
  const savedTheme = localStorage.getItem("theme") || "light"; // Obtener el tema guardado, o usar 'light' por defecto
  html_container.setAttribute("data-bs-theme", savedTheme); // Establecer el tema en el contenedor HTML

  // Actualizar el ícono del botón según el tema cargado
  if (savedTheme === "dark") {
    btn_theme.children[0].classList.add("bi-moon");
    btn_theme.children[0].classList.remove("bi-sun");
  } else {
    btn_theme.children[0].classList.add("bi-sun");
    btn_theme.children[0].classList.remove("bi-moon");
  }
});

const btn_theme = document.getElementById("btn-theme");
const html_container = document.documentElement;

btn_theme.addEventListener("click", () => {
  // Alternar entre los íconos de sol y luna
  btn_theme.children[0].classList.toggle("bi-sun");
  btn_theme.children[0].classList.toggle("bi-moon");

  // Alternar el tema entre 'light' y 'dark'
  const currentTheme = html_container.getAttribute("data-bs-theme");
  const newTheme = currentTheme === "light" ? "dark" : "light";
  html_container.setAttribute("data-bs-theme", newTheme);

  // Guardar el tema seleccionado en localStorage
  localStorage.setItem("theme", newTheme);
});

// Animar numeros
function animateNumber(targetElement, start, end, duration){
  let startTime = null;

  function step(timestamp){
    if (!startTime) startTime = timestamp;
    const progress = Math.min((timestamp - startTime) / duration, 1);
    const currentValue = Math.floor(start + progress * (end - start))
    targetElement.textContent = currentValue;
    if(progress < 1){
      requestAnimationFrame(step);
    }
  }
  requestAnimationFrame(step);
}

const counters = document.querySelectorAll('.counter-frame');

counters.forEach(counter => {
  const targetNumber = parseInt(counter.textContent, 10);
  if(!isNaN(targetNumber)){
    animateNumber(counter, 0, targetNumber, 1500);
  }
  else{
    console.error("El contenido el div no es un numero valido:" , counter.textContent)
  }
})