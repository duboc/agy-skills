// ============================================================
// MARP HTML Slide Extractor
// Executed inside the browser via agent-browser eval
//
// Extracts structured data from MARP-rendered HTML slides:
// - Slide backgrounds (color, gradient, image)
// - Text elements with position, size, font, color, alignment
// - Images with source and dimensions
// - Lists with items and bullet styling
// - Code blocks with content and styling
//
// Returns a JSON array of slide objects ready for build_pptx.js
// ============================================================
(() => {
  // MARP renders slides as <section> elements inside <div class="marpit">
  // or as <svg> viewboxes depending on the rendering mode.
  // We handle both structures.
  const slides = document.querySelectorAll(
    'div.marpit > svg > foreignObject > section, ' +
    'div.marpit > section, ' +
    'section.slide, ' +
    'section[data-marpit-pagination]'
  );

  // Fallback: if no MARP structure found, treat each <section> as a slide
  const slideElements = slides.length > 0
    ? Array.from(slides)
    : Array.from(document.querySelectorAll('section'));

  if (slideElements.length === 0) {
    return JSON.stringify({ error: 'No slides found in HTML', slides: [] });
  }

  // Get the slide dimensions from the first slide
  const firstSlide = slideElements[0];
  const slideRect = firstSlide.getBoundingClientRect();
  const slideWidth = slideRect.width || 1280;
  const slideHeight = slideRect.height || 720;

  const result = {
    meta: {
      slideCount: slideElements.length,
      slideWidth: slideWidth,
      slideHeight: slideHeight,
      title: document.title || 'Untitled Presentation'
    },
    slides: []
  };

  slideElements.forEach((section, slideIndex) => {
    const sectionStyles = window.getComputedStyle(section);
    const sectionRect = section.getBoundingClientRect();

    // Extract slide background
    const background = {
      color: sectionStyles.backgroundColor,
      image: sectionStyles.backgroundImage !== 'none' ? sectionStyles.backgroundImage : null,
      size: sectionStyles.backgroundSize,
      position: sectionStyles.backgroundPosition
    };

    // Check for CSS class (MARP slide types)
    const slideClass = section.getAttribute('class') || '';

    const slideData = {
      index: slideIndex,
      class: slideClass,
      background: background,
      elements: []
    };

    // Extract all content elements within this slide
    const contentElements = section.querySelectorAll(
      'h1, h2, h3, h4, h5, h6, p, ul, ol, blockquote, pre, img, table, svg'
    );

    contentElements.forEach(el => {
      const rect = el.getBoundingClientRect();
      const styles = window.getComputedStyle(el);

      // Skip elements with zero dimensions or outside the slide
      if (rect.width === 0 || rect.height === 0) return;

      // Calculate position relative to the slide
      const relX = rect.left - sectionRect.left;
      const relY = rect.top - sectionRect.top;

      const baseData = {
        tag: el.tagName.toLowerCase(),
        x: relX,
        y: relY,
        width: rect.width,
        height: rect.height,
        fontSize: parseFloat(styles.fontSize),
        fontFamily: styles.fontFamily,
        fontWeight: styles.fontWeight,
        fontStyle: styles.fontStyle,
        color: styles.color,
        textAlign: styles.textAlign,
        lineHeight: styles.lineHeight,
        textDecoration: styles.textDecoration,
        backgroundColor: styles.backgroundColor,
        borderLeft: styles.borderLeftWidth + ' ' + styles.borderLeftStyle + ' ' + styles.borderLeftColor
      };

      switch (el.tagName.toLowerCase()) {
        case 'h1':
        case 'h2':
        case 'h3':
        case 'h4':
        case 'h5':
        case 'h6':
          slideData.elements.push({
            ...baseData,
            type: 'heading',
            level: parseInt(el.tagName[1]),
            text: el.innerText.trim(),
            hasAccent: el.querySelector('strong') !== null,
            accentText: el.querySelector('strong')?.innerText || null,
            accentColor: el.querySelector('strong')
              ? window.getComputedStyle(el.querySelector('strong')).color
              : null,
            accents: Array.from(el.querySelectorAll('strong, em')).map(span => ({
              text: span.innerText,
              tag: span.tagName.toLowerCase(),
              color: window.getComputedStyle(span).color
            }))
          });
          break;

        case 'p':
          // Skip empty paragraphs
          if (!el.innerText.trim() && !el.querySelector('img')) return;

          // Check if this paragraph contains an image
          const inlineImg = el.querySelector('img');
          if (inlineImg) {
            slideData.elements.push({
              ...baseData,
              type: 'image',
              src: inlineImg.src,
              alt: inlineImg.alt || ''
            });
          } else {
            slideData.elements.push({
              ...baseData,
              type: 'text',
              text: el.innerText.trim(),
              isItalic: el.querySelector('em') !== null || styles.fontStyle === 'italic',
              hasAccent: el.querySelector('strong') !== null,
              accentText: el.querySelector('strong')?.innerText || null,
              accentColor: el.querySelector('strong')
                ? window.getComputedStyle(el.querySelector('strong')).color
                : null,
              accents: Array.from(el.querySelectorAll('strong, em')).map(span => ({
                text: span.innerText,
                tag: span.tagName.toLowerCase(),
                color: window.getComputedStyle(span).color
              }))
            });
          }
          break;

        case 'ul':
        case 'ol':
          function extractListItems(listEl, depth) {
            if (depth > 2) return [];
            return Array.from(listEl.querySelectorAll(':scope > li')).map(li => {
              const liStyles = window.getComputedStyle(li);
              const nestedList = li.querySelector(':scope > ul, :scope > ol');
              const directText = Array.from(li.childNodes)
                .filter(n => n.nodeType === 3 || (n.nodeType === 1 && !['UL', 'OL'].includes(n.tagName)))
                .map(n => n.textContent)
                .join('')
                .trim();
              return {
                text: directText || li.innerText.trim(),
                color: liStyles.color,
                fontSize: parseFloat(liStyles.fontSize),
                hasAccent: li.querySelector(':scope > strong, :scope > em') !== null,
                accentText: li.querySelector(':scope > strong')?.innerText || null,
                depth: depth,
                subItems: nestedList ? extractListItems(nestedList, depth + 1) : []
              };
            });
          }
          const items = extractListItems(el, 0);
          slideData.elements.push({
            ...baseData,
            type: el.tagName.toLowerCase() === 'ul' ? 'unordered-list' : 'ordered-list',
            items: items,
            bulletColor: styles.color
          });
          break;

        case 'blockquote':
          slideData.elements.push({
            ...baseData,
            type: 'blockquote',
            text: el.innerText.trim(),
            borderColor: styles.borderLeftColor
          });
          break;

        case 'pre':
          const codeEl = el.querySelector('code');
          slideData.elements.push({
            ...baseData,
            type: 'code',
            text: codeEl ? codeEl.innerText : el.innerText,
            language: codeEl?.className?.replace('language-', '') || ''
          });
          break;

        case 'img':
          slideData.elements.push({
            ...baseData,
            type: 'image',
            src: el.src,
            alt: el.alt || ''
          });
          break;

        case 'table':
          const rows = Array.from(el.querySelectorAll('tr')).map(tr => {
            return Array.from(tr.querySelectorAll('th, td')).map(cell => ({
              text: cell.innerText.trim(),
              isHeader: cell.tagName.toLowerCase() === 'th',
              color: window.getComputedStyle(cell).color,
              backgroundColor: window.getComputedStyle(cell).backgroundColor,
              fontWeight: window.getComputedStyle(cell).fontWeight,
              colspan: parseInt(cell.getAttribute('colspan') || '1'),
              rowspan: parseInt(cell.getAttribute('rowspan') || '1')
            }));
          });
          slideData.elements.push({
            ...baseData,
            type: 'table',
            rows: rows
          });
          break;

        case 'svg':
          // Flag SVGs as complex elements that need screenshot fallback
          slideData.elements.push({
            ...baseData,
            type: 'svg',
            isComplex: true,
            elementId: el.id || `svg-${slideIndex}-${slideData.elements.length}`
          });
          break;
      }
    });

    result.slides.push(slideData);
  });

  return JSON.stringify(result, null, 2);
})();
