---
name: cloud-architecture-diagram
description: >-
  Draw a cloud architecture diagram in the Google Cloud reference style as one
  self-contained, interactive HTML page — Google Cloud product icons, tinted
  environment groups, actors outside the cloud boundary, a numbered request
  path, hover explanations, and an optional step-by-step slideshow. Use
  whenever someone asks for an architecture diagram, a system drawing, a
  "desenho de arquitetura", a component map, or a page that explains how a
  deployed system works. Trigger even without those words, for example "show
  me how this app is wired", "draw the GCP components", "diagrama dos
  serviços", or when a reference-architecture image is shared as the target.
---

# Cloud architecture diagram

You draw deployed systems the way a cloud vendor's reference architecture
draws them, and you ship the drawing as one HTML file that a person can open,
hover and step through.

This is not a flowchart skill and not a whiteboard skill. Mermaid, Graphviz
and box-and-line sketches are the wrong output here: they place nodes for you,
and automatic placement is exactly what makes a diagram look generated. You
place every box yourself, and you verify the result by measuring it.

## What you produce

One `.html` file. No build step, no imports, no runtime dependency beyond a
font stylesheet. A venue network, an air-gapped laptop and an email attachment
all have to render it, so everything is inline.

Inside that file, three things stay separate:

| Part | Holds |
| :--- | :--- |
| `ICONS` | Product icons, each normalised to `{vb, d}`. |
| Diagram data | Every box, group, connector and step, with absolute coordinates and the prose. |
| Renderer | The code that turns the data into SVG. Never carries content. |

Keep them separate even inside a single file. The data is what people edit;
the renderer is what people never touch.

## The drawing's grammar

Follow the vendor grammar, because readers already know how to read it:

1. **A cloud boundary.** A thin rounded rectangle with the provider's logo and
   the region, containing everything that runs in the cloud.
2. **Actors outside it.** People, devices, printers, third-party consumers.
   Plain boxes with a line-art glyph, never product icons.
3. **Tinted groups inside it.** One per environment or concern, each a soft
   fill with a matching border and a title in the top-left. A dashed border
   means "not part of the running system" — build pipelines, CI, registries.
4. **Product cards.** The product's own icon, the service name, and one line of
   configuration underneath in a monospace face.
5. **Orthogonal connectors.** Only horizontal and vertical segments, with an
   arrowhead on the target. Never curves, never diagonals.
6. **A numbered request path.** Filled discs carrying 1, 2, 3 … along the
   arrows that one request travels. Everything else is dashed and unnumbered.

Read `references/layout-rules.md` before you place the first coordinate. It
carries the geometry rules that are expensive to rediscover.

## One numbering system

A diagram may carry exactly one sequence of numbers. If the drawing numbers
its arrows 1 to 10 and a step list beside it numbers its entries 1 to 8, a
reader who counts one lands somewhere the other does not, and they stop
trusting both. Make the step list light the numbered arrows and show which
ones, or drop the numbers from one of them.

## Workflow

1. **Get the inventory.** Ask for, or read from the code, every component that
   will appear: the services, the datastores, the models, the actors. If you
   are reading a repository, take the configuration from the source — instance
   limits, timeouts, model ids, bucket lifecycle — because a diagram whose
   numbers are invented is worse than a diagram with no numbers.
2. **Find the one request.** Pick the single path a user's request travels,
   end to end. That path is the spine of the drawing and everything else is a
   side path. If you cannot name it in one sentence, you do not understand the
   system well enough to draw it yet.
3. **Fetch the icons.** Run `scripts/fetch-gcp-icons.sh` with the names you
   need, and read *Where the icons come from* below before you publish.
   Never hand-draw a product mark, and never substitute a generic glyph for a
   product that has an icon of its own.
4. **Place the boxes.** Columns, top to bottom, actors on the left. Read
   `references/layout-rules.md` for the lane discipline in the corridors
   between columns.
5. **Write the prose.** Every component gets a `title`, a one-line `sub`, and a
   `what` that says what it does in two sentences. A `why` that names the
   decision behind it is worth more than either, when you know it.
6. **Render and measure.** Open the page and run the audit from
   `references/layout-rules.md`. It reports text that escapes its own box,
   labels a card paints over, and marks that collide. An empty result is the
   passing result.
7. **Fix and re-measure.** Then, and only then, look at a screenshot.

## Step through it, when it is for an audience

If the drawing will be presented, projected, or put on a screen people walk
past, build it as a slideshow instead of a scrolling document. Each step
lights its own arrow, dims the rest of the drawing, and zooms the frame onto
what it lit. That zoom is what makes a dense diagram readable on a phone
without a second, stacked layout.

`references/slideshow.md` has the focus maths and the rules that keep it from
turning back into a document.

## Where the icons come from

`scripts/fetch-gcp-icons.sh` reads the Iconify `gcp` collection, which mirrors
Google Cloud's product icons behind a JSON API. Use it, because it is the only
route a script can take: Google distributes the set as a ZIP for people, and
`cloud.google.com/icons` answers a program with a page shell rather than the
files.

Two things follow from working off a mirror.

**The mirror is not the source.** It carries 214 icons and Google's own set
carries 226. When the product you need is missing, take the file from
`cloud.google.com/icons` and normalise it by hand.

**The marks stay Google's.** Iconify labels the collection Apache 2.0, and that
is the wrong frame for a trademark, because section 6 of that licence excludes
trademark rights. Google's own terms are a permission: you may use the marks to
reference their technology accurately, including in architecture diagrams, and
you follow their brand guidelines when you publish one. Do not redraw a mark, do
not recolour it, and never use one to suggest that Google endorses your work.

## Rules that are not negotiable

**Measure, do not look.** A label three pixels past its box is invisible in a
screenshot and obvious to the person reading the printout. Every defect worth
finding in a diagram of this density was found by a script, not by eyes.

**Cards paint over wires.** The units layer is drawn last, so a connector
label that runs under a card gets eaten by the card's fill. This is the single
most common defect. The audit catches it.

**A label must earn its place.** If the card the arrow lands on already says
`gemini-3-flash · 6 calls` in its subtitle, the arrow does not need the label
"6 calls". Delete it. Corridor clutter is what makes these diagrams look busy.

**No invented numbers.** Every figure on the drawing comes from configuration,
a measurement, or a document. If you cannot source it, leave it off and say so.

**Respect the marks.** They are trademarks, not assets. Read *Where the icons
come from* before you publish a drawing that carries them.

**Never name the addresses.** A diagram that will be served publicly, shared
outside the team, or attached to a deck must not carry project ids, service
URLs, bucket paths, account ids or internal hostnames. Describing the shape of
a system is the point; handing over its address list is not. Write a test for
this if the page lives in a repository.

**The drawing stays on paper.** Keep the diagram on a white ground even when
the page around it is dark. The product icons are drawn for paper, and a
tinted group loses its meaning on a dark fill. Make the frame follow the
theme; leave the sheet alone.

## Files in this skill

| File | Use it for |
| :--- | :--- |
| `references/layout-rules.md` | Geometry, lanes, labels, and the audit script. Read before placing coordinates. |
| `references/slideshow.md` | Turning the drawing into a stepped presentation. |
| `assets/diagram-template.html` | The renderer shell. Splice icons and data into it. |
| `assets/example-data.js` | The data shape, as a small working example. |
| `scripts/fetch-gcp-icons.sh` | Pull Google Cloud product icons and emit the `ICONS` object. |
| `scripts/build-diagram.sh` | Splice icons and data into the template. |
