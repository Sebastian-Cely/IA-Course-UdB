---
marp: true
theme: default
style: |
  /* 1. Definición simple de la animación */
  @keyframes mi-fundido {
    from { opacity: 0; }
    to { opacity: 1; }
  }

  /* 2. Clase que aplica la animación */
  .aparecer {
    animation: mi-fundido 1.5s both;
  }
---

# Diapositiva 1

Esta es la primera diapositiva. No tiene animación.

---

<!-- _class: aparecer -->

# Diapositiva 2

Esta diapositiva debería aparecer con una animación de fundido (fade-in).