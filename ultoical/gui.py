import tempfile
import uuid

import gradio as gr
from ultoical.ul_handler import ULHandler
from datetime import datetime
from ultoical.ical_handler import ICalHandler
import zipfile

class ULToICALInterface:
  def login_with_token(self, token: str):
    self.handler.set_token(token)

  def get_timetables(self, start: float, end: float):
    timetables = self.handler.get_timetables(datetime.fromtimestamp(start), datetime.fromtimestamp(end))
    ret = []
    for timetabl in timetables["plannings"]:
        ret.append(timetabl["label"])
    return gr.CheckboxGroup(choices=ret)

  def makeical(self, timetables):
    files = []
    for timetable in self.handler.get_cached_timetable()["plannings"]:
      if timetable["label"] in timetables:
        files.append(ICalHandler(timetable["events"]).make_ical())
    if len(files) == 1:
      return gr.DownloadButton(value=files[0])
    else:
      file = tempfile.gettempdir() + "/" + str(uuid.uuid4()) + ".zip"
      _zip = zipfile.ZipFile(file, "w", zipfile.ZIP_DEFLATED)
      for file in files:
        _zip.write(file)
      _zip.close()
      return gr.DownloadButton(value=_zip.filename)

  def __init__(self):
    self.timetable = None
    self.handler = ULHandler()
    with gr.Blocks() as app:
      gr.Markdown("# ULToICAL")
      gr.Markdown("## Log into your account using token (More info [here](https://github.com/totorocodesoften/ultoical/readme.md))")  # TODO change URL
      with gr.Row(equal_height=True):
        self.token = gr.Textbox(label="Your token", value="")
        self.login_button = gr.Button("Login")
      self.login_button.click(fn=self.login_with_token, inputs=[self.token])
      gr.Markdown("## Choose dates")
      with gr.Row(equal_height=True) as self.period:
        with gr.Column():
          self.start = gr.DateTime(label="Start of the period", include_time=False)
        with gr.Column():
            self.end = gr.DateTime(label="End of the period", include_time=False)
        self.get_timetables_button = gr.Button("Get timetables")
      gr.Markdown("## Timetables")
      self.timetable = gr.CheckboxGroup(label="Timetable", info="If none are there the connection failed")
      self.get_timetables_button.click(fn=self.get_timetables, inputs=[self.start, self.end], outputs=[self.timetable])
      gr.Markdown("## Download")
      dwnbtn = gr.DownloadButton()
      self.timetable.input(fn=self.makeical, inputs=[self.timetable], outputs=[dwnbtn])
    app.launch()
