export const themeScript = `
  (function() {
    // Only run on client side
    if (typeof window === 'undefined') return;

    try {
      const theme = localStorage.getItem('theme');
      if (theme === 'dark' || (!theme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        document.documentElement.classList.add('dark');
      } else {
        document.documentElement.classList.remove('dark');
      }
    } catch (e) {
      // localStorage is not available
    }
  })();
`;