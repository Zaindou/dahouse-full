import { Notyf } from "notyf";
import "notyf/notyf.min.css"; // for React, Vue and Svelte

export default defineNuxtPlugin((nuxtApp) => {
  const notyf = new Notyf({
    duration: 3000,
    position: {
      x: "right",
      y: "top",
    },
    types: [
      {
        type: "info",
        background: "#17a2b8",
        icon: false,
      },
      {
        type: "warning",
        background: "#ffc107",
        icon: false,
      },
    ],
  });

  return {
    provide: {
      notify: notyf,
    },
  };
});
