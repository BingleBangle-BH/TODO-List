/**
* Template Name: Ninestars
* Updated: Mar 10 2023 with Bootstrap v5.2.3
* Template URL: https://bootstrapmade.com/ninestars-free-bootstrap-3-theme-for-creative/
* Author: BootstrapMade.com
* License: https://bootstrapmade.com/license/
*/
(function() {
  "use strict";

  /**
   * Easy selector helper function
   */
  const select = (el, all = false) => {
    el = el.trim()
    if (all) {
      return [...document.querySelectorAll(el)]
    } else {
      return document.querySelector(el)
    }
  }

  /**
   * Easy event listener function
   */
  const on = (type, el, listener, all = false) => {
    let selectEl = select(el, all)
    if (selectEl) {
      if (all) {
        selectEl.forEach(e => e.addEventListener(type, listener))
      } else {
        selectEl.addEventListener(type, listener)
      }
    }
  }

  /**
   * Easy on scroll event listener 
   */
  const onscroll = (el, listener) => {
    el.addEventListener('scroll', listener)
  }

  /**
   * Navbar links active state on scroll
   */
  let navbarlinks = select('#navbar .scrollto', true)
  const navbarlinksActive = () => {
    let position = window.scrollY + 200
    navbarlinks.forEach(navbarlink => {
      if (!navbarlink.hash) return
      let section = select(navbarlink.hash)
      if (!section) return
      if (position >= section.offsetTop && position <= (section.offsetTop + section.offsetHeight)) {
        navbarlink.classList.add('active')
      } else {
        navbarlink.classList.remove('active')
      }
    })
  }
  window.addEventListener('load', navbarlinksActive)
  onscroll(document, navbarlinksActive)

  /**
   * Scrolls to an element with header offset
   */
  const scrollto = (el) => {
    let header = select('#header')
    let offset = header.offsetHeight

    let elementPos = select(el).offsetTop
    window.scrollTo({
      top: elementPos - offset,
      behavior: 'smooth'
    })
  }

  /**
   * Back to top button
   */
  let backtotop = select('.back-to-top')
  if (backtotop) {
    const toggleBacktotop = () => {
      if (window.scrollY > 100) {
        backtotop.classList.add('active')
      } else {
        backtotop.classList.remove('active')
      }
    }
    window.addEventListener('load', toggleBacktotop)
    onscroll(document, toggleBacktotop)
  }

  /**
   * Mobile nav toggle
   */
  on('click', '.mobile-nav-toggle', function(e) {
    select('#navbar').classList.toggle('navbar-mobile')
    this.classList.toggle('bi-list')
    this.classList.toggle('bi-x')
  })

  /**
   * Mobile nav dropdowns activate
   */
  on('click', '.navbar .dropdown > a', function(e) {
    if (select('#navbar').classList.contains('navbar-mobile')) {
      e.preventDefault()
      this.nextElementSibling.classList.toggle('dropdown-active')
    }
  }, true)

  /**
   * Scrool with ofset on links with a class name .scrollto
   */
  on('click', '.scrollto', function(e) {
    if (select(this.hash)) {
      e.preventDefault()

      let navbar = select('#navbar')
      if (navbar.classList.contains('navbar-mobile')) {
        navbar.classList.remove('navbar-mobile')
        let navbarToggle = select('.mobile-nav-toggle')
        navbarToggle.classList.toggle('bi-list')
        navbarToggle.classList.toggle('bi-x')
      }
      scrollto(this.hash)
    }
  }, true)

  /**
   * Scroll with ofset on page load with hash links in the url
   */
  window.addEventListener('load', () => {
    if (window.location.hash) {
      if (select(window.location.hash)) {
        scrollto(window.location.hash)
      }
    }
  });

  /**
   * Porfolio isotope and filter
   */
  window.addEventListener('load', () => {
    let portfolioContainer = select('.portfolio-container');
    if (portfolioContainer) {
      let portfolioIsotope = new Isotope(portfolioContainer, {
        itemSelector: '.portfolio-item',
        layoutMode: 'fitRows'
      });

      let portfolioFilters = select('#portfolio-flters li', true);

      on('click', '#portfolio-flters li', function(e) {
        e.preventDefault();
        portfolioFilters.forEach(function(el) {
          el.classList.remove('filter-active');
        });
        this.classList.add('filter-active');

        portfolioIsotope.arrange({
          filter: this.getAttribute('data-filter')
        });
        portfolioIsotope.on('arrangeComplete', function() {
          AOS.refresh()
        });
      }, true);
    }

  });

  /**
   * Initiate portfolio lightbox 
   */
  const portfolioLightbox = GLightbox({
    selector: '.portfolio-lightbox'
  });


  /**
   * Modal
   */
  const exampleModal = document.getElementById('exampleModal')
  if (exampleModal) {
    exampleModal.addEventListener('show.bs.modal', event => {
      // Button that triggered the modal
      const button = event.relatedTarget
      // Extract info from data-bs-* attributes
      const task = button.getAttribute('data-bs-whatever')
      // If necessary, you could initiate an Ajax request here
      // and then do the updating in a callback.

      // Update the modal's content.
      const modalTitle = exampleModal.querySelector('.modal-title')
      const modalBodyInput = exampleModal.querySelector('.modal-body input[type="hidden"]')

      modalTitle.textContent = `Modify Task (Previous task: ${task})`
      modalBodyInput.value = task
    })
  }

  const postButton = document.getElementById('postButton');
  const taskNameInput = document.getElementById('task-name');
  const old_taskNameInput = document.getElementById('old_task-name');
  const alias_input = document.getElementById('account');

  // Add click event listener to the button
  postButton.addEventListener('click', () => {
    // Get the task name value
    const taskName = taskNameInput.value;
    const old_taskName = old_taskNameInput.value;
    const alias_name = alias_input.value;

    // Create a new XMLHttpRequest object
    const xhr = new XMLHttpRequest();

    // Configure the request
    xhr.open('POST', 'http://localhost:5000/Modify');
    xhr.setRequestHeader('Content-Type', 'application/json');

    // Set up the request data
    const requestData = {
      'new_task': taskName,
      'old_task': old_taskName,
      'alias': alias_name
    };

    // Convert the request data to JSON string
    const jsonData = JSON.stringify(requestData);

    // Set up the response handler
    xhr.onload = function () {
      if (xhr.status === 200) {
        // Request succeeded
        console.log(xhr.responseText);
        location.reload();
      } else {
        // Request failed
        console.error('Request failed:', xhr.status);
      }
    };

    // Send the request
    xhr.send(jsonData);
  });


  /**
   * Account Modal
   */
  const AccountModal = document.getElementById('AccountModal')

  const postAccountButton = document.getElementById('postAccountButton');
  const aliasInput = document.getElementById('alias');

  // Add click event listener to the button
  postAccountButton.addEventListener('click', () => {
    // Get the task name value
    const alias_name = aliasInput.value;

    // Create a new XMLHttpRequest object
    const xhr = new XMLHttpRequest();

    // Configure the request
    xhr.open('POST', 'http://localhost:5000/CreateAccount');
    xhr.setRequestHeader('Content-Type', 'application/json');

    // Set up the request data
    const requestData = {
      'alias': alias_name
    };

    // Convert the request data to JSON string
    const jsonData = JSON.stringify(requestData);

    // Set up the response handler
    xhr.onload = function () {
      if (xhr.status === 200) {
        // Request succeeded
        console.log(xhr.responseText);
      } else {
        // Request failed
        console.error('Request failed:', xhr.status);
      }
    };

    // Send the request
    xhr.send(jsonData);
  });

  /**
   * Page listener
   */

  const accountElements = document.querySelectorAll('.GetAccount');

  // Iterate over each account element and attach the click event listener
  accountElements.forEach((account) => {
    account.addEventListener('click', (event) => {
      event.preventDefault();

      const alias_name = event.target.getAttribute('data-value');

      // Rest of your XMLHttpRequest code...
      // Create a new XMLHttpRequest object
      const xhr = new XMLHttpRequest();
      console.log(alias_name)

      // Configure the request
      xhr.open('GET', `http://localhost:5000/Account?alias=${encodeURIComponent(alias_name)}`);
      xhr.setRequestHeader('Content-Type', 'application/json');

      // Set up the response handler
      xhr.onload = function () {
        if (xhr.status === 200) {
          // Request succeeded
          console.log(xhr.responseText);
          location.reload();
        } else {
          // Request failed
          console.error('Request failed:', xhr.status);
        }
      };

      // Send the request
      xhr.send();
    });
  });

  /**
   * Page listener (delete task)
   */

  const deleteElements = document.querySelectorAll('.DeleteTask');

  // Iterate over each account element and attach the click event listener
  deleteElements.forEach((deletetask) => {
    deletetask.addEventListener('click', (event) => {
      event.preventDefault();

      const parameters = deletetask.getAttribute('data-value');

      // Rest of your XMLHttpRequest code...
      // Create a new XMLHttpRequest object
      const xhr = new XMLHttpRequest();
      console.log(parameters)
      // Configure the request
      xhr.open('GET', `http://localhost:5000/Delete?${(parameters)}`);

      // Set up the response handler
      xhr.onload = function () {
        if (xhr.status === 200) {
          // Request succeeded
          if (xhr.responseText === "Choose a correct account!"){
            alert('Choose a correct account!');
          }else {
            console.log(xhr.responseText);
            location.reload();
          }
        } else {
          // Request failed
          console.error('Request failed:', xhr.status);
        }
      };

      // Send the request
      xhr.send();
    });
  }); 


  /**
   * Portfolio details slider
   */
  new Swiper('.portfolio-details-slider', {
    speed: 400,
    loop: true,
    autoplay: {
      delay: 5000,
      disableOnInteraction: false
    },
    pagination: {
      el: '.swiper-pagination',
      type: 'bullets',
      clickable: true
    }
  });

  /**
   * Clients Slider
   */
  new Swiper('.clients-slider', {
    speed: 400,
    loop: true,
    autoplay: {
      delay: 5000,
      disableOnInteraction: false
    },
    slidesPerView: 'auto',
    pagination: {
      el: '.swiper-pagination',
      type: 'bullets',
      clickable: true
    },
    breakpoints: {
      320: {
        slidesPerView: 2,
        spaceBetween: 40
      },
      480: {
        slidesPerView: 3,
        spaceBetween: 60
      },
      640: {
        slidesPerView: 4,
        spaceBetween: 80
      },
      992: {
        slidesPerView: 6,
        spaceBetween: 120
      }
    }
  });

  /**
   * Animation on scroll
   */
  window.addEventListener('load', () => {
    AOS.init({
      duration: 1000,
      easing: "ease-in-out",
      once: true,
      mirror: false
    });
  });

})()