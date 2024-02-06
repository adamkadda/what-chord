# what-chord

#### Video Demo: https://youtu.be/G5jOgf9mjTw

#### Description:

This project is comprised of three main parts, the python code that names a chord, the python backend, and the html, css, and javascript frontend. The majority of time on this project was in making the python code for naming chords; roughly half of the total time I spent was on that part of this project.

Before starting the project I had prepared the following checkpoints:

1. Write a function that names a chord
	1. Understand how chords are named
	2. Identify edge cases
	3. Formalize this process
2. Create a simple working backend
	1. Decide on routes
	2. Decide whether a database is necessary
3. Make a simple frontend
	1. Make a *working* piano
	2. Display results

I named the chord naming python file `what-chord.py`. This is the pseudocode for the `what_chord()` function is as follows:

```
clean notes
	remove duplicates
	check for invalid notes

prepare inversions
	use itertools.permutations
	convert letter note (C) to integer notation (0)

for each inversion:
	check for invalid inversion
	obtain chord infomation (dictionary)
		initialize chord attributes
		prepare name segments
		match case for each interval
			0: unison
			1 - 5: third/sus
			6: sus/add #4 || dim 5
			7: min/major triad completion
			8: aug triad || add b6
			9: X6 || dim 7 || add 6
			10 or 11: 7th chord completion
			13 . . . 21: extended chords
		calculate chord name conciseness
			sum length of final name segments
		prepare dictionary
			name, root, conciseness, inversion
	append chord information into list of chords
```

The most complicated part of the chord naming function is definitely the part that does the actual naming. From my understanding that chords are built conceptually upwards (from the third and so forth), assessing each interval from lowest and so forth, and checking whether specific edge cases have been met, seemed to be the most straightforward solution in my opinion. 

I considered a table lookup based solution, but that required me to create a table that contained all *correct* names for every possible inversion given a set of notes. I decided to continue with the iterative approach. Upon naming the chord, the sum of the name segment lengths are taken as the conciseness score. A lot can be improved with this metric of naming 'goodness', but for now I believe it is a step forward in the right direction.

Finally, a list of dictionaries are returned, containing the chord's name, root, conciseness score, and a tuple containing its base inversion.

The backend is really simple. This is the pseudocode:

```
if POST:
	receive json
	store notes from json
	generate key
		clean notes
		convert notes to integer notation
		sort notes
		stringify into `chord_x_y_z` format
	establisth db connection
	if {key} table NOT exists in db:
		create {key} table
		insert what_chord() output into {key} table
		commit changes
	select names, sort by conciseness then root
	return render_template('results.html', res=names)

return render_template('index.html')
```

In essence, what the backend does is check for whether the inputted notes have been searched previously, since if they have been searched for previously the names must exist already under a unique table name in the database. The backend then responds to the POST request with some `html` that contains the resulting names, ordered by conciseness.

Finally, the frontend. I knew that all I needed for this web app was a single page with a *playable* keyboard, a search button, and a way to display results. Besides the look of the page, getting the keys to work in javascript was not too simple. Here's the pseudocode:

```
obtain keys by class
for each key {
	add event listener
		playNote()
		storeNote()
}

playNote(key) {
	noteAudio = corresponding note in dataset, then cloned
	play audio
}

storeNote(key) {
	if note exists in global map
		delete from map
		remove class 'active'
	else
		add to map
		add class 'active'
}

submitNotes() {
	check if map has at least 3 notes
	prepare json data
	make a request with fetch
	handle the response
		replace innerHTML content of my "results" div
	catch error, console.log('Error: ', error)
}
```

To make the note play upon clicking on them, an event listener is used to create a clone of the audio object that corresponds to the dataset object which is a `.wav` file. 

I prepared a 2 second `.wav` audio file for every note using a piano roll in a DAW, exporting each note as its own separate `.wav` file.

Right after playing the note, a separate function checks whether that note has already been included to a global map called `selected`. At that point, an aesthetic class called `active` is toggled to show whether a note has been pressed or not. 

Finally, the fetch API is used to send a `POST` request to the backend, but first checks whether 3 notes have been selected. Then the json data is prepared by iterating through the `selected` map, and is sent as request body.

Lastly, the response from the backend is handled by replacing the contents of the `results` div with the HTML response.

I had a lot of fun with this project, and I'm looking forward to making new projects, but also improving this chord naming web app in the future. 
