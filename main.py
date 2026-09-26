import os
import datetime
import threading
import urllib.parse
import requests

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import platform

API_KEY = os.environ.get("OPENAI_API_KEY", "")
MODEL = "gpt-4o-mini"

KV = r"""
#:import dp kivy.metrics.dp

<NeonButton@Button>:
    background_normal: ''
    background_down: ''
    background_color: 0,0,0,0
    color: .35,.9,1,1
    bold: True
    font_size: '14sp'
    canvas.before:
        Color:
            rgba: .015,.07,.14,1
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(14)]
        Color:
            rgba: .05,.72,1,.95
        Line:
            rounded_rectangle: (self.x,self.y,self.width,self.height,dp(14))
            width: 1.2

<JarvisRoot>:
    orientation: 'vertical'
    padding: dp(16)
    spacing: dp(9)
    canvas.before:
        Color:
            rgba: .005,.012,.035,1
        Rectangle:
            pos: self.pos
            size: self.size
        Color:
            rgba: 0,.3,.8,.14
        Ellipse:
            size: dp(320),dp(320)
            pos: self.center_x-dp(160),self.center_y-dp(130)

    Label:
        text: '[b]J.A.R.V.I.S.[/b]'
        markup: True
        font_size: '30sp'
        color: .3,.85,1,1
        size_hint_y: None
        height: dp(43)

    Label:
        text: 'PERSONAL AI • ANDROID SYSTEM'
        font_size: '10sp'
        color: .22,.55,.78,1
        size_hint_y: None
        height: dp(18)

    FloatLayout:
        size_hint_y: None
        height: dp(225)
        Widget:
            canvas:
                Color:
                    rgba: 0,.45,.9,.13
                Ellipse:
                    size: dp(210),dp(210)
                    pos: self.center_x-dp(105),self.center_y-dp(105)
                Color:
                    rgba: .05,.78,1,.95
                Line:
                    circle: (self.center_x,self.center_y,dp(100))
                    width: 1.5
                Color:
                    rgba: .12,.48,1,.8
                Line:
                    circle: (self.center_x,self.center_y,dp(82))
                    width: 1
                Color:
                    rgba: .2,.8,1,.8
                Line:
                    circle: (self.center_x,self.center_y,dp(61))
                    width: 1
                Color:
                    rgba: .1,.6,1,.8
                Line:
                    points: [self.center_x-dp(120),self.center_y,self.center_x-dp(104),self.center_y,
                             self.center_x+dp(104),self.center_y,self.center_x+dp(120),self.center_y]
                    width: 1
                Line:
                    points: [self.center_x,self.center_y-dp(120),self.center_x,self.center_y-dp(104),
                             self.center_x,self.center_y+dp(104),self.center_x,self.center_y+dp(120)]
                    width: 1
        Label:
            text: '[b]◈[/b]'
            markup: True
            font_size: '76sp'
            color: .3,.85,1,1
            pos_hint: {'center_x':.5,'center_y':.5}

    Label:
        text: root.status
        font_size: '14sp'
        color: .45,.9,1,1
        size_hint_y: None
        height: dp(25)

    TextInput:
        id: user_input
        hint_text: 'Type or tap VOICE to speak...'
        multiline: False
        size_hint_y: None
        height: dp(48)
        background_normal: ''
        background_active: ''
        background_color: .02,.06,.12,1
        foreground_color: .85,.96,1,1
        hint_text_color: .25,.5,.65,1
        cursor_color: .2,.8,1,1
        padding: dp(12),dp(12)
        on_text_validate: root.send_text()

    GridLayout:
        cols: 2
        spacing: dp(8)
        size_hint_y: None
        height: dp(106)
        NeonButton:
            text: '🎙  VOICE'
            on_release: root.listen_voice()
        NeonButton:
            text: '✦  ASK AI'
            on_release: root.send_text()
        NeonButton:
            text: '⌕  YOUTUBE'
            on_release: root.open_site('https://www.youtube.com')
        NeonButton:
            text: '◎  GOOGLE'
            on_release: root.open_site('https://www.google.com')

    ScrollView:
        do_scroll_x: False
        bar_width: dp(4)
        Label:
            id: response
            text: root.reply
            markup: True
            color: .55,.85,1,1
            text_size: self.width,None
            size_hint_y: None
            height: self.texture_size[1]+dp(20)
            halign: 'left'
            valign: 'top'
            padding: dp(10),dp(10)

    Label:
        text: 'SECURE • VOICE • AI • WEB'
        font_size: '10sp'
        color: .15,.45,.65,1
        size_hint_y: None
        height: dp(20)
"""

