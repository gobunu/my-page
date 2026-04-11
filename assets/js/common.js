$(document).ready(function () {
  // Add toggle functionality to abstract, award and bibtex buttons.
  // Use delegated handlers for reliable mobile and desktop behavior.
  $(document).on("click", ".links .abstract", function (event) {
    event.preventDefault();
    const $entry = $(this).closest(".row");
    $entry.find(".abstract.hidden").toggleClass("open");
    $entry.find(".award.hidden.open").removeClass("open");
    $entry.find(".bibtex.hidden.open").removeClass("open");
  });

  $(document).on("click", ".links .award", function (event) {
    event.preventDefault();
    const $entry = $(this).closest(".row");
    $entry.find(".abstract.hidden.open").removeClass("open");
    $entry.find(".award.hidden").toggleClass("open");
    $entry.find(".bibtex.hidden.open").removeClass("open");
  });

  $(document).on("click", ".links .bibtex", function (event) {
    event.preventDefault();
    const $entry = $(this).closest(".row");
    $entry.find(".abstract.hidden.open").removeClass("open");
    $entry.find(".award.hidden.open").removeClass("open");
    $entry.find(".bibtex.hidden").toggleClass("open");
  });

  // Fallback for mobile: ensure navbar dropdown children are tappable in collapsed menu.
  $(document).on("click", ".navbar .dropdown-toggle", function (event) {
    if (window.matchMedia("(max-width: 575.98px)").matches) {
      event.preventDefault();
      event.stopPropagation();
      const $menu = $(this).next(".dropdown-menu");
      $(".navbar .dropdown-menu").not($menu).removeClass("show");
      $menu.toggleClass("show");
    }
  });

  $(document).on("click", ".navbar .dropdown-item", function () {
    $(".navbar .dropdown-menu").removeClass("show");
  });
  $("a").removeClass("waves-effect waves-light");

  // bootstrap-toc
  if ($("#toc-sidebar").length) {
    // remove related publications years from the TOC
    $(".publications h2").each(function () {
      $(this).attr("data-toc-skip", "");
    });
    var navSelector = "#toc-sidebar";
    var $myNav = $(navSelector);
    Toc.init($myNav);
    $("body").scrollspy({
      target: navSelector,
      offset: 100,
    });
  }

  // add css to jupyter notebooks
  const cssLink = document.createElement("link");
  cssLink.href = "../css/jupyter.css";
  cssLink.rel = "stylesheet";
  cssLink.type = "text/css";

  let jupyterTheme = determineComputedTheme();

  $(".jupyter-notebook-iframe-container iframe").each(function () {
    $(this).contents().find("head").append(cssLink);

    if (jupyterTheme == "dark") {
      $(this).bind("load", function () {
        $(this).contents().find("body").attr({
          "data-jp-theme-light": "false",
          "data-jp-theme-name": "JupyterLab Dark",
        });
      });
    }
  });

  // trigger popovers
  $('[data-toggle="popover"]').popover({
    trigger: "hover",
  });
});
