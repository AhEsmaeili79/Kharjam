export const toggleTheme = (enabled: boolean) => {
  if (typeof document !== "undefined") {
    if (enabled) {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
  }
};
