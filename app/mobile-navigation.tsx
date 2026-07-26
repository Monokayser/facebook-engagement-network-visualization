"use client";

import { useRef } from "react";

const links = [
  ["Findings", "#findings"],
  ["Networks", "#networks"],
  ["Exercises", "#exercises"],
  ["Method", "#method"],
];

export default function MobileNavigation() {
  const menu = useRef<HTMLDetailsElement>(null);

  function closeMenu() {
    menu.current?.removeAttribute("open");
  }

  return (
    <details className="mobile-menu" ref={menu}>
      <summary aria-label="Open section navigation">Menu</summary>
      <nav aria-label="Mobile navigation">
        {links.map(([label, href]) => (
          <a href={href} key={href} onClick={closeMenu}>
            {label}
          </a>
        ))}
      </nav>
    </details>
  );
}
