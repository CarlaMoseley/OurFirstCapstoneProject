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

            // Assuming your server responds with JSON data
            return response.json();
        }

        postData("/process_option", { buttonClicked })
            .then((data) => {
                console.log(data);
                // Add logic to handle the response, e.g., redirect or update UI
            });

        element.setAttribute('style', 'background-color: yellow;');
    });
});
