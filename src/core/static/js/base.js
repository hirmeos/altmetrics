/* general js functions - used on multiple pages */

// Originally used to Style Django-generated forms with bootstrap classes
// - still a work in progress

let inputTags = document.getElementsByTagName("input");
let selectTags = document.getElementsByTagName("select");

let comboTags = Array.from(inputTags).concat(Array.from(selectTags));

let idArray = [];
comboTags.forEach(function(element){
  if (element.parentElement.tagName === "P") {
    idArray.push(element.id);
  }
});

function setFormClasses(formElement, divClass, elementClass, labelClass) {
  let pElement = formElement.parentElement;
  formElement.classList.add(elementClass);

  let formDiv = document.createElement('div');
  formDiv.classList.add(divClass);

  if (labelClass) {
    let labelElement = getInputLabel(formElement);
    labelElement.classList.add(labelClass);
  }

  formDiv.innerHTML = pElement.innerHTML;
  pElement.innerHTML = null;
  pElement.appendChild(formDiv);
}

function setFileClasses(formElement) {
  setFormClasses(formElement, "custom-file", "custom-file-input", "custom-file-label")
}

function setInputClasses(formElement) {
  setFormClasses(formElement, "form-group", "form-control")
}

function setCheckClasses(formElement) {
  setFormClasses(formElement, "form-check", "form-check-input position-relative", "form-check-label position-absolute")
}

idArray.forEach(function(elementID) {

  let formElement = document.getElementById(elementID);
  let elementType = formElement.getAttribute("type");
  if (elementType === "file") {
    setFileClasses(formElement);
  } else if (elementType === "checkbox") {
    setCheckClasses(formElement);
  } else {
    setInputClasses(formElement);
  }
});
