// the link to your model provided by Teachable Machine export panel
const URL = "/static/model/";

let model, webcam, labelContainer, maxPredictions, className;

// Load the image model and setup the webcam
async function init() {
    const modelURL = URL + "model.json";
    const metadataURL = URL + "metadata.json";

    // load the model and metadata
    // Refer to tmImage.loadFromFiles() in the API to support files from a file picker
    // or files from your local hard drive
    // Note: the pose library adds "tmImage" object to your window (window.tmImage)
    model = await tmImage.load(modelURL, metadataURL);
    maxPredictions = model.getTotalClasses();

    const constraints = {
        facingMode: "environment"
    };


    // Convenience function to setup a webcam
    const flip = false; // whether to flip the webcam
    webcam = new tmImage.Webcam(200, 200, flip); // width, height, flip
    await webcam.setup(constraints); // request access to the webcam
    await webcam.play();
    window.requestAnimationFrame(loop);

    // append elements to the DOM
    document.getElementById("webcam-container").appendChild(webcam.canvas);
    labelContainer = document.getElementById("label-container");
    className = document.getElementById("class-name");

    for (let i = 0; i < maxPredictions; i++) { // and class labels
        labelContainer.appendChild(document.createElement("div"));
    }

}

async function loop() {
    webcam.update(); // update the webcam frame
    await predict();
    window.requestAnimationFrame(loop);
}

// run the webcam image through the image model
async function predict() {
    let best_match = "None";

    // predict can take in an image, video or canvas html element
    const prediction = await model.predict(webcam.canvas);
    for (let i = 0; i < maxPredictions; i++) {
        const classPrediction =
            prediction[i].className + ": " + prediction[i].probability.toFixed(2);
        labelContainer.childNodes[i].innerHTML = classPrediction;
        if (prediction[i].probability.toFixed(2) > 0.95) {
            best_match = prediction[i].className;
        }
    }
    className.innerHTML = best_match;
    if (best_match != "None") {
        fetchPokemonDetails(best_match)
    }
}

function displayPokemon(pokemon) {
    document.getElementById("pokemon-name").innerText = pokemon.name;
    document.getElementById("pokemon-race").innerText = pokemon.race;
    document.getElementById("pokemon-forms").innerText = pokemon.type;
    document.getElementById("pokemon-decription").innerText = pokemon.decription;
}

async function fetchCardDetails(detectedName) {
    try {
        const response = await fetch('/get_pokemon_details', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ className: detectedName })
        });

        const result = await response.json();

        if (result.success) {
            displayPokemon(result.pokemon);
        }
    } catch (error) {
        console.error("Error fetching Pokemon details:", error);
    }
}