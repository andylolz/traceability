**Click to drag; scroll to zoom.** Red links are downstream; black links are upstream.

[Link to full screen demo](https://bl.ocks.org/andylolz/raw/34dbc9e1d3ae04c5a331af1f978849f2/)

Some initial takehomes:

 * You can see "clouds" of black arrows around the funders who obligate their recipients to publish IATI data: DFID; Dutch MFA (`minbuza_nl`); Belgian MFA (`be_dgd`).
 * It looks like some big consultancies publish links to their implementers – see the clouds of red arrows around Crown Agents and MannionDaniels
 * There are more black (upstream) links than red (downstream) links. That’s to be expected – IATI "STRONGLY RECOMMENDS" publishing upstream links, but downstream links are recorded "if possible"
 * The graph is incomplete! Lots of big funders are missing completely, and it’s likely that most of their implementers don’t publish IATI data at all.

---

Data used, and the code to generate it from IATI [is available in this gist](https://gist.github.com/andylolz/34dbc9e1d3ae04c5a331af1f978849f2).

Implemented in [D3.js](http://d3js.org/).

Forked from [Mike Bostock’s gist](https://gist.github.com/mbostock/1153292).
