"""Builds the hunter's toolkit page:  python3 _tools/build_toolkit.py"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).parent)); from pages import page
gens=''.join(f'<option value="{i}">{l}</option>' for i,l in [(0,'the ancestor'),(1,'a child'),(2,'a grandchild'),(3,'a great-grandchild'),(4,'a 2× great-grandchild'),(5,'a 3× great-grandchild'),(6,'a 4× great-grandchild'),(7,'a 5× great-grandchild'),(8,'a 6× great-grandchild')])
body=f'''    <p class="crumb"><a href="/">← Project Scroll</a></p>
    <p class="kicker">The hunter’s toolkit</p>
    <h1>Tools for reading the record</h1>
    <p class="lede" style="font-size:1.15rem">Four small tools we use at the desk every day, and a cipher wheel for the hunt. They run entirely in your browser: nothing you type or load here is sent anywhere.</p>
    <nav class="toc" aria-label="Tools"><a href="#ink">Faded-ink enhancer</a><a href="#age">Age at death → birth date</a><a href="#soundex">Soundex finder</a><a href="#cousin">Cousin calculator</a><a href="/guide/old-handwriting/">Reading the old hand ›</a><a href="/guide/gravestones/">Reading gravestones ›</a></nav>

    <section class="tool" id="ink">
      <h2>Faded-ink enhancer</h2>
      <p>Load a photo of an old letter, deed, certificate or page. Slide until the writing stands out, then save the clearer copy. Your photo never leaves your device.</p>
      <p><label class="btn" for="inkfile">Choose a photo</label><input type="file" id="inkfile" accept="image/*" class="sr"> <span class="note" id="inkname">No photo chosen.</span></p>
      <div class="inkui" id="inkui" hidden>
        <div class="sliders">
          <label>Brightness <input type="range" id="kB" min="-100" max="100" value="0"></label>
          <label>Contrast <input type="range" id="kC" min="-50" max="150" value="0"></label>
          <label>Lift faded ink <input type="range" id="kL" min="0" max="100" value="0"></label>
          <label>Sharpen <input type="range" id="kS" min="0" max="100" value="0"></label>
          <label class="chk"><input type="checkbox" id="kG"> Black and white</label>
          <label class="chk"><input type="checkbox" id="kI"> Invert (light writing on dark)</label>
          <p class="inkbtns"><button type="button" class="btn" id="kRot">Rotate ↻</button><button type="button" class="btn" id="kReset">Reset</button><button type="button" class="btn primary" id="kSave">Save the clearer copy</button></p>
        </div>
        <canvas id="inkc" role="img" aria-label="Your enhanced photo"></canvas>
      </div>
    </section>

    <section class="tool" id="age">
      <h2>Age at death → birth date</h2>
      <p>Old certificates and gravestones often give age to the day: “aged 71 years, 4 months, 12 days.” Count back from the date of death and you have a birth date to test against everything else.</p>
      <div class="formrow">
        <label>Date of death <input type="date" id="aD" value="1912-03-15"></label>
        <label>Years <input type="number" id="aY" min="0" max="130" value="71"></label>
        <label>Months <input type="number" id="aM" min="0" max="11" value="4"></label>
        <label>Days <input type="number" id="aDd" min="0" max="31" value="12"></label>
      </div>
      <p class="result" id="aOut" aria-live="polite"></p>
      <p class="note">Remember: the informant gave that age, so it is a clue to test, not a proof. Stones carved years later can be off too.</p>
    </section>

    <section class="tool" id="soundex">
      <h2>Soundex finder</h2>
      <p>The indexes to the 1880 to 1930 censuses, made in the 1930s and 1940s, were filed by Soundex, a code that groups surnames that sound alike. Type a surname to get its code and spellings worth searching.</p>
      <div class="formrow"><label>Surname <input type="text" id="sx" value="Ashcraft" autocomplete="off"></label></div>
      <p class="result" id="sxOut" aria-live="polite"></p>
    </section>

    <section class="tool" id="cousin">
      <h2>Cousin calculator</h2>
      <p>Start from the ancestor two people share. Say how each one descends from that ancestor, and the calculator names the relationship.</p>
      <div class="formrow">
        <label>Person A is <select id="cA">{gens}</select></label>
        <label>Person B is <select id="cB">{gens}</select></label>
      </div>
      <p class="result" id="cOut" aria-live="polite"></p>
      <p class="note">“Removed” counts the generations between two cousins: your parent’s first cousin is your first cousin once removed.</p>
    </section>
    <section class="tool" id="cipher">
      <h2>Cipher wheel</h2>
      <p>The simplest secret writing of all: every letter slides the same number of places along the alphabet. Turn the wheel until the line makes sense. Somewhere on this site, a line is waiting for it.</p>
      <div class="formrow">
        <label class="wide-in">Coded line <input type="text" id="cyIn" value="LCLYF JSBL PZ AYBL" autocomplete="off" spellcheck="false"></label>
        <label>Turn the wheel <input type="range" id="cyK" min="0" max="25" value="0"></label>
        <label class="chk"><input type="checkbox" id="cyM"> Hold it to a mirror (A is Z, B is Y)</label>
      </div>
      <p class="result cyout" id="cyOut" aria-live="polite"></p>
      <p class="note">Try the sample above: it reads plainly at one turn of the wheel: seven. Old soldiers, lodges and lovers all used ciphers like this one, and so does the hunt.</p>
    </section>
    <script src="/toolkit/toolkit.js?v=3" defer></script>
'''
page('toolkit/index.html','The hunter’s toolkit · Project Scroll','Free tools for reading old records: a faded-ink enhancer, an age-at-death calculator, a Soundex finder, a cousin calculator and a cipher wheel. Everything runs in your browser.',body, og='https://projectscroll.com/og/toolkit.jpg')
print('toolkit built')
