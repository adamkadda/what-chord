const selected = new Map();

const std = new Map();

const notes = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B'];
const octaves = ['2', '3', '4'];

for (const note of notes) {
  for (const octave of octaves) {
    const originalNote = note + octave;
    std.set(originalNote, note);
  }
}

const keys = document.querySelectorAll('.key')

keys.forEach(key => {
    key.addEventListener('click', () => {
        playNote(key);
        storeNote(key);
    });
});


function playNote(key) {
    const noteAudio = document.getElementById(key.dataset.note).cloneNode()
    noteAudio.currentTime = 0
    noteAudio.play()
}


function storeNote(key) {

    const note = key.dataset.note;

    // Check if note exists in map
    if (selected.has(note)) {
        selected.delete(note);
        key.classList.remove('active')
    // If 
    } else {
        selected.set(note, 1);
        key.classList.add('active')
    }
}


const searchButton = document.getElementById("search");

searchButton.addEventListener("click", () => submitNotes());

const result_url = 'http://127.0.0.1:5000/';

function submitNotes() {
    // check if user selected at least three notes
    if (selected.size < 3) {
        console.log('size < 3');

    } else {

        // standardize notes
        let notes = [];
        for (const [key, value] of selected) {
            let note = std.get(key);

            // TODO: handle (note == undefined)

            notes.push(note);
        }
        
        // prepare JSON data
        let data = {
            "notes": notes,
        }

        // make a request with fetch
        fetch(result_url, {
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "body": JSON.stringify(data),
        })
        .then(response => response.text())
        .then(htmlContent => {
            document.getElementById("results").innerHTML = htmlContent;
        })
        .catch(error => {
            console.error('Error: ', error);
        })

    }
}