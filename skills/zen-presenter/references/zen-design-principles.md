# Presentation Zen Design Principles

Core principles from Garr Reynolds' Presentation Zen philosophy, adapted for AI-generated slide design.

## The Three Pillars

### 1. Restraint (Kanso)

The art of leaving out. Simplicity is not about being simplistic — it is about being clear.

**Rules:**
- Remove every element that does not directly serve the message.
- If a word can be removed without losing meaning, remove it.
- If a slide can be removed without breaking the story, remove it.
- Empty space (Ma) is not wasted space — it is breathing room for the idea.

**Anti-patterns:**
- Slides packed with text that the presenter reads aloud.
- Decorative elements (clip art, borders, logos on every slide).
- Agenda slides, summary slides, "Any Questions?" slides.

### 2. Naturalness (Shizen)

Design should feel effortless, not forced. The best slides look like they happened naturally.

**Rules:**
- Use real photography, not stock illustrations or clip art.
- Let images breathe — full-bleed, not crammed into boxes.
- Text should feel like a caption, not a paragraph.
- Flow from slide to slide should feel like a conversation, not a report.

**Anti-patterns:**
- Forced symmetry or rigid grid layouts.
- Overly polished corporate templates with logo watermarks.
- Transitions and animations that call attention to themselves.

### 3. Emptiness (Ma)

Ma is the Japanese concept of negative space. In presentations, it means giving each idea room to land.

**Rules:**
- One idea per slide. No exceptions.
- Let the background image carry the visual weight.
- Position text where the image naturally has empty space.
- Silence between slides is part of the presentation.

**Anti-patterns:**
- Multiple ideas crammed onto one slide "to save time."
- Text overlapping busy parts of an image.
- Rapid-fire slides that don't give the audience time to absorb.

## Signal-to-Noise Ratio

Every element on a slide is either signal (serves the message) or noise (distracts from it).

| Element | Signal | Noise |
|---------|--------|-------|
| One key phrase | Yes | — |
| Full-bleed relevant image | Yes | — |
| Bullet points | — | Yes |
| Company logo on every slide | — | Yes |
| Slide numbers | — | Usually |
| Decorative borders | — | Yes |
| Relevant data visualization | Yes | — |
| Multiple fonts | — | Yes |

**Target: 100% signal.** Every pixel should serve the message or be empty space.

## The Picture Superiority Effect

Research shows that people remember images far better than text. After 3 days:
- Text alone: ~10% recall
- Text + relevant image: ~65% recall

**Application:**
- Choose images that create an emotional connection to the idea.
- Use visual metaphors, not literal illustrations.
- The image should make the audience *feel* something before they read anything.

## Visual Metaphor Selection Guide

Instead of literal images, use metaphors that evoke the concept:

| Concept | Literal (avoid) | Metaphor (use) |
|---------|-----------------|----------------|
| Growth | Bar chart going up | Seedling, sunrise, mountain summit |
| Teamwork | People shaking hands | Rowing crew, orchestra, flock of birds |
| Innovation | Light bulb | Uncharted path, blank canvas, horizon |
| Security | Padlock icon | Fortress, shield, lighthouse |
| Speed | Speedometer | Cheetah, bullet train, waterfall |
| Complexity | Tangled wires | Labyrinth, forest, neural network |
| Clarity | Magnifying glass | Clear lake, open sky, single star |
| Change | Before/after arrows | Butterfly, seasons, river fork |
| Data | Spreadsheet | Constellation, river delta, city lights |
| Connection | Network diagram | Bridge, roots, handshake |
| Challenge | Warning sign | Stormy sea, mountain face, desert |
| Opportunity | Open door | Dawn, open road, empty stage |

## Story Arc for Presentations

Every effective presentation follows a narrative structure:

```
Tension
  /\        Climax
 /  \      /\
/    \    /  \
      \  /    \
       \/      \_____ Resolution
    Exploration
```

### Structure

1. **Hook** (1 slide) — Open with something unexpected. A bold claim, a striking image, a question that challenges assumptions.

2. **Context** (1-2 slides) — Set the stage. Why does this matter? What is the current state?

3. **Tension** (1-2 slides) — Present the problem or gap. Make the audience feel the pain or curiosity.

4. **Exploration** (2-4 slides) — Walk through the key ideas. One idea per slide. Build momentum.

5. **Climax** (1 slide) — The core insight. The moment everything clicks. This slide should be the most visually striking.

6. **Resolution** (1-2 slides) — What changes now? What should the audience do, think, or feel?

7. **Close** (1 slide) — End with resonance, not a whimper. A final image, a return to the opening question, or a call to action.

## Audience Adaptation

### Executive Audience
- Fewer slides (5-7 maximum)
- Even fewer words (5-7 per slide)
- Focus on outcomes and decisions
- Use "so what?" as a filter for every slide

### Technical Audience
- Can handle slightly more slides (7-12)
- Still keep to 10-word maximum
- Use architecture diagrams as background images where appropriate
- One technical concept per slide

### General / Conference Audience
- 7-10 slides for a standard talk
- Emotional imagery over technical diagrams
- Stories and analogies over specifications
- End with inspiration, not a summary

## Color and Contrast

### White Text on Dark Images (Default Zen)
- Set `brightness:0.3` to `brightness:0.4` on backgrounds
- Use pure white (`#ffffff`) or near-white (`#f0f0f0`) for text
- Add text shadow if needed for legibility

### Dark Text on Light Images
- Set `brightness:0.8` to `brightness:1.0` on backgrounds
- Use dark gray (`#1a1a1a`) rather than pure black
- Choose naturally bright/light images

### Accent Color
- Pick one accent color from the topic's domain
- Use it for emphasis on no more than one word per slide
- Keep all other text white or dark

## The Zen Test

Before finalizing any slide, ask:

1. Can I say this in fewer words? → Reduce.
2. Does the image make me feel something? → If not, find a better one.
3. Is there more than one idea here? → Split into two slides.
4. Would this slide work without the presenter? → If yes, it has too much text.
5. Does this advance the story? → If not, remove it.
