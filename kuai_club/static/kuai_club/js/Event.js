// Enhanced Events Slider JavaScript - FIXED VERSION
document.addEventListener('DOMContentLoaded', () => {
  // Update this to match your actual Django URL pattern
  const apiUrl = '/api/events/'; // Make sure this matches your urls.py

  const sliders = {
    upcoming: {
      wrapper: document.getElementById('upEventWrapper'),
      slider: document.getElementById('upSlider'),
      leftBtn: document.getElementById('upLeft'),
      rightBtn: document.getElementById('upRight'),
      page: 1,
      type: 'upcoming',
      perPage: 2,
      totalPages: 1,
      isLoading: false
    },
    previous: {
      wrapper: document.getElementById('prevEventWrapper'),
      slider: document.getElementById('prevSlider'),
      leftBtn: document.getElementById('prevLeft'),
      rightBtn: document.getElementById('prevRight'),
      page: 1,
      type: 'past',
      perPage: 1,
      totalPages: 1,
      isLoading: false
    }
  };

  // Debug function to check if all elements exist
  function checkElements() {
    console.log('Checking slider elements...');
    Object.keys(sliders).forEach(key => {
      const slider = sliders[key];
      console.log(`${key} slider elements:`, {
        wrapper: !!slider.wrapper,
        slider: !!slider.slider,
        leftBtn: !!slider.leftBtn,
        rightBtn: !!slider.rightBtn
      });
    });
  }

  function createEventCard(event, eventType) {
    const card = document.createElement('div');
    card.className = 'event-card';
    card.setAttribute('data-id', event.id);
    
    const timeRemainingHtml = event.time_until_start && eventType === 'upcoming' 
      ? `<p class="event-countdown" data-start="${event.event_start}"><strong>Time Remaining:</strong> ${event.time_until_start}</p>` 
      : '';
    
    card.innerHTML = `
      <img src="${event.image_url || '/static/images/default-event.jpg'}" alt="${event.title}" loading="lazy" />
      <div class="event-content">
        <h3 class="event-title">${event.title}</h3>
        <p class="event-summary">${event.summary}</p>
        ${event.organizer ? `<p class="event-organizer"><strong>Organizer:</strong> ${event.organizer}</p>` : ''}
        ${timeRemainingHtml}
        <a href="${event.event_url}" target="_blank" class="event-link">Learn More</a>
      </div>
    `;
    return card;
  }

  function showLoading(sliderObj) {
    if (!sliderObj.slider) return;
    
    // Remove existing loading if any
    removeLoading(sliderObj);
    
    const loadingCard = document.createElement('div');
    loadingCard.className = 'loading-card';
    loadingCard.innerHTML = '<p>Loading events...</p>';
    sliderObj.slider.appendChild(loadingCard);
  }

  function removeLoading(sliderObj) {
    if (!sliderObj.slider) return;
    
    const loadingCard = sliderObj.slider.querySelector('.loading-card');
    if (loadingCard) {
      loadingCard.remove();
    }
  }

  function updateNavButtons(sliderObj) {
    if (!sliderObj.leftBtn || !sliderObj.rightBtn) {
      console.error('Navigation buttons not found for slider:', sliderObj.type);
      return;
    }

    const isFirstPage = sliderObj.page <= 1;
    const isLastPage = sliderObj.page >= sliderObj.totalPages || sliderObj.totalPages <= 1;

    // Update left button
    sliderObj.leftBtn.disabled = isFirstPage;
    sliderObj.leftBtn.classList.toggle('disabled', isFirstPage);
    
    // Update right button
    sliderObj.rightBtn.disabled = isLastPage;
    sliderObj.rightBtn.classList.toggle('disabled', isLastPage);
    
    console.log(`Updated nav buttons for ${sliderObj.type}: page ${sliderObj.page}/${sliderObj.totalPages}`, {
      leftDisabled: isFirstPage,
      rightDisabled: isLastPage
    });
  }

  async function loadEvents(sliderObj, targetPage) {
    if (sliderObj.isLoading) {
      console.log(`Already loading ${sliderObj.type} events, skipping...`);
      return;
    }
    
    if (targetPage < 1) {
      console.log(`Invalid page ${targetPage} for ${sliderObj.type} events`);
      return;
    }
    
    if (!sliderObj.slider) {
      console.error(`Slider element not found for ${sliderObj.type}`);
      return;
    }
    
    sliderObj.isLoading = true;
    showLoading(sliderObj);
    
    try {
      const url = `${apiUrl}?type=${sliderObj.type}&page=${targetPage}&per_page=${sliderObj.perPage}`;
      console.log(`Loading ${sliderObj.type} events from: ${url}`);
      
      const response = await fetch(url);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status} - ${response.statusText}`);
      }
      
      const data = await response.json();
      console.log(`API response for ${sliderObj.type}:`, data);
      
      if (data.error) {
        throw new Error(data.error);
      }
      
      if (data.events && data.events.length > 0) {
        // Clear existing events
        sliderObj.slider.innerHTML = '';
        
        // Add new events
        data.events.forEach(event => {
          const card = createEventCard(event, sliderObj.type);
          sliderObj.slider.appendChild(card);
        });
        
        // Update pagination info
        sliderObj.page = targetPage;
        sliderObj.totalPages = data.total_pages || 1;
        
        console.log(`Loaded ${data.events.length} ${sliderObj.type} events for page ${targetPage}`);
      } else {
        // No events found
        sliderObj.slider.innerHTML = '<div class="no-events"><p>No events available</p></div>';
        sliderObj.totalPages = 1;
      }
      
      // Update navigation buttons
      updateNavButtons(sliderObj);
      
      // Update countdowns for upcoming events
      if (sliderObj.type === 'upcoming') {
        updateCountdowns();
      }
      
    } catch (error) {
      console.error(`Error loading ${sliderObj.type} events:`, error);
      sliderObj.slider.innerHTML = `<div class="error-message"><p>Failed to load events: ${error.message}</p></div>`;
      sliderObj.totalPages = 1;
      updateNavButtons(sliderObj);
    } finally {
      sliderObj.isLoading = false;
      removeLoading(sliderObj);
    }
  }

  function initializeSlider(sliderKey) {
    const sliderObj = sliders[sliderKey];
    
    // Verify all required elements exist
    if (!sliderObj.wrapper || !sliderObj.slider || !sliderObj.leftBtn || !sliderObj.rightBtn) {
      console.error(`Missing elements for ${sliderKey} slider:`, {
        wrapper: !!sliderObj.wrapper,
        slider: !!sliderObj.slider,
        leftBtn: !!sliderObj.leftBtn,
        rightBtn: !!sliderObj.rightBtn
      });
      return false;
    }
    
    // Set up event listeners with proper error handling
    sliderObj.leftBtn.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      console.log(`Left button clicked for ${sliderKey}, current page: ${sliderObj.page}`);
      
      if (sliderObj.page > 1 && !sliderObj.isLoading && !sliderObj.leftBtn.disabled) {
        loadEvents(sliderObj, sliderObj.page - 1);
      }
    });
    
    sliderObj.rightBtn.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      console.log(`Right button clicked for ${sliderKey}, current page: ${sliderObj.page}, total pages: ${sliderObj.totalPages}`);
      
      if (sliderObj.page < sliderObj.totalPages && !sliderObj.isLoading && !sliderObj.rightBtn.disabled) {
        loadEvents(sliderObj, sliderObj.page + 1);
      }
    });
    
    // Initialize navigation buttons
    updateNavButtons(sliderObj);
    
    // Load initial data
    loadEvents(sliderObj, 1);
    
    console.log(`Initialized ${sliderKey} slider successfully`);
    return true;
  }

  // Auto-refresh countdown timers for upcoming events
  function updateCountdowns() {
    const countdownElements = document.querySelectorAll('.event-countdown[data-start]');
    countdownElements.forEach(element => {
      const startDate = new Date(element.getAttribute('data-start'));
      const now = new Date();
      const timeDiff = startDate - now;
      
      if (timeDiff > 0) {
        const days = Math.floor(timeDiff / (1000 * 60 * 60 * 24));
        const hours = Math.floor((timeDiff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((timeDiff % (1000 * 60 * 60)) / (1000 * 60));
        
        let timeString = '';
        if (days > 0) timeString += `${days}d `;
        if (hours > 0) timeString += `${hours}h `;
        if (minutes > 0) timeString += `${minutes}m`;
        
        element.innerHTML = `<strong>Time Remaining:</strong> ${timeString || 'Less than 1 minute'}`;
      } else {
        element.innerHTML = '<strong>Event has started!</strong>';
      }
    });
  }

  // Initialize everything
  try {
    checkElements();
    
    const upcomingSuccess = initializeSlider('upcoming');
    const previousSuccess = initializeSlider('previous');
    
    if (upcomingSuccess || previousSuccess) {
      console.log('At least one slider initialized successfully');
      
      // Set up countdown updates
      updateCountdowns();
      setInterval(updateCountdowns, 60000);
    } else {
      console.error('Failed to initialize any sliders');
    }
    
  } catch (error) {
    console.error('Error during initialization:', error);
  }

  // Global error handler for debugging
  window.addEventListener('error', (e) => {
    console.error('Global error:', e.error);
  });
});