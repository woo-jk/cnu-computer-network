async function fetchRequestWithError() {
  try {
    const url = `http://localhost:8080/pastebin/api/pastes/`;
    const response = await fetch(url);
    if (response.status >= 200 && response.status < 400) {
      const data = await response.json();
      pdiv = document.getElementById("notes");

      while (pdiv.firstChild) {
        pdiv.removeChild(pdiv.firstChild);
      }

      const skipNumber = data.length - 10;
      for (var key in data) {
        if (Number(data[key]["id"]) > skipNumber) {
          ndiv = document.createElement("div");
          ndiv.innerHTML = `<h3> ${data[key]["title"]} </h3><p> ${data[key]["content"]}</p><hr>`;

          pdiv.prepend(ndiv);
        }
      }
    } else {
      console.log(`${response.statusText}: ${response.status} error`);
    }
  } catch (error) {
    console.log(error);
  }
}

fetchint = setInterval(fetchRequestWithError, 10 * 1000);
