# Responsive Navigation Patterns

Navigation patterns for multi-section HTML pages with sticky sidebar on desktop and horizontal scrollable bar on mobile.

---

## HTML Structure

```html
<nav class="ve-nav" id="ve-nav">
  <ul class="ve-nav-list">
    <li><a href="#overview" class="ve-nav-link active">Overview</a></li>
    <li><a href="#architecture" class="ve-nav-link">Architecture</a></li>
    <li>
      <a href="#components" class="ve-nav-link">Components</a>
      <ul class="ve-nav-sublist">
        <li><a href="#components-frontend" class="ve-nav-link">Frontend</a></li>
        <li><a href="#components-backend" class="ve-nav-link">Backend</a></li>
      </ul>
    </li>
    <li><a href="#data-flow" class="ve-nav-link">Data Flow</a></li>
    <li><a href="#deployment" class="ve-nav-link">Deployment</a></li>
  </ul>
</nav>

<main class="ve-main" id="ve-main">
  <section id="overview" class="ve-section">...</section>
  <section id="architecture" class="ve-section">...</section>
  <section id="components" class="ve-section">...</section>
  <section id="components-frontend" class="ve-section ve-subsection">...</section>
  <section id="components-backend" class="ve-section ve-subsection">...</section>
  <section id="data-flow" class="ve-section">...</section>
  <section id="deployment" class="ve-section">...</section>
</main>
```

---

## Sticky Sidebar TOC (Desktop)

```css
/* Page layout: sidebar + main */
body {
  display: flex;
  min-height: 100dvh;
}

.ve-nav {
  position: sticky;
  top: 0;
  height: 100dvh;
  width: 240px;
  flex-shrink: 0;
  overflow-y: auto;
  padding: 2rem 1rem;
  border-right: 1px solid var(--color-border);
  background: var(--color-surface);
}

.ve-nav-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.ve-nav-link {
  display: block;
  padding: 0.4rem 0.75rem;
  border-radius: 6px;
  color: var(--color-text-secondary);
  text-decoration: none;
  font-size: 0.875rem;
  font-weight: 500;
  transition: background 0.15s ease, color 0.15s ease;
}

.ve-nav-link:hover {
  background: var(--color-accent-bg);
  color: var(--color-text);
}

.ve-nav-link.active {
  background: var(--color-accent-muted);
  color: var(--color-accent);
  font-weight: 600;
}

/* Nested sublist */
.ve-nav-sublist {
  list-style: none;
  padding: 0 0 0 1rem;
  margin: 0.25rem 0 0 0;
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
}

.ve-nav-sublist .ve-nav-link {
  font-size: 0.8rem;
  padding: 0.3rem 0.75rem;
}

/* Main content */
.ve-main {
  flex: 1;
  min-width: 0;
  padding: 2rem 3rem;
}

.ve-section {
  scroll-margin-top: 1rem;
  padding-bottom: 3rem;
}
```

### Collapse/Expand for Nested Sections

```css
.ve-nav-sublist {
  overflow: hidden;
  max-height: 0;
  transition: max-height 0.25s ease;
}

/* Show sublist when parent link is active */
.ve-nav-link.active + .ve-nav-sublist,
.ve-nav-sublist:has(.ve-nav-link.active) {
  max-height: 200px;
}
```

---

## Horizontal Scrollable Bar (Mobile)

```css
@media (max-width: 768px) {
  body {
    flex-direction: column;
  }

  .ve-nav {
    position: sticky;
    top: 0;
    z-index: 100;
    height: auto;
    width: 100%;
    padding: 0;
    border-right: none;
    border-bottom: 1px solid var(--color-border);
    backdrop-filter: blur(12px);
  }

  .ve-nav-list {
    flex-direction: row;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    scroll-snap-type: x mandatory;
    gap: 0;
    padding: 0.5rem 0.75rem;
    scrollbar-width: none;
  }

  .ve-nav-list::-webkit-scrollbar { display: none; }

  .ve-nav-link {
    white-space: nowrap;
    scroll-snap-align: start;
    padding: 0.4rem 0.85rem;
    border-radius: 20px;
    font-size: 0.8rem;
  }

  .ve-nav-link.active {
    background: var(--color-accent);
    color: #fff;
  }

  /* Hide nested sublists on mobile */
  .ve-nav-sublist { display: none; }

  .ve-main {
    padding: 1.5rem 1rem;
  }
}
```

---

## JavaScript: Intersection Observer Active Tracking

```javascript
document.addEventListener('DOMContentLoaded', () => {
  const sections = document.querySelectorAll('.ve-section');
  const navLinks = document.querySelectorAll('.ve-nav-link');

  const observerOptions = {
    root: null,
    rootMargin: '-20% 0px -70% 0px',
    threshold: 0
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const id = entry.target.getAttribute('id');

        navLinks.forEach(link => {
          link.classList.remove('active');
          if (link.getAttribute('href') === '#' + id) {
            link.classList.add('active');

            // On mobile, scroll the active link into view in the nav bar
            if (window.innerWidth <= 768) {
              link.scrollIntoView({
                behavior: 'smooth',
                block: 'nearest',
                inline: 'center'
              });
            }
          }
        });
      }
    });
  }, observerOptions);

  sections.forEach(section => observer.observe(section));
});
```

---

## Smooth Scroll Behavior

```css
html {
  scroll-behavior: smooth;
}
```

```javascript
// Click handler for nav links (enhances default anchor behavior)
document.querySelectorAll('.ve-nav-link').forEach(link => {
  link.addEventListener('click', (e) => {
    e.preventDefault();
    const targetId = link.getAttribute('href').substring(1);
    const target = document.getElementById(targetId);
    if (target) {
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});
```

---

## Section ID Naming Convention

Use kebab-case IDs that match the section content:

| Section | ID |
|---------|-----|
| Overview | `#overview` |
| System Architecture | `#system-architecture` |
| Frontend Components | `#components-frontend` |
| Backend Services | `#components-backend` |
| Data Flow | `#data-flow` |
| Deployment | `#deployment` |

Rules:
- All lowercase
- Words separated by hyphens
- Nested sections use parent prefix: `components-frontend`, `components-backend`
- Keep IDs short but descriptive
- Avoid generic names like `section-1`

---

## Hash-Based Navigation

Update the URL hash as the user scrolls, enabling shareable deep links:

```javascript
const hashObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const id = entry.target.getAttribute('id');
      history.replaceState(null, null, '#' + id);
    }
  });
}, { rootMargin: '-30% 0px -60% 0px', threshold: 0 });

document.querySelectorAll('.ve-section').forEach(s => hashObserver.observe(s));
```

On page load, scroll to the hashed section if present:

```javascript
if (window.location.hash) {
  const target = document.querySelector(window.location.hash);
  if (target) {
    setTimeout(() => target.scrollIntoView({ behavior: 'smooth' }), 100);
  }
}
```
