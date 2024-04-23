$(document).ready(function () {
  const defaultError = document.querySelector(".default-404");
  const newError = document.querySelector(".old-version__404");
  const dropdownItems = document.getElementsByClassName("dropdown-item");
  const availableVersions = ["latest"];

  // put each available version into array availableVersions
  [...dropdownItems].forEach((element) => {
    availableVersions.push(element.innerText.trim());
  });

  if (window.location) {
    // pathname of the current page
    const pathname = window.location.pathname;

    // extract version from pathname
    const version = pathname.split('/')[1];

  // Check if the version extracted is a valid version, if it is included in available versions and if it matches the regex digit format
    if (version && !availableVersions.includes(version) && version.match(/^\d+\.\d+$/)) {
        newError.classList.toggle("d-none");
        defaultError.classList.toggle("d-none");
    }
  }

});
