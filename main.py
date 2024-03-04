import mido
from js import document
from io import BytesIO
from time import sleep
import os
import asyncio

global file
file = None

document.getElementById("load").innerText = ""

def get_notes_and_durations(midi_file):
    notes = []
    with mido.MidiFile(midi_file) as mid:
        current_time = 0
        for msg in mid:
            current_time += msg.time
            if msg.type == "note_on":
                notes.append((msg.note, current_time))
            else:
                for i in range(len(notes) - 1, -1, -1):
                  try:
                      if notes[i][0] == msg.note:
                          notes[i] = (notes[i][0], notes[i][1], current_time - notes[i][1])
                          break
                  except AttributeError:
                    pass
    return notes

async def submit(_):
    try:
        global file
        file = await document.getElementById("myFile").files.item(0).arrayBuffer();file = BytesIO(file.to_bytes())
        if os.path.exists("data.midi"):
            os.remove("data.midi")
        with open("data.midi", "wb") as f:
            f.write(file.getbuffer())
        midi_file = "data.midi"
        notes_and_durations = [tuple([round(y,2) for y in x]) for x in get_notes_and_durations(midi_file)]
        document.getElementById("output").innerText = f"Output: {notes_and_durations}"
    except AttributeError:
        print("Input a file!")
        file = None
