from django.http import HttpResponse, Http404
from django.urls import reverse
from .models import notes
from django.shortcuts import redirect


def home(request):
    sections_url = reverse('notes:sections')
    first_note_url = reverse('notes:note_by_number', args=[1])

    html = f"""
        <h1>Welcome to my course notes!</h1>
        <p>
            <a href="{sections_url}">Check the list of sections</a> |
            <a href="{first_note_url}">Read my first note</a>
        </p>
    """
    return HttpResponse(html)


def section_list_item(name):
    url = reverse('notes:section_notes', args=[name])
    return f'<li><a href="{url}">{name}</a></li>'


def sections_list(request):
    sections = set(note["section"] for note in notes)
    list_html = ''.join(section_list_item(section) for section in sections)
    back_home = reverse('notes:home')

    html = f"""
        <h1>Browse my notes by section</h1>
        <ul>
            {list_html}
        </ul>
        <a href="{back_home}">Back to home</a>
    """
    return HttpResponse(html)


def section_notes(request, section_name):
    filtered_notes = [note for note in notes if note["section"] == section_name]
    notes_html = ''.join(f'<li>{note["text"]}</li>' for note in filtered_notes)

    back_to_sections = reverse('notes:sections')
    html = f"""
        <h1>Notes about {section_name}</h1>
        <ul>
            {notes_html}
        </ul>
        <a href="{back_to_sections}">Back to sections</a>
    """
    return HttpResponse(html)


def search_notes(request, search_term):
    if search_term.isnumeric():
        return HttpResponse("Invalid search term. Please enter a non-numeric string.")

    matching_notes = [note for note in notes if search_term.lower() in note["text"].lower()]

    if not matching_notes:
        return HttpResponse(f"No notes found for '{search_term}'.")

    notes_html = ''.join(f'<li>{note["text"]} (Section: {note["section"]})</li>' for note in matching_notes)
    back_to_sections = reverse('notes:sections')

    html = f"""
        <h1>Notes matching {search_term}</h1>
        <ul>
            {notes_html}
        </ul>
        <a href="{back_to_sections}">Back to sections</a>
    """
    return HttpResponse(html)


def note_by_number(request, note_id):
    if note_id < 1 or note_id > len(notes):
        raise Http404("Note not found")

    note = notes[note_id - 1]
    section = note["section"]
    text = note["text"]

    prev_link = "previous note"
    next_link = "next note"

    if note_id > 1:
        prev_url = reverse('notes:note_by_number', args=[note_id - 1])
        prev_link = f'<a href="{prev_url}">previous note</a>'

    if note_id < len(notes):
        next_url = reverse('notes:note_by_number', args=[note_id + 1])
        next_link = f'<a href="{next_url}">next note</a>'

    home_url = reverse('notes:home')
    home_link = f'<a href="{home_url}">Back to home</a>'

    html = f"""
        <h1>Note number {note_id}</h1>
        <h2>{section}</h2>
        <p>{text}</p>
        <p>{prev_link} | {home_link} | {next_link}</p>
    """
    return HttpResponse(html)


def legacy_note_redirect(request, legacy_id):
    return redirect(reverse('notes:note_by_number', args=[legacy_id]))
