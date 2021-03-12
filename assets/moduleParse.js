// Import only core.
import hljs from 'highlight.js/lib/core';
// This line changes the syntax highlighting style.
import 'highlight.js/styles/rainbow.css';
// Import languages one-by-one.
import javascript from 'highlight.js/lib/languages/javascript';
import r from 'highlight.js/lib/languages/r';
import sql from 'highlight.js/lib/languages/sql';
import css from 'highlight.js/lib/languages/css';
import python from 'highlight.js/lib/languages/python';
import xml from 'highlight.js/lib/languages/xml';

// Register languages.
hljs.registerLanguage('javascript', javascript);
hljs.registerLanguage('r', r);
hljs.registerLanguage('sql', sql);
hljs.registerLanguage('html', xml);
hljs.registerLanguage('css', css);
hljs.registerLanguage('python', python);

// Highlight all code blocks on load.
hljs.highlightAll();