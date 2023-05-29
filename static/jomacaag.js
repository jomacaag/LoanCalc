const home = document.querySelectorAll('.nav-home');
const history = document.querySelectorAll('.nav-history');
const login = document.querySelectorAll('.nav-login');
const logout = document.querySelectorAll('.nav-logout');
const linkedin = document.querySelectorAll('.nav-linkedin');
const github = document.querySelectorAll('.nav-github');

home.forEach((element) => {
  element.setAttribute('href', '/');
});

history.forEach((element) => {
  element.setAttribute('href', '/history');
});

login.forEach((element) => {
  element.setAttribute('href', '/login');
});

logout.forEach((element) => {
  console.log()
  element.setAttribute('href', '/logout');
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