document
  .getElementById("toggle-streamlit")
  .addEventListener("click", function () {
    var container = document.getElementById("streamlit-container");
    if (container.style.height === "0px" || container.style.height === "") {
      if (!container.innerHTML) {
        var iframe = document.createElement("iframe");
        iframe.id = "streamlit-iframe";
        iframe.src = "https://jjm-chatbot.streamlit.app/";
        container.appendChild(iframe);
      }
      container.style.height = "80vh"; // Adjust the height as needed
      this.textContent = "Close Chatbot";
    } else {
      container.style.height = "0px";
      this.textContent = "Open Chatbot";
    }
  });
