document
  .getElementById("toggle-streamlit")
  .addEventListener("click", function () {
    var container = document.getElementById("streamlit-container");
    var button = this;

    // Check if the iframe is not loaded and create it
    if (!container.querySelector("iframe")) {
      var iframe = document.createElement("iframe");
      iframe.id = "streamlit-iframe";
      iframe.src = "https://jjm-chatbot.streamlit.app/";
      container.appendChild(iframe);
    }

    // Toggle the height of the container with smooth transition
    if (container.style.height === "0px" || container.style.height === "") {
      container.style.height = "80vh"; // Adjust the height as needed
      button.textContent = "Close Chatbot";
      container.style.transition = "height 0.5s fade-in-out";

      // Scroll into view with smooth behavior
      container.scrollIntoView({ behavior: "smooth" });

      // Fade in the iframe
      setTimeout(function () {
        container.style.opacity = "1";
        container.style.transition = "opacity 0.5s ease-in-out";
      }, 500);
    } else {
      container.style.height = "0px";
      button.textContent = "Open Chatbot";
      container.style.transition = "height 0.5s ease-in-out";

      // Fade out the iframe
      container.style.opacity = "0";
      container.style.transition = "opacity 0.5s ease-in-out";
    }
  });

// Add scroll effect to the document
window.addEventListener("scroll", function () {
  var header = document.querySelector("header");
  var toggleButton = document.getElementById("toggle-streamlit");

  // Add shadow to the header on scroll
  if (window.scrollY > 50) {
    header.style.boxShadow = "0 4px 10px rgba(0, 0, 0, 0.1)";
    header.style.transition = "box-shadow 0.3s ease-in-out";
  } else {
    header.style.boxShadow = "none";
  }

  // Add transition effect to the button
  if (window.scrollY > 100) {
    toggleButton.style.transform = "scale(1.1)";
    toggleButton.style.transition = "transform 0.3s ease-in-out";
  } else {
    toggleButton.style.transform = "scale(1)";
  }
});