class JarvisRoot(BoxLayout):
    status = StringProperty("SYSTEM READY")
    reply = StringProperty("Hello. I am JARVIS.\\nTap VOICE or type a message.")

    def open_site(self, url):
        try:
            if platform == "android":
                from jnius import autoclass
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                Intent = autoclass('android.content.Intent')
                Uri = autoclass('android.net.Uri')
                intent = Intent(Intent.ACTION_VIEW, Uri.parse(url))
                PythonActivity.mActivity.startActivity(intent)
            else:
                import webbrowser
                webbrowser.open(url)
            self.status = "OPENING"
        except Exception as e:
            self.reply = "Could not open website: " + str(e)

    def send_text(self):
        question = self.ids.user_input.text.strip()
        if not question:
            return
        self.ids.user_input.text = ""
        self.reply = "[b]YOU:[/b] " + question + "\\n\\nJARVIS is thinking..."
        self.status = "PROCESSING"
        threading.Thread(target=self._handle, args=(question,), daemon=True).start()

    def _handle(self, question):
        q = question.lower()
        if "time" in q or "samay" in q:
            answer = "Sir, abhi " + datetime.datetime.now().strftime("%I:%M %p") + " hai."
        elif "date" in q or "tareekh" in q:
            answer = "Aaj ki tareekh " + datetime.datetime.now().strftime("%d %B %Y") + " hai."
        elif "youtube" in q:
            Clock.schedule_once(lambda dt: self.open_site("https://www.youtube.com"))
            answer = "YouTube khol raha hoon."
        elif "google" in q:
            Clock.schedule_once(lambda dt: self.open_site("https://www.google.com"))
            answer = "Google khol raha hoon."
        elif API_KEY:
            answer = self.ask_ai(question)
        else:
            answer = "Basic commands ready hain. AI chat enable karne ke liye private backend/API configuration chahiye."
        Clock.schedule_once(lambda dt: self._show(question, answer))

    def ask_ai(self, question):
        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": "Bearer " + API_KEY,
                         "Content-Type": "application/json"},
                json={
                    "model": MODEL,
                    "messages": [
                        {"role": "system", "content":
                         "You are JARVIS, a concise helpful assistant. Reply in Hindi/Hinglish when appropriate. Never claim you control phone features unless you actually did."},
                        {"role": "user", "content": question}
                    ],
                    "max_tokens": 350
                },
                timeout=45
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"].strip()
        except Exception as e:
            return "AI request failed. Check internet/API billing/key. " + str(e)

    def _show(self, question, answer):
        self.status = "SYSTEM READY"
        self.reply = "[b]YOU:[/b] " + question + "\\n\\n[b]JARVIS:[/b] " + answer
        self.speak(answer)

    def listen_voice(self):
        if platform != "android":
            self.reply = "Voice input is available in the Android APK build."
            return
        try:
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Intent = autoclass('android.content.Intent')
            RecognizerIntent = autoclass('android.speech.RecognizerIntent')
            intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH)
            intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL,
                           RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
            intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE, "hi-IN")
            intent.putExtra(RecognizerIntent.EXTRA_PROMPT, "Speak to JARVIS")
            self.status = "LISTENING..."
            # Use Android speech recognizer through a native activity intent.
            # A production app should implement an ActivityResult callback/plugin.
            PythonActivity.mActivity.startActivityForResult(intent, 731)
            self.reply = "Android speech prompt opened. If recognized text does not return automatically, type it in the input field. Full callback bridge requires a small native Java/Kotlin activity plugin."
        except Exception as e:
            self.status = "VOICE UNAVAILABLE"
            self.reply = "Could not launch Android speech recognizer: " + str(e)

    def speak(self, text):
        if platform != "android":
            return
        try:
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Intent = autoclass('android.content.Intent')
            intent = Intent("android.intent.action.TTS_SERVICE")
            # Android intent TTS service isn't directly callable as spoken output;
            # keep app honest and use a native plugin for full TTS integration.
            self.status = "RESPONSE READY"
        except Exception:
            pass

class JarvisApp(App):
    def build(self):
        Window.clearcolor = (.005,.012,.035,1)
        Builder.load_string(KV)
        return JarvisRoot()

if __name__ == "__main__":
    JarvisApp().run()
