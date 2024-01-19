switchLang = () => {
  let selectElement = document.getElementById('switchLangSelect');
  let selectedValue = selectElement.value;
  window.location.href = window.location.origin + window.location.pathname + '?lang=' + selectedValue;
}