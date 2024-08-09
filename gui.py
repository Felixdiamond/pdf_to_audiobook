import PySimpleGUI as sg
import os
from pdf_to_audiobook import pdf_to_audiobook

# Set the theme for a dark color scheme
sg.theme('DarkGrey13')

def create_window():
    layout = [
        [sg.Text('PDF to Audiobook Converter', font=('Helvetica', 20), justification='center', expand_x=True)],
        [sg.Text('Select PDF File:', font=('Helvetica', 12)), 
         sg.Input(key='-PDF-', enable_events=True), 
         sg.FileBrowse(file_types=(("PDF Files", "*.pdf"),))],
        [sg.Text('Output File:', font=('Helvetica', 12)), 
         sg.Input(key='-OUTPUT-', enable_events=True), 
         sg.SaveAs(file_types=(("MP3 Files", "*.mp3"),))],
        [sg.Text('Language:', font=('Helvetica', 12)), 
         sg.Combo(['English', 'Spanish', 'French', 'German', 'Italian', 'Portuguese', 'Chinese', 'Japanese'], 
                  default_value='English', key='-LANG-', font=('Helvetica', 10))],
        [sg.Text('Chunk Size:', font=('Helvetica', 12)), 
         sg.Slider(range=(100, 1000), default_value=500, orientation='h', size=(20, 15), key='-CHUNK-')],
        [sg.Text('Max Decoder Steps:', font=('Helvetica', 12)), 
         sg.Slider(range=(10000, 2000000), default_value=1000000, orientation='h', size=(20, 15), key='-DECODER-')],
        [sg.Button('Convert', font=('Helvetica', 12), button_color=('white', '#007acc')), 
         sg.Button('Exit', font=('Helvetica', 12), button_color=('white', '#cc0000'))],
        [sg.ProgressBar(100, orientation='h', size=(20, 20), key='-PROGRESS-', visible=False)],
        [sg.Multiline(size=(60, 10), key='-OUTPUT-', autoscroll=True, reroute_stdout=True, 
                      reroute_stderr=True, visible=False)]
    ]

    return sg.Window('PDF to Audiobook', layout, finalize=True, resizable=True)

def run_gui():
    window = create_window()

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Exit':
            break

        if event == 'Convert':
            pdf_path = values['-PDF-']
            output_path = values['-OUTPUT-']
            lang = values['-LANG-'].lower()[:2]  # Convert to two-letter code
            chunk_size = int(values['-CHUNK-'])
            max_decoder_steps = int(values['-DECODER-'])

            if not pdf_path or not output_path:
                sg.popup_error('Please select both input PDF and output MP3 file.')
                continue

            window['-PROGRESS-'].update(visible=True)
            window['-OUTPUT-'].update(visible=True)
            window.refresh()

            try:
                pdf_to_audiobook(pdf_path, output_path, lang, chunk_size, max_decoder_steps)
                sg.popup('Conversion Complete!', 'Your audiobook has been created successfully.')
            except Exception as e:
                sg.popup_error(f'An error occurred: {str(e)}')

            window['-PROGRESS-'].update(visible=False)

    window.close()

if __name__ == '__main__':
    run_gui()