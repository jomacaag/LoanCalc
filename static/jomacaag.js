const home = document.querySelectorAll('.nav-home');
const about = document.querySelectorAll('.nav-about');
const projects = document.querySelectorAll('.nav-projects');
const contact = document.querySelectorAll('.nav-contact');
const linkedin = document.querySelectorAll('.nav-linkedin');
const github = document.querySelectorAll('.nav-github');

home.forEach((element) => {
  element.setAttribute('href', '/');
});

about.forEach((element) => {
  element.setAttribute('href', '/about');
});

projects.forEach((element) => {
  element.setAttribute('href', '/projects');
});

contact.forEach((element) => {
  console.log()
  element.setAttribute('href', '/contact');
});

github.forEach((element) => {
  console.log()
  element.setAttribute('href', 'https://github.com/jomacaag');
  element.setAttribute('target', '_blank');
});

linkedin.forEach((element) => {
  console.log()
  element.setAttribute('href', 'https://www.linkedin.com/in/jonathan-castro-aguilar-aa3372107/');
  element.setAttribute('target', '_blank');
});

