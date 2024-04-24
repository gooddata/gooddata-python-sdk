$(document).ready(function () {
  const defaultError = document.querySelector(".default-404");
  const newError = document.querySelector(".old-version__404");
  const dropdownItems = document.querySelectorAll(".dropdown-item");
  const availableVersions = ["latest"];

  // put each available version into array availableVersions
  [...dropdownItems].forEach((item) => {
    if (item) {
      availableVersions.push(item.innerText.trim());
    }
  });

  if (window.location) {
    // pathname of the current page
    const pathname = window.location.pathname;

    // extract version from pathname
    const versionMatch = pathname.match(/\/(\d+\.\d+)\//);
    const version = versionMatch ? versionMatch[1] : null;
    
  // Check if the extracted version is a valid version, if it is included in available versions and if it matches the regex digit format
    if (version && !availableVersions.includes(version) && version.match(/^\d+\.\d+$/)) {
        newError.classList.toggle("d-none");
        defaultError.classList.toggle("d-none");
    }
  }

});
