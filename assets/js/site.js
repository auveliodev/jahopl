/* =========================================================================
   JA-HO — site behaviour.
   Vanilla, no dependencies, no build step. Every effect degrades to a working
   static page if JS never runs (see the html:not(.js) rules in site.css).
   ========================================================================= */
(function () {
  "use strict";

  var root = document.documentElement;
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)");
  var finePointer = window.matchMedia("(hover: hover) and (pointer: fine)");
  var $  = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  /* ---------------------------------------------------------------- theme */
  // The no-flash paint happens inline in <head>. This only wires the button.
  (function theme() {
    var btn = $("[data-theme-toggle]");
    if (!btn) return;

    function current() {
      var set = root.getAttribute("data-theme");
      if (set) return set;
      return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
    }
    function announce(mode) {
      btn.setAttribute("aria-label",
        mode === "dark" ? "Przełącz na motyw jasny" : "Przełącz na motyw ciemny");
      var meta = $('meta[name="theme-color"]');
      if (meta) meta.content = mode === "dark" ? "#14100e" : "#faf8f5";
    }
    announce(current());

    btn.addEventListener("click", function () {
      var next = current() === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      try { localStorage.setItem("jaho-theme", next); } catch (e) {}
      announce(next);
    });
  })();

  /* ------------------------------------------- header state + scroll rail */
  (function header() {
    var hdr = $(".hdr");
    var bar = $(".progress");
    var top = $(".totop");
    if (!hdr && !bar && !top) return;

    var ticking = false;
    function paint() {
      var y = window.scrollY || window.pageYOffset;
      if (hdr) hdr.classList.toggle("is-stuck", y > 8);
      if (top) top.classList.toggle("is-on", y > 700);
      if (bar) {
        var max = document.documentElement.scrollHeight - window.innerHeight;
        bar.style.transform = "scaleX(" + (max > 0 ? Math.min(y / max, 1) : 0) + ")";
      }
      ticking = false;
    }
    window.addEventListener("scroll", function () {
      if (!ticking) { ticking = true; requestAnimationFrame(paint); }
    }, { passive: true });
    window.addEventListener("resize", paint, { passive: true });
    paint();

    if (top) {
      top.addEventListener("click", function () {
        window.scrollTo({ top: 0, behavior: reduced.matches ? "auto" : "smooth" });
      });
    }
  })();

  /* ------------------------------------------------ nav sliding pill */
  // animate-ui Tabs: one element slides between items instead of each item
  // animating its own background.
  (function navPill() {
    var nav = $(".nav");
    if (!nav) return;
    var pill = $(".nav__pill", nav);
    var links = $$(".nav__link", nav);
    if (!pill || !links.length) return;

    var home = links.filter(function (a) { return a.getAttribute("aria-current") === "page"; })[0];

    function move(el) {
      if (!el) { nav.classList.remove("has-pill"); return; }
      pill.style.width = el.offsetWidth + "px";
      pill.style.transform = "translateX(" + el.offsetLeft + "px)";
      nav.classList.add("has-pill");
    }
    links.forEach(function (a) {
      a.addEventListener("mouseenter", function () { move(a); });
      a.addEventListener("focus", function () { move(a); });
    });
    nav.addEventListener("mouseleave", function () { move(home); });
    nav.addEventListener("focusout", function (e) {
      if (!nav.contains(e.relatedTarget)) move(home);
    });
    // No transition on the very first placement.
    var prev = pill.style.transition;
    pill.style.transition = "none";
    move(home);
    requestAnimationFrame(function () { pill.style.transition = prev; });
    window.addEventListener("resize", function () { move(home); }, { passive: true });
  })();

  /* ------------------------------------------------- mobile nav sheet */
  (function sheet() {
    var burger = $(".burger");
    var panel  = $("#mobile-nav");
    if (!burger || !panel) return;
    var scrim = $(".sheet__scrim", panel);
    var lastFocus = null;

    function focusables() {
      return $$("a[href], button:not([disabled])", panel).filter(function (el) {
        return el.offsetParent !== null;
      });
    }
    function open() {
      lastFocus = document.activeElement;
      panel.classList.add("is-open");
      burger.setAttribute("aria-expanded", "true");
      document.body.style.overflow = "hidden";
      var f = focusables();
      if (f.length) setTimeout(function () { f[0].focus(); }, 220);
    }
    function close() {
      panel.classList.remove("is-open");
      burger.setAttribute("aria-expanded", "false");
      document.body.style.overflow = "";
      if (lastFocus) lastFocus.focus();
    }
    function toggle() {
      burger.getAttribute("aria-expanded") === "true" ? close() : open();
    }

    burger.addEventListener("click", toggle);
    if (scrim) scrim.addEventListener("click", close);
    $$("a", panel).forEach(function (a) { a.addEventListener("click", close); });

    document.addEventListener("keydown", function (e) {
      if (!panel.classList.contains("is-open")) return;
      if (e.key === "Escape") { close(); return; }
      if (e.key !== "Tab") return;
      // Keep focus inside the open sheet.
      var f = focusables();
      if (!f.length) return;
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    });
    // A resize past the desktop breakpoint should not strand a hidden sheet.
    window.addEventListener("resize", function () {
      if (window.innerWidth >= 1000 && panel.classList.contains("is-open")) close();
    }, { passive: true });
  })();

  /* ------------------------------------------------------ scroll reveal */
  (function reveal() {
    var targets = $$("[data-reveal], [data-reveal-group]");
    if (!targets.length) return;

    if (reduced.matches || !("IntersectionObserver" in window)) {
      targets.forEach(function (el) { el.classList.add("is-in"); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        en.target.classList.add("is-in");
        io.unobserve(en.target);
      });
    }, { rootMargin: "0px 0px -12% 0px", threshold: 0.08 });
    targets.forEach(function (el) { io.observe(el); });
  })();

  /* --------------------------------------------------- animated counters */
  // "27 years of experience" ticks up once, when it scrolls into view.
  (function counters() {
    var nums = $$("[data-count]");
    if (!nums.length) return;

    function run(el) {
      var target = parseFloat(el.getAttribute("data-count"));
      if (isNaN(target)) return;
      if (reduced.matches) { el.textContent = String(target); return; }

      var dur = 1500, t0 = null;
      function frame(ts) {
        if (t0 === null) t0 = ts;
        var p = Math.min((ts - t0) / dur, 1);
        // easeOutExpo — fast start, long settle
        var e = p === 1 ? 1 : 1 - Math.pow(2, -10 * p);
        el.textContent = String(Math.round(target * e));
        if (p < 1) requestAnimationFrame(frame);
        else el.textContent = String(target);
      }
      requestAnimationFrame(frame);
    }

    if (!("IntersectionObserver" in window)) { nums.forEach(run); return; }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        run(en.target);
        io.unobserve(en.target);
      });
    }, { threshold: 0.5 });
    // Only blank a counter that is safely below the fold. Zeroing everything up
    // front makes any stat already on screen flash 27 -> 0 -> 27 on load, and
    // leaves a wall of zeros if the observer never fires.
    nums.forEach(function (el) {
      if (el.getBoundingClientRect().top > window.innerHeight) el.textContent = "0";
      io.observe(el);
    });
  })();

  /* ------------------------------------------------------------ accordion */
  (function accordion() {
    $$(".acc").forEach(function (acc) {
      var single = acc.hasAttribute("data-single");
      var btns = $$(".acc__btn", acc);

      btns.forEach(function (btn) {
        btn.addEventListener("click", function () {
          var item = btn.closest(".acc__item");
          var open = btn.getAttribute("aria-expanded") === "true";

          if (single && !open) {
            btns.forEach(function (b) {
              if (b === btn) return;
              b.setAttribute("aria-expanded", "false");
              b.closest(".acc__item").classList.remove("is-open");
            });
          }
          btn.setAttribute("aria-expanded", open ? "false" : "true");
          item.classList.toggle("is-open", !open);
        });
      });
    });
  })();

  /* --------------------------------------------------------- ripple button */
  // animate-ui Ripple Button: a circle grows from the exact press point.
  (function ripple() {
    if (reduced.matches) return;
    document.addEventListener("pointerdown", function (e) {
      var btn = e.target.closest ? e.target.closest(".btn") : null;
      if (!btn) return;
      var host = $(".btn__ripple", btn);
      if (!host) return;

      var r = btn.getBoundingClientRect();
      var dot = document.createElement("span");
      dot.style.left = (e.clientX - r.left) + "px";
      dot.style.top  = (e.clientY - r.top) + "px";
      host.appendChild(dot);
      setTimeout(function () { dot.remove(); }, 700);
    }, { passive: true });
  })();

  /* --------------------------------------------- pointer wash on cards */
  (function cardWash() {
    if (!finePointer.matches || reduced.matches) return;
    $$(".card").forEach(function (card) {
      card.addEventListener("pointermove", function (e) {
        var r = card.getBoundingClientRect();
        card.style.setProperty("--mx", (e.clientX - r.left) + "px");
        card.style.setProperty("--my", (e.clientY - r.top) + "px");
      });
    });
  })();

  /* ------------------------------------------------------ magnetic buttons */
  // Desktop-only, and only on elements that opt in — never on touch, where it
  // would fight with the tap target.
  (function magnetic() {
    if (!finePointer.matches || reduced.matches) return;
    $$("[data-magnetic]").forEach(function (el) {
      var raf = null;
      el.addEventListener("pointermove", function (e) {
        if (raf) return;
        raf = requestAnimationFrame(function () {
          var r = el.getBoundingClientRect();
          var dx = (e.clientX - (r.left + r.width / 2)) * 0.16;
          var dy = (e.clientY - (r.top + r.height / 2)) * 0.3;
          el.style.transform = "translate(" + dx + "px," + dy + "px)";
          raf = null;
        });
      });
      el.addEventListener("pointerleave", function () {
        if (raf) { cancelAnimationFrame(raf); raf = null; }
        el.style.transform = "";
      });
    });
  })();

  /* ------------------------------------------------- project filter tabs */
  (function projectFilter() {
    var tablist = $("[data-filter-tabs]");
    var gallery = $("[data-gallery]");
    if (!tablist || !gallery) return;

    var tabs = $$(".tab", tablist);
    var shots = $$(".shot", gallery);
    var empty = $(".gallery__empty", gallery.parentNode);
    var status = $("[data-filter-status]");

    function apply(slug, push) {
      var label = "All work";
      tabs.forEach(function (t) {
        var on = t.dataset.slug === slug;
        t.setAttribute("aria-pressed", on ? "true" : "false");
        if (on) label = (t.textContent || "").replace(/\d+$/, "").trim();
      });

      var shown = 0;
      shots.forEach(function (s) {
        var on = slug === "all" || s.dataset.cat === slug;
        s.hidden = !on;
        if (on) shown++;
      });
      if (empty) empty.hidden = shown > 0;
      if (status) {
        status.textContent = shown
          ? "Pokazano zdjęcia: " + shown + " — " + label
          : "Brak zdjęć w tej kategorii.";
      }

      // Re-run the entry animation so a filter change feels like a transition,
      // not a jump cut.
      if (!reduced.matches) {
        gallery.classList.remove("is-in");
        void gallery.offsetWidth;
        gallery.classList.add("is-in");
      }
      if (push) {
        var url = slug === "all" ? location.pathname : location.pathname + "#" + slug;
        history.replaceState(null, "", url);
      }
    }

    tabs.forEach(function (t) {
      t.addEventListener("click", function () { apply(t.dataset.slug, true); });
    });

    // Arrow keys move between filters as a convenience. Every button stays
    // reachable by Tab, so this adds to keyboard access rather than gating it.
    tablist.addEventListener("keydown", function (e) {
      var i = tabs.indexOf(document.activeElement);
      if (i < 0) return;
      var n = null;
      if (e.key === "ArrowRight") n = (i + 1) % tabs.length;
      else if (e.key === "ArrowLeft") n = (i - 1 + tabs.length) % tabs.length;
      else if (e.key === "Home") n = 0;
      else if (e.key === "End") n = tabs.length - 1;
      if (n === null) return;
      e.preventDefault();
      tabs[n].focus();
      apply(tabs[n].dataset.slug, true);
    });

    var hash = (location.hash || "").replace("#", "");
    var valid = tabs.some(function (t) { return t.dataset.slug === hash; });
    apply(valid ? hash : "all", false);
  })();

  /* ----------------------------------------------------------- lightbox */
  (function lightbox() {
    var lb = $(".lb");
    if (!lb) return;
    var img   = $(".lb__img", lb);
    var cap   = $(".lb__cap", lb);
    var count = $(".lb__count", lb);
    var prevB = $(".lb__nav--prev", lb);
    var nextB = $(".lb__nav--next", lb);
    var closeB = $(".lb__close", lb);

    var pool = [], at = 0, lastFocus = null;

    function visibleShots() {
      return $$(".shot").filter(function (s) { return !s.hidden; });
    }
    function show(i) {
      if (!pool.length) return;
      at = (i + pool.length) % pool.length;
      var s = pool[at];
      var thumb = $("img", s);

      img.style.opacity = "0";
      var full = s.dataset.full;
      var pre = new Image();
      pre.onload = function () {
        img.src = full;
        img.alt = thumb ? thumb.alt : "";
        img.style.opacity = "";
      };
      pre.onerror = function () { img.src = thumb ? thumb.src : ""; img.style.opacity = ""; };
      pre.src = full;

      if (cap) cap.innerHTML = "<b>" + (s.dataset.catName || "") + "</b> — " + (thumb ? thumb.alt : "");
      if (count) count.textContent = (at + 1) + " / " + pool.length;

      var single = pool.length < 2;
      if (prevB) prevB.hidden = single;
      if (nextB) nextB.hidden = single;
    }
    function open(shot) {
      pool = visibleShots();
      lastFocus = document.activeElement;
      lb.classList.add("is-open");
      lb.setAttribute("aria-hidden", "false");
      document.body.classList.add("lb-open");
      show(pool.indexOf(shot));
      if (closeB) closeB.focus();
    }
    function close() {
      lb.classList.remove("is-open");
      lb.setAttribute("aria-hidden", "true");
      document.body.classList.remove("lb-open");
      if (lastFocus) lastFocus.focus();
      setTimeout(function () { if (!lb.classList.contains("is-open")) img.removeAttribute("src"); }, 300);
    }

    document.addEventListener("click", function (e) {
      var shot = e.target.closest ? e.target.closest(".shot") : null;
      if (shot && shot.dataset.full) { e.preventDefault(); open(shot); }
    });
    if (closeB) closeB.addEventListener("click", close);
    if (prevB) prevB.addEventListener("click", function () { show(at - 1); });
    if (nextB) nextB.addEventListener("click", function () { show(at + 1); });
    lb.addEventListener("click", function (e) { if (e.target === lb) close(); });

    document.addEventListener("keydown", function (e) {
      if (!lb.classList.contains("is-open")) return;
      if (e.key === "Escape") close();
      else if (e.key === "ArrowLeft") show(at - 1);
      else if (e.key === "ArrowRight") show(at + 1);
      else if (e.key === "Tab") {
        // Trap focus on the three controls.
        var f = [closeB, prevB, nextB].filter(function (b) { return b && !b.hidden; });
        if (!f.length) return;
        var i = f.indexOf(document.activeElement);
        e.preventDefault();
        f[(i + (e.shiftKey ? -1 : 1) + f.length) % f.length].focus();
      }
    });

    // Swipe between photos on touch.
    var x0 = null;
    lb.addEventListener("touchstart", function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener("touchend", function (e) {
      if (x0 === null) return;
      var dx = e.changedTouches[0].clientX - x0;
      if (Math.abs(dx) > 55) show(at + (dx < 0 ? 1 : -1));
      x0 = null;
    }, { passive: true });
  })();

  /* ------------------------------------------------------- contact form */
  // No backend on a static host: hand the enquiry to the user's mail client
  // with everything already filled in, and say so plainly in the UI.
  (function contactForm() {
    var form = $("[data-mailto]");
    if (!form) return;

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;

      var d = new FormData(form);
      var get = function (k) { return (d.get(k) || "").toString().trim(); };
      var subject = "Zapytanie ze strony ja-ho.pl — " + (get("scope") || "ogólne");
      var body = [
        "Imię i nazwisko: " + get("name"),
        "Telefon: " + get("phone"),
        "E-mail: " + (get("email") || "—"),
        "Lokalizacja: " + (get("place") || "—"),
        "Zakres: " + (get("scope") || "—"),
        "",
        "Wiadomość:",
        get("message")
      ].join("\n");

      window.location.href = "mailto:" + form.dataset.mailto +
        "?subject=" + encodeURIComponent(subject) +
        "&body=" + encodeURIComponent(body);

      var note = $("[data-form-note]", form);
      if (note) {
        note.textContent = "Otwieram program pocztowy z gotowym zapytaniem. " +
          "Jeśli nic się nie stało, zadzwoń pod 695 225 505 albo napisz na " +
          form.dataset.mailto + ".";
        note.style.color = "var(--c-ok)";
      }
    });
  })();

  /* -------------------------------------------------------- lazy hero swap */
  // Mark the page ready so any CSS hooked to it can settle.
  window.addEventListener("load", function () { root.classList.add("is-loaded"); });
})();
