# notes/views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Note
from .forms import NoteForm

# View to list all notes
def note_list(request):
    notes = Note.objects.all()
    return render(request, 'notes/note_list.html', {'notes': notes})

# View to create a new note
def note_create(request):
    if request.method == 'POST':#this means that the user has submitted the form
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('note_list')
    else:#this means that the user is trying to access the form page
        form = NoteForm()
    return render(request, 'notes/note_form.html', {'form': form})

# View to update an existing note
def note_update(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('note_list')
    else:
        form = NoteForm(instance=note)
    return render(request, 'notes/note_form.html', {'form': form})

# View to delete a note
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':#this means that the user has confirmed the deletion
        note.delete()#this deletes the note
        return redirect('note_list')#this redirects the user to the note list page
    return render(request, 'notes/note_confirm_delete.html', {'note': note})#this returns the note_confirm_delete.html template with the note object
