const options = document.querySelectorAll('.option');
options.forEach(element => {
    element.addEventListener('click', function handleClick(event) {
        const buttonClicked = event.target.id;
        async function postData(url = "", data = {}) {
            const response = await fetch(url, {
              method: "POST",
              headers: {
                "Content-Type": "application/json"
              },
              body: JSON.stringify(data)
            });
            return response.json();
          }
          
          postData("/start", {buttonClicked})
            .then((data) => {
              console.log(data);
            });
      element.setAttribute('style', 'background-color: yellow;');
    });
  });
